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


def run(config_path: str, outdir: str) -> str:
    cfg = load(config_path)
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    mode = getattr(cfg, "mode", "simplified")
    E = 10.0
    n = cfg.ecal_geom.n_cells
    depth = np.linspace(0.0, cfg.shower.depth_X0, n)

    if mode == "simplified":
        longE = simp_longitudinal_profile(depth, cfg["shower"]["alpha"], cfg["shower"]["beta"], E)
        
        lat = simp_lateral_template(
            n,
            cfg["shower"]["lateral_sigma_cm"],
            cfg["ecal_geom"]["cell_size_cm"],
        )
        e_true = np.zeros((n, n))
        for e in longE:
            e_true += e * lat
        meas = np.clip(
            e_true * cfg.ecal_geom.sampling_fraction
            + np.random.normal(0.0, cfg.ecal_geom.noise_sigma, size=(n, n)),
            0.0,
            None,
        )
        tag = "simplified"
    else:
 
        longE = acc_longitudinal_em(
            depth,
            E,
            X0_cm=cfg["material"]["X0_cm"],
            Ec_MeV=cfg["material"]["Ec_MeV"],
        )
        lat = acc_lateral_em(n, cfg["ecal_geom"]["cell_size_cm"], cfg["material"]["RM_cm"])
        rng = np.random.default_rng(12345)
        meas = acc_digitize_energy(
            e_true,
            cfg["material"]["sampling_fraction"],
            cfg["material"]["light_yield_pe_per_GeV"],
            cfg["material"]["electronics_noise_sigma"],
            rng=rng,
        )


        
        e_true = np.zeros((n, n))
        for e in longE:
            e_true += e * lat
        
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
