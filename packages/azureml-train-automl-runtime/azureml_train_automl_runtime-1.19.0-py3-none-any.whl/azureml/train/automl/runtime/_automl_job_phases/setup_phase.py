# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
from typing import Any, Dict, Optional, Tuple

from azureml.automl.core._experiment_observer import ExperimentObserver
from azureml.automl.runtime import training_utilities
from azureml.automl.runtime._feature_sweeped_state_container import FeatureSweepedStateContainer
from azureml.automl.core._run import RunType
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.onnx_convert import OnnxConverter
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.core import Run
from azureml.train.automl._automl_feature_config_manager import AutoMLFeatureConfigManager
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.runtime._automl_job_phases.utilities import PhaseUtil

logger = logging.getLogger(__name__)


class SetupPhase:
    """
    Setup job phase for the AutoML run. The setup phase initializes state variables used during the run.

    (For instance, depending on the run, the ONNX converter, dataset to use for training, or featurization info
    may be initialized.)
    """

    @staticmethod
    def run(
        automl_parent_run: Run,
        automl_settings: AzureAutoMLSettings,
        cache_store: CacheStore,
        current_run: RunType,
        experiment_observer: ExperimentObserver,
        feature_config_manager: AutoMLFeatureConfigManager,
        fit_iteration_parameters_dict: Dict[str, Any],
        prep_type: str,
        remote: bool,
        validate_training_data: bool,
        verifier: VerifierManager
    ) -> Tuple[Optional[DatasetBase], Optional[OnnxConverter], Optional[FeatureSweepedStateContainer]]:
        """Run the setup phase."""
        onnx_cvt = SetupPhase._build_and_initialize_onnx_converter(
            fit_iteration_parameters_dict,
            automl_settings,
            automl_parent_run.id)
        if validate_training_data:
            SetupPhase._validate_training_data(fit_iteration_parameters_dict, automl_settings)
        logger.info('Set problem info. AutoML setup phase for run {}.'.format(current_run.id))
        transformed_data_context, feature_sweeped_state_container = \
            PhaseUtil.set_problem_info_for_featurized_data(
                current_run,
                automl_parent_run,
                fit_iteration_parameters_dict,
                automl_settings,
                cache_store,
                experiment_observer,
                verifier=verifier,
                feature_config_manager=feature_config_manager,
                prep_type=prep_type)

        dataset = None
        if transformed_data_context is not None:
            dataset = training_utilities.init_dataset(
                transformed_data_context=transformed_data_context,
                cache_store=cache_store,
                automl_settings=automl_settings,
                remote=remote,
                init_all_stats=False,
                keep_in_memory=False)

        return dataset, onnx_cvt, feature_sweeped_state_container

    @staticmethod
    def _build_and_initialize_onnx_converter(
        fit_iteration_parameters_dict: Dict[str, Any],
        automl_settings: AzureAutoMLSettings,
        parent_run_id: str
    ) -> Optional[OnnxConverter]:
        onnx_cvt = PhaseUtil.build_onnx_converter(automl_settings)
        if not onnx_cvt:
            return None
        logger.info('Initialize ONNX converter from input data during setup.')
        onnx_cvt.initialize_input(X=fit_iteration_parameters_dict.get('X'),
                                  x_raw_column_names=fit_iteration_parameters_dict.get("x_raw_column_names"),
                                  model_name=PhaseUtil.get_onnx_model_name(parent_run_id),
                                  model_desc=PhaseUtil.get_onnx_model_desc(parent_run_id))
        return onnx_cvt

    @staticmethod
    def _validate_training_data(
        fit_iteration_parameters_dict: Dict[str, Any],
        automl_settings: AzureAutoMLSettings,
    ) -> None:
        logger.info('Validating training data.')
        training_utilities.validate_training_data_dict(fit_iteration_parameters_dict, automl_settings)
        logger.info('Input data successfully validated.')
