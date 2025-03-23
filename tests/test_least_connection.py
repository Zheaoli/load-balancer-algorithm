from __future__ import annotations

import pytest

from load_balancer_algorithm.context import RequestContext
from load_balancer_algorithm.node import Node
from load_balancer_algorithm.strategy.least_connection import LeastConnectionStrategy


@pytest.fixture
def two_nodes_with_weights() -> list[Node]:
    return [
        Node(node_available=True, weight=1),
        Node(node_available=True, weight=1),
    ]


def test_get_node_two_nodes_with_weights(two_nodes_with_weights):
    strategy = LeastConnectionStrategy(two_nodes_with_weights)
    node = strategy.get_node(RequestContext())
    node2 = strategy.get_node(RequestContext())
    assert node is two_nodes_with_weights[0]
    assert node2 is two_nodes_with_weights[1]
