# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods for AutoML remote runs."""
import gc
import json
import logging
import os
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, cast

import numpy as np
import pandas as pd
from azureml._restclient.constants import RUN_ORIGIN
from azureml._restclient.jasmine_client import JasmineClient
from azureml._tracing import get_tracer
from azureml.automl.core._experiment_observer import ExperimentStatus, ExperimentObserver
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.constants import FeaturizationRunConstants, PreparationRunTypeConstants
from azureml.automl.core.shared import logging_utilities, constants
from azureml.automl.core.shared.constants import SupportedModelNames, TelemetryConstants
from azureml.automl.core.shared.exceptions import AutoMLException, CacheException, UserException
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.telemetry_activity_logger import \
    TelemetryActivityLogger
from azureml.automl.runtime import (_time_series_training_utilities,
                                    data_transformation, training_utilities)
from azureml.automl.runtime._automl_settings_utilities import \
    rule_based_validation
from azureml.automl.runtime._data_transformation_utilities import (
    FeaturizationJsonParser, save_engineered_feature_names,
    save_feature_config)
from azureml.automl.runtime._feature_sweeped_state_container import \
    FeatureSweepedStateContainer
from azureml.automl.runtime.data_context import RawDataContext
from azureml.automl.runtime.distributed.utilities import (PollForMaster,
                                                          is_master_process)
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.frequency_fixer import (
    fix_data_set_regularity_may_be, str_to_offset_safe)
from azureml.automl.runtime.onnx_convert import OnnxConverter
from azureml.automl.runtime.shared import memory_utilities
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.automl.runtime import short_grain_padding
from azureml.core import Datastore, Experiment, Run
from azureml.data.azure_storage_datastore import AbstractAzureStorageDatastore
from azureml.data.constants import WORKSPACE_BLOB_DATASTORE
from azureml.train.automl._automl_datamodel_utilities import CaclulatedExperimentInfo
from azureml.train.automl._automl_feature_config_manager import AutoMLFeatureConfigManager
from azureml.train.automl._azure_experiment_observer import AzureExperimentObserver
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.constants import ComputeTargets
from azureml.train.automl.run import AutoMLRun
from azureml.train.automl.runtime._automl_job_phases import (
    FeaturizationPhase, PhaseUtil, SetupPhase, TrainingIteration,
    TrainingPhase)
from azureml.train.automl.runtime._automl_model_explain import (
    AutoMLModelExplainDriverFactory, AutoMLModelExplainTelemetryStrings,
    _automl_auto_mode_explain_model, _automl_perform_best_run_explain_model)
from azureml.train.automl.runtime._azurefilecachestore import \
    AzureFileCacheStore
from azureml.train.automl.runtime._task_queue import QueueClient
from azureml.train.automl.runtime.automl_explain_utilities import \
    ModelExplanationRunId
from azureml.train.automl.runtime._model_test_utilities import _execute_model_test_run
from azureml.train.automl.utilities import _get_package_version
from msrest.exceptions import HttpOperationError

from ._azureautomlruncontext import AzureAutoMLRunContext
from ._cachestorefactory import CacheStoreFactory
from ._data_preparer import DataPreparer, DataPreparerFactory
# Used by remote driver, don't remove
# noinspection PyUnresolvedReferences
from ._remote.notebook_generation import parent_run_notebook_generation_wrapper
from ._remote.remote_utilities import (_get_parent_run_id, _init_directory,
                                       _parse_settings)
from .utilities import _load_user_script

CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA = '_CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA_'

# The base dataset object can be cached in the setup iteration (to be later re-used during model training),
# with the following key
DATASET_BASE_CACHE_KEY = 'dataset_cached_object'


logger = logging.getLogger(__name__)
activity_logger = TelemetryActivityLogger()
tracer = get_tracer(__name__)


