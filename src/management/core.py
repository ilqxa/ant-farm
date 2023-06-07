from pydantic import BaseModel
from src.agents.base import Agent

from src.buildings.objects.base import Building
from src.fractions.base import Fraction
from src.specialties.base import Specialty


class GlobalEnvironment(BaseModel):
    agents: set[Agent] = set()
    buildings: set[Building] = set()
    fractions: set[Fraction] = set()
    specialties: set[Specialty] = set()