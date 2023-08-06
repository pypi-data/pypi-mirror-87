# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utilities for AutoML remote runs."""
import logging
import os
import re
import sys
from typing import Optional

from azureml._history.utils.constants import LOGS_AZUREML_DIR
from azureml.automl.core.shared import log_server
from azureml.core import Datastore, Experiment, Run
from azureml.train.automl import _logging   # type: ignore
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.exceptions import ClientException, DataException
from azureml.train.automl.run import AutoMLRun


logger = logging.getLogger(__name__)


def _init_logger() -> None:
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(fmt="%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s",
                                  datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    log_server.add_handler('stdout', handler)


def _parse_settings(
        current_run: Run,
        automl_settings: str,
        parent_run_id: Optional[str] = None
) -> AzureAutoMLSettings:
    if not os.path.exists(LOGS_AZUREML_DIR):
        os.makedirs(LOGS_AZUREML_DIR, exist_ok=True)
    _init_logger()

    # Don't reuse path from user's local machine for remote runs
    logger.info('Changing AutoML temporary path to current working directory.')
    automl_settings_obj = AzureAutoMLSettings.from_string_or_dict(automl_settings, overrides={
        'debug_log': os.path.join(LOGS_AZUREML_DIR, "azureml_automl.log"),
        'path': os.getcwd()
    })

    # enable traceback logging for remote runs
    os.environ['AUTOML_MANAGED_ENVIRONMENT'] = '1'

    if parent_run_id is None:
        parent_run_id = _get_parent_run_id(current_run.id)

    _logging.set_run_custom_dimensions(
        automl_settings=automl_settings_obj,
        parent_run_id=parent_run_id,
        child_run_id=current_run.id)

    return automl_settings_obj


def _init_directory(directory: Optional[str]) -> str:
    if directory is None:
        directory = os.getcwd()
        logger.info('Directory was None, using current working directory.')

    sys.path.append(directory)
    # create the outputs folder
    logger.info('Creating output folder.')
    os.makedirs('./outputs', exist_ok=True)
    return directory


def _get_parent_run_id(run_id: str) -> str:
    """
    Code for getting the AutoML parent run-id from the child run-id.
    :param run_id: This is in format AutoML_<GUID>_*
    :type run_id: str
    :return: str
    """
    try:
        return re.match("((?:AutoML_)?[a-zA-Z0-9-]+)_.+", run_id).group(1)  # type: ignore
    except (IndexError, AttributeError) as e:
        raise ClientException.from_exception(e, "Malformed AutoML child run-id passed", has_pii=False)
