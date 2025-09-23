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
from dataclasses import dataclass
@dataclass
class Material:
  name:str='PbWO4'; X0_cm:float=0.89; RM_cm:float=2.0; Ec_MeV:float=9.0; sampling_fraction:float=0.9; light_yield_pe_per_GeV:float=20000.0; electronics_noise_GeV:float=0.002
def load(path:str):
  d=yaml.safe_load(open(path))
  gp=PTGlobal(**d.get('global_pt',{})); el=ElectronTarget(**d.get('electron',{})); eg=ECALGeom(**d.get('ecal_geom',{})); sp=ShowerParams(**d.get('shower',{}))
  cfg=Config(gp,el,eg,sp)
  cfg.mode=d.get('mode','simplified')
  cfg.material=Material(**d.get('material',{}))
  return cfg
