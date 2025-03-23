from __future__ import annotations

import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from typing import ClassVar

    from load_balancer_algorithm.context import RequestContext
    from load_balancer_algorithm.node import Node


class Strategy(ABC):
    nodes: ClassVar[list[Node]] = []

    def __init__(self, nodes: list[Node]) -> None:
        self.nodes = nodes

    @abstractmethod
    def get_node(self, ctx: RequestContext) -> Node:
        pass

    def add_node(self, node: Node) -> None:
        self.nodes.append(node)

    def remove_node(self, node: Node) -> None:
        self.nodes = list(filter(lambda n: n != node, self.nodes))
