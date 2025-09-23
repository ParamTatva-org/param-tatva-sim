import os, json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from .forces.gauge import Particle
from .forces.em import UniformField, integrate_motion
from .forces.potentials import coulomb_potential, yukawa_potential, string_potential
from .forces.qcd_toy import flux_tube_map

def demo_lorentz(outdir):
  out=Path(outdir); out.mkdir(parents=True, exist_ok=True)
  e=Particle(q=-1.0,m=0.511)
  field=UniformField(E_vec=(0,0,0), B_vec=(0,0,1.0))
  xs,vs=integrate_motion(e, field, (0,0,0), (0.7,0,0), dt=0.05, steps=1200)
  plt.figure(); plt.plot(xs[:,0], xs[:,1], lw=1.2); plt.axis('equal'); plt.xlabel('x'); plt.ylabel('y'); plt.title('Electron in Uniform B (spiral)')
  p=out/'force_lorentz_spiral.png'; plt.savefig(p,dpi=160,bbox_inches='tight'); plt.close(); return str(p)

def demo_potentials(outdir):
  out=Path(outdir); out.mkdir(parents=True, exist_ok=True)
  r=np.linspace(0.05,10.0,1000); Vc=coulomb_potential(r,1.0); Vy=yukawa_potential(r,1.0,0.7); Vs=string_potential(r,0.2,0.0)
  plt.figure(); plt.plot(r,Vc,label='Coulomb 1/r'); plt.plot(r,Vy,label='Yukawa e^{-mr}/r'); plt.plot(r,Vs,label='String κr'); plt.ylim(0,10); plt.legend(); plt.xlabel('r'); plt.ylabel('V(r)'); plt.title('Force Potentials (toy)')
  p=out/'force_potentials.png'; plt.savefig(p,dpi=160,bbox_inches='tight'); plt.close(); return str(p)

def demo_flux_tube(outdir):
  out=Path(outdir); out.mkdir(parents=True, exist_ok=True)
  X,Y,E=flux_tube_map(n=160,sep=10.0,width=1.5)
  plt.figure(); plt.imshow(E,origin='lower',extent=[X.min(),X.max(),Y.min(),Y.max()],interpolation='bilinear')
  plt.colorbar(label='Normalized energy density'); plt.xlabel('x'); plt.ylabel('y'); plt.title('Toy Color Flux Tube (QCD-like)')
  p=out/'force_flux_tube.png'; plt.savefig(p,dpi=160,bbox_inches='tight'); plt.close(); return str(p)

def run_all(outdir):
  paths={'lorentz_spiral':demo_lorentz(outdir),'potentials':demo_potentials(outdir),'flux_tube':demo_flux_tube(outdir)}
  json.dump(paths, open(Path(outdir)/'forces_outputs.json','w'), indent=2)
  print('Wrote', paths)

if __name__=='__main__':
  import sys; run_all(sys.argv[1] if len(sys.argv)>1 else '../out')
