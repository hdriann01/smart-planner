from models.activity import Activity
from models.enums import Intensity

ACTIVITIES = [

    Activity(
        id=1,
        name="Rest",
        duration=0,
        calories=0,
        fatigue=-30,
        intensity=Intensity.REST,
        recovery_required=False,
        description="Recovery day to reduce accumulated fatigue."
    ),

    Activity(
        id=2,
        name="Walking",
        duration=30,
        calories=120,
        fatigue=5,
        intensity=Intensity.LIGHT,
        recovery_required=False,
        description="Light walking exercise suitable for beginners."
    ),

    Activity(
        id=3,
        name="Light Run",
        duration=30,
        calories=250,
        fatigue=15,
        intensity=Intensity.LIGHT,
        recovery_required=False,
        description="Easy jogging with light intensity."
    ),

    Activity(
        id=4,
        name="Cycling",
        duration=45,
        calories=350,
        fatigue=20,
        intensity=Intensity.MEDIUM,
        recovery_required=False,
        description="Moderate intensity cycling."
    ),

    Activity(
        id=5,
        name="Interval",
        duration=30,
        calories=450,
        fatigue=35,
        intensity=Intensity.HEAVY,
        recovery_required=True,
        description="High Intensity Interval Training (HIIT)."
    ),

    Activity(
        id=6,
        name="Long Run",
        duration=60,
        calories=700,
        fatigue=50,
        intensity=Intensity.HEAVY,
        recovery_required=True,
        description="Long distance running with high intensity."
    ),

]

ACTIVITY_BY_ID = {
    activity.id: activity
    for activity in ACTIVITIES
}

ACTIVITY_BY_NAME = {
    activity.name: activity
    for activity in ACTIVITIES
}

REST_ACTIVITY = ACTIVITY_BY_NAME["Rest"]

LIGHT_ACTIVITIES = [
    activity
    for activity in ACTIVITIES
    if activity.is_light()
]

MEDIUM_ACTIVITIES = [
    activity
    for activity in ACTIVITIES
    if activity.is_medium()
]

HEAVY_ACTIVITIES = [
    activity
    for activity in ACTIVITIES
    if activity.is_heavy()
]

RECOVERY_REQUIRED_ACTIVITIES = [
    activity
    for activity in ACTIVITIES
    if activity.requires_recovery()
]

def get_activity_by_id(activity_id: int) -> Activity:
    return ACTIVITY_BY_ID[activity_id]


def get_activity_by_name(name: str) -> Activity:
    return ACTIVITY_BY_NAME[name]


def get_all_activities() -> list[Activity]:
    return ACTIVITIES.copy()


def get_light_activities() -> list[Activity]:
    return LIGHT_ACTIVITIES.copy()


def get_medium_activities() -> list[Activity]:
    return MEDIUM_ACTIVITIES.copy()


def get_heavy_activities() -> list[Activity]:
    return HEAVY_ACTIVITIES.copy()


def get_recovery_required_activities() -> list[Activity]:
    return RECOVERY_REQUIRED_ACTIVITIES.copy()