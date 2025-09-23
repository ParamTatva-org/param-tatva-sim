# 卍 Param Tatva Simulation — How universe came into existence, and continues to do so? 卍

⚛️ **Particles + Forces + Detector Simulation**
This repository implements the **Param Tatva Simulation**, a unifying framework inspired by string theory, where **Param Tatva** (the fundamental string) gives rise to both particles and forces.

It includes:

* **Detector Simulator**

  * *Simplified mode*: fast, pedagogical EM shower (Gamma longitudinal + Gaussian lateral).
  * *Accurate mode*: PDG-inspired longitudinal profile, two-Gaussian Molière lateral spread, photo-statistics digitization.

* **Forces Module**

  * Electromagnetic motion via Lorentz force in E/B fields.
  * Force potentials: Coulomb $1/r$, Yukawa $e^{-mr}/r$, and QCD-like string $κr$.
  * Toy color flux-tube visualizer for confinement.

* **ParamSūtra Configs** for easy switching between modes and material presets.

---

## 📂 Repository Structure

```
param-tatva-sim-all/
├─ pt-core/                  # Rust crate (future kernels, algebra stubs)
│  ├─ Cargo.toml
│  └─ src/lib.rs
├─ pt-sim/
│  ├─ pyproject.toml
│  └─ pt_sim/
│     ├─ __init__.py
│     ├─ paramsutra.py        # config loader + material & mode
│     ├─ physics/             # detector physics
│     │  ├─ simplified.py
│     │  └─ accurate.py
│     ├─ forces/              # forces
│     │  ├─ gauge.py
│     │  ├─ em.py
│     │  ├─ potentials.py
│     │  └─ qcd_toy.py
│     ├─ demo_run.py          # detector demo runner
│     └─ demo_forces.py       # forces demo runner
├─ configs/
│  ├─ demo_electron.yaml            # simplified mode
│  └─ demo_electron_accurate.yaml   # accurate mode
├─ out/                        # auto-generated demo outputs
└─ README.md
```

---

## 🚀 Quickstart

### 1. Install

```bash
cd pt-sim
python -m pip install -e .
```

### 2. Run Detector Simulations

Simplified mode:

```bash
python -m pt_sim.demo_run ../configs/demo_electron.yaml ../out
```

Accurate mode:

```bash
python -m pt_sim.demo_run ../configs/demo_electron_accurate.yaml ../out
```

### 3. Run Force Demos

```bash
python -m pt_sim.demo_forces ../out
```

---

## 📊 Outputs

Detector (saved in `out/`):

* `ecal_image_simplified.png`, `ecal_image_accurate.png`
* `longitudinal_profile_simplified.png`, `longitudinal_profile_accurate.png`
* `summary_simplified.json`, `summary_accurate.json`

Forces (saved in `out/`):

* `force_lorentz_spiral.png` (electron in uniform B-field)
* `force_potentials.png` (Coulomb / Yukawa / String)
* `force_flux_tube.png` (toy QCD color flux tube)

---

## 🧩 Features

* **Toggle physics fidelity**: fast pedagogical vs. more realistic PDG-like.
* **Forces integrated**: move beyond particles to interactions.
* **Extensible**: Rust stubs for high-performance kernels; Python orchestration.
* **ParamSūtra DSL** (YAML-based) for clean configs.

---

## 🗺 Roadmap

* Add **proton/neutron toy bound states** using string potential.
* Extend detector with **tracker + HCAL + muon system**.
* Implement **parton showers + fragmentation**.
* Support **ROOT/Parquet outputs** for HEP workflows.
* Provide **CLI (`pt run ...`)** for unified interface.

---

## 📜 License

Apache-2.0

