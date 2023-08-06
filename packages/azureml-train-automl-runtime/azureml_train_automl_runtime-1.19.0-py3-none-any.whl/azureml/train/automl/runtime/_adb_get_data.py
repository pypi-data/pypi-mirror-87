# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging

from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.train.automl.runtime._remote_script import _prepare_data

from ._data_preparer import DataPreparerFactory

logger = logging.getLogger(__name__)


class _input_data_model(object):
    def __init__(self, data_dictionary):
        if data_dictionary is None:
            data_dictionary = {}
        self.X = data_dictionary.get('X', None)
        self.y = data_dictionary.get('y', None)
        self.X_valid = data_dictionary.get('X_valid', None)
        self.y_valid = data_dictionary.get('y_valid', None)
        self.sample_weight = data_dictionary.get('sample_weight', None)
        self.sample_weight_valid = data_dictionary.get('sample_weight_valid', None)
        self.cv_splits_indices = data_dictionary.get('cv_splits_indices', None)
        self.x_raw_column_names = data_dictionary.get('x_raw_column_names', None)
        self.training_data = data_dictionary.get('training_data', None)
        self.validation_data = data_dictionary.get('validation_data', None)


def _none_log_message(message, logging_level=logging.DEBUG):
    pass


def get_input_datamodel_from_dataprep_json(dataprep_json,
                                           automl_settings,
                                           log_message=_none_log_message,
                                           verifier=None):
    """
    Convert dataprep data from json to datamodel.

    :param dataprep_json: The dataprep object in json format.
    :param automl_settings: The automl settings.
    :param log_message: The log message.
    :param verifier: The verified object to perform verifications.
    :return: The dataprep object in datamodel format.
    """
    try:
        log_message("getting input data from dataprep json...")

        Contract.assert_value(dataprep_json, "dataprep_json")
        Contract.assert_value(automl_settings, "automl_settings")

        data_preparer = DataPreparerFactory.get_preparer(dataprep_json)
        new_dictionary = _prepare_data(
            data_preparer=data_preparer, automl_settings_obj=automl_settings,
            script_directory=None, entry_point=None)
        new_dictionary['is_adb_run'] = True
        new_dictionary['automl_settings'] = automl_settings
        if verifier:
            new_dictionary['verifier'] = verifier
        return _input_data_model(new_dictionary)
    except Exception:
        log_message(message="Error from getting input data from dataprep json",
                    logging_level=logging.ERROR)
        raise
