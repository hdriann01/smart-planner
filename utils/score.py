from models.user import User
from planner.result import PlannerResult


class ScheduleScorer:
    """
    Mengevaluasi kualitas jadwal olahraga.

    Seluruh skor dinormalisasi ke rentang 0–100.
    """

    CALORIE_WEIGHT = 0.40
    FATIGUE_WEIGHT = 0.30
    BALANCE_WEIGHT = 0.20
    TIME_WEIGHT = 0.10

    @staticmethod
    def target_score(
        user: User,
        result: PlannerResult,
    ) -> float:
        """
        Mengukur seberapa dekat jadwal
        terhadap target kalori pengguna.
        """

        if user.target_calories <= 0:
            return 0.0

        ratio = (
            result.total_calories /
            user.target_calories
        )

        ratio = min(ratio, 1.0)

        return ratio * 100

    @staticmethod
    def fatigue_score(
        user: User,
        result: PlannerResult,
    ) -> float:
        """
        Semakin kecil fatigue,
        semakin tinggi skor.
        """

        if user.fatigue_threshold <= 0:
            return 0.0

        ratio = (
            result.total_fatigue /
            user.fatigue_threshold
        )

        ratio = min(ratio, 1.0)

        return (1 - ratio) * 100

    @staticmethod
    def balance_score(
        result: PlannerResult,
    ) -> float:
        """
        Jadwal ideal memiliki
        sekitar 5 hari olahraga
        dan 2 hari istirahat.
        """

        workout = result.total_workout_days()

        rest = result.total_rest_days()

        ideal_workout = 5

        ideal_rest = 2

        workout_diff = abs(
            workout - ideal_workout
        )

        rest_diff = abs(
            rest - ideal_rest
        )

        score = (
            100
            -
            (
                workout_diff * 10
                +
                rest_diff * 10
            )
        )

        return max(0, score)

    @staticmethod
    def execution_score(
        result: PlannerResult,
    ) -> float:
        """
        Semakin cepat,
        semakin tinggi skor.
        """

        milliseconds = (
            result.execution_time * 1000
        )

        score = 100 - milliseconds

        return max(0, score)

    @classmethod
    def calculate(
        cls,
        user: User,
        result: PlannerResult,
    ) -> float:
        """
        Menghasilkan skor akhir jadwal.
        """

        target = cls.target_score(
            user,
            result,
        )

        fatigue = cls.fatigue_score(
            user,
            result,
        )

        balance = cls.balance_score(
            result,
        )

        execution = cls.execution_score(
            result,
        )

        final_score = (

            target * cls.CALORIE_WEIGHT

            +

            fatigue * cls.FATIGUE_WEIGHT

            +

            balance * cls.BALANCE_WEIGHT

            +

            execution * cls.TIME_WEIGHT

        )

        return round(final_score, 2)

    @classmethod
    def compare(
        cls,
        user: User,
        greedy: PlannerResult,
        astar: PlannerResult,
    ) -> PlannerResult:
        """
        Memilih hasil terbaik.
        """

        greedy_score = cls.calculate(
            user,
            greedy,
        )

        astar_score = cls.calculate(
            user,
            astar,
        )

        if astar_score >= greedy_score:

            return astar

        return greedy

    @classmethod
    def detailed_scores(
        cls,
        user: User,
        result: PlannerResult,
    ) -> dict:
        """
        Mengembalikan seluruh komponen skor.
        """

        return {

            "Target Score":
                round(
                    cls.target_score(
                        user,
                        result,
                    ),
                    2,
                ),

            "Fatigue Score":
                round(
                    cls.fatigue_score(
                        user,
                        result,
                    ),
                    2,
                ),

            "Balance Score":
                round(
                    cls.balance_score(
                        result,
                    ),
                    2,
                ),

            "Execution Score":
                round(
                    cls.execution_score(
                        result,
                    ),
                    2,
                ),

            "Final Score":
                cls.calculate(
                    user,
                    result,
                ),
        }