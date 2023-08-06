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
Class `SolveTffExperiment` uses the :class:`yafe.base.Experiment` experiment
framework to handle the main time-frequency fading experiment: It includes
loading the data, generating the problems, applying solvers, and exploiting
results.

See the `documentation <http://skmad-suite.pages.lis-lab.fr/yafe/>`_ of
package :py:mod:`yafe` for the technical details.

.. moduleauthor:: Valentin Emiya
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from pathlib import Path
from scipy.stats import linregress

from yafe import Experiment
from madarrays import Waveform

from tffpy.datasets import get_mix, get_dataset
from tffpy.tf_fading import GabMulTff, compute_lambda_oracle_sdr
from tffpy.interpolation_solver import solve_by_interpolation
from tffpy.utils import \
    sdr, plot_spectrogram, is_div_spectrum, plot_mask, db, dgt


class SolveTffExperiment(Experiment):
    """
    The main experiment to solve time-frequency fading problems with a
    number of sounds mixtures and solvers.

    Parameters
    ----------
    force_reset : bool
        If true, reset the experiment by erasing all previous results
        in order to run it from scratch. If False, the existing results are
        kept in order to proceed with the existing experiment.
    suffix : str
        Suffix that is appended to the name of the experiment, useful to
        save results in a specific folder.
    """

    def __init__(self, force_reset=False, suffix=''):
        Experiment.__init__(self,
                            name='SolveTffExperiment' + suffix,
                            get_data=get_data,
                            get_problem=Problem,
                            get_solver=Solver,
                            measure=perf_measures,
                            force_reset=force_reset,
                            log_to_file=False,
                            log_to_console=False)
        self.fig_dir = self.xp_path / 'figures'
        # a little trick to save collections when computing performance
        self.measure = lambda **x: perf_measures(**x, exp=self)

    @property
    def n_tasks(self):
        """
        Number of tasks

        Returns
        -------
        int
        """
        return len(list((self.xp_path / 'tasks').glob('0*')))

    @staticmethod
    def get_experiment(setting='full', force_reset=False):
        """
        Get the experiment instance with default values in order to handle it.

        Parameters
        ----------
        setting : {'full', 'light'}
            If 'full', the default values are set to run the full
            experiment. If 'light', the default values are set to have a
            very light experiment with few tasks, running fast, for test
            purposes.
        force_reset : bool
            If true, reset the experiment by erasing all previous results
            in order to run it from scratch. If False, the existing results are
            kept in order to proceed with the existing experiment.

        Returns
        -------
        SolveTffExperiment
        """
        assert setting in ('full', 'light')

        dataset = get_dataset()
        # Set task parameters
        data_params = dict(loc_source=list(dataset['localized'].keys()),
                           wideband_src=list(dataset['wideband'].keys()))
        problem_params = dict(win_choice=['gauss 256', 'hann 512'],
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
                             rand_state=0)
        if setting == 'light':
            data_params['loc_source'] = 'bird'
            data_params['wideband_src'] = 'car'
            problem_params['win_choice'] = ['gauss 64', 'hann 128']
            problem_params['crop'] = 4096
            problem_params['delta_loc_db'] = 20
            problem_params['wb_to_loc_ratio_db'] = 16
            solver_params['tolerance_arrf'] = 1e-2
            solver_params['proba_arrf'] = 1 - 1e-2

        # Create Experiment
        suffix = '' if setting == 'full' else '_Light'
        exp = SolveTffExperiment(force_reset=force_reset,
                                 suffix=suffix)
        exp.add_tasks(data_params=data_params,
                      problem_params=problem_params,
                      solver_params=solver_params)
        exp.generate_tasks()
        return exp

    def export_task_params(self, csv_path=None):
        """
        Export task parameters to a csv file and to a
        :class:`pandas.DataFrame` object.

        Parameters
        ----------
        csv_path : str or Path
            Name of the csv file to be written. If None, file is
            located in the experiment folder with name 'task_params.csv'.

        Returns
        -------
        pandas.DataFrame
        """
        if csv_path is None:
            csv_path = self.xp_path / 'task_params.csv'
        else:
            csv_path = Path(csv_path)
        task_list = []
        for i_task in range(self.n_tasks):
            task = self.get_task_data_by_id(idt=i_task)
            task_list.append({k + '_' + kk: task['task_params'][k][kk]
                              for k in task['task_params']
                              for kk in task['task_params'][k]})
        df = pd.DataFrame(task_list)
        df.to_csv(csv_path)
        print('Task params exported to', csv_path)
        return df

    def generate_tasks(self):
        """
        Generate tasks and export params to a csv file

        See :py:meth:`yafe.Experiment.generate_tasks`
        """
        Experiment.generate_tasks(self)
        self.export_task_params()

    def get_misc_file(self, task_params=None, idt=None):
        """
        Get file with some additional task results.

        This has been set up in order to pass additional data in a way that
        could not be handled by the :py:mod:`yafe` framework.

        Parameters
        ----------
        task_params : dict
            Task parameters.
        idt : int
            Task identifier. Either `task_params` or `idt` should be given
            in order to specify the task.

        Returns
        -------
        Path
            File containing additional task results.
        """
        if task_params is not None:
            task = self.get_task_data_by_params(
                data_params=task_params['data_params'],
                problem_params=task_params['problem_params'],
                solver_params=task_params['solver_params'])
            idt = task['id_task']
        elif idt is None:
            raise ValueError('Either `task_params` or `idt` should be given.')
        path_task = self.xp_path / 'tasks' / '{:06}'.format(idt)
        return path_task / 'misc.npz'

    def plot_results(self):
        """
        Plot and save results of the experiment
        """
        self.fig_dir.mkdir(parents=True, exist_ok=True)
        print('Figures saved in {}'.format(self.fig_dir))
        results = self.load_results(array_type='xarray')
        results = results.squeeze()
        coords_dict = results.to_dict()['coords']
        csv_path = self.fig_dir / 'exp_solve_pd.csv'
        results.to_series().to_csv(csv_path, header=True)

        print('number of nan values:',
              np.sum(np.isnan(results.values)))

        # Scatter plot for running times : tff-1 vs. tff-P
        plt.figure()
        x = []
        y = []
        for win_type in coords_dict['problem_win_choice']['data']:
            t_tff1 = results.sel(measure=['t_lambda_tff', 't_arrf', 't_evdn'],
                                 problem_win_choice=win_type,
                                 solver_tol_subregions=None)
            t_tff1 = t_tff1.sum(dim='measure')

            not_none = coords_dict['solver_tol_subregions']['data'].copy()
            not_none.remove(None)
            not_none = not_none[0]
            t_tffp = results.sel(measure=['t_lambda_tff', 't_arrf',
                                          't_evdn', 't_subreg'],
                                 problem_win_choice=win_type,
                                 solver_tol_subregions=not_none)
            t_tffp = t_tffp.sum(dim='measure')

            if win_type[:5] == 'gauss':
                win_type_label = 'Gauss'
            else:
                win_type_label = 'Hann'
            slope, intercept, r_value, p_value, std_err = \
                linregress(t_tff1.values.reshape(-1), t_tffp.values.reshape(-1))
            print('Running times ({}): slope={}, intercept={}, 1/slope={},'
                  .format(win_type, slope, intercept, 1 / slope))
            plt.plot(t_tff1.values.reshape(-1),
                     t_tffp.values.reshape(-1),
                     '+', label=win_type_label)
            # plt.plot(t_tff1.values.reshape(-1),
            #          slope * t_tff1.values.reshape(-1) + intercept)
            x.append(t_tff1.values.reshape(-1).copy())
            y.append(t_tffp.values.reshape(-1).copy())

        x = np.array(x)
        y = np.array(y)
        # for i in range(x.shape[1]):
        #     plt.plot(x[:, i], y[:, i], ':k')

        x = x.reshape(-1)
        y = y.reshape(-1)
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        print('Running times (all): slope={}, intercept={}, 1/slope={},'
              .format(slope, intercept, 1 / slope))
        print('Linear slope (not affine):')
        print(np.vdot(x, y) / np.vdot(x, x), np.vdot(x, x) / np.vdot(x, y))

        # plt.plot(x, slope * x + intercept)
        plt.xlabel(r'Running time for TFF-1 (s)')
        plt.ylabel(r'Running time for TFF-P (s)')
        plt.legend()
        plt.grid()
        plt.savefig(self.fig_dir / 'running_times_exp.pdf')
        plt.savefig(self.fig_dir / 'running_times_exp.png')
        plt.xscale('log')
        plt.yscale('log')
        plt.savefig(self.fig_dir / 'running_times_exp_loglog.pdf')
        plt.savefig(self.fig_dir / 'running_times_exp_loglog.png')

        # Scatter plot for running times : tff-1 and tff-P vs. mask size
        plt.figure()
        symbol = '+'
        for win_type in coords_dict['problem_win_choice']['data']:
            mask_size_tff1 = results.sel(measure=['mask_size'],
                                         problem_win_choice=win_type,
                                         solver_tol_subregions=None).squeeze()
            t_tff1 = results.sel(measure=['t_lambda_tff', 't_arrf', 't_evdn'],
                                 problem_win_choice=win_type,
                                 solver_tol_subregions=None)
            t_tff1 = t_tff1.sum(dim='measure')
            plt.plot(mask_size_tff1.values.reshape(-1),
                     t_tff1.values.reshape(-1),
                     symbol, label='{} - {}'.format('TFF-1', win_type))

        not_none = coords_dict['solver_tol_subregions']['data'].copy()
        not_none.remove(None)
        not_none = not_none[0]
        for win_type in coords_dict['problem_win_choice']['data']:
            mask_size_tffp = results.sel(
                measure=['mask_size'],
                problem_win_choice=win_type,
                solver_tol_subregions=not_none).squeeze()
            t_tffp = results.sel(measure=['t_lambda_tff', 't_arrf',
                                          't_evdn', 't_subreg'],
                                 problem_win_choice=win_type,
                                 solver_tol_subregions=not_none)
            t_tffp = t_tffp.sum(dim='measure')

            plt.plot(mask_size_tffp.values.reshape(-1),
                     t_tffp.values.reshape(-1),
                     symbol, label='{} - {}'.format('TFF-P', win_type))
        plt.ylabel('Running time (s)')
        plt.xlabel('Mask size')
        plt.legend()
        plt.grid()
        plt.savefig(self.fig_dir / 'running_times_masksize_exp.pdf')
        plt.savefig(self.fig_dir / 'running_times_masksize_exp.png')
        plt.xscale('log')
        plt.yscale('log')
        plt.savefig(self.fig_dir / 'running_times_masksize_exp_loglog.pdf')
        plt.savefig(self.fig_dir / 'running_times_masksize_exp_loglog.png')

        # Scatter plot : SDR vs IS
        plt.figure()
        symbol = '+'
        for k_measure in results.coords['measure'].values:
            if k_measure[:3] == 'sdr':
                sdr_res = results.sel(measure=[k_measure]).squeeze()
                is_res = results.sel(measure=['is' + k_measure[3:]]).squeeze()
                plt.plot(sdr_res.values.reshape(-1),
                         is_res.values.reshape(-1),
                         symbol,
                         label=k_measure[4:])
        plt.legend()
        plt.grid()
        plt.yscale('log')
        plt.savefig(self.fig_dir / 'sdr_vs_is.pdf')
        plt.savefig(self.fig_dir / 'sdr_vs_is.png')

        # Scatter plot : SDR vs IS with polygons
        sdr_tff1 = results.sel(
            measure='sdr_tff',
            solver_tol_subregions=None).squeeze().values.reshape(-1)
        sdr_tffp = results.sel(
            measure='sdr_tff',
            solver_tol_subregions=not_none).squeeze().values.reshape(-1)
        sdr_tffo = results.sel(
            measure='sdr_tffo',
            solver_tol_subregions=not_none).squeeze().values.reshape(-1)
        sdr_interp = results.sel(
            measure='sdr_interp',
            solver_tol_subregions=not_none).squeeze().values.reshape(-1)
        sdr_zero = results.sel(
            measure='sdr_zero',
            solver_tol_subregions=not_none).squeeze().values.reshape(-1)
        is_tff1 = results.sel(
            measure='is_tff',
            solver_tol_subregions=None).squeeze().values.reshape(-1)
        is_tffp = results.sel(
            measure='is_tff',
            solver_tol_subregions=not_none).squeeze().values.reshape(-1)
        is_tffo = results.sel(
            measure='is_tffo',
            solver_tol_subregions=not_none).squeeze().values.reshape(-1)
        is_interp = results.sel(
            measure='is_interp',
            solver_tol_subregions=not_none).squeeze().values.reshape(-1)
        is_zero = results.sel(
            measure='is_zero',
            solver_tol_subregions=not_none).squeeze().values.reshape(-1)

        plt.figure()
        symbol = '+'
        for i in range(sdr_tff1.size):
            plt.plot([sdr_tff1[i], sdr_tffp[i], sdr_tffo[i],
                      sdr_zero[i], sdr_interp[i], sdr_tff1[i]],
                     [is_tff1[i], is_tffp[i], is_tffo[i],
                      is_zero[i], is_interp[i], is_tff1[i]],
                     'k', alpha=0.2)
        plt.plot(sdr_tff1, is_tff1, symbol, label='TFF-1')
        plt.plot(sdr_tffp, is_tffp, symbol, label='TFF-P')
        plt.plot(sdr_tffo, is_tffo, symbol, label='TFF-O')
        plt.plot(sdr_interp, is_interp, symbol, label='Interp')
        plt.plot(sdr_zero, is_zero, symbol, label='Zero fill')
        plt.legend()
        plt.grid()
        plt.xlabel('SDR')
        plt.ylabel('IS divergence')
        plt.yscale('log')
        plt.savefig(self.fig_dir / 'sdr_vs_is_polygons.pdf')
        plt.savefig(self.fig_dir / 'sdr_vs_is_polygons.png')

    @staticmethod
    def _get_label(k, tol_subregions):
        if k.endswith('tffo'):
            label = 'TFF-O'
        elif k.endswith('tff'):
            label = 'TFF-1' if tol_subregions is None else 'TFF-P'
        elif k.endswith('tffe'):
            label = 'TFF-E'
        elif k.endswith('interp'):
            label = 'Interp'
        elif k.endswith('zero'):
            label = 'Zero fill'
        elif k.endswith('mix'):
            label = 'Mix'
        else:
            raise ValueError('Unknown key: ' + k)
        return label

    def plot_task(self, idt, fontsize=16):
        """
        Plot and save figures for a specific task

        Parameters
        ----------
        idt : int
            Task identifier
        fontsize : int
            Fontsize to be used in Figures.
        """
        matplotlib.rcParams.update({'font.size': fontsize})
        fig_dir = self.xp_path / 'figures' / 'tasks' / '{:06}'.format(idt)
        fig_dir.mkdir(parents=True, exist_ok=True)
        print('Save figures in:', fig_dir)

        task = self.get_task_data_by_id(idt=idt)
        misc_data = np.load(self.get_misc_file(idt=idt))

        mask = task['problem_data']['mask']
        dgt_params = task['problem_data']['dgt_params']
        signal_params = task['problem_data']['signal_params']
        x_mix = task['problem_data']['x_mix']
        x_wb = task['solution_data']['x_wb']
        tol_subregions = task['task_params']['solver_params']['tol_subregions']
        gmtff = task['solved_data']['gmtff']
        sdr_res = dict()
        is_res = dict()
        for k in task['result']:
            k_suf = k.split('_')[-1]
            if k.startswith('sdr'):
                sdr_res[k_suf] = task['result'][k]
            elif k.startswith('is'):
                is_res[k_suf] = task['result'][k]
        lambda_res = dict()
        for k in misc_data:
            k_suf = k.split('_')[-1]
            lambda_res[k_suf] = misc_data[k]

        plt.figure()
        plot_mask(mask=mask, hop=dgt_params['hop'],
                  n_bins=dgt_params['n_bins'], fs=signal_params['fs'])
        plt.title('Area: {} ({:.1%})'.format(mask.sum(), np.average(mask)))
        plt.tight_layout()
        plt.savefig(fig_dir / 'mask.pdf')

        plt.figure()
        for i_area in range(gmtff.n_areas):
            s_vec = gmtff.s_vec_list[i_area]
            plt.plot(s_vec, label='Sub-region {}'.format(i_area + 1))
        plt.xlabel('k')
        plt.ylabel('$\\sigma_k$')
        plt.yscale('log')
        plt.grid()
        plt.legend()
        plt.tight_layout()
        plt.savefig(fig_dir / 'gabmul_eigenvalues.pdf')

        # Results
        def sdr_wb(lambda_coef):
            return sdr(x_ref=x_wb, x_est=gmtff.compute_estimate(lambda_coef))

        def is_wb(lambda_coef):
            return is_div_spectrum(x_ref=x_wb,
                                   x_est=gmtff.compute_estimate(lambda_coef))

        def sdr_wb_1area(lambda_coef, i_area):
            lambda_vec = np.ones(gmtff.n_areas)
            lambda_vec[i_area] = lambda_coef
            return sdr(x_ref=x_wb, x_est=gmtff.compute_estimate(lambda_vec))

        l_range = 10 ** np.linspace(-10, 10, 100, endpoint=True)
        if tol_subregions is None:
            plt.figure()
            plt.plot(l_range, [sdr_wb(i) for i in l_range], '-',
                     label='SDR')
            for k in lambda_res:
                plt.plot(lambda_res[k], sdr_wb(lambda_res[k]), 'o',
                         label=self._get_label(k=k,
                                               tol_subregions=tol_subregions))
        else:
            plt.figure()
            for i_area in range(gmtff.n_areas):
                plt.plot(l_range,
                         [sdr_wb_1area(i, i_area) for i in l_range],
                         '-', label='SDR sub-reg {}'.format(i_area + 1))
            for k in lambda_res:
                label_prefix = self._get_label(k=k,
                                               tol_subregions=tol_subregions)
                if not isinstance(lambda_res[k], np.ndarray):
                    plt.plot(lambda_res[k], sdr_wb(lambda_res[k]),
                             'o', label=label_prefix)
                    continue

                for i_area in range(gmtff.n_areas):
                    label = '{} {}'.format(label_prefix, i_area + 1)
                    plt.plot(lambda_res[k][i_area],
                             sdr_wb_1area(lambda_res[k][i_area], i_area),
                             'o', label=label)
        plt.xlabel('$\\lambda$')
        plt.ylabel('SDR (dB)')
        plt.xscale('log')
        plt.grid()
        plt.legend()
        plt.tight_layout()
        plt.savefig(fig_dir / 'tuning_lambda.pdf')

        if tol_subregions is None:
            plt.figure()
            plt.plot(l_range, [is_wb(i) for i in l_range], '-',
                     label='IS')
            for k in lambda_res:
                plt.plot(lambda_res[k], is_wb(lambda_res[k]), 'o',
                         label=self._get_label(k=k,
                                               tol_subregions=tol_subregions))
            plt.xlabel('$\\lambda$')
            plt.ylabel('IS (dB)')
            plt.xscale('log')
            plt.grid()
            plt.legend()
            plt.tight_layout()
            plt.savefig(fig_dir / 'tuning_lambda_IS.pdf')

            fig, ax1 = plt.subplots()
            color = 'tab:blue'
            ax1.set_xlabel('$\\lambda$')
            ax1.set_ylabel('SDR (dB)', color=color)
            ax1.plot(l_range, [sdr_wb(i) for i in l_range], '-',
                     color=color)
            for k in lambda_res:
                ax1.plot(lambda_res[k], sdr_wb(lambda_res[k]), 'o',
                         label=self._get_label(k=k,
                                               tol_subregions=tol_subregions))
            ax1.tick_params(axis='y', labelcolor=color)
            plt.xscale('log')
            ax1.grid()

            # instantiate a second axes that shares the same x-axis
            ax2 = ax1.twinx()
            color = 'tab:red'
            ax2.set_xlabel('$\\lambda$')
            ax2.set_ylabel('IS divergence', color=color)
            ax2.plot(l_range, [is_wb(i) for i in l_range], '-',
                     color=color)
            for k in lambda_res:
                ax2.plot(lambda_res[k], is_wb(lambda_res[k]), 'o',
                         label=self._get_label(k=k,
                                               tol_subregions=tol_subregions))
            ax2.tick_params(axis='y', labelcolor=color)
            fig.tight_layout()
            ax2.legend()
            plt.tight_layout()
            plt.savefig(fig_dir / 'tuning_lambda_SDR_IS.pdf')

        x_dict = dict()
        for k in lambda_res:
            x_dict[k] = gmtff.compute_estimate(lambda_res[k])
            x_dict[k].to_wavfile(fig_dir / 'x_{}.wav'.format(k))
        x_dict['interp'] = Waveform(solve_by_interpolation(
            x_mix=x_mix, mask=mask, dgt_params=dgt_params,
            signal_params=signal_params), fs=signal_params['fs'])
        x_dict['interp'].to_wavfile(fig_dir / 'x_interp.wav')

        for k in sdr_res:
            print(self._get_label(k=k, tol_subregions=tol_subregions))
            print('  - SDR: {:.1f}dB'.format(sdr_res[k]))
            print('  - IS: {:.1f}'.format(is_res[k]))
            if k in lambda_res:
                print('  - lambda: ', lambda_res[k])

        x_mix_tf = dgt(sig=x_mix, dgt_params=dgt_params)
        x_max = db(x_mix_tf).max()
        clim = x_max - 100, x_max
        for k in x_dict:
            plt.figure()
            plot_spectrogram(x=x_dict[k], dgt_params=dgt_params,
                             fs=signal_params['fs'], clim=clim)
            plt.title('{} - SDR={:.1f}dB - IS={:.1f}'
                      .format(self._get_label(k=k,
                                              tol_subregions=tol_subregions),
                              sdr_res[k], is_res[k]))
            plt.tight_layout()
            plt.savefig(fig_dir / '{}.pdf'.format(k))

        plt.figure()
        plot_spectrogram(x=x_wb, dgt_params=dgt_params,
                         fs=signal_params['fs'],
                         clim=clim)
        plt.title('True signal')
        plt.tight_layout()
        plt.savefig(fig_dir / 'spectrogram_true_wb_source.pdf')


