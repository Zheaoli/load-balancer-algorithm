from __future__ import annotations

import pytest

from load_balancer_algorithm.context import RequestContext
from load_balancer_algorithm.errors import NoNodesAvailableError
from load_balancer_algorithm.node import Node
from load_balancer_algorithm.strategy.round_robin import RoundRobinStrategy


@pytest.fixture
def no_avaliable_nodes() -> list[Node]:
    return [Node(node_available=False), Node(node_available=False)]


@pytest.fixture
def one_nodes() -> list[Node]:
    return [Node(node_available=True), Node(node_available=False)]


@pytest.fixture
def two_nodes() -> list[Node]:
    return [Node(node_available=True), Node(node_available=True)]


@pytest.fixture
def three_nodes_with_different_weights() -> list[Node]:
    return [
        Node(node_available=True, weight=1),
        Node(node_available=True, weight=2),
        Node(node_available=True, weight=3),
    ]


def test_get_node_no_avaliable_nodes(no_avaliable_nodes):
    strategy = RoundRobinStrategy(no_avaliable_nodes)
    with pytest.raises(NoNodesAvailableError):
        strategy.get_node(RequestContext())


def test_get_node_one_nodes(one_nodes):
    strategy = RoundRobinStrategy(one_nodes)
    node = strategy.get_node(RequestContext())
    assert node == one_nodes[0]


def test_get_node_two_nodes(two_nodes):
    strategy = RoundRobinStrategy(two_nodes)
    node = strategy.get_node(RequestContext())
    assert node is two_nodes[0]
    node = strategy.get_node(RequestContext())
    assert node is two_nodes[1]
    node = strategy.get_node(RequestContext())
    assert node is two_nodes[0]


def test_get_node_three_nodes_with_different_weights(three_nodes_with_different_weights):
    strategy = RoundRobinStrategy(three_nodes_with_different_weights)
    nodes = []
    total_weight = sum(node.weight for node in three_nodes_with_different_weights)
    for _ in range(total_weight):
        nodes.append(strategy.get_node(RequestContext()))
    nodes = [
        three_nodes_with_different_weights[2],
        three_nodes_with_different_weights[1],
        three_nodes_with_different_weights[2],
        three_nodes_with_different_weights[0],
        three_nodes_with_different_weights[1],
        three_nodes_with_different_weights[2],
    ]
