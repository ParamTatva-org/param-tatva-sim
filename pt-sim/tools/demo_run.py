from __future__ import annotations
from pt_sim.core.rng import make_rng, write_run_manifest
import numpy as np
import os

def main(seed: int = 123):
    rng = make_rng(seed)
    xs = rng.normal(size=1024)
    outdir = "out/demo"
    os.makedirs(outdir, exist_ok=True)
    np.save(os.path.join(outdir, "xs.npy"), xs)
    write_run_manifest(os.path.join(outdir, "run.json"), seed, config={"size": 1024})
    return xs.mean(), xs.std()

if __name__ == "__main__":
    # side-effect guard: only runs when called as a script
    m, s = main()
    print(f"demo stats: mean={m:.4f}, std={s:.4f}")