def get_data(loc_source, wideband_src):
    """
    Prepare the input data information for the :py:class:`SolveTffExperiment`
    experiment.

    This function is only embedding its input in a dictionary

    Parameters
    ----------
    loc_source : Path
        File for the source localized in time-frequency (perturbation)
    wideband_src : Path
        File for the source of interest.

    Returns
    -------
    dict
        Dictionary to be given when calling the problemm (
        see :py:meth:`Problem.__call__`), with keys `'loc_source'` and
        `wideband_src`.
    """
    return dict(loc_source=loc_source, wideband_src=wideband_src)


class Problem:
    """
    Problem generation for the :py:class:`SolveTffExperiment` experiment.

    Parameters
    ----------
    crop : int or None
        If not None, a cropped, centered portion of the sound will be
        extracted with the specified length, in samples.
    win_choice : str
        String of the form 'name len' where 'name' is a window name and
        'len' is a window length, e.g. 'hann 512', 'gauss 256.
    delta_mix_db : float
        Coefficient energy ratio, in dB, between the wideband source and the
        localized source in the mixture in order to select coefficients in
        the mask.
    delta_loc_db : float
        Dynamic range, in dB, for the localized source in order to select
        coefficients in the mask.
    wb_to_loc_ratio_db : float
        Wideband source to localized source energy ratio to be adjusted in
        the mix.
    or_mask : bool
        If True, the mask is build by taking the union of the two masks
        obtained using thresholds `delta_mix_db` and `delta_loc_db`. If
        False, the intersection is taken.
    n_iter_closing : int
        Number of successive morphological closings with radius 1 (a.k.a.
        radius of one single closing)
    n_iter_opening : int
        Number of successive morphological openings with radius 1 (a.k.a.
        radius of one single opening)
    closing_first : bool
        If True, morphological closings are applied first, followed by
        openings. If False, the reverse way is used.
    fig_dir : None or str or Path
        If not None, folder where figures are stored. If None, figures are
        not plotted.
    """

    def __init__(self, crop, win_choice,
                 delta_mix_db, delta_loc_db, wb_to_loc_ratio_db, or_mask,
                 n_iter_closing, n_iter_opening, closing_first, fig_dir):
        win_type, win_len_str = win_choice.split(sep=' ')
        win_dur = int(win_len_str) / 8000
        self.win_dur = win_dur
        self.win_type = win_type
        if win_type == 'gauss':
            self.hop_ratio = 1 / 4
            self.n_bins_ratio = 4
        else:
            self.hop_ratio = 1 / 8
            self.n_bins_ratio = 2
        self.n_iter_closing = n_iter_closing
        self.n_iter_opening = n_iter_opening
        self.closing_first = closing_first
        self.delta_mix_db = delta_mix_db
        self.delta_loc_db = delta_loc_db
        self.wb_to_loc_ratio_db = wb_to_loc_ratio_db
        self.or_mask = or_mask
        self.crop = crop
        self.fig_dir = fig_dir

    def __call__(self, loc_source, wideband_src):
        """
        Generate the problem from input data.

        Parameters
        ----------
        loc_source : Path
            File for the source localized in time-frequency (perturbation)
        wideband_src : Path
            File for the source of interest.

        Returns
        -------
        problem_data : dict
            Dictionary to be given to a solver, with keys `'x_mix'` (mix
            signal), `mask` (time-frequency mask), `dgt_params` (DGT
            parameters) and `signal_params` (signal parameters).
        solution_data : dict
            Dictionary containing problem solutions, with keys `'x_loc'` (
            localized signal ) and `x_wb` (wideband signal).
        """
        x_mix, dgt_params, signal_params, mask, x_loc, x_wb = \
            get_mix(loc_source=loc_source,
                    wideband_src=wideband_src,
                    crop=self.crop,
                    win_dur=self.win_dur,
                    win_type=self.win_type,
                    hop_ratio=self.hop_ratio,
                    n_bins_ratio=self.n_bins_ratio,
                    n_iter_closing=self.n_iter_closing,
                    n_iter_opening=self.n_iter_opening,
                    closing_first=self.closing_first,
                    delta_mix_db=self.delta_mix_db,
                    delta_loc_db=self.delta_loc_db,
                    wb_to_loc_ratio_db=self.wb_to_loc_ratio_db,
                    or_mask=self.or_mask,
                    fig_dir=self.fig_dir)

        problem_data = dict(x_mix=x_mix, mask=mask,
                            dgt_params=dgt_params, signal_params=signal_params)
        solution_data = dict(x_loc=x_loc, x_wb=x_wb)
        return problem_data, solution_data


