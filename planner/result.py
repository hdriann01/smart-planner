from dataclasses import dataclass, field

from models.activity import Activity


@dataclass
class PlannerResult:
    """
    Menyimpan hasil akhir proses penyusunan
    jadwal olahraga mingguan.
    """

    schedule: list[Activity | None]

    total_calories: int

    total_fatigue: int

    algorithm: str

    success: bool

    execution_time: float = 0.0

    expanded_nodes: int = 0

    message: str = ""

    def total_workout_days(self) -> int:
        """
        Menghitung jumlah hari latihan
        (tidak termasuk Rest).
        """

        return sum(
            1
            for activity in self.schedule
            if activity is not None and not activity.is_rest()
        )

    def total_rest_days(self) -> int:
        """
        Menghitung jumlah hari Rest.
        """

        return sum(
            1
            for activity in self.schedule
            if activity is not None and activity.is_rest()
        )

    def schedule_names(self) -> list[str]:
        """
        Mengembalikan daftar nama aktivitas.
        """

        return [
            activity.name if activity else "-"
            for activity in self.schedule
        ]

    def to_dict(self) -> dict:
        """
        Mengubah hasil menjadi dictionary.
        """

        return {
            "algorithm": self.algorithm,
            "success": self.success,
            "message": self.message,
            "execution_time": self.execution_time,
            "expanded_nodes": self.expanded_nodes,
            "total_calories": self.total_calories,
            "total_fatigue": self.total_fatigue,
            "schedule": self.schedule_names(),
        }

    def __str__(self):

        return (
            f"PlannerResult("
            f"algorithm={self.algorithm}, "
            f"success={self.success}, "
            f"calories={self.total_calories}, "
            f"fatigue={self.total_fatigue}, "
            f"nodes={self.expanded_nodes}, "
            f"time={self.execution_time:.4f}s)"
        )