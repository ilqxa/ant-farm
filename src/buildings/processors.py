from typing import Type
from blocks.types.base import Processor
from src.buildings.objects.base import Building

from src.management.core import GlobalEnvironment
from src.buildings.actions import Construction, Demolition


eventTypes = (
    Construction |
    Demolition
)


class BuildingsController(Processor):
    def __init__(self, ge: GlobalEnvironment) -> None:
        self.ge = ge
        
    def __call__(self, event: eventTypes) -> None:
        if isinstance(event, Construction):
            is_available = self.construction_availability_check(event)
            if is_available and event.to_execute:
                self.construct_new_building(event.blueprint)
        elif isinstance(event, Demolition):
            is_available = self.demolition_availability_check(event)
            if is_available and event.to_execute:
                self.demolish_building(event.building)
        
    def construction_availability_check(self, event: Construction) -> bool:
        return True
        
    def construct_new_building(self, blueprint: Type[Building]) -> None:
        self.ge.add_building(blueprint())
        
    def demolition_availability_check(self, event: Demolition) -> bool:
        return True
        
    def demolish_building(self, building: Building) -> None:
        self.ge.remove_building(building)