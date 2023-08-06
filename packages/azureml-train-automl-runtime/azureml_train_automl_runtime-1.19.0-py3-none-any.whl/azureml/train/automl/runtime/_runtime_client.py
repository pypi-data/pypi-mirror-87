# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""AutoML object in charge of orchestrating various AutoML runs for predicting models."""
from typing import Any, cast, List, Optional, Dict, Tuple

import json
import logging
import math
import os
from datetime import datetime, timezone

import numpy as np
from azureml._common._error_definition import AzureMLError
from azureml._restclient.models import IterationTask
from azureml._restclient.models.create_parent_run import CreateParentRun
from azureml._restclient.service_context import ServiceContext
from azureml.automl.core import dataprep_utilities, dataset_utilities
from azureml.automl.core._experiment_observer import ExperimentStatus
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.console_interface import ConsoleInterface
from azureml.automl.core.constants import PreparationRunTypeConstants, RunHistoryEnvironmentVariableNames
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared import log_server
from azureml.automl.core.shared._diagnostics.automl_error_definitions import RunInterrupted
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared._error_response_constants import ErrorCodes
from azureml.automl.core.shared.constants import TelemetryConstants, TIMEOUT_TAG
from azureml.automl.core.shared.exceptions import (AutoMLException,
                                                   ClientException,
                                                   UserException)
from azureml.automl.core.shared.limit_function_call_exceptions import TimeoutException
from azureml.automl.runtime import training_utilities
from azureml.automl.core._run import RunType
from azureml.automl.runtime._run_history.offline_automl_run import (
    OfflineAutoMLRun, OfflineAutoMLRunContext, OfflineAutoMLRunUtil)
from azureml.automl.runtime._run_history.run_history_managers.run_manager import RunManager
from azureml.automl.runtime.automl_run_context import AutoMLAbstractRunContext
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.fit_output import FitOutput, _FitOutputUtils
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.automl.runtime.shared.problem_info import ProblemInfo
from azureml.automl.runtime.shared.types import DataInputType
from azureml.core import Run
from azureml.exceptions import AzureMLException, ServiceException as AzureMLServiceException
from azureml.telemetry.contracts import RequiredFields, RequiredFieldKeys, \
    StandardFields, StandardFieldKeys
from azureml.train.automl import constants
from azureml.train.automl import _logging   # type: ignore
from azureml.train.automl._azure_experiment_observer import AzureExperimentObserver
from azureml.train.automl._constants_azureml import ContinueFlagStates
from azureml.train.automl._remote_console_interface import RemoteConsoleInterface
from azureml.train.automl.automl_adb_run import AutoMLADBRun
from azureml.train.automl.constants import ComputeTargets
from azureml.train.automl.exceptions import FeaturizationException, ModelFitException
from azureml.train.automl.run import AutoMLRun
from azureml.train.automl.runtime import utilities as train_runtime_utilities
from azureml.train.automl.runtime._automl_job_phases import FeaturizationPhase, SetupPhase, TrainingIteration
from azureml.train.automl.runtime._synchronizable_runs import SynchronizableAutoMLRun

from ._adb_driver_node import _AdbDriverNode
from ._adb_run_experiment import adb_run_experiment
from ._azureautomlruncontext import AzureAutoMLRunContext
from ._cachestorefactory import CacheStoreFactory
from ._automl_model_explain import _automl_perform_best_run_explain_model

logger = logging.getLogger(__name__)


