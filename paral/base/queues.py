import re

from paral.base.singleton import Singleton
from paral.base.logger import get_logger
from queue import Queue

log = get_logger(__name__)


@Singleton
class QueueManager:
    def __init__(self):
        self.queues = {}
        self.router = QueueRouter(queues=self.queues)

    def get_new_queue(self, name: str):
        self.queues[name] = Queue()
        return self.queues[name]

    def deregister_queue(self, name):
        delattr(self.queues, name)

    def send_to_queue(self, func, payload):
        self.router.send(payload, func)


class QueueRouter:
    def __init__(self, queues=None, rounting_rules=None, multiplexer=False):
        self.multiplexer = multiplexer
        self.rules = rounting_rules
        self._setup_pattern_matchers()
        self.queues = QueueManager.instance().queues if queues is None else queues

    def _setup_pattern_matchers(self):
        if self.rules:
            for rule in self.rules:
                rule[1] = re.compile(rule[1]) if rule[0] == "match" else rule[1]

    def send(self, payload, func=None):
        if func:
            self.queues[func.__name__].put(payload)
        elif self.rules:
            send_to_queues = []
            for rule in self.rules:
                mapped_function_name = rule[2].__name__
                if (isinstance(payload, int) or isinstance(payload, float)) and rule[
                    0
                ] == "eq":
                    if rule[1] == payload:
                        send_to_queues.append(mapped_function_name)
                        if not self.multiplexer:
                            break
                elif (isinstance(payload, int) or isinstance(payload, float)) and rule[
                    0
                ] == "gt":
                    if payload > rule[1]:
                        send_to_queues.append(mapped_function_name)
                        if not self.multiplexer:
                            break
                elif (isinstance(payload, int) or isinstance(payload, float)) and rule[
                    0
                ] == "gteq":
                    if payload >= rule[1]:
                        send_to_queues.append(mapped_function_name)
                        if not self.multiplexer:
                            break
                elif (isinstance(payload, int) or isinstance(payload, float)) and rule[
                    0
                ] == "lt":
                    if payload < rule[1]:
                        send_to_queues.append(mapped_function_name)
                        if not self.multiplexer:
                            break
                elif (isinstance(payload, int) or isinstance(payload, float)) and rule[
                    0
                ] == "lteq":
                    if rule[1] <= payload:
                        send_to_queues.append(mapped_function_name)
                        if not self.multiplexer:
                            break
                elif (isinstance(payload, int) or isinstance(payload, float)) and rule[
                    0
                ] == "neq":
                    if rule[1] != payload:
                        send_to_queues.append(mapped_function_name)
                        if not self.multiplexer:
                            break
                elif (isinstance(payload, int) or isinstance(payload, float)) and rule[
                    0
                ] == "range":
                    if rule[1][0] <= payload >= rule[1][1]:
                        send_to_queues.append(mapped_function_name)
                        if not self.multiplexer:
                            break
                elif isinstance(payload, str) and rule[0] == "match":
                    if rule[1].match(payload):
                        send_to_queues.append(mapped_function_name)
                        if not self.multiplexer:
                            break

            if send_to_queues:
                for queue in send_to_queues:
                    self.queues[queue].put(payload)
            else:
                log.warn(f"No router rule match on data: {payload}")
