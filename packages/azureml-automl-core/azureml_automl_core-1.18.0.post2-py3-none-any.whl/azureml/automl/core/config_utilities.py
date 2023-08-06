# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for interacting with AutoMLConfig."""
from typing import Any, Optional

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import ConflictingValueForArguments
from azureml.automl.core.shared._diagnostics.validation import Validation
from azureml.automl.core.shared.exceptions import ConfigException


def _check_validation_config(
        X_valid: Any,
        y_valid: Any,
        sample_weight: Any,
        sample_weight_valid: Any,
        cv_splits_indices: Any,
        n_cross_validations: Optional[int] = None,
        validation_size: Optional[float] = None
) -> None:
    """
    Validate that validation parameters have been correctly provided.

    :param X_valid:
    :param y_valid:
    :param sample_weight:
    :param sample_weight_valid:
    :param cv_splits_indices:
    :param n_cross_validations:
    :param validation_size:
    """

    if X_valid is not None:
        Validation.validate_value(y_valid, "y_valid")
        if sample_weight is not None:
            Validation.validate_value(sample_weight_valid, "sample_weight_valid")

    if y_valid is not None:
        Validation.validate_value(X_valid, "X_valid")

    if sample_weight_valid is not None and X_valid is None:
        raise ConfigException._with_error(
            AzureMLError.create(
                ConflictingValueForArguments, target="sample_weight_valid",
                arguments=', '.join(['sample_weight_valid', 'X_valid'])
            )
        )

    if X_valid is not None:
        if n_cross_validations is not None and n_cross_validations > 0:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ConflictingValueForArguments, target="n_cross_validations",
                    arguments=', '.join(['validation_data/X_valid', 'n_cross_validations'])
                )
            )
        if validation_size is not None and validation_size > 0.0:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ConflictingValueForArguments, target="validation_size",
                    arguments=', '.join(['validation_data/X_valid', 'validation_size'])
                )
            )

    if cv_splits_indices is not None:
        if n_cross_validations is not None and n_cross_validations > 0:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ConflictingValueForArguments, target="cv_splits_indices",
                    arguments=', '.join(['cv_splits_indices', 'n_cross_validations'])
                )
            )
        if validation_size is not None and validation_size > 0.0:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ConflictingValueForArguments, target="cv_splits_indices",
                    arguments=', '.join(['cv_splits_indices', 'validation_size'])
                )
            )
        if X_valid is not None:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ConflictingValueForArguments, target="cv_splits_indices",
                    arguments=', '.join(['cv_splits_indices', 'validation_data/X_valid'])
                )
            )
