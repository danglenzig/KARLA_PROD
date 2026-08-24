# src/examples_and_templates/format_validation.py

from typing import Annotated
from pydantic import (
    BaseModel,
    AfterValidator,
    ValidationError
)

def positive_integer_validator(val: int):
    """
    This is a validation rule. It validates that the int is >= 0
    """
    if val < 0:
        raise ValueError("Must be integer greater than or equal to zero.")
    return val

# Use AfterValidator with the validation rule to perform the custom validation
PositiveInteger = Annotated[int, AfterValidator(positive_integer_validator)]

# Use the special Annoated type for age instead of int
class SimpleUser(BaseModel):
    user_name: str
    user_age: PositiveInteger


def main():
    try:
        user_brad = SimpleUser(
            user_name = "Brad Neal",
            user_age  = 52
        )
    except ValidationError as e:
        print(e)

    try:
        invalid_user = SimpleUser(
            user_name = "Joe Invalid",
            user_age  = -10
        )
    except ValidationError as e:
        print(e)

    # Output:
    # 1 validation error for SimpleUser
    # user_age
    # Value error, Must be integer greater than zero. [type=value_error, input_value=-10, input_type=int]
    #     For further information visit https://errors.pydantic.dev/2.13/v/value_error

if __name__ == "__main__":
    main()