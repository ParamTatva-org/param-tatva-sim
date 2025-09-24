# Quickstart

```bash
# from repo root
cd pt-sim
pip install -e .
pytest -q

# Docs
pip install mkdocs mkdocs-material
mkdocs serve

Week-1 delivers a Boris pusher, EM energy closure tests, and I/O stubs that pass in CI.

See Sprints → Week 1 for commands and acceptance criteria.



## `docs/getting-started/dev-env.md`
```md
# Dev Environment

- Python 3.10+
- Optional Rust toolchain for `pt-core` (Rust 1.75+)
- Recommended: micromamba or uv for reproducible envs

## Lint & tests
```bash
ruff pt-sim
mypy pt-sim
pytest -q



## `docs/architecture/overview.md`
```md
# Architecture Overview

- **pt-core/**: Rust kernels (steppers, hot loops, benches) exposed via PyO3.
- **pt-sim/**: Python SDK and orchestration.
- Optional plugins: Geant4 backend, ACTS tracking.

Design tenets: modular, testable, deterministic, interop-first (HepMC3/ROOT/GDML).
