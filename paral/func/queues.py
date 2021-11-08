from typing import Callable
from functools import wraps

from paral import QueueManager, ThreadEngine, get_logger
from paral.func.runners import run_at_intervals


engine = ThreadEngine.instance()
log = get_logger(__name__)


def queue_consumer(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        qname = func.__name__
        queue_manager = QueueManager.instance()
        queue = queue_manager.get_new_queue(qname)

        @run_at_intervals(interval_seconds=0)
        def consume(*argsx, **kwargsx):
            log.debug(f"Consuming from queue: {queue}")
            while True:
                message = queue.get()
                if message:
                    func(message, *argsx, **kwargsx)

        engine.create_component(consume, *args, **kwargs)

    return wrapper


def queue_producer(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        queue_manager = QueueManager.instance()

        def setup_producer(*argsx, **kwargsx):
            log.debug(f"Creating queue producer")
            func(queue_manager, *argsx, **kwargsx)

        engine.create_component(setup_producer, *args, **kwargs)

    return wrapper