class RuntimeClient:
    """Client to run AutoML experiments on Azure Machine Learning platform."""

    def __init__(self, azureautomlclient):
        """
        Construct the AzureMLClient class.

        :param azureautomlclient: The azureml.train.automl.AzureAutoMLClient experiment
        """

        self.azureautomlclient = azureautomlclient
        self._model_best = None
        self._model_name_best = None
        self._run_best = None
        self._started_processing_offline_run_history = False
        self._is_continued_run = False
        self._next_pipelines = None

    def __del__(self):
        """Clean up AutoML loggers and close files."""
        try:
            if self.azureautomlclient._usage_telemetry is not None:
                self.azureautomlclient._usage_telemetry.stop()
        except Exception:
            # last chance, nothing can be done, so ignore any exception
            pass

    def cancel(self):
        """
        Cancel the ongoing local run.

        :return: None
        """
        self.azureautomlclient._status = constants.Status.Terminated

    def _create_parent_run_for_local(self,
                                     use_validation_service: bool,
                                     X: Optional[DataInputType] = None,
                                     y: Optional[DataInputType] = None,
                                     sample_weight: Optional[DataInputType] = None,
                                     X_valid: Optional[DataInputType] = None,
                                     y_valid: Optional[DataInputType] = None,
                                     sample_weight_valid: Optional[DataInputType] = None,
                                     cv_splits_indices: Optional[List[Any]] = None,
                                     existing_run: bool = False,
                                     managed_run_id: Optional[str] = None,
                                     training_data: Optional[DataInputType] = None,
                                     validation_data: Optional[DataInputType] = None,
                                     verifier: Optional[VerifierManager] = None,
                                     _script_run: Optional[Run] = None,
                                     parent_run_id: Optional[str] = None) -> AutoMLRun:
        """
        Create parent run in Run History containing AutoML experiment information.

        :return: AutoML parent run
        :rtype: azureml.train.automl.AutoMLRun
        """
        #  Prepare data before entering for loop
        logger.info("Extracting user Data")
        self.azureautomlclient.input_data = training_utilities.format_training_data(
            X, y, sample_weight, X_valid, y_valid, sample_weight_valid,
            cv_splits_indices=cv_splits_indices, user_script=self.azureautomlclient.user_script,
            training_data=training_data, validation_data=validation_data,
            label_column_name=self.azureautomlclient.automl_settings.label_column_name,
            weight_column_name=self.azureautomlclient.automl_settings.weight_column_name,
            cv_split_column_names=self.azureautomlclient.automl_settings.cv_split_column_names,
            automl_settings=self.azureautomlclient.automl_settings,
            is_adb_run=True,
            verifier=verifier)
        training_utilities.set_task_parameters(y=self.azureautomlclient.input_data.get('y'),
                                               automl_settings=self.azureautomlclient.automl_settings)

        Contract.assert_value(self.azureautomlclient.input_data, "azureautomlclient.input_data")

        if managed_run_id is not None:
            self.azureautomlclient.parent_run_id = managed_run_id
        if not existing_run:
            parent_run_dto = self._validate_data_and_create_parent_run_dto(
                use_validation_service=use_validation_service, X=X, y=y, sample_weight=sample_weight, X_valid=X_valid,
                y_valid=y_valid, sample_weight_valid=sample_weight_valid, cv_splits_indices=cv_splits_indices,
                training_data=training_data, validation_data=validation_data, parent_run_id=parent_run_id
            )
            if managed_run_id is None:
                try:
                    logger.info("Start creating parent run")
                    self.azureautomlclient.parent_run_id = self.azureautomlclient._jasmine_client.post_parent_run(
                        parent_run_dto)

                    Contract.assert_value(self.azureautomlclient.parent_run_id, "parent_run_id")

                    logger.info("Successfully created a parent run with ID: {}".format(
                        self.azureautomlclient.parent_run_id))
                except (AutoMLException, AzureMLException, AzureMLServiceException):
                    raise
                except Exception as e:
                    logging_utilities.log_traceback(e, logger)
                    raise ClientException("Error when trying to create parent run in automl service",
                                          has_pii=False) from None
            _logging.set_run_custom_dimensions(automl_settings=self.azureautomlclient.automl_settings,
                                               parent_run_id=self.azureautomlclient.parent_run_id,
                                               child_run_id=None)

            self.azureautomlclient._jasmine_client.set_parent_run_status(
                self.azureautomlclient.parent_run_id, constants.RunState.PREPARE_RUN)

            if _script_run is not None:
                _script_run.add_properties({"automl_id": self.azureautomlclient.parent_run_id})
                r_fields = RequiredFields()
                r_fields[RequiredFieldKeys.SUBSCRIPTION_ID_KEY] = \
                    self.azureautomlclient.experiment.workspace.subscription_id
                r_fields[RequiredFieldKeys.WORKSPACE_ID_KEY] = self.azureautomlclient.experiment.workspace.name
                s_fields = StandardFields()
                s_fields[StandardFieldKeys.PARENT_RUN_ID_KEY] = self.azureautomlclient.parent_run_id

            if self.azureautomlclient.automl_settings.track_child_runs:
                self.azureautomlclient.current_run = AutoMLRun(
                    self.azureautomlclient.experiment,
                    self.azureautomlclient.parent_run_id,
                    host=self.azureautomlclient.automl_settings.service_url)
            else:
                self.azureautomlclient.current_run = SynchronizableAutoMLRun(
                    self.azureautomlclient.experiment,
                    self.azureautomlclient.parent_run_id,
                    host=self.azureautomlclient.automl_settings.service_url
                )

            # For back compatibility, check if the properties were added already as part of create parent run dto.
            # If not, add it here. Note that this should be removed once JOS changes are stably deployed
            if (
                    self.azureautomlclient.DISPLAY_TASK_TYPE_PROPERTY not in
                    self.azureautomlclient.current_run.properties or
                    self.azureautomlclient.SDK_DEPENDENCIES_PROPERTY not in
                    self.azureautomlclient.current_run.properties
            ):
                properties_to_update = self.azureautomlclient._get_current_run_properties_to_update()
                self.azureautomlclient.current_run.add_properties(properties_to_update)

        else:
            self.azureautomlclient.current_run = AutoMLRun(
                self.azureautomlclient.experiment,
                self.azureautomlclient.parent_run_id,
                host=self.azureautomlclient.automl_settings.service_url)

        if self.azureautomlclient.user_script:
            logger.info("[ParentRunID:{}] Local run using user script.".format(
                self.azureautomlclient.parent_run_id))
        else:
            logger.info("[ParentRunID:{}] Local run using input X and y.".format(
                self.azureautomlclient.parent_run_id))

        self.azureautomlclient._console_writer.println("Parent Run ID: {}\n".format(
            self.azureautomlclient.parent_run_id))
        logger.info("Parent Run ID: " + self.azureautomlclient.parent_run_id)

        self.azureautomlclient._status = constants.Status.InProgress

        dataset_utilities.log_dataset("X", X, self.azureautomlclient.current_run)
        dataset_utilities.log_dataset("y", y, self.azureautomlclient.current_run)
        dataset_utilities.log_dataset("X_valid", X_valid, self.azureautomlclient.current_run)
        dataset_utilities.log_dataset("y_valid", y_valid, self.azureautomlclient.current_run)

        return self.azureautomlclient.current_run

    @staticmethod
    def _should_use_validation_service(
        X: Optional[DataInputType],
        y: Optional[DataInputType],
        sample_weight: Optional[DataInputType],
        X_valid: Optional[DataInputType],
        y_valid: Optional[DataInputType],
        sample_weight_valid: Optional[DataInputType],
        cv_splits_indices: Optional[DataInputType],
        training_data: Optional[DataInputType],
        validation_data: Optional[DataInputType]
    ) -> bool:
        """Determine whether to use JOS validation service to validate data."""
        data_inputs = [X, y, sample_weight, X_valid, y_valid, sample_weight_valid, cv_splits_indices,
                       training_data, validation_data]
        # Use validation service only if every specified data input at this stage is a Dataflow.
        for data_input in data_inputs:
            if data_input is not None and not dataprep_utilities.is_dataflow(data_input):
                logger.info("Validation will be done locally, since the input is not a Dataset.")
                return False
        return True

    def _validate_data_and_create_parent_run_dto(
        self,
        use_validation_service: bool,
        X: Optional[DataInputType],
        y: Optional[DataInputType],
        sample_weight: Optional[DataInputType],
        X_valid: Optional[DataInputType],
        y_valid: Optional[DataInputType],
        sample_weight_valid: Optional[DataInputType],
        cv_splits_indices: Optional[List[Any]],
        training_data: Optional[DataInputType],
        validation_data: Optional[DataInputType],
        parent_run_id: Optional[str]
    ) -> CreateParentRun:
        if use_validation_service:
            parent_run_dto = self.azureautomlclient._create_and_validate_parent_run_dto(
                target=constants.ComputeTargets.LOCAL,
                training_data=training_data,
                validation_data=validation_data,
                X=X,
                y=y,
                sample_weight=sample_weight,
                X_valid=X_valid,
                y_valid=y_valid,
                sample_weight_valid=sample_weight_valid,
                cv_splits_indices=cv_splits_indices,
                parent_run_id=parent_run_id
            )
        else:
            # If not using validation service, validate the full training data locally.
            training_utilities.validate_training_data_dict(
                self.azureautomlclient.input_data,
                self.azureautomlclient.automl_settings,
                check_sparse=True)
            parent_run_dto = self.azureautomlclient._create_parent_run_dto(
                constants.ComputeTargets.LOCAL,
                parent_run_id=parent_run_id)
        return parent_run_dto

    def _fit_local(self, X=None, y=None, sample_weight=None, X_valid=None, y_valid=None, sample_weight_valid=None,
                   cv_splits_indices=None, existing_run=False,
                   training_data=None, validation_data=None, _script_run=None, parent_run_id=None):
        # Start telemetry in local training
        self.azureautomlclient._usage_telemetry.start()

        verifier = VerifierManager()
        self._is_continued_run = existing_run

        # Determine whether to use JOS validation service to validate data.
        use_validation_service = self._should_use_validation_service(
            X, y, sample_weight, X_valid, y_valid, sample_weight_valid, cv_splits_indices, training_data,
            validation_data
        )

        self._create_parent_run_for_local(
            use_validation_service=use_validation_service,
            X=X, y=y, sample_weight=sample_weight, X_valid=X_valid, y_valid=y_valid,
            cv_splits_indices=cv_splits_indices, existing_run=existing_run,
            managed_run_id=self.azureautomlclient.automl_settings._local_managed_run_id,
            sample_weight_valid=sample_weight_valid,
            training_data=training_data, validation_data=validation_data, verifier=verifier, _script_run=_script_run,
            parent_run_id=parent_run_id)

        cache_store = CacheStoreFactory.get_cache_store(
            temp_location=self.azureautomlclient.automl_settings.path,
            run_target=ComputeTargets.LOCAL,
            run_id=cast(str, self.azureautomlclient.parent_run_id))
        experiment_observer = AzureExperimentObserver(self.azureautomlclient.current_run,
                                                      self.azureautomlclient._console_writer,
                                                      logger,
                                                      upload_metrics=False)

        if not existing_run:
            logger.info("Setting Run {} status to: {}".format(str(self.azureautomlclient.parent_run_id),
                                                              constants.RunState.START_RUN))
            self.azureautomlclient._jasmine_client.set_parent_run_status(
                self.azureautomlclient.parent_run_id, constants.RunState.START_RUN)

        # Run the setup phase.
        dataset, self.azureautomlclient.onnx_cvt, feature_sweeped_state_container = SetupPhase.run(
            automl_parent_run=self.azureautomlclient.current_run,
            automl_settings=self.azureautomlclient.automl_settings,
            cache_store=cache_store,
            current_run=self.azureautomlclient.current_run,
            experiment_observer=experiment_observer,
            feature_config_manager=self.azureautomlclient.feature_config_manager,
            fit_iteration_parameters_dict=self.azureautomlclient.input_data,
            prep_type=PreparationRunTypeConstants.SETUP_WITHOUT_FEATURIZATION,
            remote=False,

            # When not using validation service, the full dataset has already been validated locally, so there's
            # no need to re-validate it
            validate_training_data=use_validation_service,

            verifier=verifier
        )

        # Unless the dataset was initialized in setup phase, run the featurization phase to get the featurized dataset.
        if not dataset:
            if not feature_sweeped_state_container:
                raise FeaturizationException(
                    "Neither a dataset nor a feature sweeped state container was produced by the setup phase.",
                    has_pii=False)
            dataset = FeaturizationPhase.run(
                automl_parent_run=self.azureautomlclient.current_run,
                automl_settings=self.azureautomlclient.automl_settings,
                cache_store=cache_store,
                current_run=self.azureautomlclient.current_run,
                experiment_observer=experiment_observer,
                feature_config_manager=self.azureautomlclient.feature_config_manager,
                feature_sweeped_state_container=feature_sweeped_state_container,
                fit_iteration_parameters_dict=self.azureautomlclient.input_data,
                remote=False,
                verifier=verifier
            )

        subsampling = self.azureautomlclient.current_run._get_problem_info_dict().get('subsampling', False)

        try:
            #  Set up interface to print execution progress
            ci = ConsoleInterface("score", self.azureautomlclient._console_writer, mask_sampling=not subsampling)
        except Exception as e:
            logging_utilities.log_traceback(e, logger)
            raise

        self.azureautomlclient.experiment_start_time = datetime.utcnow()

        parent_run_context = AzureAutoMLRunContext(self.azureautomlclient.current_run)

        if existing_run:
            self.azureautomlclient.current_run.tag("continue", ContinueFlagStates.ContinueSet)
            self.azureautomlclient.current_iter = len(
                list(self.azureautomlclient.current_run.get_children(_rehydrate_runs=False)))
        else:
            self.azureautomlclient.current_iter = 0
            if verifier is not None:
                verifier.write_result_file(
                    parent_run_context,
                    working_directory=self.azureautomlclient.automl_settings.path)
                ci.print_guardrails(verifier.ret_dict['faults'])

        logger.info("Beginning model selection.")
        experiment_observer.report_status(ExperimentStatus.ModelSelection, "Beginning model selection.")
        ci.print_descriptions()
        ci.print_columns()

        try:
            self._execute_all_iterations(
                ci, dataset, existing_run, experiment_observer, parent_run_context)
            logger.info("Parent Run {} Complete.".format(self.azureautomlclient.parent_run_id))
        except Exception as e:
            # TODO: uncomment when logging is safe and we're assured it doesn't throw
            # logging_utilities.log_traceback(e, logger)

            # Pass on the error, the run will eventually be marked with the right status on the service side (i.e.
            # stuck run handler from JOS)
            ci.print_error(e)
            logger.error("Encountered an exception of type {} while running model iterations.".format(type(e)))

    def _execute_all_iterations(
            self,
            ci: ConsoleInterface,
            dataset: DatasetBase,
            existing_run: bool,
            experiment_observer: AzureExperimentObserver,
            parent_run_context: AzureAutoMLRunContext) -> None:
        """
        Run all model training iterations sequentially.

        This method also attempts to set the terminal status on the parent run, but it's based on a best-effort basis.
        """
        fit_outputs = []  # type: List[FitOutput]
        try:
            logger.info("Starting local loop.")

            # If this run is synchronizable, synchronize it. This is so tags and properties (like problem info,
            # used by Miro) will be up-to-date before selecting algorithms for & running child iterations.
            self._synchronize_run()

            while self.azureautomlclient.current_iter < self.azureautomlclient.automl_settings.iterations:
                if self.azureautomlclient._status == constants.Status.Terminated:
                    self.azureautomlclient._console_writer.println(
                        "Stopping criteria reached at iteration {0}. Ending experiment.".format(
                            self.azureautomlclient.current_iter - 1))
                    logger.info(
                        "Stopping criteria reached at iteration {0}. Ending experiment.".format(
                            self.azureautomlclient.current_iter - 1))
                    break
                logger.info("Start iteration: {0}".format(self.azureautomlclient.current_iter))
                with logging_utilities.log_activity(logger=logger,
                                                    activity_name=TelemetryConstants.FIT_ITERATION_NAME):
                    fit_output = self._fit_iteration(
                        fit_outputs, ci, dataset=dataset)
                self.azureautomlclient.current_iter = self.azureautomlclient.current_iter + 1
                # History for a 'Continue'd run is kinda tricky to get (e.g. fetching all runs from RH),
                # and in some sense extraneous given this is an optimization primarily intended for ManyModels
                # Hence, don't cache previous outputs for a continued run, and let JOS figure it out.
                if not existing_run and fit_output:
                    fit_outputs.append(fit_output)

            # Upload summarized offline run history.
            # (Note: there will only be offline run history to upload if tracking child runs is disabled.)
            self._upload_and_process_offline_run_history(parent_run_context, fit_outputs)

            # Set cached outputs on the parent AutoMLRun object that will be returned to the user.
            # This enables exposing the run results without invoking RH & artifact store to fetch child runs
            # and the best model. This optimization is used only for Many Models
            self._set_cached_outputs_on_parent_run()

            if RuntimeClient._any_childruns_succeeded(fit_outputs):
                self.azureautomlclient.current_run.set_tags({
                    'best_score': str(self.azureautomlclient._score_best),
                    'best_pipeline': str(self._model_name_best)
                })

                self._set_parent_run_status(constants.RunState.COMPLETE_RUN)

                try:
                    # Perform model explanations for best run
                    _automl_perform_best_run_explain_model(
                        self.azureautomlclient.current_run, dataset,
                        self.azureautomlclient.automl_settings,
                        compute_target=constants.ComputeTargets.LOCAL,
                        current_run=None,
                        experiment_observer=experiment_observer,
                        console_interface=ci)
                except Exception:
                    pass
            else:
                error_msg = "All child runs failed."
                if all(ErrorCodes.USER_ERROR == fo.failure_reason for fo in fit_outputs):
                    # All iterations failed with user errors
                    raise UserException.create_without_pii(error_msg)
                raise ModelFitException.create_without_pii(error_msg)

            self._synchronize_run()

            # For Many Models, metrics may be configured to sync to the server infrequently.
            # Flush all queued metrics to the server before completing the run
            if self.azureautomlclient.automl_settings.many_models:
                self.azureautomlclient.current_run.flush()
        except KeyboardInterrupt:
            # (Note for when not tracking child runs: in the case of a keyboard interrupt, we forgo uploading
            # summarized offline run history. This is because we're viewing a KeyboardInterrupt here as the user's
            # quick attempt @ Ctrl + C before taking more drastic measures to kill the process. We can take the
            # time after Ctrl + C to set essential state, but if we take too long / abuse this window (by
            # uploading files, etc.), the thinking is that we may lose this opportunity altogether.)
            logger.info(
                "[ParentRunId:{}]Received interrupt. Returning now.".format(self.azureautomlclient.parent_run_id))
            self.azureautomlclient._console_writer.println("Received interrupt. Returning now.")
            self._set_parent_run_status(constants.RunState.CANCEL_RUN,
                                        cancel_reason=AzureMLError.create(RunInterrupted).error_message)
        except (UserException, ModelFitException) as e:
            self._synchronize_run(safe=True)
            self.azureautomlclient._console_writer.println("No successful child runs.")
            self._set_parent_run_status(constants.RunState.FAIL_RUN, error_details=e)
            self._upload_and_process_offline_run_history_safe(parent_run_context, fit_outputs)
        except Exception as e:
            self._synchronize_run(safe=True)
            self._upload_and_process_offline_run_history_safe(parent_run_context, fit_outputs)
            if RuntimeClient._any_childruns_succeeded(fit_outputs):
                self.azureautomlclient._console_writer.println(
                    "Exception thrown. Cancelling run, since there is at least one successful child run.")
                self._set_parent_run_status(constants.RunState.CANCEL_RUN, error_details=e)
            else:
                self.azureautomlclient._console_writer.println("Exception thrown. Terminating run.")
                self._set_parent_run_status(constants.RunState.FAIL_RUN, error_details=e)
        finally:
            # cleanup transformed, featurized data cache
            if dataset is not None:
                cache_clear_status = dataset.clear_cache()
                if not cache_clear_status:
                    logger.warning("Failed to unload the dataset from cache store.")

            # if we are from continue run, remove flag
            if existing_run:
                self.azureautomlclient.current_run.tag("continue", ContinueFlagStates.ContinueNone)

            if isinstance(self.azureautomlclient.current_run, SynchronizableAutoMLRun):
                # Set current run to be an AutoML run (that is not synchronizable).
                # The current run object is returned to the user.
                self.azureautomlclient.current_run = self.azureautomlclient.current_run.to_automl_run()

            # turn off system usage collection on run completion or failure
            if self.azureautomlclient._usage_telemetry is not None:
                self.azureautomlclient._usage_telemetry.stop()

    def _set_parent_run_status(
            self,
            status: constants.RunState,
            error_details: Optional[BaseException] = None,
            cancel_reason: Optional[str] = None
    ) -> None:
        if error_details:
            logging_utilities.log_traceback(error_details, logger)

        if status == constants.RunState.COMPLETE_RUN:
            logger.info("Setting Run {} status to: {}".format(str(self.azureautomlclient.parent_run_id), status))
            self.azureautomlclient._jasmine_client.set_parent_run_status(
                self.azureautomlclient.parent_run_id, constants.RunState.COMPLETE_RUN)
            self.azureautomlclient._status = constants.Status.Completed
        elif status == constants.RunState.CANCEL_RUN:
            logger.info("Setting Run {} status to: {}".format(str(self.azureautomlclient.parent_run_id), status))
            self.azureautomlclient._status = constants.Status.Terminated
            # Create an azureml.core.run.Run object, as a cancel() on AutoMLRun will wind up
            # with warnings / errors for local runs (since it is unsupported)
            core_run = RunManager.create_from_run(self.azureautomlclient.current_run).run
            run_lifecycle_utilities.cancel_run(core_run, cancel_reason)
            self.azureautomlclient._jasmine_client.set_parent_run_status(
                self.azureautomlclient.parent_run_id, constants.RunState.CANCEL_RUN)
        elif status == constants.RunState.FAIL_RUN:
            logger.error("Run {} failed with exception of type: {}".format(
                str(self.azureautomlclient.parent_run_id), type(error_details)))
            self.azureautomlclient._fail_parent_run(error_details=error_details, is_aml_compute=False)
            self.azureautomlclient._status = constants.Status.Terminated

    def _set_cached_outputs_on_parent_run(self) -> None:
        """Set cached outputs on the parent AutoMLRun object that will be returned to the user."""
        # Only cache the output (to avoid RH load) for Many Models.
        # Also, disable this optimization for continued runs. (Continued runs are not guaranteed
        # to have the best child run loaded in memory.)
        if not self.azureautomlclient.automl_settings.many_models or self._is_continued_run:
            return

        best_run = self._run_best

        # If the best_run is an AutoMLRun, convert it to a Run. (AutoMLRun.register_model on
        # a child run does not work / is not desgined to work.)
        if isinstance(best_run, AutoMLRun):
            best_run = Run._dto_to_run(best_run.experiment, best_run._client.run_dto)

        if not isinstance(best_run, Run):
            return

        self.azureautomlclient.current_run._cached_best_run = best_run
        self.azureautomlclient.current_run._cached_best_model = self._model_best

    @staticmethod
    def _any_childruns_succeeded(fit_outputs: List[FitOutput]) -> Optional[bool]:
        if not fit_outputs:
            return False

        result = False
        for output in fit_outputs:
            try:
                # np.nan is considered to be an invalid score, and hence a failed iteration
                # 0.0 can be a valid score
                result = not np.isnan(output.score)
                if result:
                    break   # Found a valid score, skip iterating on other outputs
            except TypeError:
                logger.error("Failed to parse the score: {}. Ignoring it to find if any other child runs had a valid "
                             "score.".format(output.score))
        if not result:
            logger.error("None of the child runs succeeded with a valid score for the given primary metric.")

        return result

    def _get_next_pipeline(
        self,
        problem_info: ProblemInfo,
        previous_fit_outputs: List[FitOutput]
    ) -> IterationTask:
        """Query Jasmine for the next set of pipelines to run."""
        # If there are no cached next pipelines to run, fetch the next batch from Jasmine
        if not self._next_pipelines:
            is_sparse = None
            if problem_info is not None:
                is_sparse = problem_info.is_sparse
            self._next_pipelines = self.azureautomlclient._get_tasks(
                previous_fit_outputs if not self._is_continued_run else None,
                self.azureautomlclient.automl_settings.pipeline_fetch_max_batch_size,
                is_sparse)

        return self._next_pipelines.pop(0)

    def _fit_iteration(self,
                       previous_fit_outputs: List[FitOutput],
                       ci: ConsoleInterface,
                       dataset: DatasetBase) -> Optional[FitOutput]:
        start_iter_time = datetime.utcnow().replace(tzinfo=timezone.utc)

        #  Query Jasmine for the next set of pipelines to run
        problem_info = dataset.get_problem_info()

        task_dto = self._get_next_pipeline(problem_info, previous_fit_outputs)

        if task_dto.is_experiment_over:
            logger.info("Complete task received. Completing experiment")
            self.azureautomlclient.cancel()
            return None

        pipeline_id = task_dto.pipeline_id
        training_percent = float(task_dto.training_percent or 100)

        logger.info('Received pipeline ID {}'.format(pipeline_id))
        ci.print_start(self.azureautomlclient.current_iter)

        errors = []
        fit_output = None   # type: Optional[FitOutput]

        child_run, child_run_context = self._get_child_run_and_context(task_dto)
        with log_server.new_log_context(run_id=child_run.id):
            try:
                # get total run time in seconds and convert to minutes
                elapsed_time = math.floor(
                    int((datetime.utcnow() - self.azureautomlclient.experiment_start_time).total_seconds()) / 60)

                run_lifecycle_utilities.start_run(child_run)

                self._set_environment_variables_for_reconstructing_run(child_run)

                fit_output = TrainingIteration.run(
                    automl_parent_run=self.azureautomlclient.current_run,
                    automl_run_context=child_run_context,
                    automl_settings=self.azureautomlclient.automl_settings,
                    dataset=dataset,
                    onnx_cvt=self.azureautomlclient.onnx_cvt,
                    pipeline_id=pipeline_id,
                    pipeline_spec=task_dto.pipeline_spec,
                    remote=False,
                    training_percent=training_percent,
                    elapsed_time=elapsed_time
                )

                _FitOutputUtils.terminate_child_run(child_run, fit_output, is_aml_compute=False)

                if fit_output.errors:
                    err_type = next(iter(fit_output.errors))
                    exception_info = fit_output.errors[err_type]
                    exception_obj = cast(BaseException, exception_info['exception'])

                    # If a Many Models run, write the exception to the console. This is useful for debugging.
                    if self.azureautomlclient.automl_settings.many_models:
                        ci.print_error('Exception: {}'.format(exception_obj))

                    if err_type == 'model_explanation' and isinstance(exception_obj, ImportError):
                        errors.append('Could not explain model due to missing dependency. Please run: pip install '
                                      'azureml-sdk[interpret]')
                    elif isinstance(exception_obj, TimeoutException):
                        errors.append(exception_obj.message)
                    else:
                        pipeline_spec_details = None    # type: Optional[str]
                        pipeline_id_details = None  # type: Optional[str]
                        if fit_output.pipeline_spec:
                            pipeline_spec_details = "Pipeline Class Names: {}".format(
                                fit_output.pipeline_spec.pipeline_name)
                            pipeline_id_details = "Pipeline ID: {}".format(fit_output.pipeline_spec.pipeline_id)
                        error_msg = ' '.join(filter(None, ['Run {} failed with exception of type: {}.'.format(
                            task_dto.childrun_id, exception_obj.__class__.__name__),
                            pipeline_spec_details, pipeline_id_details]))
                        if isinstance(exception_obj, AutoMLException):
                            msg = exception_obj.message
                            if msg:
                                error_msg = ' '.join([str(exception_obj)])
                        errors.append(error_msg)

                score = fit_output.score
                preprocessor = fit_output.run_preprocessor
                model_name = fit_output.run_algorithm
                best_model = fit_output.fitted_pipeline
            except KeyboardInterrupt:
                run_lifecycle_utilities.cancel_run(
                    child_run, warning_string=AzureMLError.create(RunInterrupted).error_message
                )
                raise   # Stop execution of any further child runs
            except Exception as e:
                logging_utilities.log_traceback(e, logger)
                score = constants.Defaults.DEFAULT_PIPELINE_SCORE
                preprocessor = ''
                model_name = ''
                best_model = None
                errors.append('Run {} failed with exception of type: {}'.format(
                    task_dto.childrun_id, e.__class__.__name__))

            ci.print_pipeline(preprocessor, model_name, train_frac=training_percent / 100)
            self._update_internal_scores_after_iteration(score, best_model, model_name, child_run)

            end_iter_time = datetime.utcnow().replace(tzinfo=timezone.utc)
            start_iter_time, end_iter_time = train_runtime_utilities._calculate_start_end_times(
                start_iter_time,
                end_iter_time,
                child_run)
            iter_duration = str(end_iter_time - start_iter_time).split(".")[0]
            ci.print_end(iter_duration, score, self.azureautomlclient._score_best)

            for error in errors:
                ci.print_error(error)

            return fit_output

    def _get_child_run_and_context(
        self,
        task_dto: IterationTask
    ) -> Tuple[RunType, AutoMLAbstractRunContext]:
        """Get child run and its associated run context."""
        if self.azureautomlclient.automl_settings.track_child_runs:
            run_id = task_dto.childrun_id
            child_run = Run(self.azureautomlclient.experiment, run_id)
            run_context = AzureAutoMLRunContext(child_run)
            return child_run, run_context
        else:
            offline_child_run = OfflineAutoMLRunUtil.create_child_run(
                path=self.azureautomlclient.automl_settings.path,
                parent_run_id=self.azureautomlclient.current_run.id,
                iteration=self.azureautomlclient.current_iter,
                pipeline_spec=task_dto.pipeline_spec)
            offline_run_context = OfflineAutoMLRunContext(offline_child_run)
            return offline_child_run, offline_run_context

    def _init_adb_driver_run(self,
                             run_configuration=None,
                             X=None,
                             y=None,
                             sample_weight=None,
                             X_valid=None,
                             y_valid=None,
                             sample_weight_valid=None,
                             cv_splits_indices=None,
                             training_data=None,
                             validation_data=None,
                             show_output=False,
                             existing_run=False):

        self.azureautomlclient._console_writer.println(
            'Running an experiment on spark cluster: {0}.\n'.format(self.azureautomlclient.experiment.name))

        if not self.azureautomlclient.automl_settings._ignore_package_version_incompatibilities:
            self.azureautomlclient._check_package_compatibilities(is_managed_run=False)

        try:
            if not existing_run:
                self.azureautomlclient._fit_remote_core(run_configuration,
                                                        X=X,
                                                        y=y,
                                                        sample_weight=sample_weight,
                                                        X_valid=X_valid,
                                                        y_valid=y_valid,
                                                        sample_weight_valid=sample_weight_valid,
                                                        cv_splits_indices=cv_splits_indices,
                                                        training_data=training_data,
                                                        validation_data=validation_data)
            # This should be refactored to have RunHistoryClient and make call on it to get token
            # use Experiment object to get name and other parameters
            token_res = self.azureautomlclient.experiment_client._client.run.\
                get_token(experiment_name=self.azureautomlclient.experiment.name,
                          resource_group_name=self.azureautomlclient.experiment.workspace.resource_group,
                          subscription_id=self.azureautomlclient.experiment.workspace.subscription_id,
                          workspace_name=self.azureautomlclient.experiment.workspace.name,
                          run_id=self.azureautomlclient.current_run.run_id)
            aml_token = token_res.token
            aml_token_expiry = token_res.expiry_time_utc

            service_context = ServiceContext(
                subscription_id=self.azureautomlclient.experiment.workspace.subscription_id,
                resource_group_name=self.azureautomlclient.experiment.workspace.resource_group,
                workspace_name=self.azureautomlclient.experiment.workspace.name,
                workspace_id=self.azureautomlclient.experiment.workspace._workspace_id,
                workspace_discovery_url=self.azureautomlclient.experiment.workspace.discovery_url,
                authentication=self.azureautomlclient.experiment.workspace._auth_object)

            run_history_url = service_context._get_run_history_url()
            fn_script = None
            if self.azureautomlclient.automl_settings.data_script:
                with open(self.azureautomlclient.automl_settings.data_script, "r") as f:
                    fn_script = f.read()

            if training_data is None and validation_data is None:
                dataprep_json = dataprep_utilities.get_dataprep_json(
                    X=X,
                    y=y,
                    sample_weight=sample_weight,
                    X_valid=X_valid,
                    y_valid=y_valid,
                    sample_weight_valid=sample_weight_valid,
                    cv_splits_indices=cv_splits_indices)
            else:
                dataprep_json = dataprep_utilities.get_dataprep_json_dataset(
                    training_data=training_data, validation_data=validation_data)

            # Remove path when creating the DTO
            settings_dict = self.azureautomlclient.automl_settings.as_serializable_dict()
            settings_dict['path'] = None

            # build dictionary of context
            run_context = {"subscription_id": self.azureautomlclient.experiment.workspace.subscription_id,
                           "resource_group": self.azureautomlclient.experiment.workspace.resource_group,
                           "location": self.azureautomlclient.experiment.workspace.location,
                           "workspace_name": self.azureautomlclient.experiment.workspace.name,
                           "experiment_name": self.azureautomlclient.experiment.name,
                           "experiment_id": self.azureautomlclient.experiment.id,
                           "parent_run_id": self.azureautomlclient.current_run.run_id,
                           "aml_token": aml_token,
                           "aml_token_expiry": aml_token_expiry,
                           "service_url": run_history_url,
                           "discovery_url": service_context._get_discovery_url(),
                           "automl_settings_str": json.dumps(settings_dict),
                           'dataprep_json': dataprep_json,
                           "get_data_content": fn_script}
            adb_automl_context = [(index, run_context) for index in range(
                0, self.azureautomlclient.automl_settings.max_concurrent_iterations)]

            if not hasattr(self.azureautomlclient.automl_settings, 'is_run_from_test'):
                adb_thread = _AdbDriverNode("AutoML on Spark Experiment: {0}".format(
                    self.azureautomlclient.experiment.name),
                    adb_automl_context,
                    self.azureautomlclient.automl_settings.spark_context,
                    self.azureautomlclient.automl_settings.max_concurrent_iterations,
                    self.azureautomlclient.current_run.run_id)
                adb_thread.start()
                self.azureautomlclient.current_run = AutoMLADBRun(
                    self.azureautomlclient.experiment,
                    self.azureautomlclient.parent_run_id,
                    adb_thread)
            else:
                automlRDD = self.azureautomlclient.automl_settings.\
                    spark_context.parallelize(adb_automl_context,
                                              self.azureautomlclient.automl_settings.max_concurrent_iterations)
                automlRDD.map(adb_run_experiment).collect()

            if show_output:
                RemoteConsoleInterface._show_output(self.azureautomlclient.current_run,
                                                    self.azureautomlclient._console_writer,
                                                    logger,
                                                    self.azureautomlclient.automl_settings.primary_metric)
        except Exception as ex:
            logging_utilities.log_traceback(ex, logger)
            raise

    def _update_internal_scores_after_iteration(self, score, model, model_name, run):
        minimize_metric = self.azureautomlclient.automl_settings.metric_operation == \
            constants.OptimizerObjectives.MINIMIZE

        if self.azureautomlclient._score_best is None or np.isnan(self.azureautomlclient._score_best) or \
                ((score is not None and not np.isnan(score)) and
                 ((minimize_metric and score < self.azureautomlclient._score_best) or
                  (not minimize_metric and score > self.azureautomlclient._score_best))):
            self.azureautomlclient._score_best = score
            self._model_best = model
            self._model_name_best = model_name
            self._run_best = run

    def _set_environment_variables_for_reconstructing_run(
        self,
        run: RunType
    ) -> None:
        """Copy the run information to environment variables. This allows a child process to reconstruct the
        run object."""
        if self.azureautomlclient.automl_settings.track_child_runs:
            self.azureautomlclient._set_environment_variables_for_reconstructing_run(run)
            # Ensure AZUREML_AUTOML_RUN_HISTORY_DATA_PATH is not set when child runs are tracked in RH
            os.environ.pop(RunHistoryEnvironmentVariableNames.AZUREML_AUTOML_RUN_HISTORY_DATA_PATH, None)
        else:
            os.environ[RunHistoryEnvironmentVariableNames.AZUREML_RUN_ID] = run.id
            os.environ[RunHistoryEnvironmentVariableNames.AZUREML_AUTOML_RUN_HISTORY_DATA_PATH] = \
                OfflineAutoMLRunUtil.get_run_history_data_folder(
                path=self.azureautomlclient.automl_settings.path,
                parent_run_id=self.azureautomlclient.parent_run_id)

    def _synchronize_run(self, safe: bool = False) -> None:
        """If this run is synchronizable, synchronize it."""
        if isinstance(self.azureautomlclient.current_run, SynchronizableAutoMLRun):
            try:
                self.azureautomlclient.current_run.synchronize()
            except Exception as e:
                logger.warning("Failed to synchronize run.")
                logging_utilities.log_traceback(e, logger)
                if not safe:
                    raise

    def _upload_and_process_offline_run_history(
        self,
        parent_run_context: AzureAutoMLRunContext,
        fit_outputs: List[FitOutput]
    ) -> None:
        """Upload and process offline run history.
        This method:
        (1) creates one online run for the best offline run
        (2) uploads a summary of all run metrics as an artifact to the parent run
        (3) sets self._run_best to the best online run
        """
        # If tracking child runs, return.
        # (There is only offline run history to process if not tracking child runs.)
        if self.azureautomlclient.automl_settings.track_child_runs:
            return

        # If you could have started
        if self._started_processing_offline_run_history:
            return

        self._started_processing_offline_run_history = True

        if not self._run_best:
            logger.info(
                "Best child run cannot be found. Aborting upload of offline run history")
            return

        # Create a single child run of the parent run in RH, with the suffix '_best'.
        # Upload the metrics, tags, etc. of the best child run to this '_best' run.
        best_run = train_runtime_utilities._create_best_run(
            parent_run=self.azureautomlclient.current_run,
            best_offline_run=cast(OfflineAutoMLRun, self._run_best))

        # Set self._run_best to the online run just created
        self._run_best = best_run

        # Upload summary of child iterations to the parent run
        train_runtime_utilities._upload_summary_of_iterations(
            parent_run_context=parent_run_context,
            fit_outputs=fit_outputs)

    def _upload_and_process_offline_run_history_safe(
        self,
        parent_run_context: AzureAutoMLRunContext,
        fit_outputs: List[FitOutput]
    ) -> None:
        """Upload summarized offline run history while catching & logging any thrown exceptions."""
        try:
            self._upload_and_process_offline_run_history(parent_run_context, fit_outputs)
        except Exception as e:
            logging_utilities.log_traceback(e, logger)
