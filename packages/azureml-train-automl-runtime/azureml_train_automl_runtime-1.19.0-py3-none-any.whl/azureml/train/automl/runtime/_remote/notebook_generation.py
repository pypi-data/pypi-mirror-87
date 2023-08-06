# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Contains functionality to generate notebooks from existing runs.
"""
from typing import Any, Callable, Dict, List, Mapping
import inspect
import json
import logging
import os
import pkg_resources
import pprint
import time
import urllib.request

from azureml.automl.core._run import run_lifecycle_utilities
from azureml.core import Datastore, Run
from azureml.data.constants import WORKSPACE_FILE_DATASTORE
from azureml._vendor.azure_storage.file import FileService, ContentSettings
from azureml.automl.core.shared import logging_utilities
from azureml.automl.runtime.notebook_generation.notebook_template import NotebookTemplate
from azureml.train.automl import AutoMLConfig, constants
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.runtime import __version__
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from .remote_utilities import _parse_settings


PACKAGE_NAME = "azureml.train.automl.runtime"
logger = logging.getLogger(__name__)

# Workspace 2.0 uses this hardcoded fileshare name for the notebook UI
DEFAULT_CODE_FILESHARE_NAME = "code-391ff5ac-6576-460f-ba4d-7e03433c68b6"

NOTEBOOK_TEMPLATE_URL = "https://automlresources-test.azureedge.net/notebook-templates/{0}/{1}"


def get_template(notebook_name: str) -> NotebookTemplate:
    """
    Load a notebook template from this package using its filename w/o extension.

    :param notebook_name: name of a notebook template in the notebook_templates folder
    :return: a notebook template object
    """
    logger.info("Loading notebook {}".format(notebook_name))

    try:
        for _ in range(3):
            updated_template_url = NOTEBOOK_TEMPLATE_URL.format(__version__, notebook_name + ".ipynb")
            logger.info("Fetching updated template from {}".format(updated_template_url))
            response = urllib.request.urlopen(updated_template_url)
            response_code = response.getcode()
            if response_code == 200:
                return NotebookTemplate(response.read())
            elif response_code == 404:
                logger.info("No updated template available. Using template from package.")
                break
            elif response_code < 500 and response_code != 429:
                # <500 codes = non retriable
                logger.info("Got non-success response code {}, falling back.".format(response_code))
                break
            else:
                # 429/5xx server codes = retriable
                logger.info("Got non-success response code {}, retrying after 3s.".format(response_code))
                time.sleep(3)
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        logger.info("Error failed while fetching updated template, falling back to template in package.")

    template_path = pkg_resources.resource_filename(
        PACKAGE_NAME, os.path.join("_remote", "notebook_templates", notebook_name + ".ipynb")
    )
    with open(template_path, "r") as f:
        return NotebookTemplate(f.read())


def create_output_dir_in_share(fs: FileService, share_name: str, remote_path: List[str]) -> str:
    """
    Create the given directory structure in the share.

    :param fs: storage account object
    :param share_name: the name of the container in the storage account
    :param remote_path: the remote path, with each path component in a list
    :return: the full remote path in string format
    """
    path = ""
    for folder in remote_path:
        path = os.path.join(path, folder)
        fs.create_directory(share_name=share_name, directory_name=path)
    return path


def upload_file_to_path(run: Run, remote_directory: List[str], file_path: str) -> None:
    """
    Upload the file to the given path in the remote share.

    :param run: the run to add the notebook output path property to
    :param remote_directory: the remote directory to upload the file to
    :param file_path: the local path to the file to upload
    :return:
    """
    logger.info("Creating FileService instance")
    ds = Datastore.get(run.experiment.workspace, WORKSPACE_FILE_DATASTORE)
    fs = FileService(account_name=ds.account_name, account_key=ds.account_key, endpoint_suffix=ds.endpoint)

    # Search for the share used by the notebook UI and create it if it doesn't exist.
    share_name = None
    for share in fs.list_shares():
        if share.name == DEFAULT_CODE_FILESHARE_NAME:
            logger.info("Existing code file share found")
            share_name = share.name
            break

    if share_name is None:
        logger.info("Code file share not found, creating one")
        fs.create_share(DEFAULT_CODE_FILESHARE_NAME)
        share_name = DEFAULT_CODE_FILESHARE_NAME

    logger.info("Creating output directory {}".format(os.path.join(*remote_directory)))
    share_output_directory = create_output_dir_in_share(fs, share_name, remote_directory)

    logger.info("Uploading notebook {} to share".format(file_path))
    fs.create_file_from_path(
        share_name=share_name,
        directory_name=share_output_directory,
        file_name=os.path.basename(file_path),
        local_file_path=file_path,
        content_settings=ContentSettings("application/octet-stream"),
    )

    run.add_properties({"notebook_output_path": os.path.join(share_output_directory, os.path.basename(file_path))})


def remove_matching_default_args(func: Callable[..., Any], args: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Given a function and function arguments, remove any arguments that match defaults in the function signature.

    :param func: the function to inspect
    :param args: a dictionary containing all arguments to be passed into the function
    :return: a dictionary containing arguments to be passed into the function, except those which match the defaults
    """
    signature = inspect.signature(func)

    # Ger all the default arguments from the function
    default_args = {k: v.default for k, v in signature.parameters.items() if v.default is not inspect.Parameter.empty}

    # Only pick arguments if they either do not match a default argument or are not in the default argument list
    new_args = {k: v for k, v in args.items() if k not in default_args or v != default_args[k]}
    return new_args


