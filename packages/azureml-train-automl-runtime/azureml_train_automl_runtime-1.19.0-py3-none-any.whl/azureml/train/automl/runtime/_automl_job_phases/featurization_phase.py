# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
from typing import Any, Dict, Optional

from azureml.automl.core._experiment_observer import ExperimentObserver
from azureml.automl.core.constants import PreparationRunTypeConstants
from azureml.automl.runtime import training_utilities
from azureml.automl.runtime._feature_sweeped_state_container import FeatureSweepedStateContainer
from azureml.automl.core._run import RunType
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.core import Run
from azureml.train.automl._automl_feature_config_manager import AutoMLFeatureConfigManager
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.exceptions import ClientException
from azureml.train.automl.runtime._automl_job_phases.utilities import PhaseUtil

logger = logging.getLogger(__name__)


class FeaturizationPhase:
    """AutoML job phase that featurizes the data."""

    @staticmethod
    def run(
        automl_parent_run: Run,
        automl_settings: AzureAutoMLSettings,
        cache_store: CacheStore,
        current_run: RunType,
        experiment_observer: ExperimentObserver,
        feature_config_manager: AutoMLFeatureConfigManager,
        feature_sweeped_state_container: FeatureSweepedStateContainer,
        fit_iteration_parameters_dict: Dict[str, Any],
        remote: bool,
        verifier: Optional[VerifierManager] = None
    ) -> DatasetBase:
        """Run the featurization phase."""
        # Transform raw input, validate and save to cache store.
        logger.info('Set problem info. AutoML featurization for run {}.'.format(current_run.id))
        transformed_data_context, _ = PhaseUtil.set_problem_info_for_featurized_data(
            current_run,
            automl_parent_run,
            fit_iteration_parameters_dict,
            automl_settings,
            cache_store,
            experiment_observer,
            verifier,
            feature_config_manager,
            PreparationRunTypeConstants.FEATURIZATION_ONLY,
            feature_sweeped_state_container)
        if transformed_data_context is None:
            raise ClientException("Unexpectedly received null TransformedDataContext after featurization completed. "
                                  "Cannot set problem info.", has_pii=False)
        return training_utilities.init_dataset(
            transformed_data_context=transformed_data_context,
            cache_store=cache_store,
            automl_settings=automl_settings,
            remote=remote,
            init_all_stats=False,
            keep_in_memory=False)
