from dataclasses import dataclass
import numpy as np


@dataclass
class Particle:
    q: float
    m: float


class Field:
    def E(self, t, x):
        return np.zeros(3)

    def B(self, t, x):
        return np.zeros(3)


def lorentz_force(particle: Particle, v, E, B):
    v = np.asarray(v, float)
    E = np.asarray(E, float)
    B = np.asarray(B, float)
    return particle.q * (E + np.cross(v, B))
