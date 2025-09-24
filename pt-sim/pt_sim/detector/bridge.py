import numpy as np
from typing import Dict, Any, List
#from ..physics.simplified import longitudinal_profile, lateral_template

def kernel_to_ecal_image(emission: Dict[str, Any], n: int = 32, E_scale: float = 1.0):
    """Very first bridge: convert particles + fields to an ECAL-like 2D energy image."""
    img = np.zeros((n,n), float)

    # Particles -> localized deposits (toy: Gaussian blobs proportional to energy)
    for p in emission.get("particles", []):
        # map node -> (row,col); start with a simple ring mapping by line/pos
        line = int(p["Q"].get("line", 1)) - 1
        pos  = int(p["Q"].get("pos", 1)) - 1
        r = int(n*0.5 * (line/14.0)); c = int(n*0.5 * (pos/9.0))
        rr, cc = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
        sigma = max(1.0, 0.5 + 0.02*p["energy"])
        img += p["energy"]*E_scale * np.exp(-0.5*((rr-r)**2+(cc-c)**2)/(sigma**2))

    # Fields -> diffuse ribbons (toy: broad smear)
    for f in emission.get("fields", []):
        img += (E_scale*0.3*f["energy"]/max(1,n*n)) * np.ones_like(img)

    return img
