import numpy as np
from matplotlib.path import Path
# gdspy is only needed for the GdsSlab structure
try:
    import gdspy
except ImportError:
    pass

from .utils import inside_box, cs2span
from .constants import fp_eps, int_, float_, xyz_dict

class Structure(object):
    
    def __init__(self, material, name=None):
        """Base class for structures 
        
        Parameters
        ----------
        material : Material
            Material of the structure.
        name : str
            Custom name.
        """

        self.material = material
        self.name = None if name is None else str(name)

    def _inside(self, mesh, include_edges=True):
        """Elementwise indicator function for the structure.
        
        Parameters
        ----------
        mesh : tuple
            3-tuple defining the xgrid, ygrid and zgrid.
        include_edges : bool
            Whether a point sitting exactly on a mesh point (within numerical 
            precision) should be returned as inside (True) or outside (False) 
            the structure.
        
        Note
        ----
        ``include_edges`` will in the future be replaced by actual dielectric 
        smoothening.
        
        Returns
        -------
        mask : np.ndarray
            A 3D array of shape (mesh[0].size, mesh[1].size, mesh[2].size)
            that is 1 inside the structure and 0 outside, and a continuous 
            value between 0 and 1 at interfaces if smoothen==True.
        """

        raise NotImplementedError("inside() needs to be implemented by "
            "Structure subclasses")

class Box(Structure):
    """ Box structure, i.e. a 3D rectangular block.
    """

    def __init__(self, center, size, material, name=None):
        """ Construct.

        Parameters
        ----------
        center : array_like
            (micron): x, y, and z position of the center of the Box.
        size : array_like
            (micron): size in x, y, and z.
        material : Material
            Material of the structure.
        name : str, optional
            Custom name of the structure.
        """
        super().__init__(material, name)
        self.center = np.array(center)
        self.size = np.array(size)
        self.span = cs2span(self.center, self.size)

    def _inside(self, mesh, include_edges=True):
        """Returns a mask defining whether the points in ``mesh`` are inside 
        the Box region."""

        tmp_span = np.copy(self.span)
        if include_edges==True:
            tmp_span[:, 0] -= (tmp_span[:, 1] - tmp_span[:, 0])*fp_eps
            tmp_span[:, 1] += (tmp_span[:, 1] - tmp_span[:, 0])*fp_eps
        else:
            tmp_span[:, 0] += (tmp_span[:, 1] - tmp_span[:, 0])*fp_eps
            tmp_span[:, 1] -= (tmp_span[:, 1] - tmp_span[:, 0])*fp_eps

        return inside_box(tmp_span, mesh, include_zero_size=False)

class Sphere(Structure):
    """ Sphere structre.
    """
    def __init__(self, center, radius, material, name=None):
        """ Construct.

        Parameters
        ----------
        center : array_like
            (micron): x, y, z position of the center of the sphere.
        radius : float
            (micron) Radius of the sphere.
        material : Material
            Material of the structure.
        name : str, optional
            Custom name of the structure.
        """
        super().__init__(material, name)
        self.center = np.array(center, dtype=float_)
        self.radius = radius

    def _inside(self, mesh, include_edges=True):
        """Returns a mask defining whether the points in ``mesh`` are inside 
        the Sphere."""

        x, y, z = self.center
        r = self.radius * (1 + (include_edges - 0.5) * 2 * fp_eps)

        return np.where((x - mesh[0][:, np.newaxis, np.newaxis])**2 + 
                    (y - mesh[1][np.newaxis, :, np.newaxis])**2 + 
                    (z - mesh[2][np.newaxis, np.newaxis, :])**2 < r**2, 1, 0)

