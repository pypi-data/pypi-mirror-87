import json
import numpy as np

from .simulation import Simulation
from .json_ops import read_structures, read_sources, read_probes

def init_sim(js: dict, print_warnings=True):
    """ Initialize Simulation object based on JSON input dictionary `js`.
    """

    # Unit scalings
    if js['parameters']['unit_length'].lower() == "mm":
        scale_l = 1e3
    elif js['parameters']['unit_length'].lower() == "um":
        scale_l = 1
    elif js['parameters']['unit_length'].lower() == "nm":
        scale_l = 1e-3

    if js['parameters']['unit_frequency'].lower() == "thz":
        scale_f = 1e12
    elif js['parameters']['unit_frequency'].lower() == "ghz":
        scale_f = 1e9
    elif js['parameters']['unit_frequency'].lower() == "mhz":
        scale_f = 1e6

    if js['parameters']['unit_time'].lower() == "fs":
        scale_t = 1e-15
    elif js['parameters']['unit_time'].lower() == "ps":
        scale_t = 1e-12
    elif js['parameters']['unit_time'].lower() == "ns":
        scale_t = 1e-9

    # Parse simulation parameters
    js_params = js['parameters']

    # Simulation span
    x_cent, y_cent, z_cent = 0, 0, 0
    for d, dstr in zip([x_cent, y_cent, z_cent],
                        ["x_cent", "y_cent", "z_cent"]):
        if dstr in js_params.keys():
            d = js_params[dstr]

    sim_cent = scale_l*np.array([x_cent, y_cent, z_cent])
    sim_size = scale_l*np.array([js_params["x_span"], js_params["y_span"],
                                js_params["z_span"]])

    # Pml size
    Npml = np.array([[0, 0], [0, 0], [0, 0]])
    if "Npml" in js_params.keys():
        Npml = js_params["Npml"]
    else:
        # If Npml not set directly, we assume BCs are defined
        for (i, si) in enumerate(['xmin', 'xmax', 'ymin', 'ymax',
                                    'zmin', 'zmax']):
            if js_params[si+'_bc'].lower()=='pml':
                # set some default PML thickness
                Npml[np.unravel_index(i, Npml.shape)] = 12

    sim_params = {
            'center': sim_cent,
            'size': sim_size, 
            'resolution': js_params['resolution'],
            'run_time': js_params['run_time']*scale_t,
            'Npml': Npml 
            }

    sim = Simulation(**sim_params)

    if "objects" in js.keys():
        sim.add(read_structures(js, scale_l=scale_l))
    if "sources" in js.keys():
        sim.add(read_sources(js, scale_l, scale_f))
    if "probes" in js.keys():
        sim.add(read_probes(js, scale_l, scale_f))

    # Parse run parameters
    run_params = js['run_parameters']
    sim.init_run(**run_params, print_warnings=print_warnings)

    return sim