def _prepare_data(data_preparer: Optional[DataPreparer],
                  automl_settings_obj: AzureAutoMLSettings,
                  script_directory: Optional[str],
                  entry_point: Optional[str],
                  verifier: Optional[VerifierManager] = None) -> Dict[str, Any]:
    if data_preparer:
        data_dict = data_preparer.prepare(automl_settings_obj)
    else:
        if script_directory is None:
            script_directory = ""
        if entry_point is None:
            entry_point = ""
        script_path = os.path.join(script_directory, entry_point)
        if script_path is None:
            script_path = '.'
        user_module = _load_user_script(script_path, False)
        data_dict = training_utilities._extract_user_data(user_module)

    # Set min and max y if needed.
    training_utilities.set_task_parameters(y=data_dict.get('y'),
                                           automl_settings=automl_settings_obj)
    # When data were read try to fix the frequency.
    if automl_settings_obj.is_timeseries and data_dict.get('X_valid') is None:
        training_utilities._check_dimensions(data_dict['X'], data_dict['y'], None, None, None, None)
        # If X and y are dataflow object, we need to deserialize it here.
        X = data_dict['X']
        if isinstance(X, np.ndarray) and data_dict.get('x_raw_column_names') is not None:
            X = pd.DataFrame(X, columns=data_dict.get('x_raw_column_names'))
        y = data_dict['y']
        fixed_freq_obj = fix_data_set_regularity_may_be(
            X,
            y,
            automl_settings_obj.time_column_name,
            automl_settings_obj.grain_column_names,
            str_to_offset_safe(automl_settings_obj.freq,
                               ReferenceCodes._REMOTE_SCRIPT_WRONG_FREQ))
        X = fixed_freq_obj.data_x
        data_dict['y'] = fixed_freq_obj.data_y
        failed = fixed_freq_obj.is_failed
        corrected = fixed_freq_obj.is_modified
        freq = fixed_freq_obj.freq
        # Do our best to clean up memory.
        del data_dict['X']
        gc.collect()
        # If we do not have enough memory, raise the exception.
        _time_series_training_utilities.check_memory_limit(X, data_dict['y'])
        # Pad the short grains if needed (the short_series_handing_config_value is
        # checked by pad_short_grains_or_raise).
        X, data_dict['y'] = short_grain_padding.pad_short_grains_or_raise(
            X, data_dict['y'], freq, automl_settings_obj, ReferenceCodes._TS_ONE_VALUE_PER_GRAIN_RSCRIPT,
            verifier)
        # We may have reordered data frame X reorder it back here.
        X = X[data_dict['x_raw_column_names']]
        # and then copy the data to new location.
        data_dict['X'] = X.values
        if verifier:
            verifier.update_data_verifier_frequency_inference(failed, corrected)

    data_dict['X'], data_dict['y'], data_dict['sample_weight'], data_dict['X_valid'], data_dict['y_valid'], \
        data_dict['sample_weight_valid'] = rule_based_validation(automl_settings_obj,
                                                                 data_dict.get('X'),
                                                                 data_dict.get('y'),
                                                                 data_dict.get('sample_weight'),
                                                                 data_dict.get('X_valid'),
                                                                 data_dict.get('y_valid'),
                                                                 data_dict.get('sample_weight_valid'),
                                                                 data_dict.get('cv_splits_indices'),
                                                                 verifier=verifier)
    return data_dict


def _get_cache_data_store(experiment: Experiment) -> Optional[AbstractAzureStorageDatastore]:
    data_store = None   # type: Optional[AbstractAzureStorageDatastore]
    start = time.time()
    try:
        data_store = Datastore.get(experiment.workspace, WORKSPACE_BLOB_DATASTORE)
        logger.info('Successfully got the cache data store, caching enabled.')
    except HttpOperationError as response_exception:
        logging_utilities.log_traceback(response_exception, logger)
        if response_exception.response.status_code >= 500:
            raise
        else:
            raise UserException.from_exception(response_exception).with_generic_msg(
                'Failed to get default datastore from Datastore Service. HTTP Status code: {}'.format(
                    response_exception.response.status_code)
            )
    end = time.time()
    logger.info('Took {} seconds to retrieve cache data store'.format(end - start))
    return data_store


def _cache_onnx_init_metadata(
    cache_store: CacheStore,
    onnx_cvt: Optional[OnnxConverter],
    parent_run_id: str
) -> None:
    if not onnx_cvt:
        return
    onnx_cvt_init_metadata_dict = onnx_cvt.get_init_metadata_dict()
    # If the cache store and the onnx converter init metadata are valid, save it into cache store.
    if onnx_cvt_init_metadata_dict:
        logger.info('Successfully initialized ONNX converter for run {}.'.format(parent_run_id))
        logger.info('Begin saving onnx initialization metadata for run {}.'.format(parent_run_id))
        cache_store.add([CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA], [onnx_cvt_init_metadata_dict])
        logger.info('Successfully Saved onnx initialization metadata for run {}.'.format(parent_run_id))
    else:
        logger.info('Failed to initialize ONNX converter for run {}.'.format(parent_run_id))


def _load_data_from_cache(cache_store: CacheStore) -> DatasetBase:
    with tracer.start_as_current_span(
            TelemetryConstants.SPAN_FORMATTING.format(
                TelemetryConstants.COMPONENT_NAME, TelemetryConstants.LOAD_CACHED_DATA
            ),
            user_facing_name=TelemetryConstants.LOAD_CACHED_DATA_USER_FACING
    ):
        try:
            cache_store.load()
            dataset_dict = cache_store.get([DATASET_BASE_CACHE_KEY])
            if dataset_dict is not None:
                result = dataset_dict.get(DATASET_BASE_CACHE_KEY, None)  # type: Optional[DatasetBase]
                if result:
                    logger.info('Successfully loaded the AutoML Dataset from cache.')
                    return result
            raise CacheException("Failed to find {} in cache_store.".format(DATASET_BASE_CACHE_KEY), has_pii=False)
        except AutoMLException as e:
            logging_utilities.log_traceback(e, logger, is_critical=False)
            logger.warning("Failed to initialize Datasets from the cache")
            raise
        except Exception as e:
            logging_utilities.log_traceback(e, logger, is_critical=False)
            logger.warning('Fatal exception encountered while trying to load data from cache')
            raise


