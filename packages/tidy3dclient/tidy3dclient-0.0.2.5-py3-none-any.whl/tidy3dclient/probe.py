import numpy as np

from .utils import listify, inside_box, cs2span, check_3D_lists
from .constants import int_, float_, fp_eps

class Probe(object):

    def __init__(self, center, size, field, name=None):
        check_3D_lists(center=listify(center), size=listify(size))
        self.center = np.array(center)
        self.size = np.array(size)
        self.span = cs2span(self.center, self.size)
        self.field = []
        for f in listify(field):
            if f.lower() in ['e', 'h']:
                self.field.append(f.lower())
            else:
                raise ValueError("Unrecognized field %s. "%f + 
                    "Valid values are 'E' and 'H'.")

        self.name = None if name is None else str(name)

        # Everything below is set after a run of store_Pvals() or load_fields()
        self.data = False # To be set to True after data is loaded
        self._E = np.empty((3, 0, 0, 0, 0), dtype=float_)
        self._H = np.empty((3, 0, 0, 0, 0), dtype=float_)
        self._xmesh = np.empty((0, ), dtype=float_)
        self._ymesh = np.empty((0, ), dtype=float_)
        self._zmesh = np.empty((0, ), dtype=float_)
        self.Pinds = np.empty((0, 3), dtype=int_)
        # Indexes defining the span of the Probe in the simulation grid in 
        # which it is embedded. 
        self.Pinds_beg = np.zeros((3, ), dtype=int_)
        self.Pinds_end = np.zeros((3, ), dtype=int_)

    @property
    def E(self):
        """ Electric field stored in the probe, if it was requested and after 
        the probe data has been loaded.
        """
        return self._E

    @property
    def H(self):
        """ Magnetic field stored in the probe, if it was requested and after 
        the probe data has been loaded.
        """
        return self._H

    @property
    def xmesh(self):
        """ Mesh along the x-axis over which the fields values are stored.
        """
        return self._xmesh

    @property
    def ymesh(self):
        """ Mesh along the y-axis over which the fields values are stored.
        """
        return self._ymesh

    @property
    def zmesh(self):
        """ Mesh along the z-axis over which the fields values are stored.
        """
        return self._zmesh
    

    def _inside(self, mesh):
        """ Get a mask equal to one if a point is inside the probe region, 
        and zero if outside.
        
        Parameters
        ----------
        mesh : 3-tuple
            Defines the x, y, and z mesh. 
        """
        return inside_box(self.span, mesh, include_zero_size=True)

    def _get_Pinds(self, mesh):
        """ Get indexes of the points at which the fields are to be recored.
        
        Parameters
        ----------
        mesh : 3-tuple
            Defines the x, y, and z mesh. 
        
        Returns
        -------
        Pinds : np.ndarray
            An array of shape (Np, 3), where Np is the total number of mesh 
            points in the probe region.
        """
        mask = self._inside(mesh)
        if np.nonzero(mask)[0].size==0: 
            return np.zeros((0, 3), dtype=int_)

        return np.array(np.nonzero(mask), dtype=int_).T

    def _store_Pvals(self, Pvals, Pinds, field):
        """ Store the raw probe values returned by the solver.
        
        Parameters
        ----------
        Pvals : np.ndarray
            An array of shape ``(Np, 3, Nsample)``, where ``Np`` is the total 
            number of probe points, and ``Nsample`` is either the number of 
            time steps in a ``TimeProbe``, or the number of requested 
            frequencies in a ``FreqProbe``.
        Pinds : np.ndarray
            An array of shape ``(Np, 3)`` giving the x, y, and z index for each 
            point in the simulation grid.

        Note
        ----
        ``Probe.Pvals`` is stored in the format ``(3, indx, indy, indz, ind)``, 
        where ``ind`` is either a time or a frequency index.
        """

        self.Pinds = Pinds
        self.Pinds_beg = np.amin(Pinds, axis = 0)
        self.Pinds_end = np.amax(Pinds, axis = 0) + 1
        Pdims = self.Pinds_end - self.Pinds_beg
        if field.lower()=='e':
            self._E = np.zeros((3, Pdims[0], Pdims[1], Pdims[2], 
                        Pvals.shape[2]), dtype=Pvals.dtype)
            for ipol in range(3):
                self._E[ipol, Pinds[:, 0]-self.Pinds_beg[0],
                    Pinds[:, 1]-self.Pinds_beg[1],
                    Pinds[:, 2]-self.Pinds_beg[2], :] = Pvals[:, ipol, :]
        elif field.lower()=='h':
            self._H = np.zeros((3, Pdims[0], Pdims[1], Pdims[2], 
                        Pvals.shape[2]), dtype=Pvals.dtype)
            for ipol in range(3):
                self._H[ipol, Pinds[:, 0]-self.Pinds_beg[0],
                    Pinds[:, 1]-self.Pinds_beg[1],
                    Pinds[:, 2]-self.Pinds_beg[2], :] = Pvals[:, ipol, :]
        self.data = True

    def _load_fields(self, inds_beg, inds_end, E, H, symmetries, Nxyz):
        """ Load the fields returned by the solver. This also applies any 
        symmetries that were present in the simulation.
        """

        # By default just store index and field values, unless changed below
        self.Pinds_beg = inds_beg
        self.Pinds_end = inds_end
        self._E = E
        self._H = H

        # Auxiliary variable for slicing along a given axis
        slices = (slice(None), slice(None), slice(None),
                        slice(None), slice(None))

        for dim, sym in enumerate(symmetries):

            # Auxiliary variable for symmetry eigenvalue along current axis
            svals = np.ones((3, 1, 1, 1, 1))
            svals[dim] = -1

            if sym==-1 and inds_beg[dim]==0:
                self.Pinds_beg[dim] = Nxyz[dim]//2 - inds_end[dim]
                self.Pinds_end[dim] = Nxyz[dim]//2 + inds_end[dim]
                sl = list(slices)
                sl[dim+1] = slice(-1, None, -1)
                if E.size > 0:
                    self._E = np.concatenate((-svals*self.E[tuple(sl)],
                                self.E), axis=dim+1)
                if H.size > 0:
                    self._H = np.concatenate((svals*self.H[tuple(sl)],
                                self.H), axis=dim+1)

            if sym==1 and inds_beg[dim]==0:
                ibeg = 1
                iend = min(inds_end[dim], Nxyz[dim]//2+1)
                self.Pinds_beg[dim] = Nxyz[dim]//2 - (iend - ibeg)
                self.Pinds_end[dim] = Nxyz[dim]//2 + (iend - ibeg)
                sl1 = list(slices)
                sl1[dim+1] = slice(iend-1, ibeg-1, -1)
                sl2 = list(slices)
                sl2[dim+1] = slice(ibeg, iend)  
                if E.size > 0:
                    self._E = np.concatenate((svals*self.E[tuple(sl1)],
                                self.E[tuple(sl2)]), axis=dim+1)
                if H.size > 0:
                    self._H = np.concatenate((-svals*self.H[tuple(sl1)],
                                self.H[tuple(sl2)]), axis=dim+1)
        self.data = True

class TimeProbe(Probe):
    """Probe recording the time-domain fields within a 3D region.
    """

    def __init__(self, center, size, t_start=0, t_stop=None, 
                    field=['E'], name=None):
        """ Construct.
        
        Parameters
        ----------
        center : array_like
            (micron) x, y, and z position of the center of the Probe.
        size : array_like
            (micron) Size in x, y, and z.
        t_start : float, optional
            (second) Starting time of field recording.
        t_stop : float, optional
            (second) Stopping time of field recording. If ``None``, record 
            until the end of the simulation.
        field : list, optional
            List of fields to be recorded. Valid values are ``'E'`` and ``'H'``.
        name : str, optional
            Custom name of the probe.

        Note
        ----
        Time probes can result in very large amounts of data if defined over 
        a large spatial region. Recommended usage is either recording the full 
        time evolution of a single point in space, or using ``t_start`` and 
        ``t_stop`` to record just a few time steps of a larger region. 
        """
        super().__init__(center, size, field)
        self.t_start = t_start
        self.t_stop = t_stop
        self.Nt = 0
        self._tmesh = np.empty((0, ), dtype=float_)

    def __repr__(self):
        rep = "Tidy3D TimeProbe:\n"
        rep += "name     = %s\n"%self.name
        rep += "center   = [" + ' '.join(["%1.4f"%c 
                                    for c in self.center]) + "] \n"
        rep += "size     = [" + ' '.join(["%1.4f"%s 
                                    for s in self.size]) + "] \n"
        rep += "t_start  = %1.2e,\n"%self.t_start
        if self.t_stop is None:
            rep += "t_stop   = None\n\n"
        else:
            rep += "t_stop   = %1.2e,\n\n"%self.t_stop

        rep += "Number of time points: %d\n"%self.Nt
        rep += "Store E:  %s\n"%('e' in self.field)
        rep += "Store H:  %s\n"%('h' in self.field)
        if self.data==False:
            rep += "Has data: False"
        else:
            rep += "Has data: xmesh, ymesh, zmesh, tmesh, " + ", ".join(
                                            [f.upper() for f in self.field])
        return rep


    @property
    def tmesh(self):
        """ Mesh in time over which the field values are stored.
        """
        return self._tmesh

    def _set_tmesh(self, tmesh):
        if self.t_stop is None:
            self.t_stop = tmesh[-1]*(1+fp_eps)
            self.tind_end = tmesh.size
        else:
            tend = np.nonzero(tmesh <= self.t_stop)[0]
            if tend.size > 0:
                self.tind_end = tend[-1] + 1
            else:
                self.tind_end = 0
        tbeg = np.nonzero(tmesh[0:self.tind_end] >= self.t_start)[0]
        if tbeg.size > 0:
            self.tind_beg = tbeg[0]
        else:
            self.tind_beg = self.tind_end
        self._tmesh = tmesh[self.tind_beg:self.tind_end]
        self.Nt = self.tind_end - self.tind_beg

class FreqProbe(Probe):
    """Probe recording a Fourier transform of the fields  
    within a 3D region, for a given list of frequencies.
    """
    
    def __init__(self, center, size, freqs, field=['E'], name=None):
        """ Construct.

        Parameters
        ----------
        center : array_like
            (micron) x, y, and z position of the center of the Probe.
        size : array_like
            (micron) Size in x, y, and z.
        freqs : float or list of float
            Frequencies at which the fields are sampled.
        field : list, optional
            List of fields to be recorded. Valid values are ``'E'`` and ``'H'``.
        name : str, optional
            Custom name of the probe.
        """

        super().__init__(center, size, field, name)
        self._freqs = listify(freqs)

    def __repr__(self):
        rep = "Tidy3D FreqProbe:\n"
        rep += "name     = %s\n"%self.name
        rep += "center   = [" + ' '.join(["%1.4f"%c 
                                    for c in self.center]) + "] \n"
        rep += "size     = [" + ' '.join(["%1.4f"%s 
                                    for s in self.size]) + "] \n"
        rep += "freqs    = [" + ' '.join(["%1.2e"%f 
                                    for f in self.freqs]) + "] \n\n"

        rep += "Store E:  %s\n"%('e' in self.field)
        rep += "Store H:  %s\n"%('h' in self.field)
        if self.data==False:
            rep += "Has data: False"
        else:
            rep += "Has data: xmesh, ymesh, zmesh, freqs, " + ", ".join(
                                            [f.upper() for f in self.field])

        return rep

    @property
    def freqs(self):
        """ List of frequencies over which the DFT fields are computed.
        """
        return self._freqs