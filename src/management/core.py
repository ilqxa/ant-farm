from pydantic import BaseModel, PrivateAttr

from src.agents.base import Agent
from src.buildings.objects.base import Building
from src.fractions.base import Fraction
from src.management.exceptions import *
from src.roles.base import Role


class GlobalEnvironment(BaseModel):
    _agents: set[Agent] = PrivateAttr(default_factory=set)
    _roles: set[Role] = PrivateAttr(default_factory=set)
    _buildings: set[Building] = PrivateAttr(default_factory=set)
    _fractions: set[Fraction] = PrivateAttr(default_factory=set)
    
    _roles_by_agents: dict[Agent, set[Role]] = PrivateAttr(default_factory=dict)
    _agents_by_roles: dict[Role, Agent | None] = PrivateAttr(default_factory=dict)
    
    _buildings_by_roles: dict[Role, Building | None] = PrivateAttr(default_factory=dict)
    _roles_by_buildings: dict[Building, set[Role]] = PrivateAttr(default_factory=dict)
    
    _fractions_by_roles: dict[Role, Fraction] = PrivateAttr(default_factory=dict)
    _roles_by_fractions: dict[Fraction, set[Role]] = PrivateAttr(default_factory=dict)
    
    _fractions_by_buildings: dict[Building, Fraction] = PrivateAttr(default_factory=dict)
    _buildings_by_fractions: dict[Fraction, set[Building]] = PrivateAttr(default_factory=dict)
    
    def add_agent(self, agent: Agent) -> None:
        self._agents.add(agent)
        self._roles_by_agents[agent] = set()
        
    def remove_agent(self, agent: Agent) -> None:
        if agent not in self._agents: raise AgentIsAbsentInModel
        
        self._agents.remove(agent)
        roles = self._roles_by_agents.pop(agent)
        for r in roles:
            if self._agents_by_roles[r] is None: raise RoleIsEmpty
            self._agents_by_roles[r] = None
            
    def add_role(self, role: Role) -> None:
        self._roles.add(role)
        self._agents_by_roles[role] = None
        
    def remove_role(self, role: Role) -> None:
        if role not in self._roles: raise RoleIsAbsentInModel
        
        self._roles.remove(role)
        if agent := self._agents_by_roles.pop(role):
            if role not in self._roles_by_agents[agent]: raise AgentDoNotHaveRole
            self._roles_by_agents[agent].remove(role)
    
    def add_building(self, building: Building) -> None:
        self._buildings.add(building)
        
    def remove_building(self, building: Building) -> None:
        if building not in self._buildings: raise BuildingIsAbsentInModel
        
        self._buildings.remove(building)
        
    def add_fraction(self, fraction: Fraction) -> None:
        self._fractions.add(fraction)
        
    def remove_fraction(self, fraction: Fraction) -> None:
        if fraction not in self._fractions: raise FractionIsAbsentInModel
        
        self._fractions.remove(fraction)
        
    def check_relation_agent_to_role(self, agent: Agent, role: Role) -> bool:
        if agent not in self._agents: raise AgentIsAbsentInModel
        if role not in self._roles: raise RoleIsAbsentInModel
        
        cond1 = role in self._roles_by_agents[agent]
        cond2 = agent is self._agents_by_roles[role]
        
        if cond1 and cond2:
            return True
        elif not cond1 and not cond2:
            return False
        else:
            raise BrokenRelation
        
    def connect_agent_to_role(self, agent: Agent, role: Role) -> None:
        if agent not in self._agents: raise AgentIsAbsentInModel
        if role not in self._roles: raise RoleIsAbsentInModel
        
        if self._agents_by_roles[role]: raise RoleIsBusy
        
        self._roles_by_agents[agent].add(role)
        self._agents_by_roles[role] = agent
        
    def break_agent_to_role(self, agent: Agent, role: Role) -> None:
        if agent not in self._agents: raise AgentIsAbsentInModel
        if role not in self._roles: raise RoleIsAbsentInModel
        
        if self._agents_by_roles[role] is not Agent: raise AgentDoNotHaveRole
        if role not in self._roles_by_agents[agent]: raise AgentDoNotHaveRole
        
        self._agents_by_roles[role] = None
        self._roles_by_agents[agent].remove(role)
