# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Custom exceptions for AzureML Fairness package."""

# For detailed info on error handling design, see spec:
# https://msdata.visualstudio.com/Vienna/_git/specs?path=%2FErrorHandling%2Ferror-handling-in-azureml-sdk.md
# For error codes see:
# <root>\src\azureml-core\azureml\_common\_error_response\_generate_constants\error_codes.json
try:
    from azureml._common._error_response._error_response_constants import ErrorCodes
except ImportError:

    class ErrorCodes:
        """Constants for error codes."""

        VALIDATION_ERROR = "ValidationError"

try:
    from azureml.exceptions import UserErrorException
except ImportError:

    class UserErrorException(Exception):
        """The base class for exceptions."""

        def __init__(self, **kwargs):
            """Initialize the UserErrorException."""
            super(UserErrorException, self).__init__(**kwargs)


class DashboardValidationException(UserErrorException):
    """An exception raised when a problem is found with a supplied Dashboard dictionary."""

    _error_code = ErrorCodes.VALIDATION_ERROR
