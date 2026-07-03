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
    """
    Forward Chaining Rule Engine.

    Menjalankan seluruh rule secara berurutan.
    """

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
        """
        Menjalankan seluruh rule.

        Berhenti pada rule pertama yang gagal.
        """

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
        """
        Menjalankan seluruh rule tanpa berhenti.
        Berguna untuk debugging dan testing.
        """

        return [
            rule(user, state, activity)
            for rule in self.rules
        ]