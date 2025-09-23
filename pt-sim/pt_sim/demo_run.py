import os, json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from .paramsutra import load
from .physics import simplified as ps
from .physics import accurate as pa
def run(cfg_path,outdir):
  cfg=load(cfg_path); out=Path(outdir); out.mkdir(parents=True, exist_ok=True)
  mode=getattr(cfg,'mode','simplified')
  E=10.0; n=cfg.ecal_geom.n; depth=np.linspace(0, cfg.ecal_geom.depth_lambda, n)
  if mode=='simplified':
    longE=ps.longitudinal_profile(depth,cfg.shower.a,cfg.shower.b,E)
    lat=ps.lateral_template(n,cfg.shower.lateral_sigma_cm,cfg.ecal_geom.cell_size_cm)
    ecal=np.zeros((n,n))
    for e in longE: ecal += e*lat
    meas=np.clip(ecal*cfg.ecal_geom.sampling_fraction + np.random.normal(0.0,cfg.ecal_geom.noise_sigma,(n,n)), 0, None)
    tag='simplified'
  else:
    longE=pa.longitudinal_em(depth,E,cfg.material.X0_cm,cfg.material.Ec_MeV)
    lat=pa.lateral_em(n,cfg.ecal_geom.cell_size_cm,cfg.material.RM_cm)
    e_true=np.zeros((n,n))
    for e in longE: e_true += e*lat
    rng=np.random.default_rng(123)
    meas=pa.digitize_energy(e_true, cfg.material.sampling_fraction, cfg.material.light_yield_pe_per_GeV, cfg.material.electronics_noise_GeV, rng)
    tag='accurate'
  # Plots
  plt.figure(); plt.imshow(meas,origin='lower',interpolation='nearest'); plt.colorbar(label='Energy (GeV)'); plt.title(f'ECAL Energy Image (electron, {tag})'); plt.savefig(out/f'ecal_image_{tag}.png',dpi=160,bbox_inches='tight'); plt.close()
  plt.figure(); plt.plot(depth,longE); plt.xlabel('Depth (X0 units)'); plt.ylabel('Energy per layer (GeV)'); plt.title(f'Longitudinal Profile (electron, {tag})'); plt.savefig(out/f'longitudinal_profile_{tag}.png',dpi=160,bbox_inches='tight'); plt.close()
  json.dump({'mode':mode,'electron_energy_GeV':E,'sum_measured_GeV':float(meas.sum()),'n_cells':int(n*n),'config_used':os.path.abspath(cfg_path)}, open(out/f'summary_{tag}.json','w'), indent=2)
  print('Wrote outputs for', tag)
if __name__=='__main__':
  import sys; run(sys.argv[1] if len(sys.argv)>1 else '../configs/demo_electron.yaml', sys.argv[2] if len(sys.argv)>2 else '../out')
