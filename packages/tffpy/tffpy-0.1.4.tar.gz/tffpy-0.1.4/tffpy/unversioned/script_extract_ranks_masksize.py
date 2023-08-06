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

import numpy as np
import matplotlib.pyplot as plt

from tffpy.experiments.exp_solve_tff import \
    SolveTffExperiment, create_and_run_light_experiment
from tffpy.utils import plot_mask

try:
    experiment = SolveTffExperiment.get_experiment(setting='full',
                                                   force_reset=False)
except RuntimeError:
    experiment = None
except FileNotFoundError:
    experiment = None

results = experiment.load_results(array_type='xarray')
results = results.squeeze()
# results_masksize = results.sel(measure='mask_size', solver_tol_subregions=None)
# results_masksize.to_series().to_csv('mask_size.csv', header=True)
# results.to_series().to_csv('mask_size.csv', header=True)

new_results = results.reindex(measure=['mask_size', 'rank', 'tf_size'])
for idt in range(experiment.n_tasks):
    task_data = experiment.get_task_data_by_id(idt=idt)
    task_params = task_data['task_params']
    gmtff = task_data['solved_data']['gmtff']
    rank = np.sum([s.size for s in gmtff.s_vec_list])
    # mask_size = results.sel(
    #     data_loc_source=task_params['data_params']['loc_source'],
    #     data_wideband_src=task_params['data_params']['wideband_src'],
    #     problem_win_choice=task_params['problem_params']['win_choice'],
    #     solver_tol_subregions=task_params['solver_params']['tol_subregions'],
    #     measure='mask_size')
    tf_size = gmtff.u_mat_list[0].shape[0]
    new_results.loc[dict(
        data_loc_source=task_params['data_params']['loc_source'],
        data_wideband_src=task_params['data_params']['wideband_src'],
        problem_win_choice=task_params['problem_params']['win_choice'],
        solver_tol_subregions=task_params['solver_params']['tol_subregions'],
        measure='tf_size')] = tf_size
    new_results.loc[dict(
        data_loc_source=task_params['data_params']['loc_source'],
        data_wideband_src=task_params['data_params']['wideband_src'],
        problem_win_choice=task_params['problem_params']['win_choice'],
        solver_tol_subregions=task_params['solver_params']['tol_subregions'],
        measure='rank')] = rank

new_results.to_series().to_csv('rank_masksize.csv', header=True)