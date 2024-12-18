from __future__ import annotations

import random
import typing

from load_balancer_algorithm.errors import NoNodesAvailableError
from load_balancer_algorithm.strategy.base import Strategy

if typing.TYPE_CHECKING:
    from load_balancer_algorithm.context import RequestContext
    from load_balancer_algorithm.node import Node


class RandomStrategy(Strategy):
    def get_node(self, ctx: RequestContext, nodes: list[Node]) -> Node:
        nodes = list(filter(lambda node: node.available, nodes))
        if not nodes:
            raise NoNodesAvailableError

        return random.choice(nodes)