def _load_onnx_converter(
    automl_settings: AzureAutoMLSettings,
    cache_store: CacheStore,
    parent_run_id: str
) -> Optional[OnnxConverter]:
    if not automl_settings.enable_onnx_compatible_models:
        return None

    with tracer.start_as_current_span(
            TelemetryConstants.SPAN_FORMATTING.format(
                TelemetryConstants.COMPONENT_NAME, TelemetryConstants.LOAD_ONNX_CONVERTER
            ),
            user_facing_name=TelemetryConstants.LOAD_ONNX_CONVERTER_USER_FACING
    ):
        onnx_cvt = PhaseUtil.build_onnx_converter(automl_settings)
        if onnx_cvt is None:
            return None
        logger.info('Get ONNX converter metadata from cache')
        cached_data_dict = cache_store.get([CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA])
        if cached_data_dict:
            onnx_cvt_init_metadata_dict = cached_data_dict.get(
                CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA, None)  # type: Optional[Dict[str, Any]]
            if onnx_cvt_init_metadata_dict is not None:
                logger.info('Initialize ONNX converter with cached metadata')
                onnx_cvt.initialize_with_metadata(metadata_dict=onnx_cvt_init_metadata_dict,
                                                  model_name=PhaseUtil.get_onnx_model_name(parent_run_id),
                                                  model_desc=PhaseUtil.get_onnx_model_desc(parent_run_id))
        if onnx_cvt.is_initialized():
            logger.info('Successfully initialized ONNX converter')
        else:
            logger.info('Failed to initialize ONNX converter')
        return onnx_cvt


def model_exp_wrapper(
        script_directory: str,
        automl_settings: str,
        run_id: str,
        child_run_id: str,
        dataprep_json: str,
        entry_point: str,
        **kwargs: Any
) -> Dict[str, Any]:
    """
    Compute best run model or on-demand explanations in remote runs.

    :param script_directory:
    :param automl_settings:
    :param run_id: The run id for model explanations run. This is AutoML_<GUID>_ModelExplain in case
                   of best run model explanations and <GUID> in case of on-demand explanations.
    :param child_run_id: The AutoML child run id for which to compute on-demand explanations for.
                         This is 'None' for best run model explanations and an AutoMl child run-id
                         for on-demand model explanation run.
    :param dataprep_json:
    :param entry_point:
    :param kwargs:
    :return:
    """
    model_exp_output = {}  # type: Dict[str, Any]
    current_run = Run.get_context()
    logger.info("The model explanation run-id is: " + str(current_run.id))
    if child_run_id:
        automl_run_obj = Run(current_run.experiment, child_run_id)
    else:
        automl_run_obj = current_run
    automl_settings_obj = _parse_settings(automl_run_obj, automl_settings)
    pkg_ver = _get_package_version()
    logger.info('Using SDK version {}'.format(pkg_ver))
    try:
        if not child_run_id:
            parent_run_id = _get_parent_run_id(run_id)
        else:
            parent_run_id = _get_parent_run_id(child_run_id)
        parent_run = AutoMLRun(current_run.experiment, parent_run_id)
        cache_store = _init_cache_store(parent_run.experiment, parent_run_id)
        dataset = _load_data_from_cache(cache_store)

        if not child_run_id:
            logger.info(AutoMLModelExplainTelemetryStrings.REMOTE_BEST_RUN_MODEL_EXPLAIN_START_STR.format(
                parent_run_id))
            print(AutoMLModelExplainTelemetryStrings.REMOTE_BEST_RUN_MODEL_EXPLAIN_START_STR.format(
                parent_run_id))

            # Get the best run model explanation
            experiment_observer = AzureExperimentObserver(parent_run, console_logger=sys.stdout, file_logger=logger)
            _automl_perform_best_run_explain_model(
                parent_run, dataset, automl_settings_obj,
                compute_target=ComputeTargets.AMLCOMPUTE,
                current_run=current_run,
                experiment_observer=experiment_observer)
        else:
            logger.info(AutoMLModelExplainTelemetryStrings.REMOTE_ON_DEMAND_RUN_MODEL_EXPLAIN_START_STR.format(
                child_run_id))
            print(AutoMLModelExplainTelemetryStrings.REMOTE_ON_DEMAND_RUN_MODEL_EXPLAIN_START_STR.format(
                child_run_id))

            child_run = Run(current_run.experiment, child_run_id)
            if current_run is not None:
                child_run.set_tags({ModelExplanationRunId: str(current_run.id)})

            # Get the model explanation for the child run
            with dataset.open_dataset():
                # Get the model explain driver class for explaining this model
                automl_model_explain_driver = AutoMLModelExplainDriverFactory._get_model_explain_driver(
                    automl_child_run=child_run,
                    dataset=dataset, automl_settings=automl_settings_obj)
                _automl_auto_mode_explain_model(automl_model_explain_driver=automl_model_explain_driver)
    except Exception as e:
        if not child_run_id:
            logger.error(AutoMLModelExplainTelemetryStrings.REMOTE_BEST_RUN_MODEL_EXPLAIN_ERROR_STR)
        else:
            logger.error(AutoMLModelExplainTelemetryStrings.REMOTE_ON_DEMAND_RUN_MODEL_EXPLAIN_ERROR_STR)
        run_lifecycle_utilities.fail_run(current_run, e)
        raise

    return model_exp_output


