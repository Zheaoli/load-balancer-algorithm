from __future__ import annotations

import typing

from load_balancer_algorithm.errors import NoNodesAvailableError
from load_balancer_algorithm.strategy.base import Strategy

if typing.TYPE_CHECKING:
    from load_balancer_algorithm.context import RequestContext
    from load_balancer_algorithm.node import Node


class RoundRobinStrategy(Strategy):
    def __init__(self, nodes: list[Node]) -> None:
        super().__init__(nodes)
        self.index = 0

    def get_node(self, ctx: RequestContext) -> Node:
        nodes = list(filter(lambda node: node.available, self.nodes))
        if not nodes:
            raise NoNodesAvailableError

        node = nodes[self.index]
        self.index += 1
        if self.index >= len(nodes):
            self.index = 0

        return node


class WeightedRoundRobinStrategy(RoundRobinStrategy):
    def get_node(self, ctx: RequestContext) -> Node:
        nodes = list(filter(lambda node: node.available, self.nodes))
        if not nodes:
            raise NoNodesAvailableError
        best_node = None
        total = 0
        for node in nodes:
            total += node.weight
            if not best_node or node.weight > best_node.weight:
                best_node = node
        if not best_node:
            raise NoNodesAvailableError
        best_node.weight -= total
        return best_node
