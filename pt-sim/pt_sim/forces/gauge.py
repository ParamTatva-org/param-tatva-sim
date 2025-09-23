from dataclasses import dataclass
import numpy as np
@dataclass
class Particle: q: float; m: float
class Field:
  def E(self,t,x): return np.zeros(3)
  def B(self,t,x): return np.zeros(3)
def lorentz_force(p, v, E, B): return p.q*(E + np.cross(v,B))
