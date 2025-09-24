# Week 1 — Relativistic-ready Boris & Test Scaffolding

**Deliverables**
- Boris pusher (Python) + analytic helix helpers
- Tests: speed conservation, radius check; EM energy closure
- I/O stubs (ROOT/HepMC3 fall back to npz/ascii)

**Exit criteria**
- `pytest -q` green
- Demo spiral stable with dt guard

**Run**
```bash
cd pt-sim && pip install -e .
pytest -q
