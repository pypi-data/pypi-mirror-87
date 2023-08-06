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
from pathlib import Path
from ltfatpy import plotdgtreal

from tffpy.utils import dgt, plot_spectrogram, plot_mask, idgt


def solve_by_interpolation(x_mix, mask, dgt_params, signal_params,
                           fig_dir=None):
    """
    Time-frequency fading solver using linear interpolation and random phases

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
    fig_dir : str or Path
        If not None, folder where figures are stored. If None, figures are
        not plotted.

    Returns
    -------
    nd-array
        Estimated signal
    """
    x_tf = dgt(sig=x_mix, dgt_params=dgt_params)
    mask = mask > 0
    x_tf[mask] = np.nan

    f_range = np.arange(x_tf.shape[0])
    for j in range(x_tf.shape[1]):
        ind_nan = np.isnan(x_tf[:, j])
        x_tf[ind_nan, j] = np.interp(x=f_range[ind_nan],
                                     xp=np.nonzero(~ind_nan)[0],
                                     fp=x_tf[~ind_nan, j])
        x_tf[ind_nan, j] *= np.exp(2 * 1j * np.pi
                                   * np.random.rand(np.sum(ind_nan)))

    x_est = idgt(tf_mat=x_tf, dgt_params=dgt_params,
                 sig_len=signal_params['sig_len'])
    if fig_dir is not None:
        fig_dir = Path(fig_dir)
        fig_dir.mkdir(exist_ok=True, parents=True)

        plt.figure()
        plot_mask(mask=mask, hop=dgt_params['hop'],
                  n_bins=dgt_params['n_bins'], fs=signal_params['fs'])
        plt.title('Mask')
        plt.savefig(fig_dir / 'interp_mask.pdf')

        plt.figure()
        plotdgtreal(coef=x_tf, a=dgt_params['hop'],
                    M=dgt_params['n_bins'], fs=signal_params['fs'])
        plt.title('Interpolated TF matrix')
        plt.savefig(fig_dir / 'interp_tf_est.pdf')

        plt.figure()
        plot_spectrogram(x=x_est, dgt_params=dgt_params,
                         fs=signal_params['fs'])
        plt.title('Reconstructed signal by interp')
        plt.savefig(fig_dir / 'interp_sig_est.pdf')

    return x_est
