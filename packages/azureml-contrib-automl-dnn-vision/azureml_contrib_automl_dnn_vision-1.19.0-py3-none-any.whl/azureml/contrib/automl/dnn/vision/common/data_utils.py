# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Helper Utils for reading input data."""

import os

from .constants import SettingsLiterals


def get_label_file_paths_from_settings(settings):
    """ Parse the settings and get file paths for training labels file and validation labels file.

    :param settings: Dictionary with all training and model settings
    :type settings: Dict
    :return: Tuple of training file path, validation file path
    :rtype: Tuple[str, str]
    """
    labels_file = settings.get(SettingsLiterals.LABELS_FILE, None)
    validation_labels_file = settings.get(SettingsLiterals.VALIDATION_LABELS_FILE, None)
    labels_path = None
    validation_labels_path = None

    if labels_file is not None:
        labels_path = os.path.join(settings[SettingsLiterals.LABELS_FILE_ROOT], labels_file)
    if validation_labels_file is not None:
        validation_labels_path = os.path.join(settings[SettingsLiterals.LABELS_FILE_ROOT], validation_labels_file)

    return labels_path, validation_labels_path
