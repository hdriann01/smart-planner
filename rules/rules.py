from models.user import User
from models.state import State
from models.activity import Activity
from models.enums import ValidationResult

from rules.validation import ValidationResponse


def rule_fatigue_threshold(
    user: User,
    state: State,
    activity: Activity,
) -> ValidationResponse:

    if user.fatigue_threshold <= 0:
        return ValidationResponse.invalid(
            ValidationResult.FATIGUE_LIMIT,
            "Invalid fatigue threshold."
        )

    return ValidationResponse.valid()


def rule_recovery(
    user: User,
    state: State,
    activity: Activity,
) -> ValidationResponse:

    yesterday = state.last_activity

    if yesterday is None:
        return ValidationResponse.valid()

    if yesterday.requires_recovery() and not activity.is_rest():

        return ValidationResponse.invalid(
            ValidationResult.RECOVERY_REQUIRED,
            (
                f"Recovery required after "
                f"{yesterday.name}. Today's activity "
                f"must be Rest."
            )
        )

    return ValidationResponse.valid()


def rule_consecutive_workout(
    user: User,
    state: State,
    activity: Activity,
) -> ValidationResponse:

    if state.day_index < 3:
        return ValidationResponse.valid()

    last_three = state.schedule[
        state.day_index - 3:state.day_index
    ]

    if any(day is None for day in last_three):
        return ValidationResponse.valid()

    trained_three_days = all(
        not day.is_rest()
        for day in last_three
    )

    if trained_three_days and not activity.is_rest():

        return ValidationResponse.invalid(
            ValidationResult.OVERTRAINING,
            (
                "Maximum of three consecutive "
                "workout days exceeded."
            )
        )

    return ValidationResponse.valid()


def rule_fatigue_limit(
    user: User,
    state: State,
    activity: Activity,
) -> ValidationResponse:

    predicted_fatigue = (
        state.fatigue +
        activity.fatigue
    )

    if predicted_fatigue > user.fatigue_threshold:

        return ValidationResponse.invalid(
            ValidationResult.FATIGUE_LIMIT,
            (
                f"Predicted fatigue "
                f"({predicted_fatigue}) "
                f"exceeds threshold "
                f"({user.fatigue_threshold})."
            )
        )

    return ValidationResponse.valid()


def rule_duration_limit(
    user: User,
    state: State,
    activity: Activity,
) -> ValidationResponse:

    if activity.duration > user.max_duration:

        return ValidationResponse.invalid(
            ValidationResult.DURATION_EXCEEDED,
            (
                f"{activity.name} requires "
                f"{activity.duration} minutes, "
                f"but user limit is "
                f"{user.max_duration} minutes."
            )
        )

    return ValidationResponse.valid()


RULES = [

    rule_fatigue_threshold,

    rule_recovery,

    rule_consecutive_workout,

    rule_fatigue_limit,

    rule_duration_limit,

]