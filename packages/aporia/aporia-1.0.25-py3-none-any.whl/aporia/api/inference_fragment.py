from datetime import datetime
from enum import Enum
import logging
from typing import Set

from aporia.consts import LOGGER_NAME
from aporia.errors import AporiaError


logger = logging.getLogger(LOGGER_NAME)


class FragmentType(Enum):
    """Fragment types."""

    PREDICTION = "prediction"
    RAW_INPUTS = "raw_inputs"
    OUTPUTS = "outputs"
    ACTUALS = "actuals"


class Fragment:
    """Inference fragment."""

    def __init__(self, type: FragmentType, data: dict):
        """Initializes a Fragment object.

        Args:
            type (FragmentType): Fragment type (this is mostly used for logging purposes)
            data (dict): Fragment data
        """
        self.type = type
        self.data = data

    def serialize(self) -> dict:
        """Serializes the fragment.

        Returns:
            dict: Serialized fragment
        """
        # Save the missing fields in a variable to avoid calculating set difference twice
        missing_fields = self.missing_fields
        if len(missing_fields) > 0:
            raise AporiaError("Missing required fields {}".format(missing_fields))

        return {"id": self.data["id"]}

    @property
    def required_fields(self) -> Set[str]:
        """Required fields property.

        Returns:
            Set[str]: Set of required field names.
        """
        return {"id"}

    @property
    def missing_fields(self) -> Set[str]:
        """Missing fields property.

        Returns:
            Set[str]: Set of missing field names
        """
        return self.required_fields - self.data.keys()

    def is_valid(self) -> bool:
        """Checks if the fragment is valid.

        Returns:
            bool: True if the fragment is valid, false otherwise
        """
        if len(self.missing_fields) > 0:
            logger.debug("Invalid input - Missing required fields {}".format(self.missing_fields))
            return False

        if not isinstance(self.data["id"], str):
            logger.debug("Invalid input - Id field must be a string.")
            return False

        return True


class PredictionFragment(Fragment):
    """Prediction fragment."""

    def __init__(self, data: dict, timestamp: datetime):
        """Initializes a PredictionFragment.

        Args:
            data (dict): Prediction data
            timestamp (datetime): Current timestamp
        """
        super().__init__(type=FragmentType.PREDICTION, data=data)
        self.timestamp = timestamp

    def serialize(self) -> dict:
        """See base class."""
        serialized_fragment = super().serialize()
        serialized_fragment["features"] = self.data["features"]
        serialized_fragment["prediction"] = self.data["prediction"]
        serialized_fragment["metrics"] = self.data.get("metrics")

        occurred_at = self.data.get("occurred_at")
        if occurred_at is None:
            occurred_at = self.timestamp

        serialized_fragment["occurredAt"] = occurred_at

        return serialized_fragment

    @property
    def required_fields(self) -> Set[str]:
        """See base class."""
        return super().required_fields | {"features", "prediction"}

    def is_valid(self) -> bool:
        """See base class."""
        if not super().is_valid():
            return False

        features = self.data["features"]
        prediction = self.data["prediction"]
        metrics = self.data.get("metrics")
        occurred_at = self.data.get("occurred_at")

        if not (isinstance(features, dict) and len(features) > 0):
            logger.debug("Invalid input - features must be a non-empty dict")
            return False

        if not (isinstance(prediction, dict) and len(prediction) > 0):
            logger.debug("Invalid input - prediction must be a non-empty dict")
            return False

        if (metrics is not None) and not (isinstance(metrics, dict) and len(metrics) > 0):
            logger.debug("Invalid input - metrics must be a non-empty dict")
            return False

        if occurred_at is not None and not isinstance(occurred_at, (datetime, str)):
            logger.debug(
                "Invalid input - occurred_at must be a datetime object, or an ISO-8601 date string"
            )
            return False

        return True


class RawInputsFragment(Fragment):
    """Raw inputs fragment."""

    def __init__(self, data: dict):
        """Initializes a RawInputsFragment.

        Args:
            data (dict): Raw inputs data
        """
        super().__init__(type=FragmentType.RAW_INPUTS, data=data)

    def serialize(self) -> dict:
        """See base class."""
        serialized_fragment = super().serialize()
        serialized_fragment["rawInputs"] = self.data["raw_inputs"]

        return serialized_fragment

    @property
    def required_fields(self) -> Set[str]:
        """See base class."""
        return super().required_fields | {"raw_inputs"}

    def is_valid(self) -> bool:
        """See base class."""
        if not super().is_valid():
            return False

        if not (isinstance(self.data["raw_inputs"], dict) and len(self.data["raw_inputs"]) > 0):
            logger.debug("Invalid input - raw_inputs must be a non-empty dict")
            return False

        return True


class OutputsFragment(Fragment):
    """Final outputs fragment."""

    def __init__(self, data: dict):
        """Initializes a Outputs Fragment.

        Args:
            data (dict): Outputs data
        """
        super().__init__(type=FragmentType.OUTPUTS, data=data)

    def serialize(self) -> dict:
        """See base class."""
        serialized_fragment = super().serialize()
        serialized_fragment["outputs"] = self.data["outputs"]

        return serialized_fragment

    @property
    def required_fields(self) -> Set[str]:
        """See base class."""
        return super().required_fields | {"outputs"}

    def is_valid(self) -> bool:
        """See base class."""
        if not super().is_valid():
            return False

        if not (isinstance(self.data["outputs"], dict) and len(self.data["outputs"]) > 0):
            logger.debug("Invalid input - outputs must be a non-empty dict")
            return False

        return True


class ActualsFragment(Fragment):
    """Prediction actuals fragment."""

    def __init__(self, data: dict):
        """Initializes a Actuals.

        Args:
            data (dict): Actuals data
        """
        super().__init__(type=FragmentType.ACTUALS, data=data)

    def serialize(self) -> dict:
        """See base class."""
        serialized_fragment = super().serialize()
        serialized_fragment["actuals"] = self.data["actuals"]

        return serialized_fragment

    @property
    def required_fields(self) -> Set[str]:
        """See base class."""
        return super().required_fields | {"actuals"}

    def is_valid(self) -> bool:
        """See base class."""
        if not super().is_valid():
            return False

        if not (isinstance(self.data["actuals"], dict) and len(self.data["actuals"]) > 0):
            logger.debug("Invalid input - actuals must be a non-empty dict")
            return False

        return True
