from concurrent.futures import ALL_COMPLETED, wait
from contextlib import contextmanager
from datetime import datetime, timezone
from functools import partial
import logging
from typing import Any, Callable, cast, Dict, Iterable, List, Optional, Union

import aporia
from aporia.api.inference_fragment import (
    ActualsFragment,
    Fragment,
    OutputsFragment,
    PredictionFragment,
    RawInputsFragment,
)
from aporia.api.log_inference import log_inference_fragments
from aporia.api.log_json import log_json
from aporia.config import Config
from aporia.consts import LOGGER_NAME
from aporia.errors import AporiaError, handle_error
from aporia.event_loop import EventLoop
from aporia.graphql_client import GraphQLClient
from aporia.inference_queue import InferenceQueue


logger = logging.getLogger(LOGGER_NAME)


SupportedValueType = Union[float, int, bool, str]


class BaseModel:
    """Base class for Model objects."""

    def __init__(
        self,
        model_id: str,
        model_version: str,
        graphql_client: Optional[GraphQLClient],
        event_loop: Optional[EventLoop],
        config: Optional[Config],
    ):
        """Initializes a BaseModel object.

        Args:
            model_id (str): Model identifier
            model_version (str): Model version
            graphql_client (Optional[GraphQLClient]): GraphQL client
            event_loop (Optional[EventLoop]): AsyncIO event loop
            config (Optional[Config]): Aporia config
        """
        logger.debug(
            "Initializing model object for model {} version {}".format(model_id, model_version)
        )
        self._model_ready = False

        self.model_id = model_id
        self.model_version = model_version
        self._graphql_client = cast(GraphQLClient, graphql_client)
        self._event_loop = cast(EventLoop, event_loop)
        self._config = cast(Config, config)
        # We keep a list of all tasks that were not awaited, to allow flushing
        # We have to do this manually to support python versions below
        # 3.7 (otherwise we could use asyncio.all_tasks())
        self._futures = []  # type: ignore

        try:
            if len(model_id) == 0 or len(model_version) == 0:
                raise AporiaError(
                    "Model object initialization failed, model_id and "
                    "model_version must be a non-empty strings"
                )

            if event_loop is not None and graphql_client is not None and config is not None:
                self._queue = InferenceQueue(
                    event_loop=self._event_loop,
                    batch_size=self._config.queue_batch_size,
                    max_size=self._config.queue_max_size,
                    flush_interval=self._config.queue_flush_interval,
                    flush_callback=self._flush_inference_callback,
                )

                self._model_ready = True

            if not self._model_ready:
                raise AporiaError(
                    "Model object initialization failed, model operations will not work."
                )

        except Exception as err:
            handle_error(
                message=str(err),
                add_trace=False if config is None else config.debug,
                raise_exception=False if config is None else config.throw_errors,
                original_exception=err,
                log_level=logging.ERROR,
            )

    @contextmanager
    def _handle_error(self, message_format: str, throw_errors: bool = False):
        try:
            yield
        except Exception as err:
            handle_error(
                message=message_format.format(str(err)),
                add_trace=self._config.debug,
                raise_exception=throw_errors,
                original_exception=err,
                log_level=logging.ERROR,
            )

    def log_prediction(
        self,
        id: str,
        features: Dict[str, SupportedValueType],
        prediction: Dict[str, SupportedValueType],
        metrics: Optional[Dict[str, SupportedValueType]] = None,
        occurred_at: Optional[datetime] = None,
    ):
        """Logs a single prediction.

        Args:
            id (str): Prediction identifier.
            features (Dict[str, SupportedValueType]): Values for all the features in the prediction
            prediction (Dict[str, SupportedValueType]): Prediction result
            metrics (Dict[str, SupportedValueType], Optional): Prediction metrics. Defaults to None.
            occurred_at (datetime, optional): Prediction timestamp. Defaults to None.

        Note:
            * If occurred_at is None, it will be reported as datetime.now()
        """
        self.log_batch_prediction(
            batch_predictions=[
                dict(
                    id=id,
                    features=features,
                    prediction=prediction,
                    metrics=metrics,
                    occurred_at=occurred_at,
                )
            ]
        )

    def log_batch_prediction(self, batch_predictions: Iterable[dict]):
        """Logs multiple predictions.

        Args:
            batch_predictions (Iterable[dict]): An iterable that produces prediction dicts.
                Each prediction dict MUST contain the following keys:
                    * id (str): Prediction identifier.
                    * features (Dict[str, SupportedValueType]): Values for all the features
                        in the prediction
                    * prediction (Dict[str, SupportedValueType]): Prediction result
                Each prediction dict MAY also contain the following keys:
                    * occurred_at (datetime): Prediction timestamp.
                    * metrics (Dict[str, SupportedValueType]): Prediction metrics

        Notes:
            * If occurred_at is None in any of the predictions, it will be reported as datetime.now()
        """
        self._log_batch_inference(
            batch=batch_predictions,
            fragment_class=partial(PredictionFragment, timestamp=datetime.now(tz=timezone.utc)),
            error_message="Logging prediction batch failed, error: {}",
        )

    def log_raw_inputs(self, id: str, raw_inputs: Dict[str, SupportedValueType]):
        """Logs raw inputs of a single prediction.

        Args:
            id (str): Prediction identifier.
            raw_inputs (Dict[str, SupportedValueType]): Raw inputs of the prediction.
        """
        self.log_batch_raw_inputs(batch_raw_inputs=[dict(id=id, raw_inputs=raw_inputs)])

    def log_batch_raw_inputs(self, batch_raw_inputs: Iterable[dict]):
        """Logs raw inputs of multiple predictions.

        Args:
            batch_raw_inputs (Iterable[dict]): An iterable that produces raw_inputs dicts.
                Each dict MUST contain the following keys:
                    * id (str): Prediction identifier.
                    * raw_inputs (Dict[str, SupportedValueType]): Raw inputs of the prediction.
        """
        self._log_batch_inference(
            batch=batch_raw_inputs,
            fragment_class=RawInputsFragment,
            error_message="Logging raw inputs batch failed, error: {}",
        )

    def log_outputs(self, id: str, outputs: Dict[str, SupportedValueType]):
        """Logs outputs of a single prediction.

        Args:
            id (str): Prediction identifier.
            outputs (Dict[str, SupportedValueType]): Final outputs of the prediction.
        """
        self.log_batch_outputs(batch_outputs=[dict(id=id, outputs=outputs)])

    def log_batch_outputs(self, batch_outputs: Iterable[dict]):
        """Logs outputs of multiple predictions.

        Args:
            batch_outputs (Iterable[dict]): An iterable that produces outputs dicts.
                Each dict MUST contain the following keys:
                    * id (str): Prediction identifier.
                    * outputs (Dict[str, SupportedValueType]): Final outputs of the prediction.
        """
        self._log_batch_inference(
            batch=batch_outputs,
            fragment_class=OutputsFragment,
            error_message="Logging outputs batch failed, error: {}",
        )

    def log_actuals(self, id: str, actuals: Dict[str, SupportedValueType]):
        """Logs actual values of a single prediction.

        Args:
            id (str): Prediction identifier.
            actuals (Dict[str, SupportedValueType]): Actual prediction results.

        Note:
            * The fields reported in actuals must be a subset of the fields reported
              in the original prediction.
        """
        self.log_batch_actuals(batch_actuals=[dict(id=id, actuals=actuals)])

    def log_batch_actuals(self, batch_actuals: Iterable[dict]):
        """Logs actual values of multiple predictions.

        Args:
            batch_actuals (Iterable[dict]): An iterable that produces actuals dicts.
                Each dict MUST contain the following keys:
                    * id (str): Prediction identifier.
                    * actuals (Dict[str, SupportedValueType]): Actual prediction results.

        Note:
            * The fields reported in actuals must be a subset of the fields reported
              in the original prediction.
        """
        self._log_batch_inference(
            batch=batch_actuals,
            fragment_class=ActualsFragment,
            error_message="Logging actuals batch failed, error: {}",
        )

    def _log_batch_inference(
        self,
        batch: Iterable[dict],
        fragment_class: Callable,
        error_message: str,
    ):
        if not self._model_ready:
            return

        with self._handle_error(error_message):
            fragments = [fragment_class(data_point) for data_point in batch]

            if self._config.debug:
                for i, fragment in enumerate(fragments):
                    if fragment.is_valid():
                        logger.debug("{} {} is valid".format(fragment.type.value, i))
                    else:
                        logger.debug("{} {} is not valid".format(fragment.type.value, i))

            count = self._event_loop.run_coroutine(self._queue.put(fragments=fragments))

            dropped_fragments = len(fragments) - count
            if dropped_fragments > 0:
                logger.warning(
                    "Message queue reached size limit, dropped {} messages.".format(
                        dropped_fragments
                    )
                )

    async def _flush_inference_callback(self, fragments: List[Fragment]):
        with self._handle_error("Server error: {}"):
            serialized_fragments = []
            for fragment in fragments:
                try:
                    serialized_fragments.append(fragment.serialize())
                except Exception as err:
                    logger.error("Serializing data failed, error: {}".format(err))

            if len(serialized_fragments) > 0:
                await log_inference_fragments(
                    graphql_client=self._graphql_client,
                    model_id=self.model_id,
                    model_version=self.model_version,
                    environment=self._config.environment,
                    serialized_fragments=serialized_fragments,
                    await_insert=self._config.debug,
                )

    def log_json(self, data: Any):
        """Logs arbitrary data.

        Args:
            data (Any): Data to log, must be JSON serializable
        """
        if not self._model_ready:
            return

        logger.debug("Logging arbitrary data.")
        with self._handle_error("Logging arbitrary data failed, error: {}"):
            future = self._event_loop.create_task(self._log_json(data=data))
            self._futures.append(future)

    async def _log_json(self, data: Any):
        with self._handle_error("Logging arbitrary data failed, error: {}"):
            await log_json(
                graphql_client=self._graphql_client,
                model_id=self.model_id,
                model_version=self.model_version,
                environment=self._config.environment,
                data=data,
            )

    def flush(self, timeout: Optional[int] = None) -> Optional[int]:
        """Waits for all currently scheduled tasks to finish.

        Args:
            timeout (int, optional): Maximum number of seconds to wait for tasks to
                complete. Default to None (No timeout).

        Returns:
            Optional[int]: Number of tasks that haven't finished running.
        """
        if not self._model_ready:
            return None

        with self._handle_error(
            message_format="Flushing remaining data failed, error: {}",
            throw_errors=self._config.throw_errors,
        ):
            futures = self._futures
            self._futures = []

            logger.debug("Flusing predictions.")
            # Add a task that flushes the queue, and another that waits for the flush to complete
            futures.append(self._event_loop.create_task(self._queue.flush()))
            futures.append(self._event_loop.create_task(self._queue.join()))

            logger.debug("Waiting for {} scheduled tasks to finish executing.".format(len(futures)))
            done, not_done = wait(futures, timeout=timeout, return_when=ALL_COMPLETED)

            logger.debug(
                "{} tasks finished, {} tasks not finished.".format(len(done), len(not_done))
            )
            self._futures.extend(not_done)

            return len(not_done)

        return None


class Model(BaseModel):
    """Model object."""

    def __init__(self, model_id: str, model_version: str):
        """Initializes a Model object.

        Args:
            model_id (str): Model identifier, as received from the Aporia dashboard.
            model_version (str): Model version - this can be any string that represents the model
                version, such as "v1" or a git commit hash.
        """
        if aporia.context is None:
            logger.error("Aporia was not initialized.")
            super().__init__(
                model_id=model_id,
                model_version=model_version,
                graphql_client=None,
                event_loop=None,
                config=None,
            )
        else:
            super().__init__(
                model_id=model_id,
                model_version=model_version,
                graphql_client=aporia.context.graphql_client,
                event_loop=aporia.context.event_loop,
                config=aporia.context.config,
            )
