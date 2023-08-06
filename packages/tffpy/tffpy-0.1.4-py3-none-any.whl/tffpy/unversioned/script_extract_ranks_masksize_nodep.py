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

import pickle

from pandas import DataFrame
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import xarray

from yafe.utils import ConfigParser

exp_name = 'SolveTffExperiment'
exp_path = ConfigParser().get_path('USER', 'data_path') / exp_name
all_tasks_path = exp_path / 'tasks'

# from tffpy.experiments.exp_solve_tff import \
#     SolveTffExperiment, create_and_run_light_experiment
# from tffpy.utils import plot_mask

# try:
#     experiment = SolveTffExperiment.get_experiment(setting='full',
#                                                    force_reset=False)
# except RuntimeError:
#     experiment = None
# except FileNotFoundError:
#     experiment = None

# results = experiment.load_results(array_type='xarray')
# results = results.squeeze()
# results_masksize = results.sel(measure='mask_size', solver_tol_subregions=None)
# results_masksize.to_series().to_csv('mask_size.csv', header=True)
# # results.to_series().to_csv('mask_size.csv', header=True)

# new_results = results.reindex(measure=['mask_size', 'rank', 'tf_size'])
# results = xarray.DataArray()
res_dict = dict(
    data_loc_source=[],
    data_wideband_src=[],
    problem_win_choice=[],
    solver_tol_subregions=[],
    measure=[],
    result=[],
)

all_mask_ratio = []
all_mask_size = []
all_ranks = []
all_is_tff1 = []
for idt, task_path in enumerate(all_tasks_path.glob('00*')):
    print(task_path)

    try:
        with open(str(task_path / 'solved_data.pickle'), 'rb') as f:
            solved_data = pickle.load(file=f)
    except FileNotFoundError:
        print('FileNotFoundError')
        continue
    with open(str(task_path / 'task_params.pickle'), 'rb') as f:
        task_params = pickle.load(file=f)

    # task_data = experiment.get_task_data_by_id(idt=idt)
    # task_params = task_data['task_params']
    gmtff = solved_data['gmtff']
    rank = np.sum([s.size for s in gmtff.s_vec_list])
    # mask_size = results.sel(
    #     data_loc_source=task_params['data_params']['loc_source'],
    #     data_wideband_src=task_params['data_params']['wideband_src'],
    #     problem_win_choice=task_params['problem_params']['win_choice'],
    #     solver_tol_subregions=task_params['solver_params']['tol_subregions'],
    #     measure='mask_size')
    mask_size = np.sum(gmtff.mask > 0)
    mask_ratio = np.mean(gmtff.mask > 0)

    all_mask_ratio.append(mask_ratio)
    all_ranks.append(rank)
    all_mask_size.append(mask_size)
    all_is_tff1.append(len(gmtff.s_vec_list) == 1)

    d = dict(
        data_loc_source=task_params['data_params']['loc_source'],
        data_wideband_src=task_params['data_params']['wideband_src'],
        problem_win_choice=task_params['problem_params']['win_choice'],
        solver_tol_subregions=task_params['solver_params']['tol_subregions'],
    )

    d_values = dict(mask_ratio=mask_ratio, mask_size=mask_size, rank=rank)
    for kv in d_values:
        for k in d:
            res_dict[k].append(d[k])
        res_dict['measure'].append(kv)
        res_dict['result'].append(d_values[kv])

df = DataFrame(res_dict)
df.to_csv('rank_masksize_nodep.csv')

np.savez('rank_masksize_nodep.npz',
         all_mask_ratio=all_mask_ratio,
         all_ranks=all_ranks,
         all_mask_size=all_mask_size,
         all_is_tff1=all_is_tff1)

loaded_data = np.load('rank_masksize_nodep.npz')
all_mask_ratio = loaded_data['all_mask_ratio']
all_ranks = loaded_data['all_ranks']
all_mask_size = loaded_data['all_mask_size']
all_is_tff1 = loaded_data['all_is_tff1']

all_is_tff1 = np.array(all_is_tff1)

plt.figure()
plt.scatter(all_mask_ratio[all_is_tff1], all_ranks[all_is_tff1], label='TFF-1')
plt.scatter(all_mask_ratio[~all_is_tff1], all_ranks[~all_is_tff1],
            label='TFF-P')
plt.xlabel('Mask area ratio')
plt.ylabel('Rank')
plt.legend()
plt.savefig('rank_maskratio_nodep.png')

plt.figure()
plt.scatter(all_mask_size[all_is_tff1], all_ranks[all_is_tff1],
            marker='x', label='TFF-1')
plt.scatter(all_mask_size[~all_is_tff1], all_ranks[~all_is_tff1],
            marker='+', label='TFF-P')
plt.xlabel('Mask area')
plt.ylabel('Rank')
plt.legend()
plt.savefig('rank_masksize_nodep.png')
# coords = {k:res_dict[k] for k in res_dict
#           if k != 'result'}
# res_xr = xarray.DataArray(res_dict['result'],
#                           coords=coords,
#                           dims=coords.keys())
# new_results.loc[dict(
#     data_loc_source=task_params['data_params']['loc_source'],
#     data_wideband_src=task_params['data_params']['wideband_src'],
#     problem_win_choice=task_params['problem_params']['win_choice'],
#     solver_tol_subregions=task_params['solver_params']['tol_subregions'],
#     measure='tf_size')] = tf_size

# res_xr = xarray.DataArray([], coords=)
    # res_dict['data_loc_source'].append(task_params['data_params']['loc_source'])
    # res_dict[].append()
    # new_results.loc[dict(
    #     data_loc_source=task_params['data_params']['loc_source'],
    #     data_wideband_src=task_params['data_params']['wideband_src'],
    #     problem_win_choice=task_params['problem_params']['win_choice'],
    #     solver_tol_subregions=task_params['solver_params']['tol_subregions'],
    #     measure='tf_size')] = tf_size
    # new_results.loc[dict(
    #     data_loc_source=task_params['data_params']['loc_source'],
    #     data_wideband_src=task_params['data_params']['wideband_src'],
    #     problem_win_choice=task_params['problem_params']['win_choice'],
    #     solver_tol_subregions=task_params['solver_params']['tol_subregions'],
    #     measure='rank')] = rank

# new_results.to_series().to_csv('rank_masksize.csv', header=True)