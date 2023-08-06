import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from .probe import TimeProbe, FreqProbe
from .material import Medium, PEC, PMC
from .constants import xyz_dict, xyz_list

def _eps_cmap(eps_r, alpha=1):
    grey = mpl.cm.get_cmap('Greys', 256)
    newgrey = grey(np.linspace(0, 1, 256))
    newgrey[:, 3] = alpha
    newgrey[0, 3] = 0
    bounds = np.hstack((-4e6, -2e6, 0, np.linspace(1, np.amax(eps_r)+1e-6, 256)))
    eps_cmap = np.vstack(([0, 0, 1, 1], [1, 0, 0, 1], [1, 1, 1, 0], newgrey))
    norm = mpl.colors.BoundaryNorm(boundaries=bounds, ncolors=259)

    return mpl.colors.ListedColormap(eps_cmap), norm, bounds

def _get_eps(structures, mesh):
    """ Compute the permittivity corresponding to a list of `structures` over a 
    given `mesh`. 
    
    Parameters
    ----------
    structures : list of Structure objects
    mesh : tuple of 3 1D arrays, or None
    
    Returns
    -------
    eps : np.ndarray
        Array of size (mesh[0].size, mesh[1].size, mesh[2].size) defining 
        the relative permittivity at each point.
    """

    Nx, Ny, Nz = [mesh[i].size for i in range(3)]

    eps = np.ones((Nx, Ny, Nz))

    # Apply all structures
    for structure in structures:
        if isinstance(structure.material, Medium):
            eps_struct = structure.material.eps
        elif isinstance(structure.material, PEC):
            eps_struct = -1e6
        elif isinstance(structure.material, PMC):
            eps_struct = -3e6
        mask = structure._inside(mesh)
        mnzero = mask > 0
        eps[mnzero] = (1-mask[mnzero])*eps[mnzero] + eps_struct*mask[mnzero]

    return eps

def _get_inside(objects, mesh):
    """ Get a mask defining points inside a list of objects.

    Parameters
    ----------
    objects : list of Structure, Source, or Probe objects
    mesh : tuple of 3 1D arrays, or None
    
    Returns
    -------
    mask : np.ndarray
        Array of size (mesh[0].size, mesh[1].size, mesh[2].size) where each 
        element is one if inside any of the objects, and zero otherwise. 
    """

    Nx, Ny, Nz = [mesh[i].size for i in range(3)]

    mask = np.zeros((Nx, Ny, Nz))

    for obj in objects:
        mtmp = obj._inside(mesh)
        mask[mtmp > 0] = 1

    return mask

def _plot_eps(eps_r, clim=None, ax=None, extent=None, 
                cbar=False, cax=None, alpha=1):

    if ax is None:
        fig, ax = plt.subplots(1, constrained_layout=True)

    cmap, norm, bounds = _eps_cmap(eps_r, alpha)

    im = ax.imshow(eps_r, interpolation='none', 
                norm=norm, cmap=cmap, origin='lower', extent=extent)

    if clim:
        im.set_clim(vmin=clim[0], vmax=clim[1])

    if cbar:
        if cax is not None:
            plt.colorbar(im, ax=ax, cax=cax, boundaries=bounds[3:])
        else:
            plt.colorbar(im, ax=ax, boundaries=bounds[3:])
        
    return im

