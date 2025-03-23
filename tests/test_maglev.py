from __future__ import annotations

import pytest

from load_balancer_algorithm.context import RequestContext
from load_balancer_algorithm.node import Node
from load_balancer_algorithm.strategy.maglev import MaglevStrategy


@pytest.fixture
def two_nodes_with_weights() -> list[Node]:
    return [
        Node(node_available=True, weight=1),
        Node(node_available=True, weight=1),
    ]


def test_get_node_two_nodes_with_weights(two_nodes_with_weights):
    strategy = MaglevStrategy(two_nodes_with_weights)
    node = strategy.get_node(RequestContext(url="/abc"))
    node2 = strategy.get_node(RequestContext(url="/abc2"))
    for _ in range(10):
        assert strategy.get_node(RequestContext(url="/abc")) is node
        assert strategy.get_node(RequestContext(url="/abc2")) is node2
