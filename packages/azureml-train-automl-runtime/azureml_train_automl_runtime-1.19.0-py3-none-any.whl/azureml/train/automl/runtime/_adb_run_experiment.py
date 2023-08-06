# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class that runs automl run on ADB worker node."""
import datetime
import json
import logging
import os
from typing import cast, Union, Any, List, Optional, Dict

import gc
from azureml._base_sdk_common.service_discovery import HISTORY_SERVICE_ENDPOINT_KEY
from azureml._restclient.jasmine_client import JasmineClient
from azureml._restclient.service_context import ServiceContext
from azureml._restclient.exceptions import ServiceException
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared._diagnostics.validation import Validation
from azureml.core import Run, Datastore
from azureml.core.authentication import AzureMLTokenAuthentication
from azureml.core.experiment import Experiment
from azureml.core.workspace import Workspace
from azureml._common.exceptions import AzureMLException
from azureml.data.constants import WORKSPACE_BLOB_DATASTORE

from azureml.automl.core import logging_utilities
from azureml.automl.core.shared import log_server
from azureml.automl.runtime import data_transformation
from azureml.automl.runtime import fit_pipeline as fit_pipeline_helper
from azureml.automl.runtime import training_utilities
from azureml.automl.runtime.automl_pipeline import AutoMLPipeline
from azureml.automl.runtime.data_context import RawDataContext, TransformedDataContext
from azureml.automl.runtime.featurizer.transformer.featurization_utilities import skip_featurization
import azureml.automl.runtime._ml_engine as ml_engine
from azureml.automl.runtime.streaming_data_context import StreamingTransformedDataContext
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.onnx_convert import OnnxConverter
from azureml.automl.core.onnx_convert import OnnxConvertConstants
from azureml.automl.core.systemusage_telemetry import SystemResourceUsageTelemetryFactory
from azureml.train.automl._automl_feature_config_manager import AutoMLFeatureConfigManager
from azureml.train.automl._amlloguploader import _AMLLogUploader
from azureml.train.automl import _logging  # type: ignore
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl._execute_with_retry import ExecuteWithRetry
from azureml.train.automl.utilities import _get_package_version
from azureml.automl.core.shared import logging_utilities as log_utils
from azureml.automl.core.shared.exceptions import CacheException, ErrorTypes
from azureml.train.automl.constants import ComputeTargets
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.datasets import ClientDatasets
from ._adb_get_data import get_input_datamodel_from_dataprep_json, _input_data_model
from ._automl import _set_problem_info
from ._azureautomlruncontext import AzureAutoMLRunContext
from ._cachestorefactory import CacheStoreFactory
from .run import AutoMLRun
from ._automl_model_explain import _automl_perform_best_run_explain_model


MAX_RETRY_COUNT_ON_EXCEPTION = 5
BACK_OFF_FACTOR = 2
MAX_RETRY_COUNT_DURING_SETUP = 10000
MAX_WAIT_IN_SECONDS = 300
SLEEP_TIME = 10


logger = logging.getLogger(__name__)


def adb_run_experiment(input_params):
    """
    Read run configuration, get next pipeline, and call fit iteration.

    :param input_params: List of input parameters.
    :type input_params: list
    :return:
    :rtype: None
    """
    worker_id = input_params[0]
    run_context = input_params[1]
    subscription_id = run_context.get('subscription_id', None)
    resource_group = run_context.get('resource_group', None)
    workspace_name = run_context.get('workspace_name', None)
    location = run_context.get('location', None)
    aml_token = run_context.get('aml_token', None)
    aml_token_expiry = run_context.get('aml_token_expiry', None)
    experiment_name = run_context.get('experiment_name', None)
    experiment_id = run_context.get('experiment_id', None)
    parent_run_id = run_context.get('parent_run_id', None)
    service_url = run_context.get('service_url', None)
    discovery_url = run_context.get('discovery_url', None)
    dataprep_json = run_context.get('dataprep_json', None)
    automl_settings_str = run_context.get('automl_settings_str', None)
    _set_env_variables(subscription_id,
                       resource_group,
                       workspace_name,
                       experiment_name,
                       aml_token,
                       aml_token_expiry,
                       service_url,
                       discovery_url)

    adb_experiment = _AdbAutomlExperiment(parent_run_id,
                                          subscription_id,
                                          resource_group,
                                          workspace_name,
                                          experiment_name,
                                          experiment_id,
                                          aml_token,
                                          aml_token_expiry,
                                          service_url,
                                          location,
                                          automl_settings_str,
                                          dataprep_json,
                                          worker_id,
                                          discovery_url)
    adb_experiment.run()


