import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from .physics.simplified import (
    longitudinal_profile as simp_longitudinal_profile,
    lateral_template as simp_lateral_template,
)
from .physics.accurate import (
    longitudinal_em as acc_longitudinal_em,
    lateral_em as acc_lateral_em,
    digitize_energy as acc_digitize_energy,
)
from .paramsutra import load


def _get(cfg: dict, path: list[str], default):
    cur = cfg
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def run(config_path: str, outdir: str) -> str:
    cfg = load(config_path)
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    mode = str(_get(cfg, ["mode"], "simplified"))
    E = 10.0

    n = int(_get(cfg, ["ecal_geom", "n_cells"], 32))
    depth_X0 = float(_get(cfg, ["shower", "depth_X0"], 20.0))
    depth = np.linspace(0.0, depth_X0, n)

    if mode == "simplified":
        alpha = float(_get(cfg, ["shower", "alpha"], 4.0))
        beta = float(_get(cfg, ["shower", "beta"], 0.3))
        sigma_cm = float(_get(cfg, ["shower", "lateral_sigma_cm"], 1.2))
        cell_cm = float(_get(cfg, ["ecal_geom", "cell_size_cm"], 1.0))
        samp = float(_get(cfg, ["ecal_geom", "sampling_fraction"], 0.15))
        noise = float(_get(cfg, ["ecal_geom", "noise_sigma"], 0.01))

        longE = simp_longitudinal_profile(depth, alpha, beta, E)
        lat = simp_lateral_template(n, sigma_cm, cell_cm)

        e_true = np.zeros((n, n))
        for e in longE:
            e_true += e * lat

        meas = np.clip(
            e_true * samp + np.random.normal(0.0, noise, size=(n, n)),
            0.0,
            None,
        )
        tag = "simplified"

    else:
        X0_cm = float(_get(cfg, ["material", "X0_cm"], 1.0))
        Ec_MeV = float(_get(cfg, ["material", "Ec_MeV"], 10.0))
        RM_cm = float(_get(cfg, ["material", "RM_cm"], 2.0))
        samp = float(_get(cfg, ["material", "sampling_fraction"], 0.15))
        ly = float(_get(cfg, ["material", "light_yield_pe_per_GeV"], 100.0))
        enoise = float(_get(cfg, ["material", "electronics_noise_sigma"], 0.01))
        cell_cm = float(_get(cfg, ["ecal_geom", "cell_size_cm"], 1.0))

        longE = acc_longitudinal_em(depth, E, X0_cm=X0_cm, Ec_MeV=Ec_MeV)
        lat = acc_lateral_em(n, cell_cm, RM_cm)

        e_true = np.zeros((n, n))
        for e in longE:
            e_true += e * lat

        rng = np.random.default_rng(12345)
        meas = acc_digitize_energy(
            e_true,
            samp,
            ly,
            enoise,
            rng=rng,
        )
        tag = "accurate"

    # Plots
    plt.figure()
    plt.imshow(meas, origin="lower", interpolation="nearest")
    plt.colorbar(label="Energy (GeV)")
    plt.title(f"ECAL Energy Image (electron, {tag})")
    plt.savefig(out / f"ecal_image_{tag}.png", dpi=160, bbox_inches="tight")
    plt.close()

    plt.figure()
    plt.plot(depth, longE)
    plt.xlabel("Depth (X0 units)")
    plt.ylabel("Energy per layer (GeV)")
    plt.title(f"Longitudinal Profile (electron, {tag})")
    plt.savefig(out / f"longitudinal_profile_{tag}.png", dpi=160, bbox_inches="tight")
    plt.close()

    with open(out / f"summary_{tag}.json", "w") as f:
        json.dump(
            {
                "mode": mode,
                "electron_energy_GeV": E,
                "sum_measured_GeV": float(meas.sum()),
                "n_cells": int(n * n),
                "config_used": str(Path(config_path).resolve()),
            },
            f,
            indent=2,
        )

    return str(out)


if __name__ == "__main__":
    import sys

    run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "../out")