def model_test_wrapper(
        script_directory: str,
        automl_settings: str,
        run_id: str,
        training_run_id: str,
        dataprep_json: str,
        entry_point: str,
        **kwargs: Any
) -> None:
    """
    Compute best run or on-demand model testing in remote runs.

    :param script_directory:
    :param automl_settings:
    :param run_id: The run id for model test run.
    :param training_run_id: The id for the AutoML child run which contains the model.
    :param dataprep_json: The dataprep json which contains a reference to the test dataset.
    :param entry_point:
    :param kwargs:
    :return:
    """
    current_run = Run.get_context()

    pkg_ver = _get_package_version()
    logger.info('Using SDK version {}'.format(pkg_ver))

    try:
        print("{} - INFO - Beginning model test wrapper.".format(datetime.now().__format__('%Y-%m-%d %H:%M:%S,%f')))
        logger.info('Beginning AutoML remote driver for run {}.'.format(run_id))

        parent_run_id = _get_parent_run_id(training_run_id)

        # TODO: should this last argument be training_run_id?
        automl_settings_obj = _parse_settings(current_run,
                                              automl_settings,
                                              parent_run_id)

        # Get the post setup/featurization training data
        # which is required for metrics computation.
        cache_store = _init_cache_store(current_run.experiment, parent_run_id=parent_run_id)
        cache_store.load()
        parent_dataset = _load_data_from_cache(cache_store)

        _execute_model_test_run(current_run,
                                training_run_id,
                                dataprep_json,
                                parent_dataset,
                                automl_settings_obj)
    except Exception as e:
        logger.error("AutoML test_wrapper script terminated with an exception of type: {}".format(type(e)))
        run_lifecycle_utilities.fail_run(current_run, e)
        raise


def driver_wrapper(
        script_directory: str,
        automl_settings: str,
        run_id: str,
        training_percent: float,
        iteration: int,
        pipeline_spec: str,
        pipeline_id: str,
        dataprep_json: str,
        entry_point: str,
        **kwargs: Any
) -> Dict[str, Any]:
    """
    Driver script that runs one child iteration
    using the given pipeline spec for the remote run.
    """
    current_run = Run.get_context()
    result = {}  # type: Dict[str, Any]
    try:
        print("{} - INFO - Beginning driver wrapper.".format(datetime.now().__format__('%Y-%m-%d %H:%M:%S,%f')))
        logger.info('Beginning AutoML remote driver for run {}.'.format(run_id))

        parent_run, automl_settings_obj, cache_store = _init_wrapper(
            current_run, automl_settings, script_directory, **kwargs)

        if automl_settings_obj.enable_streaming:
            _modify_settings_for_streaming(automl_settings_obj, dataprep_json)

        dataset = _load_data_from_cache(cache_store)
        onnx_cvt = _load_onnx_converter(automl_settings_obj, cache_store, parent_run.id)

        fit_output = TrainingIteration.run(
            automl_parent_run=parent_run,
            automl_run_context=AzureAutoMLRunContext(current_run),
            automl_settings=automl_settings_obj,
            dataset=dataset,
            onnx_cvt=onnx_cvt,
            pipeline_id=pipeline_id,
            pipeline_spec=pipeline_spec,
            remote=True,
            training_percent=training_percent,
        )
        result = fit_output.get_output_dict()
        if fit_output.errors:
            for fit_exception in fit_output.errors.values():
                if fit_exception.get("is_critical"):
                    exception = cast(BaseException, fit_exception.get("exception"))
                    raise exception.with_traceback(exception.__traceback__)
    except Exception as e:
        logger.error("AutoML driver_wrapper script terminated with an exception of type: {}".format(type(e)))
        run_lifecycle_utilities.fail_run(current_run, e)
        raise

    return result


