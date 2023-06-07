from typing import ClassVar, Type

from pydantic import BaseModel

from src.buildings.objects.base import Building
from src.fractions.base import Fraction


class Specialty(BaseModel):
    required_employer: ClassVar[Type[Fraction]]
    required_workplace: ClassVar[Type[Building] | None]
    required_max_in_fraction: ClassVar[int | None]
    required_max_in_workplace: ClassVar[int | None]
    
    current_employer: Fraction
    current_workplace: Building | None