def parent_run_notebook_generation_wrapper(automl_settings: str, parent_run_id: str, **kwargs: Any) -> None:
    """
    Generate an AutoMLConfig-based notebook.

    :param automl_settings: stringified AutoML settings
    :param parent_run_id: run ID of the parent run to create the notebook against
    :param kwargs:
    :return:
    """
    current_run = Run.get_context()
    settings = _parse_settings(current_run, automl_settings, parent_run_id)
    logger.info("Generating notebook in run {} for parent run id {}".format(current_run.id, parent_run_id))
    try:
        template_name = "automlconfig_notebook"
        template = get_template(template_name)
        logger.info("Notebook arguments: {}".format(template.get_arguments()))

        # Retrieve optional parameters for notebook generation
        output_filename = kwargs.pop("notebook_output_name", None)
        if output_filename is None:
            slice_len = len(current_run.id) if len(current_run.id) < 8 else 8
            output_filename = "{}.ipynb".format(current_run.id[:slice_len])

        dataprep_json = kwargs.pop("dataprep_json", "{}")
        dataset_id = json.loads(dataprep_json).get("datasetId")
        label_column_name = settings.label_column_name

        # Filter out any settings that aren't changed from the default values to prevent bloated output
        modified_settings = remove_matching_default_args(AutoMLConfig, settings.as_serializable_dict())
        modified_settings = remove_matching_default_args(AzureAutoMLSettings, modified_settings)
        modified_settings = remove_matching_default_args(AutoMLBaseSettings, modified_settings)

        # Remove internal arguments if they are default values to prevent warnings
        if modified_settings.get("scenario", None) == constants.Scenarios.SDK_COMPATIBLE:
            modified_settings.pop("scenario")
        if modified_settings.get("cost_mode", None) == constants.PipelineCost.COST_FILTER:
            modified_settings.pop("cost_mode")

        # Always add in the following arguments
        modified_settings["task"] = settings.task_type

        # Pretty print the settings
        stringified_modified_settings = pprint.pformat(modified_settings)

        # Generate notebook
        notebook_args = kwargs.copy()
        notebook_args.update(
            {
                "experiment_name": current_run.experiment.name,
                "compute_target": settings.compute_target,
                "modified_automl_settings": stringified_modified_settings,
                "task_type": settings.task_type,
                "dataset_id": dataset_id,
                "label_column_name": label_column_name,
            }
        )
        notebook = template.generate_notebook(notebook_args)

        with open(output_filename, "w") as f:
            f.write(notebook)

        upload_file_to_path(current_run, ["Users", "GeneratedNotebooks", parent_run_id], output_filename)
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        logger.error(
            "AutoMLConfig notebook generation script terminated with an exception of type: {}".format(type(e))
        )
        run_lifecycle_utilities.fail_run(current_run, e)
        raise