def relative_eps(sim, normal='x', offset=0, ax=None, cbar=False, 
        sources=True, probes=True, pml=True):
    """ Plot the relative permittivity distribution in a 2D cross-section.
    
    Parameters
    ----------
    sim : Simulation
        Simulation object.
    normal : str
        ``'x'``, ``'y'``, or ``'z'``, axis normal to the cross-section plane.
    offset : float
        Position along the normal axis.
    ax : int, optional
        Matplotlib axis object to use for the plot. If ``None``, a new figure 
        is created.
    cbar : bool, optional
        Whether or not a colorbar should be added to the plot.
    sources : bool, optional
        Overlay the source positions.
    probes : bool, optional
        Overlay the probe positions.
    pml : bool, optional
        Overlay the pml regions.

    Note
    ----
    The plotting is discretized at the center positions of the grid and is for 
    illustrative purposes only. In the FDTD evolution, the Yee grid is used and 
    where the permittivity, source, and probe locations depend on the field 
    polarization.
    """

    grid = sim.grid

    if ax is None:
        fig, ax = plt.subplots(1, constrained_layout=True)

    # Get normal and cross-section axes indexes
    norm = xyz_dict[normal]
    cross = [0, 1, 2]
    cross.pop(norm)

    # Get centered mesh for permittivity discretization
    mesh = [[], [], []]
    ind = np.nonzero(offset < grid.mesh[norm])[0]
    if ind.size==0:
        raise ValueError("Plane offset outside of simulation domain.")
    else:
        ind = ind[0]
    mesh[norm] = np.array([grid.mesh[norm][ind]])
    mesh[cross[0]] = grid.mesh[cross[0]]
    mesh[cross[1]] = grid.mesh[cross[1]]

    eps_r = np.squeeze(_get_eps(sim.structures, mesh=mesh))

    # Get mesh for source and probe discretization
    if ind > 0:
        mesh_sp = [[], [], []]
        mesh_sp[norm] = grid.mesh[norm][ind-1:ind+1]
        mesh_sp[cross[0]] = mesh[cross[0]]
        mesh_sp[cross[1]] = mesh[cross[1]]

    # Plot and set axes properties
    extent = [grid.mesh[cross[0]][0], grid.mesh[cross[0]][-1], 
                    grid.mesh[cross[1]][0], grid.mesh[cross[1]][-1]]
    x_lab = xyz_list[cross[0]]
    y_lab = xyz_list[cross[1]]
    ax_tit = x_lab+y_lab + "-plane at " + xyz_list[norm] + "=%1.2f" % offset
    npml = sim.Npml[[cross[0], cross[1]], :]

    im = _plot_eps(eps_r.T, clim=None, ax=ax, extent=extent, cbar=cbar)
    ax.set_xlabel(x_lab)
    ax.set_ylabel(y_lab)
    ax.set_title(ax_tit)

    def squeeze_mask(mask, axis):
        inds = [slice(None), slice(None), slice(None)]
        inds[axis] = 1
        return np.squeeze(mask[tuple(inds)])

    if probes==True:
        prb_mask = squeeze_mask(_get_inside(sim.tprobes + sim.fprobes,
                                            mesh=mesh_sp), norm)
        prb_cmap = mpl.colors.ListedColormap(np.array([[0, 0, 0, 0],
                            [236/255, 203/255, 32/255, 0.3]]))
        ax.imshow(prb_mask.T, clim=(0, 1), cmap=prb_cmap, origin='lower',
                        extent=extent)

    if sources==True:
        src_mask = squeeze_mask(_get_inside(sim.sources, mesh=mesh_sp), norm)
        src_cmap = mpl.colors.ListedColormap(np.array([[0, 0, 0, 0],
                            [78/255, 145/255, 78/255, 0.2]]))
        ax.imshow(src_mask.T, clim=(0, 1), cmap=src_cmap, origin='lower',
                        extent=extent)

    if pml==True:
        pml_mask = np.squeeze(np.zeros((mesh[0].size, mesh[1].size,
                                                mesh[2].size)))
        N1, N2 = pml_mask.shape
        pml_mask[:npml[0, 0], :] = 1
        pml_mask[N1-npml[0, 1]:, :] = 1
        pml_mask[:, :npml[1, 0]] = 1
        pml_mask[:, N2-npml[1, 1]:] = 1
        pml_cmap = mpl.colors.ListedColormap(np.array([[0, 0, 0, 0],
                            [229/255, 127/255, 25/255, 0.2]]))
        ax.imshow(pml_mask.T, clim=(0, 1), cmap=pml_cmap, origin='lower',
                        extent=extent)

    return im

def source_time(source, ax=None):
    """Plot the time dependence of a given source.
    
    Parameters
    ----------
    source : Source
        Source object to plot.   
    """

    if source.tmesh is None:
        raise ValueError("Time mesh of source not yet set. Add the source to "
            "a Simulation object first.")

    if ax is None:
        fig, ax = plt.subplots(1)

    im = plt.plot(source.tmesh, source.Jt)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Amplitude [a. u.]")
    labels = ['Jx', 'Jy', 'Jz']
    ax.legend(labels)

    return im 

