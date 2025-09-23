import numpy as np
def flux_tube_map(n=160, sep=10.0, width=1.5):
  x=np.linspace(-sep,sep,n); y=np.linspace(-sep,sep,n); X,Y=np.meshgrid(x,y,indexing='xy')
  tube=np.exp(-0.5*(Y/width)**2)*np.exp(-0.1*((np.abs(X)-sep/2)**2))
  blob1=np.exp(-0.5*(((X+sep/2)**2+Y**2)/(width**2)))
  blob2=np.exp(-0.5*(((X-sep/2)**2+Y**2)/(width**2)))
  E=tube + 0.7*(blob1+blob2)
  return X,Y,E/E.max()
