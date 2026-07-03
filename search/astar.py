from models.node import Node
from models.state import State
from models.user import User

from data.activities import get_all_activities

from rules.rule_engine import RuleEngine

from search.priority_queue import PriorityQueue
from search.heuristic import HeuristicEvaluator


class AStarSearch:
    """
    Implementasi algoritma A* Search.

    Menggunakan:

    - Open List (Priority Queue)
    - Closed List
    - Heuristic Evaluation
    """

    def __init__(self):

        self.rule_engine = RuleEngine()

        self.open_list = PriorityQueue()

        self.closed_list: list[Node] = []

    def search(
        self,
        user: User,
    ) -> State:
        """
        Menjalankan algoritma A*.
        """

        start = Node(
            state=State()
        )

        HeuristicEvaluator.update_node(
            user,
            start,
        )

        self.open_list.push(start)

        while not self.open_list.is_empty():

            current = self.open_list.pop()

            if current.goal():

                return current.state

            self.closed_list.append(current)

            self.expand_node(
                user,
                current,
            )

        raise RuntimeError(
            "No solution found."
        )

    def expand_node(
        self,
        user: User,
        current: Node,
    ) -> None:
        """
        Mengembangkan seluruh child node.
        """

        for activity in get_all_activities():

            validation = self.rule_engine.validate(
                user,
                current.state,
                activity,
            )

            if not validation.is_valid:
                continue

            child = current.expand(
                activity
            )

            HeuristicEvaluator.update_node(
                user,
                child,
            )

            if self.is_closed(
                child
            ):
                continue

            self.open_list.push(
                child
            )

    def is_closed(
        self,
        node: Node,
    ) -> bool:
        """
        Mengecek apakah state
        sudah pernah dieksplorasi.
        """

        for closed in self.closed_list:

            if (
                closed.state.schedule
                ==
                node.state.schedule
            ):
                return True

        return False

    def reconstruct_path(
        self,
        node: Node,
    ) -> list[Node]:
        """
        Mengembalikan jalur solusi.
        """

        return node.path()