def _probe_slice(sim, probe, pind=None, normal=None, normal_ind=0, field='E',
                    val='re', comp='z'):

    if normal is None:
        dmin = np.argmin(probe.Pinds_end - probe.Pinds_beg)
        normal = ['x', 'y', 'z'][dmin]

    inds = {'x': 0, 'y': 1, 'z': 2}
    comp_ind = inds[comp]
    if field.lower()=='e':
        ftmp = probe.E[:, :, :, :, pind]
    elif field.lower()=='h':
        ftmp = probe.H[:, :, :, :, pind]

    if isinstance(probe, TimeProbe):
        tit_string = 't='+"%1.2e"%(sim.grid.tmesh[pind]*1e12)+'fs'
    elif isinstance(probe, FreqProbe):
        tit_string = 'f='+"%1.2e"%(probe.freqs[pind]*1e-12)+'THz'

    if val=='int':
        fvals = ftmp[0, :, :, :]**2 + ftmp[1, :, :, :]**2 + ftmp[2, :, :, :]**2
        ax_tit = "||E||^2"
    else:
        fvals = ftmp[comp_ind, :, :, :]
        ax_tit = val + "(E" + comp + ")"

    pbeg = probe.Pinds_beg
    pend = probe.Pinds_end

    if normal=='x':
        fvals = fvals[normal_ind, :, :]
        norm_pos = sim.grid.mesh[0][pbeg[0]+normal_ind]
        mesh = (np.array([norm_pos]), sim.grid.mesh[1][pbeg[1]:pend[1]],
                    sim.grid.mesh[2][pbeg[2]:pend[2]])
    elif normal=='y':
        fvals = fvals[:, normal_ind, :]
        norm_pos = sim.grid.mesh[1][pbeg[1]+normal_ind]
        mesh = (sim.grid.mesh[0][pbeg[0]:pend[0]], np.array([norm_pos]),
                    sim.grid.mesh[2][pbeg[2]:pend[2]])
    elif normal=='z':
        fvals = fvals[:, :, normal_ind]
        norm_pos = sim.grid.mesh[2][pbeg[2]+normal_ind]
        mesh = (sim.grid.mesh[0][pbeg[0]:pend[0]],
                    sim.grid.mesh[1][pbeg[1]:pend[1]], np.array([norm_pos]))

    eps_r = np.squeeze(_get_eps(sim.structures, mesh=mesh))

    grid_dict = {
            'x': (1, 2, 0, 'y', 'z'),
            'y': (0, 2, 1, 'x', 'z'),
            'z': (0, 1, 2, 'x', 'y'),
            }

    (d1, d2, dn, x_lab, y_lab) = grid_dict[normal]
    grid1 = sim.grid.mesh[d1][pbeg[d1]:pend[d1]]
    grid2 = sim.grid.mesh[d2][pbeg[d2]:pend[d2]]

    ax_tit += ', ' + tit_string
    ax_title = 'Probe ' + probe.name + ', ' + normal + '=' + \
                '%1.2eum\n'%norm_pos + ax_tit

    return (fvals, eps_r, norm_pos, grid1, grid2, x_lab, y_lab, ax_title)

def _plot_probe_2D(sim, probe, time_ind, normal, normal_ind, field,
                    val, comp, ax, cbar, eps, clim):

    (fvals, eps_r, _, grid1, grid2, x_lab, y_lab, ax_title) = _probe_slice(sim,
                    probe, time_ind, normal, normal_ind, field, val, comp)

    cmap = "RdBu"
    if val=='re':
        fvals = np.real(fvals)
    elif val=='im':
        fvals = np.imag(fvals)
    else:
        cmap = "magma"
        fvals = np.abs(fvals)

    fmax = np.amax(np.abs(fvals))
    if clim is None:
        if cmap=="RdBu":
            clim = (-fmax, fmax)
        else:
            clim = (0, fmax)

    # Consider using grid.mesh_b and grid.mesh_f as in viz.eps
    extent = [grid1[0], grid1[-1], grid2[0], grid2[-1]]

    if ax is None:
        fig, ax = plt.subplots(1, constrained_layout=True)

    im = ax.imshow(fvals.T, extent=extent, cmap=cmap, clim=clim, origin='lower')
    # im = 0
    if eps==True and (np.amax(eps_r) - np.amin(eps_r) > 1e-10):
        _plot_eps(eps_r.T, clim=None, ax=ax, extent=extent, cbar=False,
                        alpha=0.2)

    if cbar==True:
        plt.colorbar(im, ax=ax, shrink=0.8)

    ax.set_xlabel(x_lab)
    ax.set_ylabel(y_lab)
    ax.set_title(ax_title)

    return im