class Cylinder(Structure):
    """ Cylinder structre.
    """
    def __init__(self, center, axis, radius, height, material, name=None):
        """Construct.
        
        Parameters
        ----------
        center : array_like
            (micron): x, y, z position of the center of the sphere.
        axis : str
            ``'x'``, ``'y'``, or ``'z'``.
        radius : float
            (micron) Radius of the cylinder.
        height : float
            (micron) Height of the cylinder along its axis.
        material : Material
            Material of the structure.
        name : str, optional
            Custom name of the structure.    
        """
        super().__init__(material, name)
        self.center = np.array(center, dtype=float_)
        self.axis = axis
        self.radius = radius
        self.height = height

    def _inside(self, mesh, include_edges=True):
        """Returns a mask defining whether the points in ``mesh`` are inside 
        the Cylinder."""

        ax = xyz_dict[self.axis]
        d_cross = [0, 1, 2]
        d_cross.pop(ax)
        d_a = self.center[ax]
        d1, d2 = self.center[d_cross]
        r = self.radius * (1 + (include_edges - 0.5) * 2 * fp_eps)
        h = self.height * (1 + (include_edges - 0.5) * 2 * fp_eps)

        m = [mesh[0][:, np.newaxis, np.newaxis], 
            mesh[1][np.newaxis, :, np.newaxis],
            mesh[2][np.newaxis, np.newaxis, :]]
        m_a = m[ax]
        m1 = m[d_cross[0]]
        m2 = m[d_cross[1]]

        return np.where(((d1 - m1)**2 + (d2 - m2)**2 < r**2) *  
                            (np.abs(d_a - m_a) < h/2), 1, 0)

class PolySlab(Structure):
    """ A structure defined as polygon in x and y with a constnant extent in z.
    """
    def __init__(self, vertices, z_cent, z_size, material, name=None):
        """ Construct.
        
        Parameters
        ----------
        vertices : array_like
            (micron) Shape (N, 2) defining the polygon vertices in the xy-plane.
        z_cent : float
            (micron) Center of the polygonal slab in z.
        z_size : float
            (micron) Thickness of the slab in z.
        material : Material
            Material of the structure.
        name : str, optional
            Custom name of the structure.   
        """
        super().__init__(material, name)
        self.vertices = np.array(vertices, dtype=float_)
        self.z_cent = z_cent
        self.z_size = z_size

    def _inside(self, mesh, include_edges=True):
        """Returns a mask defining whether the points in ``mesh`` are inside 
        the PolySlab."""

        z_size = self.z_size * (1 + (include_edges - 0.5) * 2 * fp_eps)

        path = Path(self.vertices)
        xm, ym = np.meshgrid(mesh[0], mesh[1])
        points = np.vstack((xm.ravel(), ym.ravel())).T
        mask2d = path.contains_points(points).reshape(xm.shape).T
        maskz = (mesh[2] >= self.z_cent - z_size/2) * \
                (mesh[2] <= self.z_cent + z_size/2)

        return np.where(mask2d[:, :, np.newaxis] * 
                        maskz[np.newaxis, np.newaxis, :] > 0, 1, 0)

class GdsSlab(Structure):
    """ A structure defined through a GDSII cell imported through ``gdspy``. 
    All polygons and paths included in the cell are assumed to lie in the 
    xy-plane, with the same center and size in z, and made of the same material.
    """
    def __init__(self, gds_cell, z_cent, z_size, material, name=None):
        """Construct.
        
        Parameters
        ----------
        gds_cell : gdspy.Cell
            A GDS Cell containing all 2D polygons and paths, in microns.
        z_cent : float
            (micron) Center of the slab(s) in z.
        z_size : float
            (micron) Thickness of the slab(s) in z.
        material : Material
            Material of the structure.
        name : str, optional
            Custom name of the structure.
        """
        super().__init__(material, name)
        self.gds_cell = gds_cell
        self.z_cent = z_cent
        self.z_size = z_size

    def _inside(self, mesh, include_edges=True):
        """Returns a mask defining whether the points in ``mesh`` are inside 
        the PolySlab."""

        z_size = self.z_size * (1 + (include_edges - 0.5) * 2 * fp_eps)

        xm, ym = np.meshgrid(mesh[0], mesh[1])
        points = np.vstack((xm.ravel(), ym.ravel())).T
        mask2d = np.array(gdspy.inside(points, self.gds_cell.get_polygons())
                            ).reshape(xm.shape).T
        maskz = (mesh[2] >= self.z_cent - z_size/2) * \
                (mesh[2] <= self.z_cent + z_size/2)

        return np.where(mask2d[:, :, np.newaxis] * 
                        maskz[np.newaxis, np.newaxis, :] > 0, 1, 0)
