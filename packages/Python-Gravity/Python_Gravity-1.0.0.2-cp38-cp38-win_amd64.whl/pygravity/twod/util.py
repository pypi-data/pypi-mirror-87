from __future__ import annotations

from pygravity.twod.physics import PhysicsManager
from pygravity.twod.gravity import GravityAcceptor, GravityCaster, GravityContainer
from pygravity.twod.vector import Vector2
from typing import Dict, Generator, Iterable, List, Optional, Tuple, TypedDict, Union


__all__ = ['Body', 'BodyWithMetadata', 'capture_simulation']


class Body:
    """Body(container: GravityContainer, position: Vector2, mass: float, has_caster: bool = True, has_acceptor: bool = True)

High level class representing everything gravity related about a spatial body

Attributes
----------
position : Vector2
    The current position of the body
mass : float
    The body's mass
physics : PhysicsManager
    The PhysicsManager responsible for managing the body's velocity
caster : GravityCaster | None
    The body's GravityCaster, or None if the body doesn't pull on other bodies
acceptor : GravityAcceptor | None
    The body's GravityAcceptor, or None if the body doesn't get pulled on by other bodies"""

    position: Vector2
    mass: float
    physics: PhysicsManager
    caster: Optional[GravityCaster]
    acceptor: Optional[GravityAcceptor]

    def __init__(self,
                 container: GravityContainer,
                 position: Vector2,
                 mass: float,
                 has_caster: bool = True,
                 has_acceptor: bool = True):
        self.position = position
        self.mass = mass
        self.physics = PhysicsManager(position)
        if has_caster:
            self.caster = GravityCaster(position, mass)
            container.add_caster(self.caster)
        else: self.caster = None
        if has_acceptor:
            self.acceptor = GravityAcceptor(position, container, self.physics)
        else: self.acceptor = None

    def step(self, time_passed: float) -> Tuple[Vector2, Vector2]:
        """Calculates the change in velocity and movement of this body
Use seconds for time_passed

Returns
-------
Change in velocity (Vector2; None if this body does not have an acceptor)
Movement (Change in position) (Vector2)"""
        res = None
        if self.acceptor is not None:
            res = self.acceptor.calculate(time_passed)
        return res, self.physics.calculate(time_passed)


class BodyWithMetadata:
    """BodyWithMetadata(body: Body, name: str = 'body', radius: float = 0, color: Tuple[float, float, float] = (0, 0, 0))

Body wrapper that contains various metadata about the body

Attributes
----------
body : Body
    The actual body
name : str
    The body's name (e.g. Saturn)
radius : float
    The body's radius
color : Tuple[float, float, float]
    The color to use for the body in rendering tasks"""

    body: Body
    name: str
    radius: float
    color: Tuple[float, float, float]

    def __init__(self, body: Body, name: str = 'body', radius: float = 0, color: Tuple[float, float, float] = (0, 0, 0)):
        self.body = body
        self.name = name
        self.radius = radius
        self.color = color

    @staticmethod
    def ensure_metadata(body: PotentialBody, *defaults) -> BodyWithMetadata:
        """Ensures that type(body) == BodyWithMetadata

Specify additional arguments to set the default metadata if the body is just a plain Body"""
        if isinstance(body, BodyWithMetadata):
            return body
        return BodyWithMetadata(body, *defaults)

    @staticmethod
    def iter_ensure_metadata(it: Iterable[PotentialBody],
                             name_format: str = 'body%03i',
                             *defaults) -> Generator[BodyWithMetadata]:
        """Generator over it that calls BodyWithMetadata.ensure_metadata

name_format is a percent format string that indicates the default name for a body
    This replaces the first argument for defaults"""
        yield from (
            BodyWithMetadata.ensure_metadata(body, name_format % i, *defaults)
            for (i, body)
            in enumerate(it)
        )

    @staticmethod
    def strip_metadata(body: PotentialBody) -> Body:
        """Opposite of BodyWithMetadata.ensure_metadata
Returns a Body regardless of whether body was a BodyWithMetadata or Body"""
        return BodyWithMetadata.ensure_metadata(body).body

    @staticmethod
    def iter_strip_metadata(it: Iterable[PotentialBody]) -> Generator[Body]:
        """Generator over it that calls BodyWithMetadata.strip_metadata"""
        yield from (
            BodyWithMetadata.strip_metadata(body)
            for body
            in it
        )


PotentialBody = Union[Body, BodyWithMetadata]

SimulationMetadata = TypedDict('SimulationMetadata',
    mass = float,
    radius = float,
    color = Tuple[float, float, float]
)

SimulationFrameBody = TypedDict('SimulationFrameBody',
    position = Tuple[float, float],
    velocity = Tuple[float, float]
)

SimulationFrame = Dict[str, SimulationFrameBody]

SimulationResult = TypedDict('SimulationResult',
    meta = Dict[str, SimulationMetadata],
    data = List[SimulationFrame]
)


def capture_simulation(
        bodies: List[PotentialBody],
        focus: Optional[PotentialBody] = None,
        step_distance=36800,
        step_count=5000) -> SimulationResult:
    result = {}
    focus = BodyWithMetadata.strip_metadata(focus)

    bodies = list(BodyWithMetadata.iter_ensure_metadata(bodies))
    metadata = {}
    result['meta'] = metadata
    for body in bodies:
        body_meta_dict = {}
        result['meta'][body.name] = body_meta_dict
        body_meta_dict['mass'] = body.body.mass
        body_meta_dict['radius'] = body.radius
        body_meta_dict['color'] = body.color

    bodies.reverse()
    data = []
    result['data'] = data
    def report():
        frame = {}
        for body in bodies:
            body_frame = {}
            if focus is None:
                use_position = body.body.position
            else:
                use_position = body.body.position - focus.position
            body_frame['position'] = tuple(use_position)
            body_frame['velocity'] = tuple(body.body.physics.velocity)
            frame[body.name] = body_frame
        data.append(frame)
    report()
    for i in range(step_count):
        for body in bodies:
            body.body.step(step_distance)
        report()

    return result


def system_from_capture(capture_data: SimulationResult,
                        container: Optional[GravityContainer] = None, *,
                        selected_frame: int = -1,
                        create_casters: bool = True,
                        create_acceptors: bool = True) -> Dict[str, BodyWithMetadata]:
    if container is None:
        container = GravityContainer()
    result = {}

    metadata = capture_data['meta']
    frame = capture_data['data'][selected_frame]
    for (name, body_meta) in metadata.items():
        body_frame = frame[name]
        base_body = Body(container, Vector2(*body_frame['position']), body_meta['mass'], create_casters, create_acceptors)
        result[name] = BodyWithMetadata(base_body, name, body_meta['radius'], body_meta['color'])
    
    return result
