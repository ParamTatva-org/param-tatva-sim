import numpy as np
from .gauge import Field, lorentz_force


class UniformField(Field):
    def __init__(self, E_vec=(0, 0, 0), B_vec=(0, 0, 1)):
        self._E = np.array(E_vec, float)
        self._B = np.array(B_vec, float)

    def E(self, t, x):
        return self._E

    def B(self, t, x):
        return self._B


def integrate_motion(particle, field, x0, v0, dt, steps):
    x = np.array(x0, float)
    v = np.array(v0, float)
    xs = np.zeros((steps, 3))
    vs = np.zeros((steps, 3))

    for i in range(steps):
        E = field.E(i * dt, x)
        B = field.B(i * dt, x)
        a = lorentz_force(particle, v, E, B) / max(particle.m, 1e-9)

        v_half = v + 0.5 * dt * a
        x = x + dt * v_half

        E2 = field.E((i + 1) * dt, x)
        B2 = field.B((i + 1) * dt, x)
        a2 = lorentz_force(particle, v_half, E2, B2) / max(particle.m, 1e-9)

        v = v_half + 0.5 * dt * a2

        xs[i] = x
        vs[i] = v

    return xs, vs
