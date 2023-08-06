import logging
import typing

from rasa.utils import endpoints

if typing.TYPE_CHECKING:
    from ragex.community.services.event_consumers.event_consumer import EventConsumer

logger = logging.getLogger(__name__)


def from_endpoint_config(
    broker_config: endpoints.EndpointConfig, should_run_liveness_endpoint: bool
) -> "EventConsumer":
    """Instantiate an event consumer based on an endpoint config.

    Args:
        broker_config: Event consumer endpoint config.
        should_run_liveness_endpoint: If `True`, runs a simple Sanic server as a
            background process that can be used to probe liveness of this service.
            The service will be exposed at a port defined by the
            `SELF_PORT` environment variable (5673 by default).

    Returns:
        `KafkaEventConsumer` or `PikaEventConsumer` if valid endpoint config.
        was provided. `SQLiteEventConsumer` if no config was provided.
        `None` if an unknown type was requested.

    """

    consumer = None
    if broker_config is None:
        from ragex.community.services.event_consumers.sqlite_consumer import (
            SQLiteEventConsumer,
        )

        consumer = SQLiteEventConsumer(should_run_liveness_endpoint)
    elif broker_config.type.lower() == "pika" or broker_config.type is None:
        from ragex.community.services.event_consumers.pika_consumer import (
            PikaEventConsumer,
        )

        logging.getLogger("pika").setLevel(logging.WARNING)
        consumer = PikaEventConsumer.from_endpoint_config(
            broker_config, should_run_liveness_endpoint
        )
    elif broker_config.type.lower() == "kafka":
        from ragex.community.services.event_consumers.kafka_consumer import (
            KafkaEventConsumer,
        )

        consumer = KafkaEventConsumer.from_endpoint_config(
            broker_config, should_run_liveness_endpoint
        )

    if consumer:
        return consumer
    else:
        raise ValueError(
            f"Found event broker `EndpointConfig` of type "
            f"'{broker_config.type}', which is not supported."
        )
