from models.node import Node
from models.state import State
from models.user import User


class HeuristicEvaluator:
    """
    Bertugas menghitung seluruh nilai heuristik
    yang digunakan oleh Greedy Search maupun A*.
    """

    @staticmethod
    def remaining_calories(
        user: User,
        state: State,
    ) -> int:
        """
        Menghitung sisa target kalori.
        """

        return max(
            0,
            user.target_calories - state.total_calories
        )

    @staticmethod
    def estimated_daily_calories(
        user: User,
        state: State,
    ) -> float:
        """
        Estimasi kebutuhan kalori
        pada hari yang tersisa.
        """

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
        """
        Nilai heuristik h(n).

        Semakin kecil nilainya,
        semakin baik state tersebut.
        """

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
        """
        g(n)

        Biaya perjalanan dari root
        menuju state sekarang.

        Saat ini menggunakan fatigue.
        """

        return state.fatigue

    @staticmethod
    def evaluate(
        user: User,
        state: State,
    ) -> float:
        """
        f(n)

        Digunakan oleh A*.
        """

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
        """
        Memperbarui nilai
        g(n), h(n), dan f(n).
        """

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
        """
        Mengembalikan node terbaik.
        """

        if node_a.f_cost <= node_b.f_cost:
            return node_a

        return node_b