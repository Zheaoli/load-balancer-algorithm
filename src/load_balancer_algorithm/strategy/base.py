from __future__ import annotations

import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from load_balancer_algorithm.context import RequestContext
    from load_balancer_algorithm.node import Node


class Strategy(ABC):
    @abstractmethod
    def get_node(self, ctx: RequestContext, nodes: list[Node]) -> Node:
        pass
