
import json
import time
import sys
from datetime import datetime

from .config import Config
from .httputils import post2, get2, delete2
from .s3utils import s3Client, keys


def newProject(taskParam, solverVersion=Config.SOLVER_VERSION, taskName=None):
    """ Create new project.
    
    Parameters
    ----------
    taskParam : dict
        Dictionary containing all simulation parameters, which can be generated 
        by ``Simulation.export()``.
    solverVersion : str, optional
        Version of the Tidy3D solver.
    
    Returns
    -------
    dict
        Project dictionary with simulation and task data.
    """
    if taskName == None:
        taskName = f'Task_{int(datetime.now().timestamp())}'

    return post2(f'fdtd/model/default/task', {
        'taskParam': json.dumps(taskParam),
        'solverVersion': solverVersion,
        'taskName': taskName
    })


def getProject(taskId):
    """ Get all project details from a given taskId.
    
    Parameters
    ----------
    taskId : str
        Task identification string.
    
    Returns
    -------
    dict
        Project dictionary with simulation and task data.
    """

    return get2(f'fdtd/task/{taskId}')

def deleteProject(taskId):
    """ Delete a project from a given taskId.
    
    Parameters
    ----------
    taskId : str
        Task identification string.
    
    Returns
    -------
    dict
        Project dictionary of the deleted project.
    """

    return delete2(f'fdtd/task/{taskId}')

def monitorProject(taskId):
    """Monitor the status of a given project every second. Function exits when 
    the exit status is either ``'success'`` or ``'error'``. 
    
    Parameters
    ----------
    taskId : str
        Task identification string.
    """
    status = ''
    while status not in ['success', 'error']:
        project = getProject(taskId)
        status = project['status']
        name = project['taskName']
        sys.stdout.write('\rProject "' + name + '" status: %s       '%status)
        sys.stdout.flush()
        time.sleep(.5)
        sys.stdout.write('\rProject "' + name + '" status: %s.      '%status)
        sys.stdout.flush()
        time.sleep(.5)
        sys.stdout.write('\rProject "' + name + '" status: %s..     '%status)
        sys.stdout.flush()
        time.sleep(.5)
        sys.stdout.write('\rProject "' + name + '" status: %s...    '%status)
        sys.stdout.flush()
        time.sleep(.5)

def getProjects():
    """ Get a list with all details of all projects of the current user. 
    
    Returns
    -------
    list
        A list of ``dict``, with one entry for every folder name. Each of those 
        can contain multiple projects whose corresponding data is listed in 
        the ``'children'`` entry.
    """

    return get2(f'fdtd/models')

def listProjects(Nprojects=None):
    """Print a summary of all projects of the current user, in chronological 
    order of submission.
    
    Parameters
    ----------
    Nprojects : None, optional
        If supplied, only the last ``Nprojects`` will be listed.
    """

    # w1 = 20
    # w2 = 14
    # w3 = 24
    # w4 = 38
    # print("Project ")
    # print("Sbumit time (UTC)".center(w1) + "|" + "Status".center(w2) + 
    #         "|" + "Task name".center(w3) + "|" + "Task ID".center(w4))
    # print("-"*(w1+w2+w3+w4+3))

    projects = getProjects()
    store_dict = {'submit_time': [],
                  'status': [],
                  'name': [],
                  'id': []}
    for pfolder in projects:
        for task in pfolder['children']:
            store_dict['submit_time'].append(task['submitTime'])
            store_dict['status'].append(task['status'])
            store_dict['name'].append(task['taskName'])
            store_dict['id'].append(task['taskId'])

    sort_inds = sorted(range(len(store_dict['submit_time'])),
                key=store_dict['submit_time'].__getitem__,
                reverse=True)
    for key in store_dict.keys():
        store_dict[key] = [store_dict[key][i] for i in sort_inds]

    if Nprojects is None or Nprojects > len(sort_inds):
        Nprojects = len(sort_inds)

    for ip in range(Nprojects):
        # print(store_dict['submit_time'][ip].center(w1) + "|" +
        #         store_dict['status'][ip].center(w2) + "|" + 
        #         store_dict['name'][ip].center(w3) + "|" + 
        #         store_dict['id'][ip].center(w4))
        print("Project name: %s"%store_dict['name'][ip])
        print("Task ID     : %s"%store_dict['id'][ip])
        print("Submit time : %s"%store_dict['submit_time'][ip])
        print("Status      : %s"%store_dict['status'][ip])
        print("-"*50)

def downloadResultsFile(taskId, src, target=None):
    """Download all the results recorded by simulation probes.
    
    Parameters
    ----------
    taskId : str
        Task ID of the project (after a successful run).
    src : str
        File to download. Valid file names are ``'probe_data.hdf5'`` and 
        ``'tidy3d.log'``.
    target : None, optional
        Filename to store locally. If ``None``, the same name as ``src`` 
        will be used.
    """
    if target is None:
        target = src
    if src is None:
        raise ValueError("'src' cannot be None.")
    
    try:
        project = getProject(taskId)
    except:
        raise RuntimeError("Unable to get project " + taskId)
    
    try:
        s3Client.download_file(Bucket=Config.STUDIO_BUCKET,
                           Filename=target,
                           Key='users/{0}/{1}/output/{2}'.format(keys['UserId'],
                           taskId, src))
    except:
        RuntimeError("Cannot retrieve requested file, check the file name and "
                    "make sure the project has run correctly. Current "
                    "project status is '%s'."%(project['status']))

def downloadResults(taskId, target_folder=''):
    """Download the results of a solver run, including a json file defining the 
    simulation, a single file containing all the probe data, and a log file.
    
    Parameters
    ----------
    taskId : str
        Task ID of the project (after a successful run).
    target_folder : str, optional
        Folder in which to download the files. Folder must exist. 
        Default is working folder. 
    """

    if len(target_folder) > 0:
        target_folder += '/'

    for fname in ['probe_data.hdf5', 'tidy3d.log']:
        downloadResultsFile(taskId, fname, target=target_folder+fname)

    project = getProject(taskId)
    with open(target_folder+'simulation.json', 'w') as sim_file:
        json.dump(json.loads(project['taskParam']), sim_file, indent=4)