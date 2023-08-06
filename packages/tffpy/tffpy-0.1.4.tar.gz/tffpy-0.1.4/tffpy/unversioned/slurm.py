# -*- coding: utf-8 -*-
# ######### COPYRIGHT #########
# Credits
# #######
#
# Copyright(c) 2020-2020
# ----------------------
#
# * Laboratoire d'Informatique et Systèmes <http://www.lis-lab.fr/>
# * Université d'Aix-Marseille <http://www.univ-amu.fr/>
# * Centre National de la Recherche Scientifique <http://www.cnrs.fr/>
# * Université de Toulon <http://www.univ-tln.fr/>
#
# Contributors
# ------------
#
# * `Valentin Emiya <mailto:valentin.emiya@lis-lab.fr>`_
# * `Ama Marina Krémé <mailto:ama-marina.kreme@lis-lab.fr>`_
#
# This package has been created thanks to the joint work with Florent Jaillet
# and Ronan Hamon on other packages.
#
# Description
# -----------
#
# Time frequency fading using Gabor multipliers
#
# Version
# -------
#
# * tffpy version = 0.1.4
#
# Licence
# -------
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ######### COPYRIGHT #########
"""

.. moduleauthor:: Valentin Emiya
"""
import configparser
import importlib
import logging
import os
from pathlib import Path
import stat
import sys


def generate_slurm_script(script_file_path, xp_var_name, task_ids=None,
                          n_simultaneous_jobs=10, slurm_walltime='02:00:00',
                          activate_env_command=None, use_gpu=False):
    """Generate a script to launch an experiment using Slurm.

    Tasks are divided into batches that are executed by oar jobs.

    The resulting script is written in the experiment folder, and the command
    to launch the jobs with Slurm is displayed in the terminal.

    An example script illustrating how to use
    :func:`yafe.utils.generate_slurm_script` is available in the corresponding
    :ref:`tutorial <tutorial_oar>`.

    Parameters
    ----------
    script_file_path : str
        File path to the script that defines the experiment.
    xp_var_name : str
        Name of the variable containing the experiment in the script.
    task_ids : list
        List of tasks ids to run.
        If ``task_ids`` is ``None``, the list of pending tasks of the
        experiment is used.
    batch_size : int
        Number of tasks run in each batch.
    slurm_walltime : str
        Wall time for each Slurm job ('HH:MM:SS').
    activate_env_command : str or None
        Optional command that must be run to activate a Python virtual
        environment before launching the experiment.
        Typically, this is a command of the form
        ``source some_virtual_env/bin/activate`` when using virtualenv and
        ``source activate some_conda_env`` when using conda.
        If ``activate_env_command`` is ``None``, no virtual environment is
        activated.
    use_gpu : bool
        Flag specifying if a gpu ressource is needed when running the
        experiment.
    """
    script_file_path = Path(script_file_path)
    script_dir = script_file_path.parent
    script_name = script_file_path.stem

    sys.path.append(str(script_dir))
    mod = importlib.import_module(script_name)
    xp = getattr(mod, xp_var_name)
    script_dir = xp.xp_path / 'scripts'
    script_dir.mkdir(exist_ok=True)
    for f in script_dir.glob('*.sh'):
        os.remove(f)
    # script_dir.rm

    if task_ids is None:
        task_ids = xp.get_pending_task_ids()

    # split and save the tasks
    # task_ids = list(map(str, task_ids))
    # batches = [
    #     task_ids[i:(i + batch_size)]
    #     for i in range(0, len(task_ids), batch_size)
    # ]
    # file_path = xp.xp_path / 'listoftasks.txt'
    #
    # with open(str(file_path), 'wt') as fout:
    #     fout.write('\n'.join(map(lambda batch: ','.join(batch), batches)))

    # generate and save script
    # script_path = Path(os.path.abspath(script_file_path))
    # script_dir = script_path.parent
    # script_name = script_path.stem

    # Generate job script

    script = '#!/bin/sh\n'

    # define parameters
    script += '#SBATCH --job-name={}\n'.format(xp.name)
    script += '#SBATCH --array={}%{}\n'.format(
        ','.join(str(i) for i in task_ids), n_simultaneous_jobs)
    script += '#SBATCH --output={}/stdout_%A_%a.slurm\n'.format(xp.xp_path)
    script += '#SBATCH --error={}/stderr_%A_%a.slurm\n'.format(xp.xp_path)
    script += '#SBATCH --time={}\n'.format(slurm_walltime)
    # if use_gpu:
    #     script += '#SBATCH -p gpu IS NOT NULL\n'
    # else:
    #     script += '#SBATCH -p gpu IS NULL\n'

    script += 'srun -N1 -n1 run_$SLURM_ARRAY_TASK_ID.sh'
    # script += 'echo "OAR_JOB_ID: $OAR_JOB_ID"\n'
    # script += 'echo "OAR_ARRAY_ID: $OAR_ARRAY_ID"\n'
    # script += 'echo "SLURM_ARRAY_TASK_ID: $SLURM_ARRAY_TASK_ID"\n'

    script_path = script_dir / 'script_slurm.sh'
    with script_path.open('w') as file:
        file.write(script)
    status = os.stat(script_path)
    os.chmod(script_path, status.st_mode | stat.S_IXUSR)

    # Generate a script of each array element
    for i_elt, idt in enumerate(task_ids):
        script = '#!/bin/sh\n'

        # activate the virtual env
        if activate_env_command is not None and len(activate_env_command) > 0:
            script += '{}\n'.format(activate_env_command)

        # python command
        script += 'echo "Running {}.launch_experiment(task_ids={})"\n'\
            .format(xp_var_name, idt)
        script += 'python -c "import sys; sys.path.append(\'{0}\'); ' \
            'from {1} import {2}; ' \
            '{2}.launch_experiment(task_ids={3})"\n'.format(
                script_dir, script_name, xp_var_name, idt)
        script += 'exit $?'

        script_i_path = script_dir / 'run_{}.sh'.format(i_elt)
        with script_i_path.open('w') as file:
            file.write(script)
        status = os.stat(script_i_path)
        os.chmod(script_i_path, status.st_mode | stat.S_IXUSR)

    print('sbatch {}'.format(str(script_path)))


from tffpy.experiments.exp_variance import VarianceExperiment

try:
    experiment = VarianceExperiment.get_experiment(setting='full',
                                                   force_reset=False)
except RuntimeError:
    experiment = None
except FileNotFoundError:
    experiment = None

if __name__ == '__main__':
