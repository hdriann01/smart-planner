from planner.result import PlannerResult


DAY_NAMES = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def schedule_table(result: PlannerResult) -> list[dict]:

    rows = []

    for day, activity in zip(DAY_NAMES, result.schedule):

        rows.append(
            {
                "Day": day,
                "Activity": activity.name if activity else "-",
                "Duration (min)": (
                    activity.duration if activity else 0
                ),
                "Calories": (
                    activity.calories if activity else 0
                ),
                "Fatigue": (
                    activity.fatigue if activity else 0
                ),
                "Intensity": (
                    activity.intensity.name
                    if activity
                    else "-"
                ),
            }
        )

    return rows


def comparison_table(
    greedy: PlannerResult,
    astar: PlannerResult,
) -> list[dict]:

    return [
        {
            "Algorithm": greedy.algorithm,
            "Calories": greedy.total_calories,
            "Fatigue": greedy.total_fatigue,
            "Workout Days": greedy.total_workout_days(),
            "Rest Days": greedy.total_rest_days(),
            "Expanded Nodes": greedy.expanded_nodes,
            "Execution Time (s)": round(
                greedy.execution_time,
                5,
            ),
        },
        {
            "Algorithm": astar.algorithm,
            "Calories": astar.total_calories,
            "Fatigue": astar.total_fatigue,
            "Workout Days": astar.total_workout_days(),
            "Rest Days": astar.total_rest_days(),
            "Expanded Nodes": astar.expanded_nodes,
            "Execution Time (s)": round(
                astar.execution_time,
                5,
            ),
        },
    ]


def summary(result: PlannerResult) -> dict:

    return {
        "Algorithm": result.algorithm,
        "Total Calories": result.total_calories,
        "Total Fatigue": result.total_fatigue,
        "Workout Days": result.total_workout_days(),
        "Rest Days": result.total_rest_days(),
        "Expanded Nodes": result.expanded_nodes,
        "Execution Time": round(
            result.execution_time,
            5,
        ),
    }