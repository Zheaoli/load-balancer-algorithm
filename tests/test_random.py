from __future__ import annotations

import pytest

from load_balancer_algorithm.context import RequestContext
from load_balancer_algorithm.errors import NoNodesAvailableError
from load_balancer_algorithm.node import Node
from load_balancer_algorithm.strategy.random import RandomStrategy


@pytest.fixture
def no_avaliable_nodes() -> list[Node]:
    return [Node(node_available=False), Node(node_available=False)]


@pytest.fixture
def one_nodes() -> list[Node]:
    return [Node(node_available=True), Node(node_available=False)]


@pytest.fixture
def two_nodes() -> list[Node]:
    return [Node(node_available=True), Node(node_available=True)]


def test_get_node_no_avaliable_nodes(no_avaliable_nodes):
    strategy = RandomStrategy()
    with pytest.raises(NoNodesAvailableError):
        strategy.get_node(RequestContext(), no_avaliable_nodes)


def test_get_node_one_nodes(one_nodes):
    strategy = RandomStrategy()
    node = strategy.get_node(RequestContext(), one_nodes)
    assert node == one_nodes[0]


def test_get_node_two_nodes(two_nodes):
    strategy = RandomStrategy()
    node = strategy.get_node(RequestContext(), two_nodes)
    assert node in two_nodes