from __future__ import annotations

from typing import List

from pygravity.twod.physics import PhysicsManager
from pygravity.twod.vector import Vector2


class GravityContainer:
    casters: List[GravityCaster]

    def __init__(*casters: GravityCaster): ...
    def add_caster(self, caster: GravityCaster) -> None: ...
    def add_casters(self, *casters: GravityCaster) -> None: ...
    def remove_caster(self, caster: GravityCaster) -> GravityCaster: ...


class GravityCaster:
    position: Vector2
    mass: float

    def __init__(position: Vector2, mass: float): ...


class GravityAcceptor:
    position: Vector2
    container: GravityContainer
    physics_manager: PhysicsManager

    def __init__(position: Vector2, container: GravityContainer, physics_manager: PhysicsManager): ...
    def calculate(self, time_passed: float) -> Vector2: ...
