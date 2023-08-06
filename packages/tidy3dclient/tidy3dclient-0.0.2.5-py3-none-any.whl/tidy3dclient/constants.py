import numpy as np

"""
This file contains constants that are used throghout the codebase.
"""

# Machine precision
dp_eps = np.finfo(np.float64).eps
fp_eps = np.finfo(np.float32).eps

# Data types to use
int_ = np.int32
float_ = np.float32

# Physical constants. Base unit of length is micron.
EPSILON_0 = np.float32(8.85418782e-18)         # vacuum permittivity
MU_0 = np.float32(1.25663706e-12)              # vacuum permeability
C_0 = 1 / np.sqrt(EPSILON_0 * MU_0)            # speed of light in vacuum
ETA_0 = np.sqrt(MU_0 / EPSILON_0)              # vacuum impedance
Q_e = 1.602176634e-19                          # funamental charge

# Conversion between 'x', 'y', 'z' and 0, 1, 2
xyz_dict = {'x': 0, 'y': 1, 'z': 2}
xyz_list = ['x', 'y', 'z']