def tprobe_2D(sim, probe_ind, time_ind=-1, normal=None, normal_ind=0, field='E',
            val='re', comp='z', ax=None, cbar=False, clim=None, eps=True):
    """Plot a 2D cross-section of the field stored in a TimeProbe object at a 
    given time step.
    
    Parameters
    ----------
    sim : Simulation
        A simulation object.
    probe_ind : int
        Index of the time probe in ``sim``.
    time_ind : int, optional
        Index of the time step in the ``TimeProbe``. Default is the last step.
    normal : None, optional
        Axis normal to the 2D plane of plotting. If ``None``, the shortest 
        dimension is taken as the normal.
    normal_ind : int, optional
        Spatial index along the normal dimension, for 3D probes.
    field : str
        ``'E'`` or ``'H'`` field to plot.
    val : {'re', 'abs', 'int'}, optional
        Plot the real part (default), or the absolute value of a field 
        component, or the total field intensity. 
    comp : {'x', 'y', 'z'}, optional
        Component of the field to plot. If ``val`` is ``'int'``, this parameter 
        is irrelvant.
    ax : Matplotlib axis object, optional
        If None, a new figure is created. 
    cbar : bool, optional
        Add a colorbar to the plot.
    clim : List[float], optional
        Matplotlib color limit to use for plot.
    eps : bool, optional
        If True, also plot a contour of the underlying permittivity.
    
    Returns
    -------
    Matplotlib image object
    """

    probe = sim.tprobes[probe_ind]

    if field=='E':
        if probe.E.size==0:
            raise ValueError("Probe has no stored E-field values.")
    elif field=='H':
        if probe.H.size==0:
            raise ValueError("Probe has no stored H-field values.")
    else:
        raise ValueError("'field' can be 'E' or 'H'.")

    im = _plot_probe_2D(sim, probe, time_ind, normal, normal_ind, field,
                        val, comp, ax, cbar, eps, clim)

    return im

def fprobe_2D(sim, probe_ind, freq_ind=0, normal=None, normal_ind=0, field='E',
            val='re', comp='z', ax=None, cbar=False, clim=None, eps=True):
    """Plot a 2D cross-section of the field stored in a FreqProbe object at a 
    given frequency.
    
    Parameters
    ----------
    sim : Simulation
        A simulation object.
    probe_ind : int
        Index of the frequency probe in ``sim``.
    freq_ind : int, optional
        Index of the frequency in the ``FreqProbe``. Default is 0.
    normal : None, optional
        Axis normal to the 2D plane of plotting. If ``None``, the shortest 
        dimension is taken as the normal.
    normal_ind : int, optional
        Spatial index along the normal dimension, for 3D probes.
    field : str
        ``'E'`` or ``'H'`` field to plot.
    val : {'re', 'im', 'abs', 'int'}, optional
        Plot the real part (default), or the imaginary or absolute value of a 
        field component, or the total field intensity. 
    comp : {'x', 'y', 'z'}, optional
        Component of the field to plot. If ``val`` is ``'int'``, this parameter 
        is irrelvant.
    ax : Matplotlib axis object, optional
        If None, a new figure is created. 
    cbar : bool, optional
        Add a colorbar to the plot.
    clim : List[float], optional
        Matplotlib color limit to use for plot.
    eps : bool, optional
        If True, also plot a contour of the underlying permittivity.
    
    Returns
    -------
    Matplotlib image object
    """

    probe = sim.fprobes[probe_ind]

    if field=='E':
        if probe.E.size==0:
            raise ValueError("Probe has no stored E-field values.")
    elif field=='H':
        if probe.H.size==0:
            raise ValueError("Probe has no stored H-field values.")
    else:
        raise ValueError("'field' can be 'E' or 'H'.")

    im = _plot_probe_2D(sim, probe, freq_ind, normal, normal_ind, field,
                        val, comp, ax, cbar, eps, clim)

    return im

def export_fprobes(sim, folder_path, val='int', comp='z'):
    """Export png images of 2D cross-sections for all frequency probes in a 
    given simulation. For 3D probes, all 2D slices along the shortest dimension 
    are exported. 

    Parameters
    ----------
    sim : Simulation
        Simulation object with stored probe data after a run.
    folder_path : string
        Path in which the images will be exported.
    """

    fig = plt.figure(constrained_layout=True)

    for (ip, probe) in enumerate(sim.fprobes):
        Pdims = probe.Pinds_end - probe.Pinds_beg
        min_dir = np.argmin(Pdims)
        normal = ['x', 'y', 'z'][min_dir]

        for normal_ind in range(Pdims[min_dir]):
            for (find, _) in enumerate(probe.freqs):
                ax = fig.add_subplot(111)
                fprobe_2D(sim, ip, freq_ind=find, normal=normal,
                            normal_ind=normal_ind, val=val, comp=comp, ax=ax,
                            cbar=True, eps=True)
                fname = probe.name + "_find%d_nind%d.png"%(find, normal_ind)
                plt.savefig(folder_path+fname)
                plt.clf()

    plt.close(fig)
