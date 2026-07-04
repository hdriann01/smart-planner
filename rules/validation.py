from dataclasses import dataclass

from models.enums import ValidationResult


@dataclass(frozen=True)
class ValidationResponse:

    is_valid: bool

    result: ValidationResult

    message: str = ""

    @classmethod
    def valid(cls, message: str = "Validation passed."):
        return cls(
            is_valid=True,
            result=ValidationResult.VALID,
            message=message,
        )

    @classmethod
    def invalid(cls, result: ValidationResult, message: str):
        return cls(
            is_valid=False,
            result=result,
            message=message,
        )