def batch_driver_wrapper(
        script_directory: str,
        automl_settings: str,
        batch_run_id: str,
        dataprep_json: str,
        **kwargs: Any
) -> None:
    """
    Driver script that runs multiple iterations
    using the pipelines queued in Azure Storage Queue for the remote run.
    """
    batch_job_run = Run.get_context()  # current batch job context

    try:
        print("{} - INFO - Beginning driver wrapper v2.".format(datetime.now().__format__('%Y-%m-%d %H:%M:%S,%f')))
        logger.info('Beginning AutoML remote driver for {}.'.format(batch_run_id))

        parent_run, automl_settings_obj, cache_store = _init_wrapper(
            batch_job_run, automl_settings, script_directory, **kwargs)

        if automl_settings_obj.enable_streaming:
            _modify_settings_for_streaming(automl_settings_obj, dataprep_json)

        dataset = _load_data_from_cache(cache_store)
        onnx_cvt = _load_onnx_converter(automl_settings_obj, cache_store, parent_run.id)

        cache_store = cast(AzureFileCacheStore, cache_store)

        task_queue = QueueClient(
            parent_run.id,
            cache_store.account_name,
            cache_store.account_key,
            cache_store.file_service.protocol,
            cache_store.endpoint_suffix
        )

        TrainingPhase.run(
            automl_parent_run=parent_run,
            automl_settings=automl_settings_obj,
            dataset=dataset,
            onnx_cvt=onnx_cvt,
            remote=True,
            task_queue=task_queue
        )

        logger.info("No more training iteration task in the queue, ending the script run for {}"
                    .format(batch_run_id))

    except Exception as e:
        logger.error("AutoML batch_driver_wrapper script terminated with an exception of type: {}".format(type(e)))
        run_lifecycle_utilities.fail_run(batch_job_run, e)
        raise


def _get_cache_store(data_store: Optional[AbstractAzureStorageDatastore], run_id: str) -> CacheStore:
    cache_location = '{0}/{1}'.format('_remote_cache_directory_', run_id)

    os.makedirs(cache_location, exist_ok=True)
    return CacheStoreFactory.get_cache_store(temp_location=cache_location,
                                             run_target=ComputeTargets.AMLCOMPUTE,
                                             run_id=run_id,
                                             data_store=data_store)


def _build_feature_config_manager(experiment: Experiment) -> AutoMLFeatureConfigManager:
    """Build an AutoML feature config manager for the run."""
    jasmine_client = JasmineClient(
        experiment.workspace.service_context,
        experiment.name,
        experiment.id,
        user_agent=type(JasmineClient).__name__)
    return AutoMLFeatureConfigManager(jasmine_client=jasmine_client)


def _modify_settings_for_streaming(
        automl_settings_obj: AzureAutoMLSettings,
        dataprep_json: str
) -> None:
    automl_settings_obj.enable_streaming = True
    # check if UX and update the settings appropriately
    dataprep_json_obj = json.loads(dataprep_json)
    if 'activities' not in dataprep_json_obj:
        # for UI we need to set the label_column_name
        if automl_settings_obj.label_column_name is None:
            automl_settings_obj.label_column_name = dataprep_json_obj.get('label', None)
            logger.info('Set label_column_name')

    if automl_settings_obj.enable_stack_ensembling is True or automl_settings_obj.enable_ensembling is True:
        logger.warning('The training data is large. Ensembling is not available for this run.')
        automl_settings_obj.enable_stack_ensembling = False
        automl_settings_obj.enable_ensembling = False


def _are_inputs_conducive_for_streaming(
        automl_settings: AzureAutoMLSettings,
        data_preparer: DataPreparer
) -> bool:
    if automl_settings.force_streaming:
        return True

    # List storing all the reasons due to which streaming could not be enabled
    incompatibility_reasons = []    # type: List[str]

    if data_preparer._original_training_data is None:
        incompatibility_reasons.append("'training_data' is not provided")

    if automl_settings.spark_context is not None:
        incompatibility_reasons.append("Spark runs are not supported")

    if automl_settings.is_timeseries:
        incompatibility_reasons.append("Forecasting is not supported")

    if automl_settings.n_cross_validations is not None:
        incompatibility_reasons.append("'n_cross_validations' was non-empty")

    if automl_settings.enable_onnx_compatible_models:
        incompatibility_reasons.append("ONNX compatibility is not supported")

    if automl_settings.enable_dnn:
        incompatibility_reasons.append("DNN is not supported")

    if automl_settings.enable_subsampling:
        incompatibility_reasons.append("Subsampling is enabled")

    if automl_settings.whitelist_models is not None:
        supported_set = set([model.customer_model_name for model in SupportedModelNames.SupportedStreamingModelList])
        if not set(automl_settings.whitelist_models).issubset(supported_set):
            incompatibility_reasons.append("Allowed models are unsupported. "
                                           "Supported models: [{}]".format(','.join(supported_set)))

    if incompatibility_reasons:
        logger.info("Streaming is not conducive due to incompatible settings. "
                    "Reason[s]: [{}]".format(', '.join(incompatibility_reasons)))
        return False

    return True


