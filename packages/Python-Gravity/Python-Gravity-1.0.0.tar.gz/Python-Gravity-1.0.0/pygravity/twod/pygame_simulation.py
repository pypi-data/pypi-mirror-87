from typing import Sequence

import pygame
from pygame import Rect, Surface
from pygame.constants import MOUSEBUTTONDOWN, QUIT

from pygravity import twod
from pygravity.twod import util

INT_LIMITS = 256 ** 4 // 2 - 1
GRAVITY_CONTAINER = twod.GravityContainer()


__all__ = ['Settings', 'Body', 'bodies', 'start_simulation', 'register_event_handler', 'visual_radius_from_radius', 'create_surface_from_capture']


class Settings:
    scale = 778125000
    time_scale = 1840000
    screen_size = (1280, 960)
    background_color = (0, 0, 0)
    focus = None
    event_handlers = {}


class Camera:
    position = twod.Vector2()
    scale = Settings.scale


class Body(util.Body):
    def __init__(self, position, mass, visual_color, visual_radius, has_caster=True, has_acceptor=True):
        super().__init__(GRAVITY_CONTAINER, position, mass, has_caster, has_acceptor)
        self.visual_color = visual_color
        self.visual_radius = visual_radius

    @classmethod
    def from_metadata(cls, body: util.BodyWithMetadata, *defaults):
        body = util.BodyWithMetadata.ensure_metadata(body, *defaults)
        return cls(
            body.body.position,
            body.body.mass,
            body.color,
            visual_radius_from_radius(body.radius),
            body.body.caster is not None,
            body.body.acceptor is not None
        )

    def update(self, time_passed):
        self.step(time_passed * Settings.time_scale)

    def render(self, surface: Surface):
        render_pos = self.get_render_position()
        if render_pos[0] < -INT_LIMITS or render_pos[0] > INT_LIMITS \
            or render_pos[1] < -INT_LIMITS or render_pos[1] > INT_LIMITS:
            return
        if not self.get_rect().colliderect(Rect((0, 0), Settings.screen_size)):
            return
        pygame.draw.circle(surface, self.visual_color, render_pos, self.get_radius())

    def get_radius(self):
        return int(self.visual_radius * Settings.scale / Camera.scale)

    def get_render_position(self):
        # render_pos = [c for c in self.position]
        # render_pos[0] = int(render_pos[0] + 640 * Camera.scale - Camera.position.x) // Camera.scale
        # render_pos[1] = int(480 - render_pos[1] * Camera.scale + Camera.position.y) // Camera.scale
        render_pos = list(self.position)
        # render_pos[0] //= Camera.scale
        render_pos[0] = (render_pos[0] - Camera.position.x) / Camera.scale + Settings.screen_size[0] / 2
        # render_pos[1] //= Camera.scale
        render_pos[1] = Settings.screen_size[1] / 2 - (render_pos[1] - Camera.position.y) / Camera.scale
        return [int(x) for x in render_pos]

    def get_rect(self):
        render_pos = self.get_render_position()
        return Rect(render_pos[0] - self.visual_radius,
                    render_pos[1] - self.visual_radius,
                    2 * self.visual_radius,
                    2 * self.visual_radius)


def register_event_handler(func, *events):
    for event in events:
        if event not in Settings.event_handlers:
            Settings.event_handlers[event] = []
        Settings.event_handlers[event].append(func)


bodies = []


def start_simulation():
    Camera.scale = Settings.scale

    pygame.init()
    screen = pygame.display.set_mode(Settings.screen_size)

    clock = pygame.time.Clock()
    while True:
        clock.tick(50)

        for handler in Settings.event_handlers.get(None, []):
            handler()

        for event in pygame.event.get():
            for handler in Settings.event_handlers.get(event.type, []):
                handler(event)
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    print('mouse click:', end=' ')
                    for body in bodies:
                        if body.get_rect().collidepoint(*event.pos):
                            print(body)
                            Settings.focus = body
                            break
                    else:
                        print('space')
                        Settings.focus = None
                        Camera.position.set_to(twod.Vector2())
                elif event.button == 4:
                    Camera.scale /= 1.5
                    print('zoom in:', Camera.scale)
                elif event.button == 5:
                    Camera.scale *= 1.5
                    print('zoom out:', Camera.scale)

        if Settings.focus is not None:
            Camera.position.set_to(Settings.focus.position)

        for body in reversed(bodies):
            body.update(0.02)

        screen.fill(Settings.background_color)

        for body in bodies:
            body.render(screen)

        pygame.display.update()


def visual_radius_from_radius(radius):
    return radius / Settings.scale


def create_surface_from_capture(capture_data: dict, line_thickness=1, render_planets_when: Sequence[int] = (0,)) -> Surface:
    result = Surface(Settings.screen_size)
    result.fill(Settings.background_color)

    bodies = {}
    lines = {}
    for (name, body_data) in capture_data['meta'].items():
        body = Body.__new__(Body)
        body.visual_color = body_data['color']
        body.visual_radius = visual_radius_from_radius(body_data['radius'])
        body.mass = body_data['mass']
        bodies[name] = body
        if line_thickness:
            lines[name] = []

    for (i, frame) in enumerate(capture_data['data']):
        render_planets = i in render_planets_when
        for (body_name, frame_data) in frame.items():
            body = bodies[body_name]
            body.position = frame_data['position']
            if render_planets:
                body.render(result)
            if line_thickness:
                lines[body_name].append(body.get_render_position())

    if line_thickness:
        for (body_name, line_set) in lines.items():
            body = bodies[body_name]
            pygame.draw.lines(result, body.visual_color, False, line_set, line_thickness)

    return result
