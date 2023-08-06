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
Class :class:`GabMulTff` is the main object to solve a time-frequency fading
problem.

.. moduleauthor:: Valentin Emiya
"""
from time import perf_counter
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar, minimize
from matplotlib import pyplot as plt
from ltfatpy import plotdgtreal

from skpomade.range_approximation import \
    adaptive_randomized_range_finder, randomized_range_finder
from skpomade.factorization_construction import evd_nystrom

from tffpy.tf_tools import GaborMultiplier
from tffpy.create_subregions import create_subregions
from tffpy.utils import dgt, plot_spectrogram, db


class GabMulTff:
    """
    Time-frequency fading using Gabor multipliers

    Main object to solve the TFF problem

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
    tol_subregions : None or float
        If None, the mask is considered as a single region. If float,
        tolerance to split the mask into sub-regions using
        :py:func:`~tffpy.create_subregions.create_subregions`.
    fig_dir : str or Path
        If not None, folder where figures are stored. If None, figures are
        not plotted.
    """

    def __init__(self, x_mix, mask, dgt_params, signal_params,
                 tol_subregions=None, fig_dir=None):
        self.x_mix = x_mix
        self.dgt_params = dgt_params
        self.signal_params = signal_params
        self.tol_subregions = tol_subregions
        self.t_subreg = None
        if tol_subregions is not None:
            if np.issubdtype(mask.dtype, np.bool_):
                t0 = perf_counter()
                mask = create_subregions(mask_bool=mask,
                                         dgt_params=dgt_params,
                                         signal_params=signal_params,
                                         tol=tol_subregions,
                                         fig_dir=fig_dir)
                self.t_subreg = perf_counter() - t0
            n_areas = np.unique(mask).size - 1
            self.mask = mask
        else:
            n_areas = 1
            self.mask = mask > 0
        self.gabmul_list = [GaborMultiplier(mask=(mask == i + 1),
                                            dgt_params=dgt_params,
                                            signal_params=signal_params)
                            for i in range(n_areas)]
        self.s_vec_list = [None for i in range(n_areas)]
        self.u_mat_list = [None for i in range(n_areas)]
        self.uh_x_list = [None for i in range(n_areas)]
        self.t_arrf = [None for i in range(n_areas)]
        self.t_evdn = [None for i in range(n_areas)]
        self.t_uh_x = [None for i in range(n_areas)]
        self.fig_dir = fig_dir
        if fig_dir is not None:
            fig_dir = Path(fig_dir)
            fig_dir.mkdir(parents=True, exist_ok=True)

    @property
    def n_areas(self):
        """
        Number of sub-regions
        """
        return len(self.u_mat_list)

    def compute_decomposition(self, tolerance_arrf, proba_arrf, rand_state=0):
        """
        Decompose each Gabor multiplier using a random EVD

        The decomposition is obtained using
        :py:func:`skpomade.range_approximation.adaptive_randomized_range_finder`
        followed by :py:func:`skpomade.factorization_construction.evd_nystrom`.
        The rank of each decomposition is estimated using parameters
        `tolerance_arrf` and `proba_arrf`.
        Running times to compute the range approximation, the
        EVD itself and the additional matrix products for subsequent
        computations are stored in attributes `t_arrf`, `t_evdn` and
        `t_uh_x`, respectively.

        Parameters
        ----------
        tolerance_arrf : float
            Tolerance for
            :py:func:`~skpomade.range_approximation.adaptive_randomized_range_finder`
        proba_arrf : float
            Probability of error for
            :py:func:`~skpomade.range_approximation.adaptive_randomized_range_finder`
        rand_state : RandomState, int or None
            If RandomState, random generator.
            If int or None, random seed used to initialize the pseudo-random
            number generator.

        """
        if rand_state is None:
            rand_state = np.random.RandomState(None)
        if np.issubdtype(type(rand_state), np.dtype(int).type):
            rand_state = np.random.RandomState(rand_state)
        for i in range(self.n_areas):
            print('Random EVD of Gabor multiplier #{}'.format(i))
            print('#coefs in mask: {} ({:.1%} missing)'
                  .format(np.sum(self.gabmul_list[i].mask),
                          np.sum(self.gabmul_list[i].mask)
                          / self.gabmul_list[i].mask.size))
            t0 = perf_counter()
            q_mat = adaptive_randomized_range_finder(a=self.gabmul_list[i],
                                                     tolerance=tolerance_arrf,
                                                     proba=proba_arrf, r=None,
                                                     rand_state=rand_state,
                                                     n_cols_Q=32)
            self.t_arrf[i] = perf_counter() - t0
            print('Q shape:', q_mat.shape)
            t0 = perf_counter()
            self.s_vec_list[i], self.u_mat_list[i] = \
                evd_nystrom(a=self.gabmul_list[i], q_mat=q_mat)
            self.t_evdn[i] = perf_counter() - t0
            print('Running times:')
            print('   - adaptive_randomized_range_finder: {} s'.format(
                self.t_arrf[i]))
            print('   - evd_nystrom: {} s'.format(self.t_evdn[i]))

            t0 = perf_counter()
            self.uh_x_list[i] = self.u_mat_list[i].T.conj() @ self.x_mix
            self.t_uh_x[i] = perf_counter() - t0

    def compute_decomposition_fixed_rank(self, rank, rand_state=0):
        """
        Decompose each Gabor multiplier using a random EVD with given rank

        The decomposition is obtained using
        :py:func:`skpomade.range_approximation.randomized_range_finder`
        followed by :py:func:`skpomade.factorization_construction.evd_nystrom`.
        Running times are stored in attributes `t_rrf`, `t_evdn` and `t_uh_x`.

        Parameters
        ----------
        rank : int
            Rank of the decompostion
        rand_state : RandomState, int or None
            If RandomState, random generator.
            If int or None, random seed used to initialize the pseudo-random
            number generator.
        """
        if rand_state is None:
            rand_state = np.random.RandomState(None)
        if np.issubdtype(type(rand_state), np.dtype(int).type):
            rand_state = np.random.RandomState(rand_state)

        t_rrf = [None for i in range(self.n_areas)]
        t_evdn = [None for i in range(self.n_areas)]
        t_uh_x = [None for i in range(self.n_areas)]
        for i in range(self.n_areas):
            print('Random EVD of Gabor multiplier #{}'.format(i))
            print('#coefs in mask: {} ({:.1%})'
                  .format(np.sum(self.gabmul_list[i].mask),
                          np.sum(self.gabmul_list[i].mask)
                          / self.gabmul_list[i].mask.size))
            t0 = perf_counter()
            q_mat = randomized_range_finder(a=self.gabmul_list[i],
                                            n_l=rank,
                                            rand_state=rand_state)
            t_rrf[i] = perf_counter() - t0
            print('Q shape:', q_mat.shape)
            t0 = perf_counter()
            self.s_vec_list[i], self.u_mat_list[i] = \
                evd_nystrom(a=self.gabmul_list[i], q_mat=q_mat)
            t_evdn[i] = perf_counter() - t0
            print('Running times:')
            print('   - randomized_range_finder: {} s'.format(t_rrf[i]))
            print('   - evd_nystrom: {} s'.format(t_evdn[i]))

            t0 = perf_counter()
            self.uh_x_list[i] = self.u_mat_list[i].T.conj() @ self.x_mix
            t_uh_x[i] = perf_counter() - t0

    def compute_estimate(self, lambda_coef):
        """
        Compute the signal estimate for a given hyperparameter
        :math:`\lambda_i` for each sub-region :math:`i`.

        Prior decomposition should have been performed using
        :meth:`compute_decomposition` or
        :meth:`compute_decomposition_fixed_rank`.

        Parameters
        ----------
        lambda_coef : nd-array or float
            If nd-array, hyperparameters :math:`\lambda_i` for each sub-region
            :math:`i`. If float, the same value :math:`\lambda` is used
            for each sub-region.

        Returns
        -------
        nd-array
            Reconstructed signal
        """
        if isinstance(lambda_coef, np.ndarray):
            assert lambda_coef.size == self.n_areas
        else:
            lambda_coef = np.full(self.n_areas, fill_value=lambda_coef)
        x = self.x_mix.copy()
        for i in range(self.n_areas):
            gamma_vec = lambda_coef[i] * self.s_vec_list[i] \
                        / (1 - (1 - lambda_coef[i]) * self.s_vec_list[i])
            x -= self.u_mat_list[i] @ (gamma_vec * self.uh_x_list[i])
        return x

    def compute_lambda(self, x_mix, e_target=None):
        """
        Estimate hyperparameters :math:`\lambda_i` from target energy in each
        sub-region :math:`i`.

        Parameters
        ----------
        x_mix : nd-array
            Mix signal

        e_target : nd-array or None
            Target energy for each sub-region/. If None, function
            :py:func:`estimate_energy_in_mask` is used to estimate the
            target energies.

        Returns
        -------
        lambda_est : nd-array
            Hyperparameters :math:`\lambda_i` for each sub-region :math:`i`.
        t_est : nd-array
            Running time to estimate each hyperparameter.
        """
        if e_target is None:
            e_target = estimate_energy_in_mask(
                x_mix=x_mix, mask=self.mask,
                dgt_params=self.dgt_params, signal_params=self.signal_params,
                fig_dir=self.fig_dir)
        t_est = np.empty(self.n_areas)
        lambda_est = np.empty(self.n_areas)
        for i_area in range(self.n_areas):
            mask_i = self.mask == i_area + 1

            def obj_fun_est(lambda_coef):
                x = self.compute_estimate(lambda_coef)
                x_tf_masked = mask_i * self.gabmul_list[i_area].dgt(x)
                e_mask = np.linalg.norm(x_tf_masked, 'fro') ** 2
                return np.abs(e_target[i_area] - e_mask)

            t0 = perf_counter()
            sol_est = minimize_scalar(obj_fun_est, bracket=[0, 1],
                                      method='brent')
            t_est[i_area] = perf_counter() - t0
            lambda_est[i_area] = sol_est.x
        return lambda_est, t_est


def reconstruction(x_mix, lambda_coef, u_mat, s_vec):
    return GabMulTff(x_mix=x_mix, u_mat=u_mat, s_vec=s_vec)(lambda_coef)


def estimate_energy_in_mask(x_mix, mask, dgt_params, signal_params,
                            fig_dir=None, prefix=None):
    """
    Estimate energy in time-frequency mask

    Parameters
    ----------
    x_mix : nd-array
        Mix signal
    mask: nd-array
        Time-frequency mask for each sub-region
    dgt_params : dict
        DGT parameters
    signal_params : dict
        Signal parameters
    fig_dir : str or Path
        If not None, folder where figures are stored. If None, figures are
        not plotted.
    prefix : str
        If not None, this prefix is used when saving the figures.

    Returns
    -------
    nd-array
        Estimated energy in each sub-region.
    """
    x_tf_mat = dgt(sig=x_mix, dgt_params=dgt_params)
    x_tf_mat[mask > 0] = np.nan
    e_f_mean = np.nanmean(np.abs(x_tf_mat) ** 2, axis=1)

    mask = mask.astype(int)
    n_areas = np.unique(mask).size - 1
    estimated_energy = np.empty(n_areas)
    e_mat = e_f_mean[:, None] @ np.ones((1, x_tf_mat.shape[1]))
    e_mat[mask == 0] = 0
    for i_area in range(n_areas):
        mask_i = mask == i_area + 1
        estimated_energy[i_area] = np.sum(e_mat * mask_i)

    if fig_dir is not None:
        fig_dir = Path(fig_dir)
        fig_dir.mkdir(parents=True, exist_ok=True)
        if prefix is None:
            prefix = ''
        else:
            prefix = prefix + '_'
        dynrange = 100
        c_max = np.nanmax(db(x_tf_mat))
        clim = c_max - dynrange, c_max

        fs = signal_params['fs']
        plt.figure()
        plot_spectrogram(x=x_mix, dgt_params=dgt_params, fs=fs, clim=clim)
        plt.title('Mix')
        plt.savefig(fig_dir / '{}mix.pdf'.format(prefix))

        plt.figure()
        plotdgtreal(coef=np.sqrt(e_mat), a=dgt_params['hop'],
                    M=dgt_params['n_bins'], fs=fs, clim=clim)
        plt.title('Mask filled with average energy (total: {})'
                  .format(estimated_energy))
        plt.savefig(fig_dir / '{}filled_mask.pdf'.format(prefix))

        x_tf_mat[mask > 0] = np.sqrt(e_mat[mask > 0])
        plt.figure()
        plotdgtreal(coef=x_tf_mat, a=dgt_params['hop'],
                    M=dgt_params['n_bins'], fs=fs, clim=clim)
        plt.title('Mix filled with average energy (total: {})'
                  .format(estimated_energy))
        plt.savefig(fig_dir / '{}filled_mask.pdf'.format(prefix))

        plt.figure()
        plt.plot(db(e_f_mean) / 2)
        plt.xlabel('Frequency index')
        plt.ylabel('Average energy')
        plt.title('Average energy per frequency bin in mix')
        plt.savefig(fig_dir / '{}average_energy.pdf'.format(prefix))

        e_f_mean_check = np.mean(np.abs(x_tf_mat) ** 2, axis=1)
        plt.figure()
        plt.plot(db(e_f_mean) / 2, label='Before filling')
        plt.plot(db(e_f_mean_check) / 2, '--', label='After filling')
        plt.xlabel('Frequency index')
        plt.ylabel('Average energy')
        plt.title('Average energy per frequency bin in mix')
        plt.legend()
        plt.savefig(fig_dir / '{}average_energy_check.pdf'.format(prefix))

    return estimated_energy


def compute_lambda_oracle_sdr(gmtff, x_wb):
    """
    Compute oracle value for hyperparameter :math:`\lambda_i` from true
    solution.

    If only one region is considered, the Brent's algorithm is used (see
    :py:func:`scipy.optimize.minimize_scalar`). If multiple sub-regions are
    considered the BFGS
    algorithm is used (see :py:func:`scipy.optimize.minimize`).

    Parameters
    ----------
    gmtff : GabMulTff
    x_wb : nd-array
        True signal for the wideband source.

    Returns
    -------
    lambda_oracle : nd-array
        Oracle values for hyperparameters :math:`\lambda_i` for each
        sub-region :math:`i`.
    t_oracle : nd-array
        Running times for the computation of each hyperparameter
    """
    t0 = perf_counter()

    def obj_fun_oracle(lambda_coef):
        return np.linalg.norm(x_wb - gmtff.compute_estimate(lambda_coef))

    if gmtff.tol_subregions is None:
        sol_oracle = minimize_scalar(obj_fun_oracle,
                                     bracket=[0, 1], method='brent')
        lambda_oracle = np.array([sol_oracle.x])
    else:
        sol_oracle = minimize(obj_fun_oracle,
                              np.ones(gmtff.n_areas),
                              method='BFGS',
                              options={'disp': True})
        lambda_oracle = sol_oracle.x
    t_oracle = perf_counter() - t0
    return lambda_oracle, t_oracle