def _init_wrapper(
        current_run: Run,
        automl_settings_str: str,
        script_directory: Optional[str],
        **kwargs: Any
) -> Tuple[Run, AzureAutoMLSettings, CacheStore]:
    """Initialize common variables across remote wrappers."""
    with tracer.start_as_current_span(
            TelemetryConstants.SPAN_FORMATTING.format(
                TelemetryConstants.COMPONENT_NAME, TelemetryConstants.RUN_INITIALIZATION
            ),
            user_facing_name=TelemetryConstants.RUN_INITIALIZATION_USER_FACING
    ):
        pkg_ver = _get_package_version()
        logger.info('Using SDK version {}'.format(pkg_ver))

        _init_directory(directory=script_directory)

        parent_run_id = _get_parent_run_id(current_run.id)
        parent_run = Run(current_run.experiment, parent_run_id)

        automl_settings_obj = _parse_settings(current_run, automl_settings_str)

        # cache_store_parent_run_id kwarg is only expected to be used in backwards compatibility e2e tests,
        # it is not expected to be used in production scenarios.
        cache_store_parent_run_id = kwargs.pop('cache_store_parent_run_id', parent_run_id)
        cache_store = _init_cache_store(parent_run.experiment, parent_run_id=cache_store_parent_run_id)
        cache_store.load()

    return parent_run, automl_settings_obj, cache_store


def _save_setup_run_state_for_featurization_run(
    setup_run: Run,
    feature_sweeped_state_container: FeatureSweepedStateContainer
) -> None:
    logger.info("Saving artifacts required for separate featurization run.")

    feature_config = feature_sweeped_state_container.get_feature_config()

    save_feature_config(feature_config)
    save_engineered_feature_names(feature_sweeped_state_container.get_engineered_feature_names())

    featurization_properties = FeaturizationJsonParser._build_jsonifiable_featurization_props(
        feature_config)

    setup_run.add_properties({
        FeaturizationRunConstants.CONFIG_PROP: FeaturizationRunConstants.CONFIG_PATH,
        FeaturizationRunConstants.NAMES_PROP: FeaturizationRunConstants.NAMES_PATH,
        FeaturizationRunConstants.FEATURIZATION_JSON_PROP:
        FeaturizationRunConstants.FEATURIZATION_JSON_PATH})
    FeaturizationJsonParser.save_featurization_json(featurization_properties)


def _build_feature_sweeped_state_container(
        parent_run: Run,
        featurization_json: str,
        fit_iteration_parameters_dict: Dict[str, Any],
        automl_settings: AzureAutoMLSettings,
        feature_config_manager: AutoMLFeatureConfigManager,
        cache_store: CacheStore,
        experiment_observer: ExperimentObserver,
) -> FeatureSweepedStateContainer:
    featurizer_container = FeaturizationJsonParser.parse_featurizer_container(featurization_json)
    raw_data_context = PhaseUtil.build_raw_data_context(fit_iteration_parameters_dict, automl_settings)
    feature_sweeping_config = feature_config_manager.get_feature_sweeping_config(
        enable_feature_sweeping=automl_settings.enable_feature_sweeping,
        parent_run_id=parent_run.id,
        task_type=automl_settings.task_type)
    feature_sweeped_state_container = data_transformation.build_feature_sweeped_state_container(
        raw_data_context,
        cache_store=cache_store,
        is_onnx_compatible=automl_settings.enable_onnx_compatible_models,
        experiment_observer=experiment_observer,
        enable_feature_sweeping=automl_settings.enable_feature_sweeping,
        feature_sweeping_config=feature_sweeping_config,
        enable_dnn=automl_settings.enable_dnn,
        force_text_dnn=automl_settings.force_text_dnn,
        featurizer_container=featurizer_container)
    return feature_sweeped_state_container


def setup_wrapper(
        script_directory: Optional[str],
        dataprep_json: str,
        entry_point: str,
        automl_settings: str,
        prep_type: str = PreparationRunTypeConstants.SETUP_ONLY,
        **kwargs: Any
) -> None:
    """
    Code for setup iterations for AutoML remote runs.
    """
    setup_run = Run.get_context()
    try:
        verifier = VerifierManager()
        parent_run, automl_settings_obj, cache_store = _init_wrapper(setup_run, automl_settings, script_directory)
        fit_iteration_parameters_dict, experiment_observer, feature_config_manager = \
            _prep_input_data(setup_run, "setup", automl_settings_obj,
                             script_directory, dataprep_json, entry_point, parent_run, verifier)
        dataset, onnx_cvt, feature_sweeped_state_container = SetupPhase.run(
            automl_parent_run=parent_run,
            automl_settings=automl_settings_obj,
            cache_store=cache_store,
            current_run=setup_run,
            experiment_observer=experiment_observer,
            feature_config_manager=feature_config_manager,
            fit_iteration_parameters_dict=fit_iteration_parameters_dict,
            prep_type=prep_type,
            remote=True,
            validate_training_data=True,
            verifier=verifier
        )
        _cache_onnx_init_metadata(cache_store, onnx_cvt, parent_run.id)
        if dataset:
            _cache_dataset(cache_store, dataset, experiment_observer, parent_run)
        if feature_sweeped_state_container:
            # We will kick off a separate feature sweeping run, so we must save
            # the artifacts necessary for that to succeed.
            _save_setup_run_state_for_featurization_run(setup_run, feature_sweeped_state_container)
        parent_run_context = AzureAutoMLRunContext(parent_run)
        verifier.write_result_file(parent_run_context)
    except Exception as e:
        logger.error("AutoML setup script terminated with an exception of type: {}".format(type(e)))
        run_lifecycle_utilities.fail_run(setup_run, e)
        raise


