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

    def next(self, prev_p: int) -> int:
        return self.np ^ prev_p

    def prev(self, next_p: int) -> int:
        return self.np ^ next_p


class XorDoublyLinkedList:
    def __init__(self) -> None:
        self.head: Element = None
        self.tail: Element = None
        self.__nodes: list[Element] = []

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        if self.empty():
            return ""

        node_keys = []
        next_id = id(self.head)
        prev_id = 0

        while next_id != 0:
            next_el = ctypes.cast(next_id, ctypes.py_object).value
            node_keys.append(str(next_el.key))
            prev_id, next_id = next_id, next_el.next(prev_id)

        return " <-> ".join(node_keys)

    def to_pylist(self) -> list[Any]:
        if self.empty():
            return []

        py_list = []
        next_id = id(self.head)
        prev_id = 0

        while next_id != 0:
            next_el = ctypes.cast(next_id, ctypes.py_object).value
            py_list.append(next_el.key)
            prev_id, next_id = next_id, next_el.next(prev_id)

        return py_list

    def empty(self):
        return self.head is None

    def search(self, k: Element) -> Element:
        """Complexity: O(n)"""
        if self.empty():
            raise ValueError("List is empty!")

        next_id = id(self.head)
        prev_id = 0
        next_el = self.head

        while next_id != 0 and next_el.key != k.key:
            prev_id, next_id = next_id, next_el.next(prev_id)

            if next_id == 0:
                raise ValueError("List doesn't store this element!")

            next_el = ctypes.cast(next_id, ctypes.py_object).value

        return next_el

    def insert(self, x: Element) -> None:
        """Insert to the front of the list (i.e., it is 'prepend')
        Complexity: O(1)
        """
        if self.head is None:
            self.head = self.tail = x
        else:
            x.np = id(self.head)
            self.head.np = self.head.np ^ id(x)
            self.head = x
        self.__nodes = [x] + self.__nodes

    def remove(self, x: Element) -> None:
        """Remove x from the list
        Complexity: O(n)
        """
        if self.empty():
            raise ValueError("List is empty!")

        if self.head.key == x.key:
            if self.head == self.tail:
                self.__nodes.remove(self.head)
                self.head = self.tail = None
            else:
                if self.tail == ctypes.cast(self.head.next(0), ctypes.py_object).value:
                    self.head = self.tail
                    self.head.np = self.tail.np = 0
                    self.__nodes = [self.head]
                else:
                    next_el = ctypes.cast(self.head.next(0), ctypes.py_object).value
                    NEXT_EL = ctypes.cast(next_el.next(id(self.head)), ctypes.py_object).value
                    self.head = next_el
                    self.head.np = 0 ^ id(NEXT_EL)
                    self.__nodes.pop(0)
        elif self.tail.key == x.key:
            if self.head == ctypes.cast(self.tail.prev(0), ctypes.py_object).value:
                self.tail = self.head
                self.head.np = self.tail.np = 0
                self.__nodes = [self.tail]
            else:
                next_el = ctypes.cast(self.head.prev(0), ctypes.py_object).value
                NEXT_EL = ctypes.cast(next_el.next(id(self.tail)), ctypes.py_object).value
                self.tail = next_el
                self.tail.np = 0 ^ id(NEXT_EL)
                self.__nodes.pop(len(self.__nodes) - 1)
        else:
            next_id = id(self.head)
            prev_id = 0
            next_el = self.head

            while next_id != 0 and next_el.key != x.key:
                prev_id, next_id = next_id, next_el.next(prev_id)

                if next_id == 0:
                    raise ValueError("List doesn't store this element!")

                next_el = ctypes.cast(next_id, ctypes.py_object).value

            prev_el = ctypes.cast(prev_id, ctypes.py_object).value
            NEXT_ID = next_el.np ^ prev_id
            NEXT_EL = ctypes.cast(NEXT_ID, ctypes.py_object).value

            prev_el.np = prev_el.np ^ next_id ^ NEXT_ID
            NEXT_EL.np = NEXT_EL.np ^ next_id ^ prev_id

            self.__nodes.remove(next_el)

    def reverse(self) -> XorDoublyLinkedList:
        """Returns the same list but in the reserved order
        Complexity: O(1)
        """
        if self.empty():
            raise ValueError("List is empty!")

        self.head, self.tail = self.tail, self.head
        return self


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