def _set_env_variables(subscription_id, resource_group, workspace_name, experiment_name,
                       aml_token, aml_token_expiry, service_url, discovery_url):
    df_value_list = [(subscription_id, "subscription_id"),
                     (resource_group, "resource_group"),
                     (workspace_name, "workspace_name"),
                     (experiment_name, "experiment_name"),
                     (aml_token, "aml_token"),
                     (aml_token_expiry, "aml_token_expiry"),
                     (service_url, "service_url")]
    for var, var_name in df_value_list:
        Validation.validate_value(var, var_name)

    os.environ["AZUREML_ARM_SUBSCRIPTION"] = subscription_id
    os.environ["AZUREML_ARM_RESOURCEGROUP"] = resource_group
    os.environ["AZUREML_ARM_WORKSPACE_NAME"] = workspace_name
    os.environ["AZUREML_ARM_PROJECT_NAME"] = experiment_name
    os.environ["AZUREML_RUN_TOKEN"] = aml_token
    os.environ["AZUREML_RUN_TOKEN_EXPIRY"] = str(aml_token_expiry)
    os.environ["AZUREML_SERVICE_ENDPOINT"] = service_url
    os.environ["AZUREML_DISCOVERY_SERVICE_ENDPOINT"] = discovery_url


def log_message(logging_level=logging.INFO, parent_run_id=None, worker_id=None, message=None):
    """
    Use to log messages.

    :param logging_level: The logging level to use.
    :type logging_level: int
    :param parent_run_id: The associated parent run ID.
    :type parent_run_id: str
    :param worker_id: The associated worker node ID.
    :type worker_id: str
    :param message: The associated message.
    :type message: str
    :return:
    :rtype: None
    """
    if logging_level == logging.ERROR:
        logger.error("{0}, {1}, {2}".format(parent_run_id, worker_id, message))
    elif logging_level == logging.DEBUG:
        logger.debug("{0}, {1}, {2}".format(parent_run_id, worker_id, message))
    elif logging_level == logging.WARNING:
        logger.warning("{0}, {1}, {2}".format(parent_run_id, worker_id, message))
    else:
        logger.info("{0}, {1}, {2}".format(parent_run_id, worker_id, message))


