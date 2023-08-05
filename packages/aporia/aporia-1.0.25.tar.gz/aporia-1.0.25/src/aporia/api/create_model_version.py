import logging
from typing import Dict, List, Optional

from aporia.consts import LOGGER_NAME
from aporia.errors import AporiaError
from aporia.graphql_client import GraphQLClient


logger = logging.getLogger(LOGGER_NAME)

VALID_FIELD_TYPES = ["numeric", "categorical", "string", "boolean", "datetime"]


async def run_create_model_version_query(
    graphql_client: GraphQLClient,
    model_id: str,
    model_version: str,
    features: Dict[str, str],
    prediction: Dict[str, str],
    raw_inputs: Optional[Dict[str, str]] = None,
    outputs: Optional[Dict[str, str]] = None,
    metrics: Optional[Dict[str, str]] = None,
):
    """Defines the schema for a specific model version.

    Args:
        graphql_client (GraphQLClient): GraphQL client
        model_id (str): Model ID
        model_version (str): Model Version
        features (Dict[str, str]): Feature fields
        prediction (Dict[str, str]): Prediction fields
        raw_inputs (Dict[str, str], optional): Raw input fields. Defaults to None.
        outputs (Dict[str, str], optional): Output fields. Defaults to None.
        metrics (Dict[str, str], optional): Prediction metric fields. Defaults to None.
    """
    query = """
        mutation CreateModelVersion(
            $modelId: String!,
            $modelVersion: String!,
            $features: [Field]!,
            $prediction: [Field]!,
            $rawInputs: [Field],
            $outputs: [Field],
            $metrics: [Field]
        ) {
            createModelVersion(
                modelId: $modelId,
                modelVersion: $modelVersion,
                features: $features,
                prediction: $prediction
                rawInputs: $rawInputs,
                outputs: $outputs,
                metrics: $metrics
            ) {
                warnings
            }
        }
    """

    variables = {
        "modelId": model_id,
        "modelVersion": model_version,
        "features": prepare_fields(features),
        "prediction": prepare_fields(prediction),
        "rawInputs": None if raw_inputs is None else prepare_fields(raw_inputs),
        "outputs": None if outputs is None else prepare_fields(outputs),
        "metrics": None if metrics is None else prepare_fields(metrics),
    }

    result = await graphql_client.query_with_retries(query, variables)
    for warning in result["createModelVersion"]["warnings"]:
        logger.warning(warning)


def prepare_fields(fields: Dict[str, str]) -> List[Dict[str, str]]:
    """Creates a list of Field GraphQL objects from a fields dict.

    Args:
        fields (Dict[str, str]): Fields dict

    Returns:
        List[Dict[str, str]]: List of GraphQL Field objects.
    """
    return [{"name": field_name, "type": field_type} for field_name, field_type in fields.items()]


def validate_fields_input(
    features: Dict[str, str],
    prediction: Dict[str, str],
    raw_inputs: Optional[Dict[str, str]] = None,
    outputs: Optional[Dict[str, str]] = None,
    metrics: Optional[Dict[str, str]] = None,
):
    """Checks if the fields passed to create_model_version are valid.

    Args:
        prediction (Dict[str, str]): Prediction fields
        features (Dict[str, str]): Feature fields
        raw_inputs (Dict[str, str], optional): Raw input fields. Defaults to None.
        outputs (Dict[str, str], optional): Output fields. Defaults to None.
        metrics (Dict[str, str], optional): Prediction metric fields. Defaults to None.
    """
    fields_to_validate = {"features": features, "prediction": prediction}

    if raw_inputs is not None:
        fields_to_validate["raw_inputs"] = raw_inputs

    if outputs is not None:
        fields_to_validate["outputs"] = outputs

    if metrics is not None:
        fields_to_validate["metrics"] = metrics

    for category, fields in fields_to_validate.items():
        if not isinstance(fields, dict):
            raise AporiaError("{} parameter must be a dict".format(category))

        if len(fields) == 0:
            raise AporiaError("{} parameter must contain items".format(category))

        for key, value in fields.items():
            if not isinstance(key, str):
                raise AporiaError(
                    "Invalid field name {} in the {} parameter - field names must be strings".format(
                        key, category
                    )
                )

            if value not in VALID_FIELD_TYPES:
                raise AporiaError(
                    "Invalid field type {} in the {} parameter - valid field types are {}".format(
                        value, category, VALID_FIELD_TYPES
                    )
                )
