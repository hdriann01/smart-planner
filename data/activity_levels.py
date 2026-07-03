from models.enums import ActivityLevel
from data.constants import (
    SEDENTARY_FATIGUE_THRESHOLD,
    LIGHTLY_ACTIVE_FATIGUE_THRESHOLD,
    VERY_ACTIVE_FATIGUE_THRESHOLD,
)

ACTIVITY_LEVELS = {
    ActivityLevel.SEDENTARY: {
        "fatigue_threshold": SEDENTARY_FATIGUE_THRESHOLD,
        "description": "Little or no regular physical activity."
    },

    ActivityLevel.LIGHTLY_ACTIVE: {
        "fatigue_threshold": LIGHTLY_ACTIVE_FATIGUE_THRESHOLD,
        "description": "Exercise 1-3 days per week."
    },

    ActivityLevel.VERY_ACTIVE: {
        "fatigue_threshold": VERY_ACTIVE_FATIGUE_THRESHOLD,
        "description": "Exercise almost every day."
    }
}