import numpy as np

from .constants import int_, float_, EPSILON_0

class Medium(object):
    """
    Base class for a custom defined material.
    """

    def __init__(self, epsilon=1., sigma=0, name=None):
        """ Define a (conductive) material. When ``sigma=0`` (default), this is 
        an isotropic, lossy dielectric.
        
        Parameters
        ----------
        epsilon : float, optional
            Real part of the relative permittivity. Default is vacuum.
        sigma : float, optional
            (S/micron) Electric conductivity, s.t. 
            ``Im(eps(omega)) = sigma/omega``, where ``eps(omega)`` is the 
            complex permittivity at frequency omega.
        """
        self.eps = epsilon
        self.sigma = sigma
        self.name = None if name is None else str(name)

    @classmethod
    def from_nk(cls, n, k, freq, name=None):
        """ Define a material through the real and imaginary part of the 
        refractive index at a given frequency.

        Parameters
        ----------
        n : float
            Real part of the refractive index.
        k : float
            Imaginary part of the refractive index.
        freq : float
            Frequency in Hetz
        name : str, optional
            Custom name of the material.
        """
        eps_real = n**2 - k**2
        eps_imag = 2*n*k
        
        sigma = 2*np.pi*freq*eps_imag*EPSILON_0
        return cls(eps_real, sigma, name)

class PEC(object):
    """ Perfect electric conductor. All tangential electric fields vanish.
    """
    def __init__(self, name='PEC'):
        """ Construct.
        name : str, optional
            Custom name of the material.
        """
        self.name=name

class PMC(object):
    """ Perfect magnetic conductor. All tangential magnetic fields vanish.
    """
    def __init__(self, name='PMC'):
        """ Construct.
        name : str, optional
            Custom name of the material.
        """
        self.name=name