class Solver:
    """
    Solver for the :py:class:`SolveTffExperiment` experiment.

    This solver is computing

    * the `TFF-1` of `TFF-P` solution (depending on parameter `tol_subregions`)
      using a :py:class:`~tffpy.tf_fading.GabMulTff` instance
    * the `Interp` solution using function
      :py:func:`~tffpy.interpolation_solver.solve_by_interpolation`

    Parameters
    ----------
    tol_subregions : None or float
        Tolerance to split the mask into sub-regions in
        :py:class:`~tffpy.tf_fading.GabMulTff`.
    tolerance_arrf : float
        Tolerance for the randomized EVD in
        :py:class:`~tffpy.tf_fading.GabMulTff`, see method
        :py:meth:`~tffpy.tf_fading.GabMulTff.compute_decomposition`.
    proba_arrf : float
        Probability of error for the randomized EVD in
        :py:class:`~tffpy.tf_fading.GabMulTff`, see method
        :py:meth:`~tffpy.tf_fading.GabMulTff.compute_decomposition`.
    """

    def __init__(self, tol_subregions, tolerance_arrf, proba_arrf,
                 rand_state=0):
        self.tol_subregions = tol_subregions
        self.tolerance_arrf = tolerance_arrf
        self.proba_arrf = proba_arrf
        self.rand_state = rand_state

    def __call__(self, x_mix, mask, dgt_params, signal_params):
        """
        Apply the solver to estimate solutions from the problem data.

        The output dictionary is composed of data with keys:

        * `'x_tff'`: solution estimated by :py:class:`~tffpy.tf_fading.GabMulTff`
        * `'x_zero'`: solution when applying the Gabor
          multiplier (i.e., :math:`\lambda=1`)
        * `'x_interp'`: solution from function
          :py:func:`~tffpy.interpolation_solver.solve_by_interpolation`
        * `'gmtff'`: `GabMulTff` instance
        * `'t_lambda_tff'`: running times to estimate hyperparameter in method
          :py:meth:`~tffpy.tf_fading.GabMulTff.compute_lambda`
        * `'t_arrf'`: running times to compute range approximation in method
          :py:meth:`~tffpy.tf_fading.GabMulTff.compute_decomposition`
        * `'t_evdn'`: running times to compute EVD in method
          :py:meth:`~tffpy.tf_fading.GabMulTff.compute_decomposition`
        * `'t_uh_x'`: running times to compute additional matrix products in
          method :py:meth:`~tffpy.tf_fading.GabMulTff.compute_decomposition`
        * `'t_subreg'`: running times to split mask into sub-regions in class
          :py:class:`~tffpy.tf_fading.GabMulTff`
        * `'lambda_tff'`: estimated values for hyper-parameters
          :math:`\lambda_i` estimated by
          :py:meth:`~tffpy.tf_fading.GabMulTff`.compute_lambda`

        Parameters
        ----------
        x_mix : nd-array
            Mix signal
        mask : nd-array
            Time-frequency mask
        dgt_params : dict
            DGT parameters
        signal_params : dict
            Signal parameters

        Returns
        -------
        dict
            The estimated solution and additional information
        """
        gmtff = GabMulTff(x_mix=x_mix, mask=mask, dgt_params=dgt_params,
                          signal_params=signal_params,
                          tol_subregions=self.tol_subregions)
        gmtff.compute_decomposition(tolerance_arrf=self.tolerance_arrf,
                                    proba_arrf=self.proba_arrf,
                                    rand_state=self.rand_state)

        # Estimate energy and lambda
        lambda_tff, t_lambda_tff = gmtff.compute_lambda(x_mix=x_mix)
        print('Running time to tune lambda (est): {} s'.format(t_lambda_tff))

        x_tff = gmtff.compute_estimate(lambda_tff)
        x_zero = gmtff.compute_estimate(1)
        x_interp = solve_by_interpolation(
            x_mix=x_mix, mask=mask, dgt_params=dgt_params,
            signal_params=signal_params)
        return dict(x_tff=x_tff, x_zero=x_zero, x_interp=x_interp, gmtff=gmtff,
                    t_lambda_tff=t_lambda_tff, t_arrf=gmtff.t_arrf,
                    t_evdn=gmtff.t_evdn, t_uh_x=gmtff.t_uh_x,
                    t_subreg=gmtff.t_subreg, lambda_tff=lambda_tff)


