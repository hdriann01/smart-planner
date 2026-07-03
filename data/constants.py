"""
Global constants for Smart Planner System.
"""

# ==========================================================
# GENERAL CONFIGURATION
# ==========================================================

DAYS_PER_WEEK = 7

DEFAULT_START_DAY = 0

# ==========================================================
# FATIGUE THRESHOLD
# ==========================================================

SEDENTARY_FATIGUE_THRESHOLD = 40

LIGHTLY_ACTIVE_FATIGUE_THRESHOLD = 60

VERY_ACTIVE_FATIGUE_THRESHOLD = 80

# ==========================================================
# RECOVERY
# ==========================================================

RECOVERY_FATIGUE_REDUCTION = 30

MAX_CONSECUTIVE_WORKOUT = 3

# ==========================================================
# DEFAULT TARGETS
# ==========================================================

DEFAULT_TARGET_CALORIES = 2000

DEFAULT_MAX_DURATION = 60

# ==========================================================
# SEARCH CONFIGURATION
# ==========================================================

GREEDY = "GREEDY"

ASTAR = "ASTAR"