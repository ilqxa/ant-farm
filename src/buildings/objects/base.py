from typing import Type, ClassVar
from pydantic import BaseModel

from src.fractions.base import Fraction


class Building(BaseModel):
    required_owner: ClassVar[Type[Fraction]]
    required_max_in_cell: ClassVar[int | None]
    required_max_in_town: ClassVar[int | None]
    required_max_in_fraction: ClassVar[int | None]