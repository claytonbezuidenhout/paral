from paral import ThreadEngine, get_logger
from paral.func.runners import run_at_intervals
from kafka import KafkaProducer, KafkaConsumer
from typing import Callable
from functools import wraps

engine = ThreadEngine.instance()
log = get_logger(__name__)


def kafka_producer(*kafka_args, **kafka_kwargs):
    def inner_wrapper(func: Callable):
        @wraps(func)
        def wrapper(*_args, **_kwargs):
            topic = kafka_args[0]
            producer = KafkaProducer(**kafka_kwargs)

            def run_producer():
                log.debug(f"Producing on topic: {topic}")
                func(producer, topic)
                log.debug(f"Completed topic: {topic}")

            engine.create_component(run_producer)

        return wrapper

    return inner_wrapper


def kafka_consumer(*kafka_args, **kafka_kwargs):
    interval_seconds = kafka_kwargs.get("interval_seconds", 2)
    del kafka_kwargs["interval_seconds"]

    def inner_wrapper(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            topic = kafka_args
            consumer = KafkaConsumer(
                *kafka_args,
                **kafka_kwargs,
            )

            @run_at_intervals(interval_seconds=interval_seconds)
            def consume(*argsx, **kwargsx):
                log.debug(f"Checking topic: {topic}")
                for message in consumer:
                    func(message, *argsx, **kwargsx)
                    consumer.commit()
                log.debug(f"Completed topic: {topic}")

            engine.create_component(consume, *args, **kwargs)

        return wrapper

    return inner_wrapper