def perf_measures(task_params, source_data, problem_data,
                  solution_data, solved_data, exp=None):
    """
    Performance measure, including computation of oracle solutions

    Parameters
    ----------
    task_params : dict
        Task parameters
    source_data : dict
        Input data
    problem_data : dict
        Problem data
    solution_data : dict
        Solver output
    solved_data : dict
        True solution data
    exp : SolveTffExperiment
        The experiment

    Returns
    -------
    dict
        All data useful for result analysis including SDR and Itakura-Saito
        performance, running times, hyperparameter values, mask size,
        number of sub-regions, estimated rank (summed over sub-regions),
        lowest singular value.
    """
    x_tff = solved_data['x_tff']
    x_zero = solved_data['x_zero']
    gmtff = solved_data['gmtff']
    lambda_tff = solved_data['lambda_tff']
    x_interp = solved_data['x_interp']
    x_mix = problem_data['x_mix']
    x_wb = solution_data['x_wb']

    # Trick for storing additional results
    misc_file = exp.get_misc_file(task_params=task_params)

    # Orcale SDR
    lambda_tffo, t_lambda_tffo = compute_lambda_oracle_sdr(gmtff=gmtff, x_wb=x_wb)
    x_tffo = gmtff.compute_estimate(lambda_tffo)

    # Oracle true energy
    e_target_tffe = np.empty(gmtff.n_areas)
    x_wb_tf_mat = dgt(x_wb, dgt_params=gmtff.dgt_params)
    for i_area in range(gmtff.n_areas):
        mask_i = gmtff.mask == i_area + 1
        x_wb_tf_masked = mask_i * x_wb_tf_mat
        e_target_tffe[i_area] = \
            np.linalg.norm(x_wb_tf_masked, 'fro') ** 2

    lambda_tffe, t_lambda_tffe = gmtff.compute_lambda(
        x_mix=x_mix, e_target=e_target_tffe)
    x_tffe = gmtff.compute_estimate(lambda_tffe)

    solutions = dict(tffo=x_tffo,
                     tff=x_tff,
                     tffe=x_tffe,
                     zero=x_zero,
                     mix=x_mix,
                     interp=x_interp)
    sdr_res = {'sdr_' + k: sdr(x_ref=x_wb, x_est=x)
               for k, x in solutions.items()}
    is_res = {'is_' + k: is_div_spectrum(x_ref=x_wb, x_est=x)
              for k, x in solutions.items()}

    np.savez(misc_file,
             lambda_tffe=lambda_tffe,
             lambda_tffo=lambda_tffo,
             lambda_tff=lambda_tff)
    running_times = dict(t_lambda_tffe=np.sum(t_lambda_tffe),
                         t_lambda_tffo=np.sum(t_lambda_tffo),
                         t_lambda_tff=np.sum(solved_data['t_lambda_tff']),
                         t_arrf=np.sum(solved_data['t_arrf']),
                         t_evdn=np.sum(solved_data['t_evdn']),
                         t_uh_x=np.sum(solved_data['t_uh_x']),
                         t_subreg=solved_data['t_subreg']
                         )
    features = dict(mask_size=np.sum(gmtff.mask > 0),
                    mask_ratio=np.mean(gmtff.mask > 0),
                    n_subregions=gmtff.n_areas,
                    rank_sum=np.sum([s.size for s in gmtff.s_vec_list]),
                    lowest_sv=np.min([np.min(s) for s in gmtff.s_vec_list])
                    )
    return dict(**running_times, **sdr_res, **is_res, **features)


def create_and_run_light_experiment():
    """
    Create a light experiment and run it
    """
    exp = SolveTffExperiment.get_experiment(setting='light', force_reset=True)
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
