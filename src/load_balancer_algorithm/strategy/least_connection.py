from __future__ import annotations

import typing

from load_balancer_algorithm.errors import NoNodesAvailableError
from load_balancer_algorithm.strategy.base import Strategy

if typing.TYPE_CHECKING:
    from load_balancer_algorithm.context import RequestContext
    from load_balancer_algorithm.node import Node


class LeastConnectionStrategy(Strategy):
    def get_node(self, ctx: RequestContext) -> Node:
        best = None
        for node in self.nodes:
            if not node.available:
                continue
            if not best or node.connections < best.connections:
                best = node
        if not best:
            raise NoNodesAvailableError
        best.connections += 1
        return best


class WeightedLeastConnectionStrategy(LeastConnectionStrategy):
    def get_node(self, ctx: RequestContext) -> Node:
        best = None
        for node in self.nodes:
            if not node.available:
                continue
            if not best or (node.connections / node.weight) < (best.connections / best.weight):
                best = node
        if not best:
            raise NoNodesAvailableError
        best.connections += 1
        return best
