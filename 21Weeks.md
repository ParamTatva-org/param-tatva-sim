# Guiding principles

* **Two engines**: (A) native fast engine (Rust/Py) for speed & pedagogy, (B) Geant4/ACTS interop for reference validation.
* **Always-green physics tests**: every feature lands with a minimal golden test (numbers + plots).
* **Determinism**: seeded runs, versioned configs, conditions DB.
* **CERN-speak**: HepMC3, ROOT, ACTS, GDML from the start (stubbed until linked).

---

# Tracks (run in parallel)

* **Core Physics** (steppers, materials, interactions)
* **Detector & Digitization** (calo/tracker/muon, shaping, pileup)
* **Geometry & Conditions** (GDML, field maps, alignment, gains)
* **Interop & I/O** (HepMC3/ROOT/Acts/Geant4 plugin)
* **ML Fast-Sim** (Calo surrogate, basic GNN tracking)
* **Orchestration & Scale** (job graph, Ray/SLURM, containers)
* **Validation & QA** (unit + physics + performance)
* **Docs & Center Ops** (ParamTatva Centers, curriculum, datasets)

---

# Week-by-week plan (21 weeks)

### Weeks 1–3: Relativistic transport, scaffolding, conditions

**W1** (already specced)

* Deliver: Python Boris pusher + tests; HepMC/ROOT stubs; energy-closure tests.
* Exit: `pytest -q` green; simple spiral demo stable.

**W2**

* Core Physics: **Relativistic Boris** (γ refresh) + analytic uniform-B propagator.
* Geometry: field map interface (`B(r)`, `E(r)`) + uniform/gradient generators.
* Conditions: **sqlite Conditions DB** with IOV tags; APIs for gains, pedestals, field maps.
* Exit: tests—helix residual < 1e-6, conditions fetch benchmark < 0.1 ms.

**W3**

* Materials: material mixing + **Bethe–Bloch** dE/dx, **Highland** multiple scattering.
* Repo: `materials/PDG_2024.yaml` and helper to compute X0, λI per volume.
* Interop: GDML loader stub → in-memory volumes with materials.
* Exit: unit tests for dE/dx curves vs PDG tables (within 2–5%).

### Weeks 4–6: EM showers v1, geometry navigation, ROOT/HepMC real I/O

**W4**

* Transport: boundary stepping with **BVH/KD-tree** navigator; step limiter by curvature/radius.
* EM Showers: longitudinal gamma model + **Molière** radius lateral kernel.
* Exit: energy/moment tests vs reference curves; navigator unit tests on toy barrel.

**W5**

* I/O: **uproot/ROOT writer** (RNTuple/TTree) + schema v1; **HepMC3** ASCII → native Event.
* Digitization: calo tile model, shaping (CR-RC), noise, thresholds.
* Exit: write/read sanity; energy closure |Σcell−E|/E < 0.5% no-noise; timing spectrum plotted.

**W6**

* Scale: **Ray** job runner (param grid); seed protocol; run registry (git SHA, seed, container).
* Docs: mkdocs site skeleton; “Physics Notes: EM v1”.
* Exit: 1k events EM electron scan (E, η) completes < 3 min on laptop; plots auto-generated.

### Weeks 7–9: Tracking chain, hadronic toy, Geant4/ACTS integration points

**W7**

* Tracking: ACTS minimal chain (truth seeding → CKF) on toy barrel; material effects toggle.
* Exit: efficiency vs pT/η curve in CI; hit residuals distribution sane.

**W8**

* Hadronic: two-component toy (EM fraction fluctuations, simple nuclear interaction length) as a placeholder before Geant4.
* Digitization: tracker strips/pixels digitizers (thresholds, ToT/ToA).
* Exit: calorimeter response linearity plot; tracker fake/duplication rate plotted.

**W9**

* Interop: **Geant4 backend plugin** (compile-time optional, runtime selectable).
* Geometry: GDML → Acts surfaces transform utility.
* Exit: cross-check: native vs Geant4 EM moments within bands; feature flag switch works.

### Weeks 10–12: Pileup, triggers, calibration & alignment loops

**W10**

* Pileup: mixing framework (in-time/out-of-time), bunch structure config.
* Trigger: L1 toy (sliding window sums), HLT hooks (Python filters).
* Exit: latency budget logged; turn-on curve for L1 EM trigger.

**W11**

* Calibration: ECAL intercalibration workflow (minbias or electron scan); pedestal/gain updates into Conditions DB.
* Alignment: tracker global alignment toy (Millepede-like least squares).
* Exit: response uniformity before/after calibration; alignment residuals improve by >50%.

**W12**

* Time-of-Flight: TOF digitizer + simple PID bands; **muon system** stubs (drift time).
* Exit: β resolution plot; muon timing spectrum.

### Weeks 13–15: ML fast-sim & graph tracking, performance hardening

**W13**

