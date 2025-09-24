# Packages & Layout

param-tatva-sim/
├─ pt-core/ # Rust core library (optional at first)
├─ pt-sim/ # Python package (pip install -e .)
│ ├─ pt_sim/
│ │ ├─ forces/ # boris.py, analytic refs, field maps
│ │ ├─ physics/ # simplified.py, accurate.py
│ │ ├─ io/ # rootio.py, hepmc.py
│ │ ├─ geom/ # (Week-3) GDML adapters
│ │ ├─ validate/ # figure builders
│ │ └─ ...
└─ tests/ # unit & physics tests