import sys
from abc import ABCMeta, abstractmethod
from typing import List, Optional

from zuper_commons.logs import monkeypatch_findCaller
from zuper_nodes.structures import TimingInfo
from zuper_typing import PYTHON_36, PYTHON_37

__all__ = [
    "Context",
    "wrap_direct",
]


def wrap_direct(node, protocol, args: Optional[List[str]] = None):
    if args is None:
        args = sys.argv[1:]

    from zuper_nodes_wrapper.wrapper import check_implementation, run_loop

    if PYTHON_36 or PYTHON_37:
        monkeypatch_findCaller()
    check_implementation(node, protocol)
    run_loop(node, protocol, args)


class Context(metaclass=ABCMeta):
    @abstractmethod
    def write(
        self, topic: str, data: object, timing: TimingInfo = None, with_schema: bool = False,
    ):
        pass

    @abstractmethod
    def info(self, msg: str):
        pass

    @abstractmethod
    def debug(self, msg: str):
        pass

    @abstractmethod
    def warning(self, msg: str):
        pass

    @abstractmethod
    def error(self, msg: str):
        pass

    @abstractmethod
    def get_hostname(self):
        pass
