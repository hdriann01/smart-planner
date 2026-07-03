from enum import Enum, auto


class Intensity(Enum):
    REST = auto()
    LIGHT = auto()
    MEDIUM = auto()
    HEAVY = auto()


class ActivityLevel(Enum):
    SEDENTARY = auto()
    LIGHTLY_ACTIVE = auto()
    VERY_ACTIVE = auto()


class SearchAlgorithm(Enum):
    GREEDY = auto()
    ASTAR = auto()


class GoalStatus(Enum):
    IN_PROGRESS = auto()
    SUCCESS = auto()
    FAILED = auto()


class ValidationResult(Enum):
    VALID = auto()
    RECOVERY_REQUIRED = auto()
    OVERTRAINING = auto()
    FATIGUE_LIMIT = auto()
    DURATION_EXCEEDED = auto()


class Day(Enum):
    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()