class _AdbAutomlExperiment:

    DATASET_CACHED_KEY = 'dataset_cached_object'
    CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA = '_CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA_'

    def __init__(self,
                 parent_run_id,
                 subscription_id,
                 resource_group,
                 workspace_name,
                 experiment_name,
                 experiment_id,
                 aml_token,
                 aml_token_expiry,
                 service_url,
                 location,
                 automl_settings_str,
                 dataprep_json,
                 worker_id,
                 discovery_url):
        self.parent_run_id = parent_run_id
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.workspace_name = workspace_name
        self.experiment_name = experiment_name
        self.experiment_id = experiment_id
        self.aml_token = aml_token
        self.aml_token_expiry = aml_token_expiry
        self.service_url = service_url
        self.location = location
        self.worker_id = worker_id
        self.automl_settings_str = automl_settings_str
        self.dataset = None  # type: Optional[ClientDatasets]
        self.discovery_url = discovery_url

        os.environ["AZUREML_RUN_TOKEN"] = self.aml_token
        os.environ["AZUREML_RUN_TOKEN_EXPIRY"] = str(self.aml_token_expiry)

        self.feature_config_manager = AutoMLFeatureConfigManager(jasmine_client=self._create_client())

        Contract.assert_value(automl_settings_str, "automl_settings_str")
        self.automl_settings = AzureAutoMLSettings(
            self._rehydrate_experiment(), **json.loads(self.automl_settings_str))

        # Don't reuse path from user's local machine for ADB runs
        self.automl_settings.path = os.getcwd()

        _logging.set_run_custom_dimensions(automl_settings=self.automl_settings,
                                           parent_run_id=self.parent_run_id,
                                           child_run_id=None)

        self._usage_telemetry = SystemResourceUsageTelemetryFactory.get_system_usage_telemetry()
        self._usage_telemetry.start()

        Contract.assert_value(dataprep_json, "dataprep_json")
        self.dataprep_json = dataprep_json
        self.jasmine_client_exception_count = 0

        try:
            # Note that this is due to known issue in shap library
            # Until that issue is fixed this is temporary mitigation specific
            # to AzureDatabricks.
            import matplotlib as mpl
            mpl.use('AGG')
        except Exception as e:
            log_utils.log_traceback(e, logger, is_critical=False)
            self.log_message(message="Failed set the matplot backend", logging_level=logging.ERROR)

    def _should_retry(self, output, exception, current_retry):
        pipeline_dto = output
        if pipeline_dto is not None:
            # reset exception counter since we were able to establish connnection
            self.jasmine_client_exception_count = 0
            should_retry = ((pipeline_dto.pipeline_spec is None or pipeline_dto.pipeline_spec == '') and
                            not pipeline_dto.is_experiment_over)
            should_retry = (should_retry and
                            ((pipeline_dto.childrun_id is not None or pipeline_dto.childrun_id == '') and
                             not self._is_special_run(pipeline_dto.childrun_id)))
            return (should_retry, BACK_OFF_FACTOR)
        elif exception is not None:
            self.jasmine_client_exception_count += 1
            if self.jasmine_client_exception_count == MAX_RETRY_COUNT_ON_EXCEPTION:
                return (False, BACK_OFF_FACTOR)

            return (True, BACK_OFF_FACTOR)

        return (False, BACK_OFF_FACTOR)

    def _is_special_run(self, run_id):
        return run_id.endswith("setup") or run_id.endswith("ModelExplain")

    def _get_next_pipeline(self):
        jasmine_client = self._create_client()
        pipeline_dto = jasmine_client.get_next_pipeline(
            self.parent_run_id, self.worker_id)
        return pipeline_dto

    def log_message(self, message, logging_level=logging.DEBUG):
        log_message(logging_level=logging_level,
                    parent_run_id=self.parent_run_id,
                    worker_id=self.worker_id,
                    message=message)

    def run(self):

        parent_run_id = self.parent_run_id
        worker_id = self.worker_id
        log_message(parent_run_id=parent_run_id, worker_id=worker_id,
                    message="Starting experiment run on worker node...")

        try:
            while True:
                execute_with_retry = ExecuteWithRetry(
                    MAX_RETRY_COUNT_DURING_SETUP,
                    MAX_WAIT_IN_SECONDS,
                    self._should_retry,
                    self.log_message,
                    "jasmine_client.get_next_pipeline()")
                pipeline_dto = execute_with_retry.execute(
                    self._get_next_pipeline,
                    func_name="get_next_pipeline")
                if pipeline_dto.is_experiment_over:
                    log_message(parent_run_id=parent_run_id, worker_id=worker_id,
                                message="Experiment finished.")
                    break
                child_run_id = pipeline_dto.childrun_id
                with log_server.new_log_context(run_id=child_run_id):
                    os.environ["AZUREML_RUN_ID"] = child_run_id
                    self.fit_iteration(pipeline_dto, child_run_id)
        except Exception as e:
            log_utils.log_traceback(e, logger, is_critical=False)
            log_message(logging_level=logging.ERROR, parent_run_id=parent_run_id,
                        worker_id=worker_id, message='Spark experiment failed')
            raise
        finally:
            try:
                parent_run = self._rehydrate_run(parent_run_id)
                filename, file_extension = os.path.splitext(self.automl_settings.debug_log)
                if os.path.exists(self.automl_settings.debug_log):
                    if not self.automl_settings.debug_log.startswith("/dbfs"):
                        formatted_file_name = "logs/{0}_{1}_{2}{3}".format(
                            filename, str(worker_id),
                            datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%SZ"),
                            file_extension)

                        parent_run.upload_file(formatted_file_name, self.automl_settings.debug_log)
            except Exception as e:
                log_utils.log_traceback(e, logger, is_critical=False)
                log_message(logging_level=logging.WARNING, parent_run_id=parent_run_id,
                            worker_id=worker_id, message="Upload to parent run failed")

        log_message(parent_run_id=parent_run_id, worker_id=worker_id,
                    message="Finished experiment run on worker node.")

    def _rehydrate_experiment(self):
        auth = AzureMLTokenAuthentication.create(self.aml_token,
                                                 AzureMLTokenAuthentication._convert_to_datetime(
                                                     self.aml_token_expiry),
                                                 self.service_url,
                                                 self.subscription_id,
                                                 self.resource_group,
                                                 self.workspace_name,
                                                 self.experiment_name,
                                                 self.parent_run_id)
        workspace = Workspace(self.subscription_id,
                              self.resource_group, self.workspace_name,
                              auth=auth,
                              _location=self.location,
                              _disable_service_check=True)
        experiment = Experiment(workspace, self.experiment_name)
        return experiment

    def _rehydrate_run(self, run_id):
        return Run(self._rehydrate_experiment(), run_id)

    def setup_iteration(self, verifier, current_run, onnx_cvt, pkg_ver, run_id):
        logger.info('Beginning setup iteration: {}.'.format(run_id))
        input_data = get_input_datamodel_from_dataprep_json(
            dataprep_json=self.dataprep_json, automl_settings=self.automl_settings,
            log_message=self.log_message, verifier=verifier)

        with logging_utilities.log_activity(logger, activity_name='validate_training_data'):
            ml_engine.validate(
                X=input_data.X,
                y=input_data.y,
                X_valid=input_data.X_valid,
                y_valid=input_data.y_valid,
                sample_weight=input_data.sample_weight,
                sample_weight_valid=input_data.sample_weight_valid,
                cv_splits_indices=input_data.cv_splits_indices,
                automl_settings=self.automl_settings)

        _X = input_data.X
        _y = input_data.y
        transformed_data_context = None
        cache_store = self._get_cache_store()
        logger.info('Using {} for caching transformed data.'.format(type(cache_store).__name__))

        if self.automl_settings.enable_onnx_compatible_models:
            # Initialize the ONNX converter with the raw data and save metadata in the cache store.
            enable_split_onnx_models = self.automl_settings.enable_split_onnx_featurizer_estimator_models
            onnx_cvt = \
                OnnxConverter(logger=logger,
                              version=pkg_ver,
                              is_onnx_compatible=self.automl_settings.enable_onnx_compatible_models,
                              enable_split_onnx_featurizer_estimator_models=enable_split_onnx_models)
            self._initialize_onnx_converter_with_cache_store(onnx_cvt=onnx_cvt,
                                                             input_data=input_data,
                                                             parent_run_id=self.parent_run_id,
                                                             cache_store=cache_store)

        transformed_data_context = self._get_transformed_data_context(
            input_data,
            cache_store,
            verifier
        )
        # Cache the dataset irrespective of whether featurization was turned off or not.
        # We save the hard work done to transform the data
        # on the Azure Blob Store cache / local disk, from where other worker nodes can download from.
        self.dataset = training_utilities.init_client_dataset(
            transformed_data_context=cast(TransformedDataContext, transformed_data_context),
            cache_store=cache_store,
            automl_settings=self.automl_settings,
            remote=False,
            init_all_stats=False,
            keep_in_memory=False)
        cache_store.set(self.DATASET_CACHED_KEY, self.dataset)
        logger.info("Initialized ClientDatasets from transformed_data_context during setup.")

        _X = transformed_data_context.X
        _y = transformed_data_context.y

        with logging_utilities.log_activity(logger, activity_name='_set_problem_info'):
            # P.S. The set_problem_info method also featurizes the data.
            _set_problem_info(X=_X,
                              y=_y,
                              automl_settings=self.automl_settings,
                              current_run=current_run,
                              transformed_data_context=transformed_data_context,
                              cache_store=cache_store,
                              is_adb_run=True)

        log_message(parent_run_id=self.parent_run_id, worker_id=self.worker_id,
                    message="{0}: set_problem_info completed ..".
                    format(run_id))

        if verifier is not None:
            parent_run = self._rehydrate_run(self.parent_run_id)
            parent_run_context = AzureAutoMLRunContext(parent_run, False)
            verifier.write_result_file(parent_run_context)

        # Setup's finished. Eagerly clean up the input and/or featurized data.
        # The model iteration workers will either recreate the featurized data (cache=False)
        # or load the data from the Azure Blob Store cache (cache=True)
        _X = None
        _y = None
        self.clear_input_data([transformed_data_context, input_data])
        logger.info('Setup iteration "{}" finished successfully.'.format(run_id))

    def fit_iteration_core(self,
                           verifier, current_run, pkg_ver, train_frac,
                           pipeline_dto, run_id, onnx_cvt):
        # worker node
        logger.info('Beginning fit iteration: {}.'.format(run_id))
        pipeline_id = pipeline_dto.pipeline_id
        # if transformed_data_context is not set and if cache is enabled and featurization is turned on
        # try to load from cache
        cache_store = self._get_cache_store()

        if self.automl_settings.enable_onnx_compatible_models:
            enable_split_onnx_models = self.automl_settings.enable_split_onnx_featurizer_estimator_models
            onnx_cvt = \
                OnnxConverter(logger=logger,
                              version=pkg_ver,
                              is_onnx_compatible=self.automl_settings.enable_onnx_compatible_models,
                              enable_split_onnx_featurizer_estimator_models=enable_split_onnx_models)
            onnx_mdl_name = 'AutoML_ONNX_Model_[{}]'.format(self.parent_run_id)
            onnx_mdl_desc = {'ParentRunId': self.parent_run_id}

        self._recover_dataset(current_run, verifier, onnx_cvt=onnx_cvt)

        if self.automl_settings.enable_onnx_compatible_models and onnx_cvt is not None:
            if cache_store is not None and not onnx_cvt.is_initialized():
                # Try to initialize the ONNX converter with cached converter metadata if it's
                # not initialized.
                logger.info('Get ONNX converter init metadata for run {}.'.format(run_id))
                cache_store.load()
                cached_data_dict = cache_store.get([self.CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA])
                if cached_data_dict is not None and cached_data_dict:
                    onnx_cvt_init_metadata_dict = cached_data_dict.get(
                        self.CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA,
                        None)  # type: Optional[Dict[str, Any]]
                    if onnx_cvt_init_metadata_dict is not None:
                        logger.info(
                            'Initialize ONNX converter with cached metadata run {}.'.format(run_id))
                        onnx_cvt.initialize_with_metadata(metadata_dict=onnx_cvt_init_metadata_dict,
                                                          model_name=onnx_mdl_name,
                                                          model_desc=onnx_mdl_desc)

            if onnx_cvt.is_initialized():
                logger.info('Successfully initialized ONNX converter for run {}.'.format(run_id))
            else:
                logger.info('Failed to initialize ONNX converter for run {}.'.format(run_id))

        automl_run_context = AzureAutoMLRunContext(Run.get_context(), is_adb_run=True)
        automl_pipeline = AutoMLPipeline(automl_run_context, pipeline_dto.pipeline_spec, pipeline_id,
                                         train_frac)

        parent_run = self._rehydrate_run(self.parent_run_id)
        result = fit_pipeline_helper.fit_pipeline(
            automl_pipeline=automl_pipeline,
            automl_settings=self.automl_settings,
            automl_run_context=automl_run_context,
            remote=True,
            dataset=self.dataset,
            onnx_cvt=onnx_cvt,
            bypassing_model_explain=parent_run.get_tags().get('model_explain_run'),
        )

        if result.errors:
            err_type = next(iter(result.errors))
            exception_info = result.errors[err_type]
            exception_obj = cast(BaseException, exception_info['exception'])
            log_message(logging_level=logging.ERROR,
                        parent_run_id=self.parent_run_id, worker_id=self.worker_id,
                        message="Exception raised")

            if exception_info['is_critical']:
                raise exception_obj.with_traceback(exception_obj.__traceback__)

        score = result.score
        duration = result.actual_time
        log_message(parent_run_id=self.parent_run_id,
                    worker_id=self.worker_id, message="Score: {0}".format(score))
        log_message(parent_run_id=self.parent_run_id,
                    worker_id=self.worker_id, message="Duration: {0}".format(duration))

    def model_explain_iteration(self, verifier, current_run):
        log_message(parent_run_id=self.parent_run_id, worker_id=self.worker_id,
                    message="Model explain for best run starts.")
        # Rehydrate the parent run
        parent_run = AutoMLRun(self._rehydrate_experiment(), self.parent_run_id)
        # Recover the dataset from cache store
        self._recover_dataset(current_run, verifier)
        # Perform model explanations for best run
        _automl_perform_best_run_explain_model(
            parent_run, cast(ClientDatasets, self.dataset), self.automl_settings,
            ComputeTargets.ADB, current_run)
        current_run.complete()
        log_message(parent_run_id=self.parent_run_id, worker_id=self.worker_id,
                    message="Model explain for best run ends.")

    def fit_iteration(self, pipeline_dto, run_id):
        """
        Fit iteration method.

        :param pipeline_dto: Pipeline details to fit.
        :type pipeline_dto: PipelineDto
        :param run_id: run id.
        :type run_id: string
        """
        run_id = pipeline_dto.childrun_id
        pipeline_id = pipeline_dto.pipeline_id

        train_frac = 1.0
        if hasattr(pipeline_dto, 'training_percent') and pipeline_dto.training_percent is not None:
            train_frac = float(pipeline_dto.training_percent) / 100

        """
        # TODO: Fix pipeline spec logging (#438111)
        log_message(parent_run_id=self.parent_run_id, worker_id=self.worker_id,
                    message="Received pipeline: {0} for run id '{1}'".format(pipeline_dto.pipeline_spec, run_id))
        """
        logger.info('Received pipeline ID {}'.format(pipeline_id))

        verifier = VerifierManager()

        # This is due to token expiry issue
        current_run = self._rehydrate_run(run_id)

        with _AMLLogUploader(current_run, self.worker_id):
            try:
                log_message(parent_run_id=self.parent_run_id, worker_id=self.worker_id,
                            message="{0}: Starting childrun...".format(run_id))
                self._execute_with_retry_ignored(current_run.start)

                onnx_cvt = None     # type: Optional[OnnxConverter]
                pkg_ver = _get_package_version()
                if run_id.endswith("setup"):
                    self.setup_iteration(verifier, current_run, onnx_cvt, pkg_ver, run_id)
                elif run_id.lower().endswith("ModelExplain".lower()):
                    self.model_explain_iteration(verifier, current_run)
                else:
                    self.fit_iteration_core(verifier, current_run, pkg_ver, train_frac,
                                            pipeline_dto, run_id, onnx_cvt)
                self._execute_with_retry_ignored(current_run.complete)
                log_message(parent_run_id=self.parent_run_id, worker_id=self.worker_id,
                            message="{0}: Fit iteration completed successfully.".format(run_id))

            except Exception as e:
                log_utils.log_traceback(e, logger, is_critical=False)
                log_message(logging_level=logging.ERROR, parent_run_id=self.parent_run_id,
                            worker_id=self.worker_id, message='{}: Iteration failed'.format(run_id))
                if current_run is not None:
                    run_lifecycle_utilities.fail_run(current_run, e)
                if run_id.endswith("setup"):
                    try:
                        error_message = str({'exception': e})
                        current_run.tag("errors", error_message)

                        errors = {
                            'errors': error_message,
                            'error_code': getattr(e, 'error_code', ErrorTypes.Unclassified),
                            'failure_reason': getattr(e, 'error_type', ErrorTypes.Unclassified)
                        }
                        current_run.add_properties(errors)

                    except AzureMLException as ae:
                        log_utils.log_traceback(ae, logger, is_critical=False)
                        self.log_message(logging_level=logging.ERROR,
                                         message="Failed to add 'errors' properties to run due to exception")
                        raise

    def _execute_with_retry_ignored(self, func: Any) -> None:
        try:
            func()
        except ServiceException as e:
            log_utils.log_traceback(e, logger, is_critical=False)
            log_message(logging_level=logging.ERROR,
                        parent_run_id=self.parent_run_id,
                        worker_id=self.worker_id,
                        message="Exception occurred while making call to RunHistory")
            if e.status_code == 400 and " is already set." in e.message:
                pass
            else:
                raise

    def _recover_dataset(self, current_run, verifier, onnx_cvt=None):
        """Recover the dataset object for training and model explanation iteration."""

        logger.info('Recovering dataset from cache store for run {}.'.format(current_run.id))

        cache_store = self._get_cache_store()

        if (self.dataset is None or
                not skip_featurization(self.automl_settings.featurization, self.automl_settings.is_timeseries)):
            current_run.add_properties({'LoadedFromCache': 'True'})
            self.dataset = self._load_data_from_cache(cache_store)

        logger.info('Successfully recovering dataset from cache store for run {}.'.format(current_run.id))

    def _create_client(self):
        auth = AzureMLTokenAuthentication.create(self.aml_token,
                                                 AzureMLTokenAuthentication._convert_to_datetime(
                                                     self.aml_token_expiry),
                                                 self.service_url,
                                                 self.subscription_id,
                                                 self.resource_group,
                                                 self.workspace_name,
                                                 self.experiment_name,
                                                 self.parent_run_id)
        os.environ[HISTORY_SERVICE_ENDPOINT_KEY] = self.service_url
        # Discovery url will not be same as history service end point
        # Based on workspace vnet, workspace will have workspace dependent discovery end point
        os.environ["AZUREML_DISCOVERY_SERVICE_ENDPOINT"] = self.discovery_url
        service_context = ServiceContext(self.subscription_id,
                                         self.resource_group,
                                         self.workspace_name,
                                         None,
                                         self.discovery_url,
                                         auth)
        return JasmineClient(service_context=service_context,
                             experiment_name=self.experiment_name,
                             experiment_id=self.experiment_id,
                             user_agent="JasmineClient")

    def _get_transformed_data_context(self,
                                      input_data: _input_data_model,
                                      cache_store: CacheStore,
                                      verifier: VerifierManager) \
            -> Union[TransformedDataContext, StreamingTransformedDataContext]:
        with logging_utilities.log_activity(logger, activity_name='_setup_cache'):
            try:
                log_message(parent_run_id=self.parent_run_id, worker_id=self.worker_id,
                            message="Trying to setup cache")

                raw_data_context = RawDataContext(automl_settings_obj=self.automl_settings,
                                                  X=input_data.X,
                                                  y=input_data.y,
                                                  X_valid=input_data.X_valid,
                                                  y_valid=input_data.y_valid,
                                                  sample_weight=input_data.sample_weight,
                                                  sample_weight_valid=input_data.sample_weight_valid,
                                                  x_raw_column_names=input_data.x_raw_column_names,
                                                  cv_splits_indices=input_data.cv_splits_indices)

                feature_sweeping_config = self.feature_config_manager.get_feature_sweeping_config(
                    enable_feature_sweeping=self.automl_settings.enable_feature_sweeping,
                    parent_run_id=self.parent_run_id,
                    task_type=self.automl_settings.task_type)
                with logging_utilities.log_activity(logger, activity_name='transform_data'):
                    transformed_data_context = data_transformation\
                        .transform_data(raw_data_context=raw_data_context,
                                        cache_store=cache_store,
                                        is_onnx_compatible=self.automl_settings.enable_onnx_compatible_models,
                                        enable_feature_sweeping=self.automl_settings.enable_feature_sweeping,
                                        enable_dnn=self.automl_settings.enable_dnn,
                                        force_text_dnn=self.automl_settings.force_text_dnn,
                                        verifier=verifier,
                                        feature_sweeping_config=feature_sweeping_config,
                                        working_dir=self.automl_settings.path)

                log_message(parent_run_id=self.parent_run_id, worker_id=self.worker_id,
                            message="Cache is setup")

                return transformed_data_context
            except Exception as e:
                log_utils.log_traceback(e, logger, is_critical=False)
                log_message(logging_level=logging.ERROR, parent_run_id=self.parent_run_id,
                            worker_id=self.worker_id, message="Featurization failed with exception")
                raise

    def _load_data_from_cache(self, cache_store: CacheStore) -> Optional[ClientDatasets]:
        with logging_utilities.log_activity(logger, activity_name='_load_data_from_cache'):
            try:
                log_message(parent_run_id=self.parent_run_id, worker_id=self.worker_id,
                            message="Loading from cache")
                cache_store.load()
                dataset_dict = cache_store.get([self.DATASET_CACHED_KEY])
                if dataset_dict is None or dataset_dict.get(self.DATASET_CACHED_KEY) is None:
                    raise CacheException("Failed to find {} in cache_store.".format(self.DATASET_CACHED_KEY),
                                         has_pii=False)
                return cast(Optional[ClientDatasets], dataset_dict.get(self.DATASET_CACHED_KEY))
            except CacheException:
                raise
            except Exception as e:
                log_utils.log_traceback(e, logger, is_critical=False)
                log_message(logging_level=logging.ERROR, parent_run_id=self.parent_run_id,
                            worker_id=self.worker_id,
                            message="Load from cache failed with exception")
                raise

    def _get_cache_store(self):
        data_store = self._get_data_store()

        return CacheStoreFactory.get_cache_store(temp_location=self.automl_settings.path,
                                                 run_target='adb',
                                                 run_id=self.parent_run_id,
                                                 data_store=data_store)

    def _get_data_store(self):
        try:
            experiment = self._rehydrate_experiment()
            return Datastore.get(experiment.workspace, WORKSPACE_BLOB_DATASTORE)
        except Exception as e:
            log_utils.log_traceback(e, logger, is_critical=False)
            log_message(logging_level=logging.ERROR, parent_run_id=self.parent_run_id,
                        worker_id=self.worker_id,
                        message="No default data store found")
            return None

    def _initialize_onnx_converter_with_cache_store(self,
                                                    onnx_cvt: OnnxConverter,
                                                    input_data: _input_data_model,
                                                    parent_run_id: str,
                                                    cache_store: Optional[CacheStore]) -> None:
        # Initialize the ONNX converter with the raw data and save metadata in the cache store.
        if cache_store is not None and self.automl_settings.enable_onnx_compatible_models:
            onnx_mdl_name = '{}[{}]'.format(OnnxConvertConstants.OnnxModelNamePrefix, parent_run_id)
            onnx_mdl_desc = {'ParentRunId': parent_run_id}
            logger.info('Initialize ONNX converter for run {}.'.format(parent_run_id))
            onnx_cvt.initialize_input(X=input_data.X,
                                      x_raw_column_names=input_data.x_raw_column_names,
                                      model_name=onnx_mdl_name,
                                      model_desc=onnx_mdl_desc)
            onnx_cvt_init_metadata_dict = onnx_cvt.get_init_metadata_dict()
            # If the cache store and the onnx converter init metadata are valid, save it into cache store.
            if (onnx_cvt_init_metadata_dict is not None and
                    onnx_cvt_init_metadata_dict):
                logger.info('Successfully initialized ONNX converter for run {}.'.format(parent_run_id))
                logger.info('Begin saving onnx initialization metadata for run {}.'.format(parent_run_id))
                cache_store.set(self.CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA, onnx_cvt_init_metadata_dict)
                logger.info('Successfully Saved onnx initialization metadata for run {}.'.format(parent_run_id))
            else:
                logger.info('Failed to initialize ONNX converter for run {}.'.format(parent_run_id))

    def __del__(self):
        """
        Clean up AutoML loggers and close files.
        """
        if self._usage_telemetry is not None:
            self._usage_telemetry.stop()

    def clear_input_data(self, input_data_list: List[Union[TransformedDataContext, Any]]) -> None:
        for input_data in input_data_list:
            if input_data is not None:
                input_data.X = None
                input_data.y = None
                input_data.X_valid = None
                input_data.y_valid = None
                if isinstance(input_data, TransformedDataContext):
                    input_data.cv_splits = None
                self._gc_object(input_data)

    def _gc_object(self, obj):
        if obj is not None:
            del obj
            gc.collect()
