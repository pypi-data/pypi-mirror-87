"""Common math functions for pygravity

Constants
---------
GRAVITATIONAL_CONSTANT

Functions
---------
acceleration_due_to_gravity(attractor_mass: float, distance: float) -> float
"""


cdef double gravitational_constant = 6.67430e-11
GRAVITATIONAL_CONSTANT = gravitational_constant


cdef inline double acceleration_due_to_gravity_squared(double mass, double distance) nogil:
    return (gravitational_constant * mass) / distance


def acceleration_due_to_gravity(double attractor_mass, double distance):
    """acceleration_due_to_gravity(attractor_mass: float, distance: float) -> float

Calculate the speed that a body `distance` meters from a body with a mass of
`attractor_mass` would fall toward that body."""
    return acceleration_due_to_gravity_squared(attractor_mass, distance ** 2)


__all__ = ['acceleration_due_to_gravity', 'GRAVITATIONAL_CONSTANT']
