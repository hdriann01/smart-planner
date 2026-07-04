import heapq

from models.node import Node


class PriorityQueue:

    def __init__(self):
        self._queue: list[Node] = []

    def push(self, node: Node) -> None:

        heapq.heappush(self._queue, node)

    def pop(self) -> Node:

        if self.is_empty():
            raise IndexError("Priority Queue is empty.")

        return heapq.heappop(self._queue)

    def peek(self) -> Node:

        if self.is_empty():
            raise IndexError("Priority Queue is empty.")

        return self._queue[0]

    def is_empty(self) -> bool:

        return len(self._queue) == 0

    def size(self) -> int:

        return len(self._queue)

    def clear(self) -> None:

        self._queue.clear()

    def contains(self, state) -> bool:

        return any(node.state == state for node in self._queue)

    def get_all(self) -> list[Node]:

        return list(self._queue)

    def __len__(self) -> int:
        return len(self._queue)

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __str__(self) -> str:
        return (
            f"PriorityQueue("
            f"size={len(self._queue)})"
        )