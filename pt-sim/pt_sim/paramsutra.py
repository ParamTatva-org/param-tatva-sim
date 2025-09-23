import yaml
from dataclasses import dataclass
@dataclass
class PTGlobal: alpha_prime: float=1.0; intercept: float=1.0
@dataclass
class ElectronTarget: mass_mev: float=0.511; charge: int=-1; spin: float=0.5
@dataclass
class ECALGeom: n:int=32; cell_size_cm:float=1.0; moliere_radius_cm:float=2.0; depth_lambda:float=25.0; sampling_fraction:float=0.9; noise_sigma:float=0.002
@dataclass
class ShowerParams: a:float=4.0; b:float=0.3; lateral_sigma_cm:float=1.2
@dataclass
class Config: global_pt:PTGlobal; electron:ElectronTarget; ecal_geom:ECALGeom; shower:ShowerParams
def load(path:str)->Config:
  d=yaml.safe_load(open(path))
  return Config(PTGlobal(**d.get('global_pt',{})), ElectronTarget(**d.get('electron',{})), ECALGeom(**d.get('ecal_geom',{})), ShowerParams(**d.get('shower',{})))
