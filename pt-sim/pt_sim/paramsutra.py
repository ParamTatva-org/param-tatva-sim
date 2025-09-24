from typing import TypedDict, cast
import yaml


class ShowerCfg(TypedDict, total=False):
    alpha: float
    beta: float
    depth_X0: float
    lateral_sigma_cm: float


class EcalGeomCfg(TypedDict, total=False):
    n_cells: int
    cell_size_cm: float
    sampling_fraction: float
    noise_sigma: float


class MaterialCfg(TypedDict, total=False):
    X0_cm: float
    Ec_MeV: float
    RM_cm: float
    sampling_fraction: float
    light_yield_pe_per_GeV: float
    electronics_noise_sigma: float


class Config(TypedDict, total=False):
    mode: str
    shower: ShowerCfg
    ecal_geom: EcalGeomCfg
    material: MaterialCfg


def load(path: str) -> Config:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    # We accept partial configs; callers should guard with defaults.
    return cast(Config, data if isinstance(data, dict) else {})
