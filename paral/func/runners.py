from paral import ThreadEngine, get_logger

from time import sleep
from typing import Callable
from datetime import datetime
from croniter import croniter

engine = ThreadEngine.instance()
log = get_logger(__name__)


def run_once(func: Callable):
    def wrapper(*args, **kwargs):
        engine.create_component(func, *args, **kwargs)

    return wrapper


def run_at_intervals(interval_seconds=1, repeat_times=-1, keep_alive=True):
    def inner_wrapper(func: Callable):
        def wrapper(*args, **kwargs):
            def interval_build_func(*_args, **_kwargs):
                repeates_left = [i for i in range(
                    repeat_times)] if repeat_times > 0 else None

                def run():
                    try:
                        repeates_left.pop() if repeat_times != -1 else ...
                        func(*_args, **_kwargs)
                        sleep(interval_seconds)
                    except Exception as e:
                        log.error(e)
                        if not keep_alive:
                            raise

                while True:
                    if repeat_times != -1:
                        if len(repeates_left) > 0:
                            run()
                        else:
                            break
                    else:
                        run()

            engine.create_component(interval_build_func, *args, **kwargs)

        return wrapper

    return inner_wrapper


def cron_job(cron=None, interval_seconds=1):
    def inner_wrapper(func: Callable):

        def wrapper(*args, **kwargs):

            def cron_job_run_func(*_args, **_kwargs):
                base = datetime.now()
                cron_itr = croniter(cron, base)

                next_run = cron_itr.get_next(datetime)
                while True:
                    if datetime.now() >= next_run:
                        next_run = cron_itr.get_next(datetime)
                        func(*_args, **_kwargs)
                        sleep(interval_seconds)

            engine.create_component(cron_job_run_func, *args, **kwargs)

        return wrapper

    return inner_wrapper
