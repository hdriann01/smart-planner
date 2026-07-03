from dataclasses import dataclass
from models.enums import Intensity


@dataclass(frozen=True)
class Activity:
    """
    Merepresentasikan satu jenis aktivitas olahraga
    yang menjadi bagian dari Knowledge Base sistem.
    """

    id: int
    name: str
    duration: int              
    calories: int             
    fatigue: int              
    intensity: Intensity
    recovery_required: bool
    description: str

    def is_rest(self) -> bool:
        """
        Mengembalikan True jika aktivitas adalah Rest.
        """
        return self.intensity == Intensity.REST

    def is_light(self) -> bool:
        """
        Mengecek apakah aktivitas termasuk intensitas ringan.
        """
        return self.intensity == Intensity.LIGHT

    def is_medium(self) -> bool:
        """
        Mengecek apakah aktivitas termasuk intensitas sedang.
        """
        return self.intensity == Intensity.MEDIUM

    def is_heavy(self) -> bool:
        """
        Mengecek apakah aktivitas termasuk intensitas berat.
        """
        return self.intensity == Intensity.HEAVY

    def requires_recovery(self) -> bool:
        """
        Mengembalikan True jika aktivitas
        memerlukan hari recovery.
        """
        return self.recovery_required

    def to_dict(self) -> dict:
        """
        Mengubah objek Activity menjadi dictionary.
        Berguna untuk Streamlit atau penyimpanan data.
        """
        return {
            "id": self.id,
            "name": self.name,
            "duration": self.duration,
            "calories": self.calories,
            "fatigue": self.fatigue,
            "intensity": self.intensity.name,
            "recovery_required": self.recovery_required,
            "description": self.description,
        }

    def __str__(self) -> str:
        return (
            f"{self.name} "
            f"({self.duration} menit | "
            f"{self.calories} kcal | "
            f"Fatigue {self.fatigue})"
        )