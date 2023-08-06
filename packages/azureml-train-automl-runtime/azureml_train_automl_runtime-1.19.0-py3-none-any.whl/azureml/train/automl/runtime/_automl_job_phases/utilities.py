# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
from typing import Any, Dict, Optional, Tuple, Union

from azureml.automl.core._experiment_observer import ExperimentObserver
from azureml.automl.core.constants import PreparationRunTypeConstants
from azureml.automl.core.onnx_convert import OnnxConvertConstants
from azureml.automl.core.shared import logging_utilities
from azureml.automl.runtime import data_transformation
from azureml.automl.runtime._feature_sweeped_state_container import FeatureSweepedStateContainer
from azureml.automl.core._run import RunType
from azureml.automl.runtime.data_context import RawDataContext, TransformedDataContext
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.onnx_convert import OnnxConverter
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.streaming_data_context import StreamingTransformedDataContext
from azureml.core import Run
from azureml.train.automl._automl_feature_config_manager import AutoMLFeatureConfigManager
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.runtime import _automl
from azureml.train.automl.utilities import _get_package_version

logger = logging.getLogger(__name__)


class PhaseUtil:
    """Utils leveraged by AutoML job phases."""

    @staticmethod
    def build_onnx_converter(
        automl_settings: AzureAutoMLSettings
    ) -> Optional[OnnxConverter]:
        """Build the ONNX converter for the run."""
        if not automl_settings.enable_onnx_compatible_models:
            return None
        pkg_ver = _get_package_version()
        enable_split_onnx_models = automl_settings.enable_split_onnx_featurizer_estimator_models
        return OnnxConverter(
            logger=logger,
            version=pkg_ver,
            is_onnx_compatible=automl_settings.enable_onnx_compatible_models,
            enable_split_onnx_featurizer_estimator_models=enable_split_onnx_models)

    @staticmethod
    def build_raw_data_context(
        fit_iteration_parameters_dict: Dict[str, Any],
        automl_settings: AzureAutoMLSettings
    ) -> RawDataContext:
        return RawDataContext(
            automl_settings_obj=automl_settings,
            X=fit_iteration_parameters_dict.get('X'),
            y=fit_iteration_parameters_dict.get('y'),
            X_valid=fit_iteration_parameters_dict.get('X_valid'),
            y_valid=fit_iteration_parameters_dict.get('y_valid'),
            sample_weight=fit_iteration_parameters_dict.get('sample_weight'),
            sample_weight_valid=fit_iteration_parameters_dict.get('sample_weight_valid'),
            x_raw_column_names=fit_iteration_parameters_dict.get('x_raw_column_names'),
            cv_splits_indices=fit_iteration_parameters_dict.get('cv_splits_indices'),
            training_data=fit_iteration_parameters_dict.get('training_data'),
            validation_data=fit_iteration_parameters_dict.get('validation_data'))

    @staticmethod
    def get_onnx_model_desc(parent_run_id: str) -> Dict[str, str]:
        """Get the description for the ONNX model."""
        return {'ParentRunId': parent_run_id}

    @staticmethod
    def get_onnx_model_name(parent_run_id: str) -> str:
        """Get the name for the ONNX model."""
        return '{}[{}]'.format(OnnxConvertConstants.OnnxModelNamePrefix, parent_run_id)

    @staticmethod
    def set_problem_info_for_featurized_data(
        current_run: RunType,
        parent_run: Run,
        fit_iteration_parameters_dict: Dict[str, Any],
        automl_settings: AzureAutoMLSettings,
        cache_store: CacheStore,
        experiment_observer: ExperimentObserver,
        verifier: Optional[VerifierManager] = None,
        feature_config_manager: Optional[AutoMLFeatureConfigManager] = None,
        prep_type: str = PreparationRunTypeConstants.SETUP_ONLY,
        feature_sweeped_state_container: Optional[FeatureSweepedStateContainer] = None
    ) -> Tuple[Optional[Union[TransformedDataContext, StreamingTransformedDataContext]],
               Optional[FeatureSweepedStateContainer]]:
        """
        Sets problem info in the run that generates it, which will either be the setup or featurization run,
        depending on the code path/scenario.

        :param current_run: The current run.
        :param fit_iteration_parameters_dict: Dictionary of parameters for fit iteration.
        :param automl_settings: Object containing AutoML settings as specified by user.
        :param cache_store: The cache store.
        :param experiment_observer: The experiment observer.
        :param verifier: The fault verifier manager.
        :param feature_sweeped_state_container: The feature sweeped state container.
        :param prep_type: The type of preparation run currently being performed.
        :return: The transformed data context (after the problem info has been set),
            the featurization properties, and the raw data context.
        """
        transformed_data_context, featurization_properties = \
            PhaseUtil._transform_and_validate_input_data(
                parent_run,
                fit_iteration_parameters_dict,
                automl_settings,
                cache_store,
                feature_config_manager,
                experiment_observer,
                verifier=verifier,
                prep_type=prep_type,
                feature_sweeped_state_container=feature_sweeped_state_container)
        if transformed_data_context is not None:
            logger.info('Setting problem info.')
            _automl._set_problem_info(
                transformed_data_context.X,
                transformed_data_context.y,
                automl_settings=automl_settings,
                current_run=current_run,
                transformed_data_context=transformed_data_context,
                cache_store=cache_store
            )
        return transformed_data_context, featurization_properties

    @staticmethod
    def _transform_and_validate_input_data(
        parent_run: Run,
        fit_iteration_parameters_dict: Dict[str, Any],
        automl_settings: AzureAutoMLSettings,
        cache_store: CacheStore,
        feature_config_manager: AutoMLFeatureConfigManager,
        experiment_observer: Optional[ExperimentObserver] = None,
        verifier: Optional[VerifierManager] = None,
        prep_type: str = PreparationRunTypeConstants.SETUP_ONLY,
        feature_sweeped_state_container: Optional[FeatureSweepedStateContainer] = None
    ) -> Tuple[Optional[Union[TransformedDataContext, StreamingTransformedDataContext]],
               Optional[FeatureSweepedStateContainer]]:
        with logging_utilities.log_activity(logger=logger, activity_name="Getting transformed data context."):
            raw_data_context = PhaseUtil.build_raw_data_context(fit_iteration_parameters_dict, automl_settings)
            logger.info('Using {} for caching transformed data.'.format(type(cache_store).__name__))

            feature_sweeping_config = feature_config_manager.get_feature_sweeping_config(
                enable_feature_sweeping=automl_settings.enable_feature_sweeping,
                parent_run_id=parent_run.id,
                task_type=automl_settings.task_type)

            transformed_data_context = None
            if prep_type == PreparationRunTypeConstants.SETUP_WITHOUT_FEATURIZATION:
                logger.info("Checking if feature sweeping is necessary.")
                feature_sweeped_state_container = data_transformation.get_transformers_for_full_featurization(
                    raw_data_context,
                    cache_store=cache_store,
                    is_onnx_compatible=automl_settings.enable_onnx_compatible_models,
                    experiment_observer=experiment_observer,
                    enable_feature_sweeping=automl_settings.enable_feature_sweeping,
                    verifier=verifier,
                    enable_streaming=automl_settings.enable_streaming,
                    feature_sweeping_config=feature_sweeping_config,
                    enable_dnn=automl_settings.enable_dnn,
                    force_text_dnn=automl_settings.force_text_dnn
                )
                if feature_sweeped_state_container is None:
                    # we do not kick off a separate featurization run
                    with logging_utilities.log_activity(logger=logger,
                                                        activity_name="Skipping setup/featurization run split. "
                                                                      "Beginning full featurization logic."):
                        transformed_data_context = data_transformation.complete_featurization(
                            raw_data_context,
                            working_dir=automl_settings.path,
                            cache_store=cache_store,
                            experiment_observer=experiment_observer,
                            verifier=verifier,
                            enable_streaming=automl_settings.enable_streaming,
                            feature_sweeping_config=feature_sweeping_config,
                        )
            elif prep_type == PreparationRunTypeConstants.FEATURIZATION_ONLY:
                with logging_utilities.log_activity(logger=logger,
                                                    activity_name="Beginning full featurization logic."):
                    transformed_data_context = data_transformation.complete_featurization(
                        raw_data_context,
                        working_dir=automl_settings.path,
                        cache_store=cache_store,
                        experiment_observer=experiment_observer,
                        verifier=verifier,
                        enable_streaming=automl_settings.enable_streaming,
                        feature_sweeping_config=feature_sweeping_config,
                        feature_sweeped_state_container=feature_sweeped_state_container
                    )
            else:
                # likely equal to PreparationRunTypeConstants.SETUP_ONLY,
                # in which we want to default to legacy setup behavior.
                with logging_utilities.log_activity(logger=logger,
                                                    activity_name="Invoking default data transformation behavior."):
                    transformed_data_context = data_transformation.transform_data(
                        raw_data_context,
                        working_dir=automl_settings.path,
                        cache_store=cache_store,
                        is_onnx_compatible=automl_settings.enable_onnx_compatible_models,
                        enable_feature_sweeping=automl_settings.enable_feature_sweeping,
                        enable_dnn=automl_settings.enable_dnn,
                        force_text_dnn=automl_settings.force_text_dnn,
                        experiment_observer=experiment_observer,
                        verifier=verifier,
                        enable_streaming=automl_settings.enable_streaming,
                        feature_sweeping_config=feature_sweeping_config)
        return transformed_data_context, feature_sweeped_state_container
