from dataclasses import dataclass, field

from models.enums import ActivityLevel


@dataclass
class User:

    id: int
    name: str
    age: int
    weight: float
    activity_level: ActivityLevel
    target_calories: int
    max_duration: int

    fatigue_threshold: int = field(init=False)

    def __post_init__(self):

        self.validate()
        self.fatigue_threshold = self.calculate_fatigue_threshold()

    def validate(self) -> None:

        if self.age <= 0:
            raise ValueError("Age must be greater than 0.")

        if self.weight <= 0:
            raise ValueError("Weight must be greater than 0.")

        if self.height <= 0:
            raise ValueError("Height must be greater than 0.")

        if self.target_calories <= 0:
            raise ValueError("Target calories must be greater than 0.")

        if self.max_duration <= 0:
            raise ValueError("Maximum duration must be greater than 0.")

    def calculate_bmi(self) -> float:

        height_meter = self.height / 100

        return round(self.weight / (height_meter ** 2), 2)

    def bmi_category(self) -> str:

        bmi = self.calculate_bmi()

        if bmi < 18.5:
            return "Underweight"

        elif bmi < 25:
            return "Normal"

        elif bmi < 30:
            return "Overweight"

        return "Obese"

    def calculate_fatigue_threshold(self) -> int:

        mapping = {
            ActivityLevel.SEDENTARY: 40,
            ActivityLevel.LIGHTLY_ACTIVE: 60,
            ActivityLevel.VERY_ACTIVE: 80,
        }

        return mapping[self.activity_level]

    def is_beginner(self) -> bool:

        return self.activity_level == ActivityLevel.SEDENTARY

    def to_dict(self) -> dict:

        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "height": self.height,
            "activity_level": self.activity_level.name,
            "target_calories": self.target_calories,
            "max_duration": self.max_duration,
            "fatigue_threshold": self.fatigue_threshold,
            "bmi": self.calculate_bmi(),
            "bmi_category": self.bmi_category(),
        }

    def __str__(self) -> str:
        return (
            f"{self.name} | "
            f"{self.age} tahun | "
            f"{self.weight} kg | "
            f"{self.height} cm | "
            f"{self.activity_level.name}"
        )