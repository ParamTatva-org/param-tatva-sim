# pt-sim/pt_sim/core/rng.py
from __future__ import annotations
import os, json, hashlib, time
from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any

import numpy as np

DEFAULT_SEED = 1337

@dataclass
class RunManifest:
    seed: int
    git_sha: Optional[str] = None
    config_hash: Optional[str] = None
    started_at: float = field(default_factory=time.time)
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        d = asdict(self)
        return json.dumps(d, indent=2, sort_keys=True)

def stable_hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def stable_hash_obj(obj: Any) -> str:
    return stable_hash_bytes(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode())

def make_rng(seed: Optional[int] = None) -> np.random.Generator:
    if seed is None:
        seed = DEFAULT_SEED
    return np.random.default_rng(seed)

def write_run_manifest(path: str, seed: int, config: Optional[Dict[str, Any]] = None,
                       extra: Optional[Dict[str, Any]] = None, git_sha: Optional[str] = None) -> RunManifest:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cfg_hash = stable_hash_obj(config) if config is not None else None
    manifest = RunManifest(seed=seed, git_sha=git_sha, config_hash=cfg_hash, extra=extra or {})
    with open(path, "w") as f:
        f.write(manifest.to_json())
    return manifest
