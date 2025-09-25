from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Ledger:
    """A minimal conservation ledger.
    Track scalar totals for energy and charge at each step.
    """
    energy_in: float = 0.0
    energy_out: float = 0.0
    energy_field: float = 0.0
    energy_particles: float = 0.0
    charge_in: float = 0.0
    charge_out: float = 0.0
    extra: Dict[str, float] = field(default_factory=dict)

    def add(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, getattr(self, k) + float(v))
            else:
                self.extra[k] = self.extra.get(k, 0.0) + float(v)

    def energy_closure(self) -> float:
        """Relative closure |in - out - field - particles| / max(1, |in|)."""
        denom = max(1.0, abs(self.energy_in))
        resid = self.energy_in - self.energy_out - self.energy_field - self.energy_particles
        return abs(resid) / denom

    def charge_closure(self) -> float:
        denom = max(1.0, abs(self.charge_in))
        resid = self.charge_in - self.charge_out
        return abs(resid) / denom

    def assert_within(self, energy_tol=0.02, charge_tol=1e-9):
        e = self.energy_closure()
        c = self.charge_closure()
        assert e <= energy_tol, f"Energy closure {e:.4%} exceeds tolerance {energy_tol:.4%}"
        assert c <= charge_tol, f"Charge closure {c:.4%} exceeds tolerance {charge_tol:.4%}"
