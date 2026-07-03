import plotly.graph_objects as go

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


def calories_chart(result: PlannerResult):

    calories = [
        activity.calories if activity else 0
        for activity in result.schedule
    ]

    fig = go.Figure()

    fig.add_bar(
        x=DAY_NAMES,
        y=calories,
        name="Calories",
    )

    fig.update_layout(
        title="Daily Calories Burned",
        xaxis_title="Day",
        yaxis_title="Calories (kcal)",
        template="plotly_white",
    )

    return fig


def fatigue_chart(result: PlannerResult):

    fatigue = [
        activity.fatigue if activity else 0
        for activity in result.schedule
    ]

    fig = go.Figure()

    fig.add_bar(
        x=DAY_NAMES,
        y=fatigue,
        name="Fatigue",
    )

    fig.update_layout(
        title="Daily Fatigue",
        xaxis_title="Day",
        yaxis_title="Fatigue",
        template="plotly_white",
    )

    return fig


def workout_pie_chart(result: PlannerResult):

    fig = go.Figure()

    fig.add_pie(

        labels=[
            "Workout",
            "Rest",
        ],

        values=[
            result.total_workout_days(),
            result.total_rest_days(),
        ],

        hole=0.4,
    )

    fig.update_layout(
        title="Workout vs Rest Days"
    )

    return fig


def comparison_chart(
    greedy: PlannerResult,
    astar: PlannerResult,
):

    metrics = [
        "Calories",
        "Fatigue",
        "Expanded Nodes",
    ]

    greedy_values = [
        greedy.total_calories,
        greedy.total_fatigue,
        greedy.expanded_nodes,
    ]

    astar_values = [
        astar.total_calories,
        astar.total_fatigue,
        astar.expanded_nodes,
    ]

    fig = go.Figure()

    fig.add_bar(
        name="Greedy",
        x=metrics,
        y=greedy_values,
    )

    fig.add_bar(
        name="A*",
        x=metrics,
        y=astar_values,
    )

    fig.update_layout(

        title="Greedy vs A* Comparison",

        barmode="group",

        template="plotly_white",

        yaxis_title="Value",
    )

    return fig


def execution_time_chart(
    greedy: PlannerResult,
    astar: PlannerResult,
):

    fig = go.Figure()

    fig.add_bar(

        x=[
            "Greedy",
            "A*",
        ],

        y=[
            greedy.execution_time,
            astar.execution_time,
        ],

        name="Execution Time",
    )

    fig.update_layout(

        title="Execution Time Comparison",

        xaxis_title="Algorithm",

        yaxis_title="Seconds",

        template="plotly_white",
    )

    return fig


def fatigue_progress_chart(result: PlannerResult):

    cumulative = []

    total = 0

    for activity in result.schedule:

        if activity:

            total += activity.fatigue

        cumulative.append(total)

    fig = go.Figure()

    fig.add_scatter(

        x=DAY_NAMES,

        y=cumulative,

        mode="lines+markers",

        name="Fatigue",
    )

    fig.update_layout(

        title="Cumulative Fatigue",

        xaxis_title="Day",

        yaxis_title="Fatigue",

        template="plotly_white",
    )

    return fig