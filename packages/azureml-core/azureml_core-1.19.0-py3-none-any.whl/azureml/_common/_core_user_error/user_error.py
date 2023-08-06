# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml._common._error_definition import error_decorator
from azureml._common._error_definition.error_strings import AzureMLErrorStrings

from azureml._common._error_definition.user_error import (
    ArgumentOutOfRange,
    InvalidData,
)


@error_decorator(use_parent_error_code=True)
class ArgumentSizeOutOfRange(ArgumentOutOfRange):
    @property
    def message_format(self):
        return AzureMLErrorStrings.UserErrorStrings.ARGUMENT_SIZE_OUT_OF_RANGE


@error_decorator(use_parent_error_code=True)
class InvalidColumnLength(InvalidData):
    @property
    def message_format(self):
        return AzureMLErrorStrings.UserErrorStrings.INVALID_COLUMN_LENGTH


@error_decorator(use_parent_error_code=True)
class InvalidColumnData(InvalidData):
    @property
    def message_format(self):
        return AzureMLErrorStrings.UserErrorStrings.INVALID_COLUMN_DATA
