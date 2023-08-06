# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
from typing import Any, Union, Tuple, Optional

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import AutoMLInternal
from azureml.automl.core.shared.exceptions import ValidationException

logger = logging.getLogger(__name__)


class Contract:
    """Class with helper methods to enforce and validate system invariants.
    Use this class' methods to enforce system asserts (i.e. contracts defined within AutoML are adhered to). The
    methods defined in this class will raise a ValidationException, containing an 'AutoMLInternal' system error, should
    the asserts fail.
    """

    @staticmethod
    def assert_true(condition: bool, message: str,
                    target: Optional[str] = None, reference_code: Optional[str] = None,
                    log_safe: bool = False) -> None:
        """
        Asserts that the provided condition evaluates to True.

        :param condition: The condition to evaluate, should result in a boolean.
        :param message: The assertion message that explains the condition when the assertion evaluates to False.
        :param target: The name of the element (e.g. argument) that caused the error.
        :param reference_code: A string that a developer or the user can use to get further context on the error.
        :param log_safe: If the assertion message is safe to log. Defaults to False.
        :return: None
        :raises ValidationException (with an 'AutoMLInternal' system error)
        """
        if not condition:
            if log_safe:
                logger.error(message)

            raise ValidationException._with_error(AzureMLError.create(
                AutoMLInternal, target=target, reference_code=reference_code, error_details=message)
            )

    @staticmethod
    def assert_value(value: Any, name: str, reference_code: Optional[str] = None, log_safe: bool = True) -> None:
        """
        Asserts that the value is non-null, fails otherwise. For also checking for empty strings or lists, please
        instead see :func:`assert_non_empty`.

        Note: log_safe is true by default, since the error message only gets printed for a null value (no PII)

        :param value: The object that should be evaluated for the null check.
        :param name: The name of the object.
        :param reference_code: A string that a developer or the user can use to get further context on the error.
        :param log_safe: If the assertion message is safe to log. Defaults to True.
        :return: None
        :raises ValidationException (with an 'AutoMLInternal' system error)
        """
        error_details = "Expected argument {} to have a valid value.".format(name)

        Contract.assert_true(value is not None, message=error_details,
                             target=name, reference_code=reference_code, log_safe=log_safe)

    @staticmethod
    def assert_non_empty(value: Any, name: str, reference_code: Optional[str] = None, log_safe: bool = False) -> None:
        """
        Asserts that the value is non-null and non-empty (as defined by the len attribute), fails otherwise.

        :param value: The object that should be evaluated for the non-empty check.
        :param name: The name of the object.
        :param reference_code: A string that a developer or the user can use to get further context on the error.
        :param log_safe: If the assertion message is safe to log. Defaults to False.
        :return: None
        :raises ValidationException (with an 'AutoMLInternal' system error)
        """
        error_details = "Expected argument {} to have a valid and non-empty value.".format(name)

        is_non_null = value is not None
        is_non_empty = len(value) > 0 if hasattr(value, '__len__') else True

        Contract.assert_true(is_non_null and is_non_empty, message=error_details,
                             target=name, reference_code=reference_code, log_safe=log_safe)

    @staticmethod
    def assert_type(value: Any, name: str,
                    expected_types: Union[type, Tuple[type, ...]],
                    reference_code: Optional[str] = None, log_safe: bool = True) -> None:
        """
        Asserts that the value type conforms to the ones provided in expected_types.

        :param value: The object that should be evaluated for type checking
        :param name: The name of the object
        :param expected_types: A type (or a tuple of types) to which the argument should adhere to.
        :param reference_code: A string that a developer or the user can use to get further context on the error.
        :param log_safe: If the assertion message is safe to log. Defaults to True.
        :return: None
        :raises ValidationException (with an 'AutoMLInternal' system error)
        """
        error_details = "Expected '{}' of type {}, but is of type {}.".format(name, expected_types, type(value))

        Contract.assert_true(isinstance(value, expected_types), message=error_details,
                             target=name, reference_code=reference_code, log_safe=log_safe)
