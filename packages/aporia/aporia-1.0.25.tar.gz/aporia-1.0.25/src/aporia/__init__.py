import atexit
from contextlib import suppress
import logging
import sys
from typing import Dict, Optional

from aporia.api.create_model_version import run_create_model_version_query, validate_fields_input
from aporia.config import Config
from aporia.consts import LOG_FORMAT, LOGGER_NAME
from aporia.errors import AporiaError, handle_error
from aporia.event_loop import EventLoop
from aporia.graphql_client import GraphQLClient
from aporia.model import Model

try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"


__all__ = ["init", "shutdown", "Model"]


class Context:
    """Global context."""

    def __init__(
        self,
        graphql_client: GraphQLClient,
        event_loop: EventLoop,
        config: Config,
    ):
        """Initializes the context.

        Args:
            graphql_client (GraphQLClient): GraphQL client.
            event_loop (EventLoop): Event loop.
            config (Config): Aporia config.
        """
        self.graphql_client = graphql_client
        self.event_loop = event_loop
        self.config = config


context = None
logger = logging.getLogger(LOGGER_NAME)


def init(
    token: Optional[str] = None,
    host: Optional[str] = None,
    environment: Optional[str] = None,
    port: Optional[int] = None,
    debug: Optional[bool] = None,
    throw_errors: Optional[bool] = None,
    blocking_call_timeout: Optional[int] = None,
):
    """Initializes the Aporia SDK.

    Args:
        token (str): Authentication token.
        host (str): Controller host.
        environment (str): Environment in which aporia is initialized (e.g production, staging).
        port (int, optional): Controller port. Defaults to 443.
        debug (bool, optional): True to enable debug mode - this will cause additional logs
            and stack traces during exceptions. Defaults to False.
        throw_errors (bool, optional): True to cause errors to be raised
            as exceptions. Defaults to False.
        blocking_call_timeout (int, optional): Timeout, in seconds, for blocking aporia API
            calls - Model(), set_features(), add_extra_inputs(), add_extra_outputs().

    Notes:
        * The token, host and environment parameters are required.
        * All of the parameters here can also be defined as environment variables:
            * token -> APORIA_TOKEN
            * host -> APORIA_HOST
            * environment -> APORIA_ENVIRONMENT
            * port -> APORIA_PORT
            * debug -> APORIA_DEBUG
            * throw_errors -> APORIA_THROW_ERRORS
            * blocking_call_timeout -> APORIA_BLOCKING_CALL_TIMEOUT
        * Values passed as parameters to aporia.init() override the values from
          the corresponding environment variables.
    """
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, style="{"))
        logger.addHandler(handler)

    logger.debug("Initializing Aporia SDK.")

    try:
        config = Config(
            token=token,
            host=host,
            environment=environment,
            port=port,
            debug=debug,
            throw_errors=throw_errors,
            blocking_call_timeout=blocking_call_timeout,
        )

        # Init graphql client and event loop
        event_loop = EventLoop()
        graphql_client = GraphQLClient(token=config.token, host=config.host, port=config.port)
        event_loop.run_coroutine(graphql_client.open())

        global context
        context = Context(
            graphql_client=graphql_client,
            event_loop=event_loop,
            config=config,
        )

        atexit.register(shutdown)
        logger.debug("Aporia SDK initialized.")
    except Exception as err:
        handle_error(
            message="Initializing Aporia SDK failed, error: {}".format(str(err)),
            add_trace=False if debug is None else debug,
            raise_exception=False if throw_errors is None else throw_errors,
            original_exception=err,
        )


def shutdown():
    """Shuts down the Aporia SDK.

    Notes:
        * It is advised to call flush() before calling shutdown(), to ensure that
          all of the data that was sent reaches the controller.
    """
    with suppress(Exception):
        global context
        if context is not None:
            context.event_loop.run_coroutine(context.graphql_client.close())
            context = None


def create_model_version(
    model_id: str,
    model_version: str,
    features: Dict[str, str],
    prediction: Dict[str, str],
    raw_inputs: Optional[Dict[str, str]] = None,
    outputs: Optional[Dict[str, str]] = None,
    metrics: Optional[Dict[str, str]] = None,
):
    """Create a new model version, and defines a schema for it.

    Args:
        model_id (str): Model identifier, as received from the Aporia dashboard.
        model_version (str): Model version - this can be any string that represents the model
            version, such as "v1" or a git commit hash.
        features (Dict[str, str]): Schema for model features (See notes)
        prediction (Dict[str, str]): Schema for prediction results (See notes)
        raw_inputs (Dict[str, str], optional): Schema for raw inputs (See notes). Defaults to None.
        outputs (Dict[str, str], optional): Schema for final outputs (See notes). Defaults to None.
        metrics (Dict[str, str], optional): Schema for prediction metrics (See notes). Defaults to None.

    Notes:
        * A schema is a dict, in which the keys are the fields you wish to report, and the
          values are the types of those fields. For example:
            {
                "feature1": "numeric",
                "feature2": "datetime"
            }
        * The valid field types (and corresponding python types) are:
            | Field Type    | Python Types
            | ------------- | ------------
            | "numeric"     | float, int
            | "categorical" | int
            | "boolean"     | bool
            | "string"      | str
            | "datetime"    | datetime.datetime, or str representing a datetime in ISO-8601 format
    """
    if context is None:
        raise AporiaError("Aporia SDK was not initialized")

    try:
        if len(model_id) == 0 or len(model_version) == 0:
            raise AporiaError("model_id and model_version must be non-empty strings.")

        validate_fields_input(
            features=features,
            prediction=prediction,
            raw_inputs=raw_inputs,
            outputs=outputs,
            metrics=metrics,
        )

        context.event_loop.run_coroutine(
            run_create_model_version_query(
                graphql_client=context.graphql_client,
                model_id=model_id,
                model_version=model_version,
                features=features,
                prediction=prediction,
                raw_inputs=raw_inputs,
                outputs=outputs,
                metrics=metrics,
            )
        )
    except Exception as err:
        handle_error(
            message="Creating model version failed, error: {}".format(str(err)),
            add_trace=context.config.debug,
            raise_exception=context.config.throw_errors,
            original_exception=err,
        )