def featurization_wrapper(
        script_directory: Optional[str],
        dataprep_json: str,
        entry_point: str,
        automl_settings: str,
        setup_container_id: str,
        featurization_json: str,
        **kwargs: Any) -> None:
    """
    Code for featurization part of setup iterations for AutoML remote runs.
    """
    featurization_run = Run.get_context()
    try:
        parent_run, automl_settings_obj, cache_store = _init_wrapper(
            featurization_run, automl_settings, script_directory)
        property_dict = featurization_run.get_properties()
        transfer_files_from_setup(featurization_run, setup_container_id,
                                  property_dict.get(FeaturizationRunConstants.CONFIG_PROP,
                                                    FeaturizationRunConstants.CONFIG_PATH),
                                  property_dict.get(FeaturizationRunConstants.NAMES_PROP,
                                                    FeaturizationRunConstants.NAMES_PATH))
        fit_iteration_parameters_dict, experiment_observer, feature_config_manager = _prep_input_data(
            featurization_run, "featurization", automl_settings_obj, script_directory, dataprep_json,
            entry_point, parent_run)
        # The setup run has produced information about the featurizers that will be run on the dataset.
        # This information is encapsulated in FeatureSweepedStateContainer. We need to
        # rehyrdrate a FeatureSweepedStateContainer from state saved by the setup run.
        feature_sweeped_state_container = _build_feature_sweeped_state_container(
            parent_run, featurization_json, fit_iteration_parameters_dict, automl_settings_obj, feature_config_manager,
            cache_store, experiment_observer)
        dataset = FeaturizationPhase.run(
            automl_parent_run=parent_run,
            automl_settings=automl_settings_obj,
            cache_store=cache_store,
            current_run=featurization_run,
            experiment_observer=experiment_observer,
            feature_config_manager=feature_config_manager,
            feature_sweeped_state_container=feature_sweeped_state_container,
            fit_iteration_parameters_dict=fit_iteration_parameters_dict,
            remote=True
        )
        _cache_dataset(cache_store, dataset, experiment_observer, parent_run)
    except Exception as e:
        logger.error("AutoML featurization script terminated with an exception of type: {}".format(type(e)))
        run_lifecycle_utilities.fail_run(featurization_run, e)
        raise


def fit_featurizers_wrapper(
        script_directory: Optional[str],
        dataprep_json: str,
        entry_point: str,
        automl_settings: str,
        setup_container_id: str,
        featurization_json: str,
        **kwargs: Any) -> None:
    """
    Code for fitting individual featurizer(s) as a part of the featurization iteration for AutoML remote runs.
    """
    fit_featurizer_run = Run.get_context()
    parent_run, automl_settings_obj, cache_store = _init_wrapper(
        fit_featurizer_run, automl_settings, script_directory)
    property_dict = fit_featurizer_run.get_properties()

    transfer_files_from_setup(fit_featurizer_run, setup_container_id,
                              property_dict.get(FeaturizationRunConstants.CONFIG_PROP,
                                                FeaturizationRunConstants.CONFIG_PATH),
                              property_dict.get(FeaturizationRunConstants.NAMES_PROP,
                                                FeaturizationRunConstants.NAMES_PATH))
    try:
        fit_iteration_parameters_dict, experiment_observer, feature_config_manager = _prep_input_data(
            fit_featurizer_run, "individual featurizer", automl_settings_obj, script_directory, dataprep_json,
            entry_point, parent_run)

        raw_data_context = RawDataContext(automl_settings_obj=automl_settings_obj,
                                          X=fit_iteration_parameters_dict.get('X'),
                                          y=fit_iteration_parameters_dict.get('y'),
                                          X_valid=fit_iteration_parameters_dict.get('X_valid'),
                                          y_valid=fit_iteration_parameters_dict.get('y_valid'),
                                          sample_weight=fit_iteration_parameters_dict.get('sample_weight'),
                                          sample_weight_valid=fit_iteration_parameters_dict.get('sample_weight_valid'),
                                          x_raw_column_names=fit_iteration_parameters_dict.get('x_raw_column_names'),
                                          cv_splits_indices=fit_iteration_parameters_dict.get('cv_splits_indices'),
                                          training_data=fit_iteration_parameters_dict.get('training_data'),
                                          validation_data=fit_iteration_parameters_dict.get('validation_data')
                                          )

        feature_sweeping_config = feature_config_manager.get_feature_sweeping_config(
            enable_feature_sweeping=automl_settings_obj.enable_feature_sweeping,
            parent_run_id=parent_run.id,
            task_type=automl_settings_obj.task_type)

        featurizer_container = FeaturizationJsonParser.parse_featurizer_container(
            featurization_json,
            is_onnx_compatible=automl_settings_obj.enable_onnx_compatible_models)

        logger.info("Beginning to fit and cache specified featurizers.")
        data_transformation.fit_and_cache_featurizers(
            raw_data_context=raw_data_context,
            featurizer_container=featurizer_container,
            cache_store=cache_store,
            observer=experiment_observer,
            is_onnx_compatible=automl_settings_obj.enable_onnx_compatible_models,
            enable_feature_sweeping=automl_settings_obj.enable_feature_sweeping,
            enable_dnn=automl_settings_obj.enable_dnn,
            force_text_dnn=automl_settings_obj.force_text_dnn,
            feature_sweeping_config=feature_sweeping_config
        )
    except Exception as e:
        logger.error("AutoML featurizer fitting script terminated with an exception of type: {}".format(type(e)))
        run_lifecycle_utilities.fail_run(fit_featurizer_run, e)
        raise


