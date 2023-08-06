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

task_params = {'data_params': {'loc_source': 'bird',
                               'wideband_src': 'car'},
               'problem_params': {'closing_first': True,
                                  'delta_loc_db': 40,
                                  'delta_mix_db': 0,
                                  'fig_dir': None,
                                  'n_iter_closing': 3,
                                  'n_iter_opening': 3,
                                  'or_mask': True,
                                  'wb_to_loc_ratio_db': 8,
                                  'win_choice': 'gauss 256',
                                  'crop': None},
               'solver_params': {'proba_arrf': 0.9999,
                                 'tolerance_arrf': 0.001,
                                 'tol_subregions': None}}

task = experiment.get_task_data_by_params(**task_params)

idt = task['id_task']
experiment.run_task_by_id(idt=idt)

task_data = experiment.get_task_data_by_id(idt=idt)
mask = task_data['problem_data']['mask']
fs = task_data['problem_data']['signal_params']['fs']
n_bins = task_data['problem_data']['dgt_params']['n_bins']
hop = task_data['problem_data']['dgt_params']['hop']
plot_mask(mask, hop, n_bins, fs=fs)
plt.savefig('mask.png')
from scipy.io import savemat, loadmat
savemat('mask.mat', {'mask': mask})
# a = loadmat('mask.mat')
