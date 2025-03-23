from __future__ import annotations

import typing

import mmh3
import xxhash

from load_balancer_algorithm.strategy.base import Strategy

if typing.TYPE_CHECKING:
    from load_balancer_algorithm.context import RequestContext
    from load_balancer_algorithm.node import Node

M = 65537


class MaglevStrategy(Strategy):
    @staticmethod
    def calculate_lookup_table(n: int, m: int, permutations: list[list[int]]) -> list[int]:
        # result 是最终记录分布的 Hash 表
        result: list[int] = [-1] * m
        # next 是用来解决冲突的，在遍历过程中突然想要填入的 entry 表已经被占用，
        # 则通过 next 找到下一行。一直进行该过程直到找到一个空位。
        # 因为每一列都包含有 0~M-1 的每一个值，所以最终肯定能遍历完每一行。
        # 计算复杂度为 O(M logM) ~ O(M^2)
        next: list[int] = [0] * n
        flag = 0
        while True:
            for i in range(n):
                x = permutations[i][next[i]]
                while True:
                    # 找到空位，退出查找
                    if result[x] == -1:
                        break
                    next[i] += 1
                    x = permutations[i][next[i]]
                result[x] = i
                next[i] += 1
                flag += 1
                # 表已经填满，退出计算
                if flag == m:
                    return result

    def __init__(self, nodes: list[Node]) -> None:
        super().__init__(nodes)
        permutations = []
        for i in range(len(nodes)):
            permutation = [0] * M
            offset = mmh3.hash(str(nodes[i])) % M
            skip = (xxhash.xxh32(str(nodes[i])).intdigest() % (M - 1)) + 1
            for j in range(M):
                permutation[j] = (offset + j * skip) % M
            permutations.append(permutation)
        self.tables = self.calculate_lookup_table(len(nodes), M, permutations)

    def get_node(self, ctx: RequestContext) -> Node:
        hash_value = mmh3.hash(str(ctx))
        index = hash_value % M
        node_index = self.tables[index]
        return self.nodes[node_index]
