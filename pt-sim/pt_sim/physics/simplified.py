import numpy as np
def longitudinal_profile(depth,a,b,E):
  xs=np.linspace(0, depth.max(), 2048); ys=(xs**(a-1))*np.exp(-b*xs); norm=np.trapz(ys,xs); return (depth**(a-1))*np.exp(-b*depth)*(E/norm)
def lateral_template(n,sigma,cell):
  idx=np.arange(n)-(n-1)/2; X,Y=np.meshgrid(idx,idx,indexing='xy'); X*=cell; Y*=cell; G=np.exp(-0.5*(X**2+Y**2)/(sigma**2)); return G/G.sum()
