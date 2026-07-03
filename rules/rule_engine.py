from collections.abc import Callable

from models.activity import Activity
from models.state import State
from models.user import User

from rules.validation import ValidationResponse

from rules.rules import (
    rule_fatigue_threshold,
    rule_recovery,
    rule_consecutive_workout,
    rule_fatigue_limit,
)


Rule = Callable[
    [User, State, Activity],
    ValidationResponse
]


class RuleEngine:

    def __init__(self):

        self.rules: list[Rule] = [

            rule_fatigue_threshold,

            rule_recovery,

            rule_consecutive_workout,

            rule_fatigue_limit,

        ]

    def validate(
        self,
        user: User,
        state: State,
        activity: Activity,
    ) -> ValidationResponse:

        for rule in self.rules:

            response = rule(
                user,
                state,
                activity,
            )

            if not response.is_valid:
                return response

        return ValidationResponse.valid()

    def validate_all(
        self,
        user: User,
        state: State,
        activity: Activity,
    ) -> list[ValidationResponse]:

        return [
            rule(user, state, activity)
            for rule in self.rules
        ]