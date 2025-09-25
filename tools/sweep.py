from __future__ import annotations
import itertools, json, os, subprocess

def run_one(seed: int, size: int):
    # Placeholder: call your real driver here
    subprocess.check_call(["python", "-m", "pt_sim.tools.demo_run"])

def main():
    seeds = [11, 22]
    sizes = [256, 1024]
    for s, n in itertools.product(seeds, sizes):
        run_one(seed=s, size=n)

if __name__ == "__main__":
    main()