* ML: **Calo surrogate v0** (CaloGAN-style) trained on native EM; inference wrapper.
* QA: compare shower moments + images; add “surrogate allowed” flags in configs.
* Exit: surrogate runs 10× faster with Δmoment < 5%.

**W14**

* ML: **GNN seeding** (HEP-Trkx-style) prototype for track seeds; export ONNX for portability.
* Exit: seeding efficiency vs rate curve; throughput numbers.

**W15**

* Performance: Rust kernels (vectorized) for shower fill & digitization; **criterion** benches + asv suite.
* Scale: SLURM profile; containerization (micromamba/Nix) with pinned envs.
* Exit: 2–3× speedup on hotspots; reproducible container hash in run registry.

### Weeks 16–18: Hadronic via Geant4, PF prototype, analysis ergonomics

**W16**

* Geant4 hadronic lists wired; validation grids (pions, protons) at a few energies.
* Exit: response & resolution curves vs Geant4 references (within published bands).

**W17**

* Particle-Flow v0: simple PF building from tracks + calo clusters; neutral/charged separation.
* Exit: jet response/resolution on a mini sample; PF vs calo-only comparison.

**W18**

* Analysis: Parquet sidecar writers; plotting utilities; example notebooks (ROOT and pandas paths).
* Exit: end-to-end demo notebook produces all validation plots from raw events.

### Weeks 19–21: Hardening, docs, and ParamTatva Center launch

**W19**

* Observability: Prometheus metrics; Grafana dashboards (throughput, mem, IO); MLflow/W\&B logging.
* Exit: dashboard up in docker-compose; perf regression alerts wired in CI.

**W20**

* Docs: mkdocs → versioned “Physics Validation Report v1”; ADRs for major design choices.
* Education: draft **Center curriculum** (Sanskrit-first config vocab, Maheshwara-sutra param schema).
* Exit: published docs; tutorial labs (EM, Tracking, Pileup, PF).

**W21**

* Release: **v1.0** tag; long CI on small cluster; artifacted datasets; sample configs.
* Outreach: ParamTatva Center portal page (Research/Stack/Fund/Centre alignment); seed school/startup briefs.
* Exit: reproducible runs from a clean checkout to plots in <1 hour on a 16-core box.

---

# Deliverables matrix (what lands where)

* **pt-core/**: Rust steppers (Boris/Vay), geometry nav kernels, digitizer hotloops, benches.
* **pt-sim/**:

  * `pt_sim/forces/`: boris, analytic refs, field map APIs.
  * `pt_sim/physics/`: EM v1, hadronic toy, material effects.
  * `pt_sim/detector/`: calo/tracker/muon digitizers, TOF.
  * `pt_sim/io/`: ROOT RNTuple writer/reader, HepMC3 adapters, Parquet sidecars.
  * `pt_sim/geom/`: GDML import, Acts surfaces.
  * `pt_sim/reco/`: tracking (ACTS), clusters, PF v0.
  * `pt_sim/ml/`: calo surrogate, GNN seeding wrappers.
  * `pt_sim/exec/`: job graph, Ray/SLURM runners, registry.
  * `pt_sim/validate/`: golden tests, plotting, report builder.
* **configs/**: detector, beam, pileup, triggers, conditions tags (IOV).
* **docs/**: physics notes, ADRs, tutorials, validation report.
* **dash/**: docker-compose for Prometheus/Grafana/MLflow.

---

# Staffing & cadence (lean team)

* **Physics core (1–2)**: transports, showers, materials.
* **Software/interop (1)**: IO, schemas, GDML/ROOT/Geant4/ACTS.
* **ML (1)**: surrogates + GNN seeding.
* **Infra (0.5)**: CI, containers, dashboards.
* **Validation (0.5)**: plots, reports, curriculum.

> Weekly 45-min triage (board: Backlog → Doing → Review → Done). Every PR: tests + doc snippet.

---

# Exit metrics (what “CERN-grade v1.0” means here)

* **Physics**: EM calorimeter shower moments vs Geant4 within target bands; hadronic via Geant4 validated at a few energies; tracking eff/fakes in expected ranges on toy geom.
* **Scale**: 10^7 EM-only events/month on a modest 8-GPU/64-CPU cluster; deterministic seeds.
* **Reproducibility**: run registry (SHA, seed, container) → rebuild plots exactly.
* **Interoperability**: ingest HepMC3; write ROOT; run ACTS; optional Geant4 backend toggle.

---

# ParamTatva tie-ins

* **Fundamental String Center**: host field solvers, KK/winding scans in `pt-core`, and publish Sanskrit-encoded config taxonomy.
* **AI/Data Stacks**: Calo surrogate & GNN pipelines + Parquet/ROOT dual I/O; search/curation of runs.
* **Fund**: “school” labs around weeks 6, 12, 18 artifacts; “startup” kits on fast-sim and PF.

