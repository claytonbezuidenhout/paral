from uuid import uuid1
from threading import Thread

from paral.base.singleton import Singleton
from paral.base.logger import get_logger

log = get_logger(__name__)


@Singleton
class ThreadEngine:
    """
    This is the main driver of all tasks that are wrapped with paral runners.

    As functions that has been wrapped are loaded or executed, the underlying logic
    always uses `create_component()` which loads the function into the `self.threads` list.
    and when `.start()` is called, starts the wrapped functions in seperate threads.

    A thread index keeps track of the active threads, this is to prevent duplicate spin up
    of threads in the thread-join loop when new threads are added at runtime instead of startup.
    """
    def __init__(self):
        self.threads = {}
        self.thread_index = 0
        pass

    @staticmethod
    def load(*args):
        """
        A helper method that executes all wrapped methods passed as arguments.
        This expects the wrapper functions to call `create_component()`
        """
        for method in args:
            method()

    def create_component(self, func, *args, **kwargs):
        """
        Loads the threads list with a Thread class using unique index that consists of
        the wrapped function and its associated args and kwargs.
        """
        self.threads[f"{func.__name__}_{uuid1()}"] = Thread(
            target=func,
            args=args,
            kwargs=kwargs,
            daemon=True
        )
        log.debug(f"created component thread {func.__name__}")

    def start(self):
        """
        Loops over all threads loaded into the thread list and
        awaits the stop of all threads before exiting.

        Runtime errors that occur here is because the thread list
        gets increased at runtime and causes the join() loop to raise
        that the list has changed.

        it executes start method again,
        and use the thread_index to skip the threads that was loaded before.
        Thereafter it starts the threads that was added when the RuntimeError occurred.
        """
        log.debug("Starting Thread engine")
        try:
            if (self.thread_index + 1) <= len(self.threads.keys()):
                for i, key in enumerate(self.threads):
                    if i >= self.thread_index:
                        log.debug(f"starting component thread {i}:{key}")
                        self.thread_index += 1
                        self.threads[key].start()
            for i in self.threads:
                self.threads[i].join()

        except RuntimeError as e:
            log.debug(e)
            self.start()

        log.info(f"Thread Engine stopped.")
