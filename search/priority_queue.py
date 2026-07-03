import heapq

from models.node import Node


class PriorityQueue:
    """
    Priority Queue untuk algoritma A*.

    Queue diurutkan berdasarkan nilai f(n)
    yang dimiliki setiap Node.
    """

    def __init__(self):
        self._queue: list[Node] = []

    def push(self, node: Node) -> None:
        """
        Menambahkan node ke priority queue.
        """

        heapq.heappush(self._queue, node)

    def pop(self) -> Node:
        """
        Mengambil node dengan nilai f(n)
        paling kecil.
        """

        if self.is_empty():
            raise IndexError("Priority Queue is empty.")

        return heapq.heappop(self._queue)

    def peek(self) -> Node:
        """
        Melihat node terbaik tanpa
        menghapusnya dari queue.
        """

        if self.is_empty():
            raise IndexError("Priority Queue is empty.")

        return self._queue[0]

    def is_empty(self) -> bool:
        """
        Mengecek apakah queue kosong.
        """

        return len(self._queue) == 0

    def size(self) -> int:
        """
        Mengembalikan jumlah node.
        """

        return len(self._queue)

    def clear(self) -> None:
        """
        Menghapus seluruh isi queue.
        """

        self._queue.clear()

    def contains(self, state) -> bool:
        """
        Mengecek apakah State sudah ada
        di dalam queue.
        """

        return any(node.state == state for node in self._queue)

    def get_all(self) -> list[Node]:
        """
        Mengembalikan seluruh node.
        """

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