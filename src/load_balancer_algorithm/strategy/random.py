from __future__ import annotations

import random
import typing

from load_balancer_algorithm.errors import NoNodesAvailableError
from load_balancer_algorithm.strategy.base import Strategy

if typing.TYPE_CHECKING:
    from load_balancer_algorithm.context import RequestContext
    from load_balancer_algorithm.node import Node


class RandomStrategy(Strategy):
    def get_node(self, ctx: RequestContext) -> Node:
        nodes = list(filter(lambda node: node.available, self.nodes))
        if not nodes:
            raise NoNodesAvailableError

        return random.choice(nodes)


class WeightedRandomStrategy(Strategy):
    def get_node(self, ctx: RequestContext) -> Node:
        nodes = list(filter(lambda node: node.available, self.nodes))
        if not nodes:
            raise NoNodesAvailableError

        weights = [node.weight for node in nodes]
        return random.choices(nodes, weights=weights)[0]
