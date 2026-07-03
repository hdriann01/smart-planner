from dataclasses import dataclass, field
from copy import deepcopy

from models.activity import Activity


@dataclass
class State:
    """
    Merepresentasikan kondisi Smart Planner
    pada suatu titik dalam proses pencarian.
    """

    schedule: list[Activity | None] = field(
        default_factory=lambda: [None] * 7
    )

    last_activity: Activity | None = None

    day_index: int = 0

    total_calories: int = 0

    fatigue: int = 0

    completed: bool = False

    history: list[str] = field(default_factory=list)

    def add_activity(self, activity: Activity) -> None:
        """
        Menambahkan aktivitas ke hari saat ini.
        """

        if self.completed:
            raise ValueError("Schedule has already been completed.")

        self.schedule[self.day_index] = activity

        self.last_activity = activity

        self.total_calories += activity.calories

        self.fatigue += activity.fatigue

        self.history.append(activity.name)

    def next_day(self) -> None:
        """
        Berpindah ke hari berikutnya.
        """

        self.day_index += 1

        if self.day_index >= len(self.schedule):
            self.completed = True

    def advance(self, activity: Activity) -> None:
        """
        Menjalankan satu langkah simulasi.
        """

        self.add_activity(activity)

        self.next_day()

    def clone(self):
        """
        Membuat salinan State.
        """

        return deepcopy(self)

    def current_day(self) -> int:
        return self.day_index + 1

    def remaining_days(self) -> int:
        return len(self.schedule) - self.day_index

    def is_goal(self) -> bool:
        return self.completed

    def reset(self):
        """
        Mengembalikan State ke kondisi awal.
        """

        self.schedule = [None] * 7

        self.last_activity = None

        self.day_index = 0

        self.total_calories = 0

        self.fatigue = 0

        self.completed = False

        self.history.clear()

    def get_schedule(self):
        return self.schedule

    def to_dict(self):

        return {

            "day": self.day_index,

            "calories": self.total_calories,

            "fatigue": self.fatigue,

            "completed": self.completed,

            "last_activity": (
                self.last_activity.name
                if self.last_activity
                else None
            ),

            "history": self.history,
        }

    def __str__(self):

        schedule = [
            activity.name if activity else "-"
            for activity in self.schedule
        ]

        last = (
            self.last_activity.name
            if self.last_activity
            else "-"
        )

        return (
            f"Day={self.day_index + 1}, "
            f"Calories={self.total_calories}, "
            f"Fatigue={self.fatigue}, "
            f"Last={last}, "
            f"Schedule={schedule}"
        )