from models.node import Node
from models.state import State
from models.user import User

from data.activities import get_all_activities

from rules.rule_engine import RuleEngine

from search.heuristic import HeuristicEvaluator


class GreedySearch:
    """
    Implementasi Greedy Best First Search.

    Memilih node dengan nilai heuristik
    terkecil pada setiap langkah.
    """

    def __init__(self):

        self.rule_engine = RuleEngine()

    def search(
        self,
        user: User,
    ) -> State:
        """
        Menjalankan Greedy Search.
        """

        current_state = State()

        while not current_state.is_goal():

            best_node = self.select_best(
                user,
                current_state,
            )

            if best_node is None:
                raise RuntimeError(
                    "No valid activity found."
                )

            current_state = best_node.state

        return current_state

    def select_best(
        self,
        user: User,
        state: State,
    ) -> Node | None:
        """
        Memilih node dengan heuristic terkecil.
        """

        candidates: list[Node] = []

        parent = Node(state=state)

        for activity in get_all_activities():

            validation = self.rule_engine.validate(
                user,
                state,
                activity,
            )

            if not validation.is_valid:
                continue

            node = parent.expand(activity)

            HeuristicEvaluator.update_node(
                user,
                node,
            )

            candidates.append(node)

        if not candidates:
            return None

        return min(
            candidates,
            key=lambda node: node.h_cost,
        )

    def goal_reached(
        self,
        state: State,
    ) -> bool:
        """
        Mengecek apakah goal tercapai.
        """

        return state.is_goal()