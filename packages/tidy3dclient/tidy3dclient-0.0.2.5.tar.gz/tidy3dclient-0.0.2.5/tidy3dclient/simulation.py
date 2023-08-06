import numpy as np
import json
import h5py

from .utils import listify, cs2span, intersect_box, check_3D_lists
from .constants import int_, float_, fp_eps
from .structure import Structure, Box
from .source import Source, PlaneSource
from .probe import Probe, TimeProbe, FreqProbe
from .grid import Grid
from . import PEC, PMC
from .json_ops import write_parameters, write_structures, write_sources, \
                        write_probes

class Simulation(object):
    """
    Main class for building a simulation model.
    """

    def __init__(self,
                size,
                center=[0., 0., 0.],
                resolution=None,
                mesh_step=None,
                structures=[],
                sources=[],
                probes=[],
                symmetries=[0, 0, 0],
                pml_layers=[0, 0, 0],
                run_time=0.,
                courant=0.9,
                verbose=True
                ):
        """
        Parameters
        ----------
        center : list or np.ndarray, optional
            (micron) 3D vector defining the center of the simulation domain.
        size : list or np.ndarray, optional
            (micron) 3D vector defining the size of the simulation domain.
        resolution : float or array_like of float, optional
            (1/micron) Number of pixels per micron, or a 3D vector defining the 
            number of pixels per mircon in x, y, and z seprately.
        mesh_step : float or array_like of float, optional
            (micron) Step size in all directions, or a 3D vector defining the 
            step size in x, y, and z seprately. If provided, ``mesh_step`` 
            overrides the ``resolution`` parameter, otherwise 
            ``mesh_step = 1/resolution``.
        structures : Structure or a list of Structure objects, optional
            Empty list (default) means vacuum. 
        sources : Source or a list of Source objects, optional
            Source(s) to be added to the simulation.
        probes : Probe or a list of Probe objects, optional
            Probe(s) to be added to the simulation.
        symmetries : list of int, optional
            List of three elements defining reflection symmetry across a plane 
            bisecting the simulation domain normal to the x-, y-, and z-axis, 
            respectively. Each element can be ``0`` (no symmetry), ``1`` 
            (even, i.e. 'PMC' symmetry) or ``-1`` (odd, i.e. 'PEC' symmetry). 
            Note that the vectorial nature of the fields must be taken into 
            account to correctly determine the symmetry value.
        pml_layers : list of int, optional
            List of three elements defining the number of PML layers on both 
            sides of the simulation domain along x, y, and z. When set to ``0`` 
            (default), periodic boundary conditions are applied.
        run_time : float, optional
            (second) Total electromagnetic evolution time.
        courant : float, optional
            Courant stability factor, must be smaller than 1.
        verbose : bool, optional
            Print helpful messages regarding the simulation.
        """

        check_3D_lists(center=listify(center), size=listify(size),
                            symmetries=listify(symmetries),
                            pml_layers=listify(pml_layers))

        self.verbose = verbose
        self._print("Initializing simulation...")

        self.center = np.array(center, dtype=float_)
        self.size = np.array(size, dtype=float_)
        self.span = cs2span(self.center, self.size)
    
        # Space and time grid
        if mesh_step is None:
            if resolution is None:
                raise ValueError("Either 'mesh_step' or 'resolution' must be "
                                "set.")
            mesh_step = 1/np.array(resolution)
        else:
            if resolution is not None:
                self._print("Note: parameter 'mesh_step' overrides "
                            "'resolution'.")
        self.grid = Grid(self.span, mesh_step, symmetries, courant)
        self._print("Simulation domain in number of pixels: "
                    "%d, %d, %d."%(self.grid.Nxyz[0], self.grid.Nxyz[1], 
                                    self.grid.Nxyz[2]))

        # Computational domain including symmetries, if any
        self.span_sym = np.copy(self.span)
        self.Nxyz_sym = np.copy(self.grid.Nxyz)
        for d, sym in enumerate(symmetries):
            if sym==-1:
                self.span_sym[d, 0] += self.size[d]/2
                self.Nxyz_sym[d] = self.Nxyz_sym[d]//2
            elif sym==1:
                self.span_sym[d, 0] += self.size[d]/2 - self.grid.res[d]
                self.span_sym[d, 1] += self.grid.res[d]
                self.Nxyz_sym[d] = self.Nxyz_sym[d]//2 + 2
        # Print new size, if there are any symmetries
        if np.any(np.array(symmetries)!=0):
            self._print("Computation domain (after symmetries): "
                    "%d, %d, %d."%(self.Nxyz_sym[0], self.Nxyz_sym[1], 
                                    self.Nxyz_sym[2]))

        # Print resolution, set and print run time
        self._print("Mesh step (micron): %1.2e, %1.2e, %1.2e."%(
                        self.grid.res[0], self.grid.res[1], self.grid.res[2]))
        self._set_run_time(run_time)
        self.courant = courant
        self._print("Total number of time steps: %d."%(self.Nt))
        self._check_size()

        # Materials and indexing populated when adding ``Structure`` objects.
        self._mat_inds = [] # material index of each structure
        self._materials = [] # list of materials included in the simulation
        # Structures, sources and probes
        self._structures = []
        self._sources = []
        self._tprobes, self._fprobes = [], []
        # Structures and material indexing for symmetry boxes
        self._structures_sym = [] # PEC/PMC boxes added for symmetry
        self._mat_inds_sym = []
        
        self.add(structures)
        self.add(sources)
        self.add(probes)
        self._add_symmetries(symmetries)

        # Set PML size and compute parameters
        self.pml_layers = listify(pml_layers)
        self.Npml = np.vstack((pml_layers, pml_layers)).astype(int_).T

        # JSON file from which the simulation is loaded
        self.fjson = None

    def __repr__(self):
        rep = "Tidy3D Simulation:\n"
        rep += "center     = [" + ' '.join(["%1.4f"%c 
                                    for c in self.center]) + "] \n"
        rep += "size       = [" + ' '.join(["%1.4f"%s 
                                    for s in self.size]) + "] \n"
        rep += "mesh_step  = [" + ' '.join(["%1.4f"%r
                                    for r in self.grid.res]) + "] \n"
        rep += "run_time   = %1.2e\n"%self.run_time
        rep += "symmetries = [" + ' '.join(["%d"%s 
                                    for s in self.symmetries]) + "] \n"
        rep += "pml_layers = [" + ' '.join(["%d"%p
                                    for p in self.pml_layers]) + "] \n\n"

        rep += "Number of time points      : %d\n"%self.Nt
        rep += "Number of pixels in x, y, z: %d, %d, %d\n"%(self.grid.Nx,
                                            self.grid.Ny, self.grid.Nz)
        rep += "Number of pixels including \n" +\
               "symmetries                 : %d, %d, %d\n"%(self.Nxyz_sym[0],
                                            self.Nxyz_sym[1], self.Nxyz_sym[2])
        rep += "Number of strictures       : %d\n"%len(self._structures)
        rep += "Number of sources          : %d\n"%len(self.sources)
        rep += "Number of time probes      : %d\n"%len(self.tprobes)
        rep += "Number of frequency probes : %d\n"%len(self.fprobes)

        return rep

    @property
    def materials(self):
        """ List conaining all materials included in the simulation."""
        return self._materials

    @property
    def mat_inds(self):
        """ List conaining the material index in ``materials`` of every 
        ``structure``. """
        return self._mat_inds + self._mat_inds_sym

    @property
    def structures(self):
        """ List conaining all Structure objects. """
        return self._structures + self._structures_sym

    @structures.setter
    def structures(self, new_struct):
        # Make a list if a single object was given.
        self.add(new_struct)

    @property
    def sources(self):
        """ List conaining all Source objects. """
        return self._sources

    @sources.setter
    def sources(self, new_sources):
        # Make a list if a single object was given.
        self.add(new_sources)

    @property
    def tprobes(self):
        """ List conaining all TimeProbe objects. """
        return self._tprobes

    @tprobes.setter
    def tprobes(self, new_probes):
        # Make a list if a single object was given.
        self.add(new_probes)

    @property
    def fprobes(self):
        """ List conaining all FreqProbe objects. """
        return self._fprobes

    @fprobes.setter
    def fprobes(self, new_probes):
        # Make a list if a single object was given.
        self.add(new_probes)

    def _print(self, message):
        if self.verbose==True:
            print(message)

    def _check_size(self):
        Np = np.prod(self.Nxyz_sym)
        if self.Nt > 1e8:
            raise RuntimeError("Time steps %1.2e exceed current limit 1e8, "
                "reduce 'run_time' or increase the spatial mesh step."%self.Nt)

        if Np > 1e10:
            raise RuntimeError("Total number of grid points %1.2e exceeds "
                "current limit 1e10, increase the mesh step or decrease the "
                "size of the simulation domain."%Np)

        if Np*self.Nt > 1e15:
            raise RuntimeError("Total number of grid points times time steps "
                "%1.2e exceeds current limit 1e15, increase the mesh step or "
                "decrease the size or 'run_time' of the simulation."%Np*self.Nt)

    def _add_structure(self, structure):
        """ Adds a Structure object to the list of structures and to the 
        permittivity array. """
        self._structures.append(structure)
        if structure.name is None:
            structure.name = 'obj' + str(len(self.structures))

        try:
            mind = self.materials.index(structure.material)
            self._mat_inds.append(mind)
        except ValueError:
            if len(self.materials) < 200:
                self._materials.append(structure.material)
                self._mat_inds.append(len(self.materials)-1)
            else:
                raise RuntimeError("Maximum 200 distinct materials allowed.")

    def _add_source(self, source):
        """ Adds a Source object to the list of sources.
        """
        if isinstance(source, PlaneSource):
            # Make the PlaneSource span the whole simulation
            source._sim_span(self.span)

        source._get_Jt(self.grid.tmesh)
        self._sources.append(source)
        if source.name is None:
            source.name = 'source' + str(len(self.sources))

    def _add_probe(self, probe):
        """ Adds a time or frequency domain Probe object to the 
        corresponding list of probes.
        """
        span_in = intersect_box(self.span_sym, probe.span)
        size_in = span_in[:, 1] - span_in[:, 0]
        if np.any(size_in < 0):
            Np = 0
        else:
            Np = np.prod([int(s)/self.grid.res[d] + 1 
                    for (d, s) in enumerate(size_in)])

        if isinstance(probe, TimeProbe):
            self._tprobes.append(probe)
            if probe.name is None:
                probe.name = 'tprobe' + str(len(self.tprobes))
            probe._set_tmesh(self.grid.tmesh)
            memGB = Np*probe.Nt*4*3*len(probe.field)/1e9
            if memGB > 10:
                raise RuntimeError("Estimated time probe size %1.2f GB "
                "exceeds current limit of 10GB per probe. Decrease probe size "
                "or the time interval using 't_start' and 't_stop'."%memGB)

        elif isinstance(probe, FreqProbe):
            self._fprobes.append(probe)
            if probe.name is None:
                probe.name = 'fprobe' + str(len(self.fprobes))
            memGB = Np*len(probe.freqs)*4*3*len(probe.field)/1e9

            if memGB > 10:
                raise RuntimeError("Estimated frequency probe size %1.2f GB "
                "exceeds current limit of 10GB per probe. Decrease probe size "
                "or the number of frequencies."%memGB)

        self._print("Estimated data size of probe %s: %1.4fGB."%(probe.name,
                                                                memGB))

    def _add_symmetries(self, symmetries):
        """ Add all symmetries as PEC or PMC boxes.
        """
        self.symmetries = listify(symmetries)
        for dim, sym in enumerate(symmetries):
            if sym not in [0, -1, 1]:
                raise ValueError ("Reflection symmetry values can be 0 (no "
                                "symmetry), 1, or -1.")
            elif sym==1 or sym==-1:
                sym_cent = np.copy(self.center)
                sym_size = np.copy(self.size)
                sym_cent[dim] -= self.size[dim]/2
                sym_size[dim] = sym_size[dim] + fp_eps 
                sym_mat = PEC if sym==-1 else PMC
                self._structures_sym.append(Box(center=sym_cent,
                                                size=sym_size,
                                                material=sym_mat,
                                                name='sym%d'%dim))
                try:
                    mind = self.materials.index(sym_mat)
                    self._mat_inds_sym.append(mind)
                except ValueError:
                    self._materials.append(sym_mat)
                    self._mat_inds_sym.append(len(self.materials)-1)

    def _pml_config(self):
        """Set the CPML parameters. Default configuration is hard-coded. This 
        could eventually be exposed to the user, or, better, named PML profiles 
        can be created.
        """
        cfs_config = {'sorder': 3, 'smin': 0., 'smax': None, 
                    'korder': 3, 'kmin': 1., 'kmax': 3., 
                    'aorder': 1, 'amin': 0., 'amax': 0}
        return cfs_config

    def _set_run_time(self, run_time):
        """ Set the total time (in seconds) of the simulated field evolution.
        """
        self.run_time = run_time
        self.grid.set_tmesh(self.run_time)
        self.Nt = np.int(self.grid.tmesh.size)

    def add(self, objects):
        """
        Add a list of objects. Can contain structures, sources, and/or probes.
        """

        for obj in listify(objects):
            if isinstance(obj, Structure):
                self._add_structure(obj)
            elif isinstance(obj, Source):
                self._add_source(obj)
            elif isinstance(obj, Probe):
                self._add_probe(obj)

    def load_results(self, dfile):
        """Load the probe data recorded from a Tidy3D run. The simulation 
        object stores a list of all TimeProbes and all FreqProbes 
        (``Simulation.tprobes`` and ``Simulation.fprobes``, respectively). 
        The requested fields of each probe ('E' and 'H') are then stored as 
        arrays of size ``[pol, indx, indy, indz, inds]``, where ``pol`` is the 
        polarization component and ``inds`` is either the time or the frequency 
        index.
        
        Parameters
        ----------
        dfile : str
            Path to the file containing the simulation results.
        """

        pfile = h5py.File(dfile, "r")
        for (ip, probe) in enumerate(self.tprobes + self.fprobes):
            if isinstance(probe, TimeProbe):
                pname = "tprobe_" + probe.name
            elif isinstance(probe, FreqProbe):
                pname = "fprobe_" + probe.name
            probe._load_fields(pfile[pname]["indspan"][0, :],
                            pfile[pname]["indspan"][1, :],
                            np.array(pfile[pname]["E"]),
                            np.array(pfile[pname]["H"]), 
                            self.symmetries, self.grid.Nxyz)
            probe._xmesh = np.array(pfile[pname]["xmesh"])
            probe._ymesh = np.array(pfile[pname]["ymesh"])
            probe._zmesh = np.array(pfile[pname]["zmesh"])

        pfile.close()

    def export(self):
        """Return a dictionary with all simulation parameters and objects.
        """
        
        js = {}
        js["parameters"] = write_parameters(self)
        js["objects"], js["materials"] = write_structures(self.structures,
                                            self.materials, self.mat_inds)
        js["sources"] = write_sources(self.sources)
        js["probes"] = write_probes(self.tprobes)
        js["probes"] += write_probes(self.fprobes)

        return js

    def export_json(self, fjson):
        """Export the simulation to a JSON file.
        
        Parameters
        ----------
        fjson : str
            JSON file name.
        """
        
        self.fjson = fjson
        with open(fjson, 'w') as json_file:
            json.dump(self.export(), json_file, indent=4)