def _prep_input_data(
    run: Run,
    iteration_name: str,
    automl_settings_obj: AzureAutoMLSettings,
    script_directory: Optional[str],
    dataprep_json: str,
    entry_point: str,
    parent_run: Run,
    verifier: Optional[VerifierManager] = None
) -> Tuple[Dict[str, Any], ExperimentObserver, AutoMLFeatureConfigManager]:

    with tracer.start_as_current_span(
            TelemetryConstants.SPAN_FORMATTING.format(
                TelemetryConstants.COMPONENT_NAME, TelemetryConstants.DATA_PREPARATION
            ),
            user_facing_name=TelemetryConstants.DATA_PREPARATION_USER_FACING
    ):
        logger.info('Preparing input data for {} iteration for run {}.'.format(iteration_name, run.id))

        calculated_experiment_info = None
        data_preparer = None
        if dataprep_json:
            data_preparer = DataPreparerFactory.get_preparer(dataprep_json)
            conducive_for_streaming = _are_inputs_conducive_for_streaming(automl_settings_obj, data_preparer)
            if conducive_for_streaming and data_preparer.data_characteristics is not None:
                calculated_experiment_info = \
                    CaclulatedExperimentInfo(data_preparer.data_characteristics.num_rows,
                                             data_preparer.data_characteristics.num_numerical_columns,
                                             data_preparer.data_characteristics.num_categorical_columns,
                                             data_preparer.data_characteristics.num_text_columns,
                                             memory_utilities.get_available_physical_memory())

        feature_config_manager = _build_feature_config_manager(run.experiment)
        feature_config_manager.fetch_all_feature_profiles_for_run(
            parent_run_id=parent_run.id,
            automl_settings=automl_settings_obj,
            caclulated_experiment_info=calculated_experiment_info
        )

        if feature_config_manager.is_streaming_enabled():
            logger.info('Service responded with streaming enabled')
            _modify_settings_for_streaming(
                automl_settings_obj,
                dataprep_json)
        else:
            logger.info('Service responded with streaming disabled')

        fit_iteration_parameters_dict = _prepare_data(
            data_preparer=data_preparer,
            automl_settings_obj=automl_settings_obj,
            script_directory=script_directory,
            entry_point=entry_point,
            verifier=verifier
        )

    experiment_observer = AzureExperimentObserver(parent_run, file_logger=logger)

    if automl_settings_obj.enable_streaming:
        logger.info("Streaming enabled")

    return fit_iteration_parameters_dict, experiment_observer, feature_config_manager


def _cache_dataset(
    cache_store: CacheStore,
    dataset: DatasetBase,
    experiment_observer: ExperimentObserver,
    parent_run: Run
) -> None:
    try:
        cache_store.set(DATASET_BASE_CACHE_KEY, dataset)
        logger.info("Successfully cached dataset.")
    except Exception:
        logger.error("Failed to cache dataset.")
        raise

    logger.info('Preparation for run id {} finished successfully.'.format(parent_run.id))
    experiment_observer.report_status(ExperimentStatus.ModelSelection, "Beginning model selection.")


def _init_cache_store(experiment: Experiment, parent_run_id: str) -> CacheStore:
    cache_data_store = _get_cache_data_store(experiment)
    return _get_cache_store(data_store=cache_data_store, run_id=parent_run_id)


def transfer_files_from_setup(run: Run, setup_container_id: str,
                              feature_config_path: str, engineered_names_path: str) -> None:
    """
    Helper function that transfers essential files from the setup run's data container to the featurization run.
    Note that download only occurs for the master process.

    :param run: the run object to which we are downloading the files.
    :param setup_container_id: the id string of the setup run's data container.
    :param feature_config_path: the path to the feature_config object in the setup run's data container.
    :param engineered_names_path: the path to the engineered_feature_names object in the setup run's data container.
    :return: None
    """
    if is_master_process():
        run._client.artifacts.download_artifact(RUN_ORIGIN, setup_container_id,
                                                feature_config_path, feature_config_path)
        run._client.artifacts.download_artifact(RUN_ORIGIN, setup_container_id,
                                                engineered_names_path, engineered_names_path)

    with PollForMaster(
            proceed_on_condition=lambda: os.path.exists(feature_config_path) and os.path.exists(engineered_names_path)
    ):
        # TODO replace this with an MPI barrier
        logger.info("Setup artifacts successfully retrieved.")
