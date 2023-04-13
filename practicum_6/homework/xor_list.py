from __future__ import annotations
from dataclasses import dataclass
from typing import Any

import ctypes
import yaml


@dataclass
class Element:
    key: Any
    data: Any = None
    np: int = 0

    def next(self, prev_el: Element) -> Element:
        if prev_el is None:
            return ctypes.cast(0 ^ id(self), ctypes.py_object).value
        return ctypes.cast(prev_el.np ^ id(self), ctypes.py_object).value

    def prev(self, next_el: Element) -> Element:
        if next_el is None:
            return ctypes.cast(0 ^ id(self), ctypes.py_object).value
        return ctypes.cast(next_el.np ^ id(self), ctypes.py_object).value


class XorDoublyLinkedList:
    def __init__(self) -> None:
        self.head: Element = None
        self.tail: Element = None

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        node_keys = []
        next_el: Element = self.head
        prev_el: Element = None
        while next_el is not None:
            node_keys.append(str(next_el.key))
            prev_el, next_el = next_el, next_el.next(prev_el)
        return " <-> ".join(node_keys)

    def to_pylist(self) -> list[Any]:
        py_list = []
        next_el: Element = self.head
        prev_el: Element = None
        while next_el is not None:
            py_list.append(next_el.key)
            prev_el, next_el = next_el, next_el.next(prev_el)
        return py_list

    def empty(self):
        return self.head is None

    def search(self, k: Element) -> Element:
        """Complexity: O(n)"""
        next_el: Element = self.head
        prev_el: Element = None
        while next_el is not None and next_el != k:
            prev_el, next_el = next_el, next_el.next(prev_el)
        return next_el

    def insert(self, x: Element) -> None:
        """Insert to the front of the list (i.e., it is 'prepend')
        Complexity: O(1)
        """
        if self.head is None:
            self.head = self.tail = x
        else:
            x.np = id(self.head) ^ 0
            self.head.np = id(x) ^ self.head.np
            self.head = x

    def remove(self, x: Element) -> None:
        """Remove x from the list
        Complexity: O(1)
        """

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def reverse(self) -> XorDoublyLinkedList:
        """Returns the same list but in the reserved order
        Complexity: O(1)
        """

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass


if __name__ == "__main__":
    # You need to implement a doubly linked list using only one pointer
    # self.np per element. In python, by pointer, we understand id(object).
    # Any object can be accessed via its id, e.g.
    # >>> import ctypes
    # >>> a = ...
    # >>> ctypes.cast(id(a), ctypes.py_object).value
    # Hint: assuming that self.next and self.prev store pointers
    # define self.np as self.np = self.next XOR self.prev

    with open("practicum_6/homework/xor_list_cases.yaml", "r") as f:
        cases = yaml.safe_load(f)

    for i, c in enumerate(cases):
        l = XorDoublyLinkedList()
        for el in reversed(c["input"]["list"]):
            l.insert(Element(key=el))
        for op_info in c["input"]["ops"]:
            if op_info["op"] == "insert":
                l.insert(Element(key=op_info["key"]))
            elif op_info["op"] == "remove":
                l.remove(Element(key=op_info["key"]))
            elif op_info["op"] == "reverse":
                l = l.reverse()
        py_list = l.to_pylist()
        print(f"Case #{i + 1}: {py_list == c['output']}")
