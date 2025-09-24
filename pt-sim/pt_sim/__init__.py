__version__ = "0.2.0"

# Explicit re-exports so Ruff treats them as used
from . import physics as physics  # re-export
from . import forces as forces    # re-export
from . import io as io            # re-export

__all__ = ["physics", "forces", "io", "__version__"]