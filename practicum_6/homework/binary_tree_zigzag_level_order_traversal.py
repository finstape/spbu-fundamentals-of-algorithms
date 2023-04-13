from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from collections import deque

import yaml


@dataclass
class Node:
    key: Any
    data: Any = None
    left: Node = None
    right: Node = None


class BinaryTree:
    def __init__(self) -> None:
        self.root: Node = None

    def empty(self) -> bool:
        return self.root is None

    def zigzag_level_order_traversal(self) -> list[Any]:
        answer = []

        # return [] if BinaryTree is empty
        if self.empty():
            return answer

        q = deque([self.root])
        is_reverse = True

        # bfs
        while q:
            res = []
            for _ in range(len(q)):
                node = q.popleft()
                res.append(node.key)

                if node.left:
                    q.append(node.left)

                if node.right:
                    q.append(node.right)

            # check each level of the tree to zigzag level order traversal
            if not is_reverse:
                res = res[::-1]

            answer.append(res)
            is_reverse = not is_reverse

        return answer


def build_tree(list_view: list[Any]) -> BinaryTree:
    bt = BinaryTree()
    nodes = []

    # creating nodes
    for item in list_view:
        node = Node(item) if item is not None else None
        nodes.append(node)

    # connect nodes
    for k, node in enumerate(nodes):
        if node is None:
            continue
        if 2 * k + 1 < len(list_view):
            node.left = nodes[2 * k + 1]
        if 2 * k + 2 < len(list_view):
            node.right = nodes[2 * k + 2]

    # root node
    if len(nodes) != 0:
        bt.root = nodes[0]

    return bt


if __name__ == "__main__":
    # Let's solve Binary Tree Zigzag Level Order Traversal problem from leetcode.com:
    # https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/
    # First, implement build_tree() to read a tree from a list format to our class
    # Second, implement BinaryTree.zigzag_traversal() returning the list required by the task
    # Avoid recursive traversal!

    with open(
        "practicum_6/homework/binary_tree_zigzag_level_order_traversal_cases.yaml", "r"
    ) as f:
        cases = yaml.safe_load(f)

    for i, c in enumerate(cases):
        bt = build_tree(c["input"])
        zz_traversal = bt.zigzag_level_order_traversal()
        print(f"Case #{i + 1}: {zz_traversal == c['output']}")
