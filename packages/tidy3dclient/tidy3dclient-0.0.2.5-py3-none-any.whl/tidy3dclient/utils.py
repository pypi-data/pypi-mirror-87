import numpy as np
import subprocess

from .constants import fp_eps, EPSILON_0

def listify(obj):
    # Make a list if not a list
    if isinstance(obj, list):
        return obj
    elif isinstance(obj, np.ndarray):
        return list(obj)
    else:
        return [obj] 

def subprocess_cmd(command):
    """Execute a (multi-line) shell command.
    
    Parameters
    ----------
    command : str
        Semicolon separated lines. 
    """
    comm_lines = command.split(';')
    for line in comm_lines:
        comm_list = list(line.split())
        process = subprocess.run(comm_list, stdout=None, check=True,
                                stdin=subprocess.DEVNULL)

def inside_box(span, mesh, include_zero_size=False):
    """Elementwise indicator function showing which points in the ``span`` are 
    inside a grid defined by ``mesh``. 
    
    Parameters
    ----------
    span : np.ndarray of shape (3, 2)
        Defines (xmin, xmax), (ymin, ymax), (zmin, zmax) of the box.
    mesh : tuple
        3-tuple defining the xgrid, ygrid and zgrid.
    include_zero_size : bool, optional
        If True, a span of zero (max - min = 0) in any direction will be taken 
        as one pixel. If False, the mask will be all empty.  
    
    Returns
    -------
    mask : np.ndarray
        A 3D array of shape (mesh[0].size, mesh[1].size, mesh[2].size)
        that is 1 inside the box and 0 outside. 
    """

    # Check if min and max values are in order
    for dim in range(3):
        if span[dim, 1] < span[dim, 0]:
            raise ValueError("Incorrect object span (max value smaller than "
                "min value).")

    # Initialize empty mask
    mask = np.zeros((mesh[0].size, mesh[1].size, mesh[2].size))

    # Check if box is completely outside mesh, and return empty mask if so.
    # Also check if there's a strictly zero span and it was not requested.
    for dim in range(3):
        if (span[dim, 0] > mesh[dim][-1]) or (span[dim, 1] < mesh[dim][0]):
            return mask
        if (span[dim, 1] - span[dim, 0]==0) and (not include_zero_size):
            return mask

    indx = np.nonzero((span[0, 0] < mesh[0]) * (mesh[0] < span[0, 1]))[0]
    indy = np.nonzero((span[1, 0] < mesh[1]) * (mesh[1] < span[1, 1]))[0]
    indz = np.nonzero((span[2, 0] < mesh[2]) * (mesh[2] < span[2, 1]))[0]

    # If there's still a zero span and it was not requested, we're done.
    if (indx.size==0 or indy.size==0 or indz.size==0) and \
            (not include_zero_size):
        return mask

    # Otherwise, we build the mask. For zero span, we just take the first 
    # element of the mesh that is larger than the requested min value. 
    if indx.size==0:
        indsx = np.nonzero(span[0, 0] < mesh[0])[0][0]
    else:
        indsx = slice(indx[0], indx[-1]+1)
    if indy.size==0:
        indsy = np.nonzero(span[1, 0] < mesh[1])[0][0]
    else:
        indsy = slice(indy[0], indy[-1]+1)
    if indz.size==0:
        indsz = np.nonzero(span[2, 0] < mesh[2])[0][0]
    else:
        indsz = slice(indz[0], indz[-1]+1)

    mask[indsx, indsy, indsz] = 1.
    return mask

def intersect_box(span1, span2):
    """ Return a span of a box that is the intersection between two spans.
    """
    span = np.zeros((3, 2))
    for d in range(3):
        span[d, 0] = max(span1[d, 0], span2[d, 0])
        span[d, 1] = min(span1[d, 1], span2[d, 1])

    return span

def x_to_center(Ex):
    """Interpolate Ex positions to the center of a Yee lattice
    """
    return (Ex + np.roll(Ex, -1, 1) + np.roll(Ex, -1, 2) + 
                np.roll(np.roll(Ex, -1, 1), -1, 2))/4

def y_to_center(Ey):
    """Interpolate Ey positions to the center of a Yee lattice
    """
    return (Ey + np.roll(Ey, -1, 0) + np.roll(Ey, -1, 2) + 
                np.roll(np.roll(Ey, -1, 0), -1, 2))/4

def z_to_center(Ez):
    """Interpolate Ez positions to the center of a Yee lattice
    """
    return (Ez + np.roll(Ez, -1, 0) + np.roll(Ez, -1, 1) + 
                np.roll(np.roll(Ez, -1, 0), -1, 1))/4

def E_to_center(Ex, Ey, Ez):
    return (x_to_center(Ex), y_to_center(Ey), z_to_center(Ez))

def eps_to_center(eps_xx, eps_yy, eps_zz):
    """Interpolate eps_r to the center of the Yee lattice. Used for plotting.
    """ 
    # # Simple averaging of one x, y, z values per cell.
    # return (eps_xx + eps_yy + eps_zz)/3

    # Average all 4 eps_xx, 4 eps_yy, and 4 eps_zz values around the 
    # cell center, similar to the probe field recording.
    return (x_to_center(eps_xx) + y_to_center(eps_yy) + z_to_center(eps_zz))/3

def cs2span(center, size):
    """ Get shape (3, 2) span from center and size, each (3, ) arrays.
    """
    return np.vstack((np.array(center) - np.array(size)/2,
                    np.array(center) + np.array(size)/2)).T

def span2cs(span):
    """ Get center, size: each arrays of shape (3,), from a shape (3, 2) array 
    span. 
    """
    center = np.array([(span[d, 1] + span[d, 0])/2 for d in range(3)])
    size = np.array([(span[d, 1] - span[d, 0]) for d in range(3)])
    return center, size
    
def check_3D_lists(**kwargs):
    """ Verify that input arguments are lists with three elements """
    for key, val in kwargs.items():
        try: 
            if not isinstance(val, list):
                raise ValueError
            if len(val)!=3:
                raise ValueError
            for v in val:
                if type(v) in [list, tuple, np.ndarray]:
                    raise ValueError
        except:
            raise ValueError("'%s' must be array-like with three elements."
                                %key)