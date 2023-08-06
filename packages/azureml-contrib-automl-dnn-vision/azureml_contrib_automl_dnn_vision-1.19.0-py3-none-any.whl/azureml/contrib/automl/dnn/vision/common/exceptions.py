# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Exceptions for the package."""

from azureml._common._error_response._error_response_constants import ErrorCodes
from azureml.exceptions import UserErrorException
from azureml.automl.core.shared import exceptions


class AutoMLVisionValidationException(exceptions.DataException, UserErrorException):
    """Exception for any errors caught when validating inputs."""

    _error_code = ErrorCodes.VALIDATION_ERROR


class AutoMLVisionDataException(AutoMLVisionValidationException):
    """Exception related to data validations."""

    _error_code = ErrorCodes.INVALIDDATA_ERROR


class AutoMLVisionSystemException(exceptions.AutoMLException):
    """Exception for internal errors that happen within the SDK."""

    _error_code = ErrorCodes.SYSTEM_ERROR


class AutoMLVisionExperimentException(AutoMLVisionSystemException):
    """Exception that happens during AutoML runtime."""


class AutoMLVisionTrainingException(AutoMLVisionExperimentException):
    """Exception for issues that arise during model training."""
