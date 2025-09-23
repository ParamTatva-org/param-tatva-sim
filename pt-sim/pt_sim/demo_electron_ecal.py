import os, json, math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from .paramsutra import load
def _longitudinal_profile(depth,a,b,E):
  xs=np.linspace(0, depth.max(), 2048); ys=(xs**(a-1))*np.exp(-b*xs); norm=np.trapz(ys,xs); scale=E/norm
  return (depth**(a-1))*np.exp(-b*depth)*scale
def _lateral_template(n,sigma,cell):
  idx=np.arange(n)-(n-1)/2; X,Y=np.meshgrid(idx,idx,indexing='xy'); X*=cell; Y*=cell; G=np.exp(-0.5*(X**2+Y**2)/(sigma**2)); return G/G.sum()
def run(cfg_path,outdir):
  cfg=load(cfg_path); out=Path(outdir); out.mkdir(parents=True,exist_ok=True)
  E=10.0; n=cfg.ecal_geom.n; cell=cfg.ecal_geom.cell_size_cm
  depth=np.linspace(0,cfg.ecal_geom.depth_lambda,n)
  longE=_longitudinal_profile(depth,cfg.shower.a,cfg.shower.b,E)
  lateral=_lateral_template(n,cfg.shower.lateral_sigma_cm,cell)
  ecal=np.zeros((n,n))
  for e in longE: ecal+=e*lateral
  meas=np.clip(ecal*cfg.ecal_geom.sampling_fraction+np.random.normal(0.0,cfg.ecal_geom.noise_sigma,(n,n)),0,None)
  plt.figure(); plt.imshow(meas,origin='lower',interpolation='nearest'); plt.colorbar(label='Energy (GeV)'); plt.title('Tiny ECAL Energy Image (electron)'); plt.savefig(out/'ecal_image.png',dpi=160,bbox_inches='tight'); plt.close()
  plt.figure(); plt.plot(depth,longE); plt.xlabel('Depth (X0 units, toy)'); plt.ylabel('Energy per layer (GeV)'); plt.title('Longitudinal Shower Profile (electron)'); plt.savefig(out/'longitudinal_profile.png',dpi=160,bbox_inches='tight'); plt.close()
  json.dump({'electron_energy_GeV':E,'ecal_sum_meas_GeV':float(meas.sum()),'n_cells':int(n*n),'config_used':os.path.abspath(cfg_path)}, open(out/'summary.json','w'), indent=2)
  print('Wrote outputs in', out)
if __name__=='__main__':
  import sys; run(sys.argv[1] if len(sys.argv)>1 else '../configs/demo_electron.yaml', sys.argv[2] if len(sys.argv)>2 else '../out')
