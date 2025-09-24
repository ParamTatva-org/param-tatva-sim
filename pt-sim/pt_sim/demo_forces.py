from pathlib import Path
from typing import Union
import json
import numpy as np
import matplotlib.pyplot as plt

from .forces.gauge import Particle
from .forces.em import integrate_motion, UniformField
from .forces.potentials import (
    coulomb_potential,
    yukawa_potential,
    string_potential,
)
from .forces.qcd_toy import flux_tube_map

Pathish = Union[str, Path]


def demo_lorentz(outdir: Pathish) -> str:
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    e = Particle(q=-1.0, m=0.511)
    field = UniformField(E_vec=(0.0, 0.0, 0.0), B_vec=(0.0, 0.0, 1.0))
    xs, vs = integrate_motion(e, field, (0.0, 0.0, 0.0), (0.7, 0.0, 0.0), dt=0.05, steps=1200)

    plt.figure()
    plt.plot(xs[:, 0], xs[:, 1], lw=1.2)
    plt.axis("equal")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Electron in Uniform B (toy NR integrator)")

    png_path = out / "force_lorentz_spiral.png"
    plt.savefig(png_path, dpi=160, bbox_inches="tight")
    plt.close()
    return str(png_path)


def demo_potentials(outdir: Pathish) -> str:
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    r = np.linspace(0.05, 10.0, 1000)
    Vc = coulomb_potential(r, 1.0)
    Vy = yukawa_potential(r, 1.0, 0.7)
    Vs = string_potential(r, 0.2, 0.0)

    plt.figure()
    plt.plot(r, Vc, label="Coulomb 1/r")
    plt.plot(r, Vy, label="Yukawa e^{-mr}/r")
    plt.plot(r, Vs, label="String κr")
    plt.ylim(0, 10)
    plt.legend()
    plt.xlabel("r")
    plt.ylabel("V(r)")
    plt.title("Force Potentials (toy)")

    png_path = out / "force_potentials.png"
    plt.savefig(png_path, dpi=160, bbox_inches="tight")
    plt.close()
    return str(png_path)


def demo_flux_tube(outdir: Pathish) -> str:
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    X, Y, E = flux_tube_map(n=160, sep=10.0, width=1.5)

    plt.figure()
    """ plt.imshow(
        E,
        origin="lower",
        extent=[X.min(), X.max(), Y.min(), Y.max()],
        interpolation="bilinear",
    ) """
    extent: tuple[float, float, float, float] = (
        float(X.min()), float(X.max()), float(Y.min()), float(Y.max())
    )
    plt.imshow(
        E,
        origin="lower",
        extent=extent,
        interpolation="bilinear",
    )
    plt.colorbar(label="Normalized energy density")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Toy Color Flux Tube (QCD-like)")

    png_path = out / "force_flux_tube.png"
    plt.savefig(png_path, dpi=160, bbox_inches="tight")
    plt.close()
    return str(png_path)


def run_all(outdir: Pathish) -> str:
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    results = {
        "spiral_png": demo_lorentz(out),
        "potentials_png": demo_potentials(out),
        "flux_tube_png": demo_flux_tube(out),
    }

    with open(out / "demo_forces_summary.json", "w") as f:
        json.dump(results, f, indent=2)

    return str(out)


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "../out"
    run_all(target)
