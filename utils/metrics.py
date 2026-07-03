from planner.result import PlannerResult
from models.user import User


def calorie_target_percentage(
    user: User,
    result: PlannerResult,
) -> float:
    """
    Menghitung persentase pencapaian target kalori.
    """

    if user.target_calories == 0:
        return 0.0

    return (
        result.total_calories
        / user.target_calories
    ) * 100


def average_daily_calories(
    result: PlannerResult,
) -> float:
    """
    Menghitung rata-rata kalori per hari.
    """

    if not result.schedule:
        return 0.0

    return (
        result.total_calories
        / len(result.schedule)
    )


def average_daily_fatigue(
    result: PlannerResult,
) -> float:
    """
    Menghitung rata-rata fatigue per hari.
    """

    if not result.schedule:
        return 0.0

    return (
        result.total_fatigue
        / len(result.schedule)
    )


def workout_ratio(
    result: PlannerResult,
) -> float:
    """
    Persentase hari olahraga.
    """

    total_days = len(result.schedule)

    if total_days == 0:
        return 0.0

    return (
        result.total_workout_days()
        / total_days
    ) * 100


def rest_ratio(
    result: PlannerResult,
) -> float:
    """
    Persentase hari istirahat.
    """

    total_days = len(result.schedule)

    if total_days == 0:
        return 0.0

    return (
        result.total_rest_days()
        / total_days
    ) * 100


def schedule_efficiency(
    user: User,
    result: PlannerResult,
) -> float:
    """
    Mengukur efisiensi jadwal berdasarkan
    pencapaian target kalori.
    """

    target = user.target_calories

    if target == 0:
        return 0.0

    diff = abs(
        target -
        result.total_calories
    )

    efficiency = (
        1 -
        (diff / target)
    ) * 100

    return max(0.0, efficiency)


def remaining_calories(
    user: User,
    result: PlannerResult,
) -> int:
    """
    Menghitung sisa target kalori.
    """

    return max(
        0,
        user.target_calories -
        result.total_calories
    )


def fatigue_utilization(
    user: User,
    result: PlannerResult,
) -> float:
    """
    Persentase penggunaan fatigue threshold.
    """

    if user.fatigue_threshold == 0:
        return 0.0

    return (
        result.total_fatigue
        / user.fatigue_threshold
    ) * 100


def summary_metrics(
    user: User,
    result: PlannerResult,
) -> dict:
    """
    Mengembalikan seluruh metrik dalam
    satu dictionary.
    """

    return {

        "Target Achievement (%)":
            round(
                calorie_target_percentage(
                    user,
                    result,
                ),
                2,
            ),

        "Average Calories":
            round(
                average_daily_calories(
                    result,
                ),
                2,
            ),

        "Average Fatigue":
            round(
                average_daily_fatigue(
                    result,
                ),
                2,
            ),

        "Workout Ratio (%)":
            round(
                workout_ratio(
                    result,
                ),
                2,
            ),

        "Rest Ratio (%)":
            round(
                rest_ratio(
                    result,
                ),
                2,
            ),

        "Efficiency (%)":
            round(
                schedule_efficiency(
                    user,
                    result,
                ),
                2,
            ),

        "Remaining Calories":
            remaining_calories(
                user,
                result,
            ),

        "Fatigue Utilization (%)":
            round(
                fatigue_utilization(
                    user,
                    result,
                ),
                2,
            ),
    }