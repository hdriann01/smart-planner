from models.node import Node
from models.state import State
from models.user import User


class HeuristicEvaluator:

    @staticmethod
    def remaining_calories(
        user: User,
        state: State,
    ) -> int:

        return max(
            0,
            user.target_calories - state.total_calories
        )

    @staticmethod
    def estimated_daily_calories(
        user: User,
        state: State,
    ) -> float:

        remaining_days = state.remaining_days()

        if remaining_days == 0:
            return 0

        remaining = HeuristicEvaluator.remaining_calories(
            user,
            state,
        )

        return remaining / remaining_days

    @staticmethod
    def heuristic(
        user: User,
        state: State,
    ) -> float:

        calorie_score = (
            HeuristicEvaluator
            .estimated_daily_calories(
                user,
                state,
            )
        )

        fatigue_penalty = state.fatigue * 0.25

        return calorie_score + fatigue_penalty

    @staticmethod
    def path_cost(state: State) -> float:

        return state.fatigue

    @staticmethod
    def evaluate(
        user: User,
        state: State,
    ) -> float:

        return (
            HeuristicEvaluator.path_cost(state)
            +
            HeuristicEvaluator.heuristic(
                user,
                state,
            )
        )

    @staticmethod
    def update_node(
        user: User,
        node: Node,
    ) -> None:

        node.g_cost = (
            HeuristicEvaluator
            .path_cost(node.state)
        )

        node.h_cost = (
            HeuristicEvaluator
            .heuristic(
                user,
                node.state,
            )
        )

        node.calculate_f_cost()

    @staticmethod
    def compare(
        node_a: Node,
        node_b: Node,
    ) -> Node:

        if node_a.f_cost <= node_b.f_cost:
            return node_a

        return node_b