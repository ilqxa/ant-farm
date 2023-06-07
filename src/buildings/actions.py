from abc import ABC
from typing import Type
from pydantic import BaseModel, Field
from src.agents.base import Agent

from src.buildings.objects.base import Building


class BuildingAction(BaseModel, ABC):
    initiator: Agent = Field(description='The agent who initiate the query')
    to_execute: bool = Field(description='If false, availability check only')


class Construction(BuildingAction):
    blueprint: Type[Building]
    
    
class Demolition(BuildingAction):
    building: Building