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

from tffpy.experiments.exp_solve_tff import SolveTffExperiment


class VarianceExperiment(SolveTffExperiment):
    """
    A variant of the main experiment (`SolveTffExperiment`) in order to
    analyze the variability of results with respect to the randomness of
    rand-EVD, by generating 100 draws for the same pair of signals (bird+car).
    """
    def __init__(self, force_reset=False, suffix=''):
        SolveTffExperiment.__init__(self,
                                    force_reset=force_reset,
                                    suffix='Variance' + suffix)

    def display_results(self):
        res = self.load_results(array_type='xarray')
        res = res.squeeze()
        tff_list = res.to_dict()['coords']['solver_tol_subregions']['data']
        for measure in ['sdr_tff', 'sdr_tffo', 'sdr_tffe',
                        'is_tff', 'is_tffo', 'is_tffe']:
            for solver_tol_subregions in tff_list:
                std_res = float(res.sel(
                    measure=measure,
                    solver_tol_subregions=solver_tol_subregions).std())
                if solver_tol_subregions is None:
                    measure_name = measure + '-1'
                else:
                    measure_name = measure + '-P'
                print('std({}): {}'.format(measure_name, std_res))

    def plot_results(self):
        # No more need for this method
        pass

    def plot_task(self, idt, fontsize=16):
        # No more need for this method
        pass

    @staticmethod
    def get_experiment(setting='full', force_reset=False):
        assert setting in ('full', 'light')

        # Set task parameters
        data_params = dict(loc_source='bird',
                           wideband_src='car')
        problem_params = dict(win_choice='gauss 256',
                              # win_choice=['gauss 256', 'hann 512'],
                              wb_to_loc_ratio_db=8,
                              n_iter_closing=3, n_iter_opening=3,
                              closing_first=True,
                              delta_mix_db=0,
                              delta_loc_db=40,
                              or_mask=True,
                              crop=None,
                              fig_dir=None)
        solver_params = dict(tol_subregions=[None, 1e-5],
                             tolerance_arrf=1e-3,
                             proba_arrf=1 - 1e-4,
                             rand_state=np.arange(100))
        if setting == 'light':
            problem_params['win_choice'] = 'gauss 64',
            problem_params['crop'] = 4096
            problem_params['delta_loc_db'] = 20
            problem_params['wb_to_loc_ratio_db'] = 16
            solver_params['tolerance_arrf'] = 1e-2
            solver_params['proba_arrf'] = 1 - 1e-2
            solver_params['rand_state'] = np.arange(3)

        # Create Experiment
        suffix = '' if setting == 'full' else '_Light'
        exp = VarianceExperiment(force_reset=force_reset,
                                 suffix=suffix)
        exp.add_tasks(data_params=data_params,
                      problem_params=problem_params,
                      solver_params=solver_params)
        exp.generate_tasks()
        return exp


def create_and_run_light_experiment():
    """
    Create a light experiment and run it
    """
    exp = VarianceExperiment.get_experiment(setting='light', force_reset=True)
    print('*' * 80)
    print('Created experiment')
    print(exp)
    print(exp.display_status())

    print('*' * 80)
    print('Run task 0')
    task_data = exp.get_task_data_by_id(idt=0)
    print(task_data.keys())
    print(task_data['task_params']['data_params'])

    problem = exp.get_problem(
        **task_data['task_params']['problem_params'])
    print(problem)

    print('*' * 80)
    print('Run all')
    exp.launch_experiment()

    print('*' * 80)
    print('Collect and plot results')
    exp.collect_results()
