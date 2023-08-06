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
""" Base functions and classes.

.. moduleauthor:: Valentin Emiya

"""
import warnings

import numpy as np
from ltfatpy import dgtreal, idgtreal, arg_firwin, gabwin, plotdgtreal
from scipy.sparse.linalg import LinearOperator

from tffpy.utils import plot_mask, plot_win


def get_dgt_params(win_type, approx_win_len, hop, n_bins,
                   phase_conv='freqinv', sig_len=None):
    """
    Build dictionary of DGT parameter

    The output dictionary `dgt_params` is composed of:

    * `dgt_params['win']`: the window array (nd-array)
    * `dgt_params['hop']`: the hop size (int)
    * `dgt_params['n_bins']`: the number of frequency bins (int)
    * `dgt_params['input_win_len']`: the effective window length (input window
      length rounded to the nearest power of two).
    * `dgt_params['phase_conv']`: the phase convention `'freqinv'` or
      `'timeinv'`, see `pt` argument in :py:func:`ltfatpy.gabor.dgtreal`

    Parameters
    ----------
    win_type : str
        Window name, e.g. 'hann', 'gauss' (see :py:func:`ltfatpy.arg_firwin`)
    approx_win_len : int
        Approximate window length
    hop : int
        Hop size
    n_bins : int
        Number of frequency bins
    phase_conv : 'freqinv' or 'timeinv'
        Phase convention
    sig_len : int
        Signal length

    Returns
    -------
    dict
        DGT parameters (see above)
    """
    supported_wins = arg_firwin() | {'gauss'}
    msg = '{} not supported, try {}'.format(win_type, supported_wins)
    assert win_type in supported_wins, msg
    msg = 'Signal length should be given if win_type is "gauss"'
    assert win_type != 'gauss' or sig_len is not None, msg

    input_win_len = int(2 ** np.round(np.log2(approx_win_len)))
    if input_win_len != approx_win_len:
        warnings.warn('Input window length {} has been changed to {}.'
                      .format(approx_win_len, input_win_len))

    if win_type == 'gauss':
        tfr = float((np.pi * input_win_len ** 2) / (4 * sig_len * np.log(2)))
        win, info = gabwin(g={'name': ('tight', 'gauss'), 'tfr': tfr},
                           a=hop, M=n_bins, L=sig_len)
    else:
        win, info = gabwin(g={'name': ('tight', win_type), 'M': input_win_len},
                           a=hop, M=n_bins, L=sig_len)
    return dict(win=win, hop=hop, n_bins=n_bins, input_win_len=input_win_len,
                phase_conv=phase_conv)


def get_signal_params(sig_len, fs):
    """
    Build dictionary of DGT parameter

    The output dictionary `signal_params` is composed of:

    * `signal_params['sig_len']` : the signal length
    * `signal_params['fs']` : the sampling frequency

    This function is only embedding the input parameters into a dictionary
    without changing their values.

    Parameters
    ----------
    sig_len : int
        Signal length
    fs : int
        Sampling frequency

    Returns
    -------
    dict
        See above
    """
    return dict(sig_len=sig_len, fs=fs)


class GaborMultiplier(LinearOperator):
    """
    Gabor multipliers

    Parameters
    ----------
    mask : nd-array
        Time-frequency mask
    dgt_params : dict
        DGT parameters
    signal_params : dict
        Signal parameters
    """

    def __init__(self, mask, dgt_params, signal_params):
        self.sig_len = signal_params['sig_len']
        LinearOperator.__init__(self,
                                dtype=np.float,
                                shape=(self.sig_len, self.sig_len))
        self.win = dgt_params['win']
        self.hop = dgt_params['hop']
        self.n_bins = dgt_params['n_bins']
        self.fs = signal_params['fs']
        self.phase_conv = dgt_params['phase_conv']
        assert mask.shape[0] == self.n_bins // 2 + 1
        assert mask.shape[1] == self.sig_len // self.hop
        self.mask = mask

    # @property
    # def shape(self):
    #     return self.sig_len, self.sig_len

    def _adjoint(self):
        """
        Adjoint of the Gabor multiplier

        Note that since the Gabor multiplier is self-adjoint, this method
        returns the object itself.

        Returns
        -------
        GaborMultiplier
        """
        return self

    def _matvec(self, x):
        if x.ndim == 2:
            x = x.reshape(-1)
        return self.idgt(tf_mat=self.dgt(sig=x) * self.mask)

    def dgt(self, sig):
        """
        Apply the DGT related to the Gabor multiplier

        Parameters
        ----------
        sig : nd-array
            Real signal to be transformed

        Returns
        -------
        nd-array
            DGT coefficients
        """
        return dgtreal(f=sig, g=self.win, a=self.hop, M=self.n_bins,
                       L=self.sig_len, pt=self.phase_conv)[0]

    def idgt(self, tf_mat):
        """
        Apply the invers DGT related to the Gabor multiplier

        Parameters
        ----------
        tf_mat : nd-array
            Time-frequency coefficients (non-negative frequencies only)
        Returns
        -------
        nd-array
            Real signal
        """
        return idgtreal(coef=tf_mat, g=self.win, a=self.hop, M=self.n_bins,
                        Ls=self.sig_len, pt=self.phase_conv)[0]

    def plot_win(self, label=None):
        """
        Plot the window in the current figure.

        Parameters
        ----------
        label : str or None
            If not None, label to be assigned to the curve.
        """
        plot_win(win=self.win, fs=self.fs, label=label)

    def plot_mask(self):
        """
        Plot the time-frequency mask
        """
        plot_mask(mask=self.mask, hop=self.hop, n_bins=self.n_bins, fs=self.fs)

    def compute_ambiguity_function(self, fftshift=True):
        """
        Compute the ambiguity function of the window

        Parameters
        ----------
        fftshift : bool
            If true, shift the window in time before computing its DGT.
        """
        if fftshift:
            w = self.win.copy()
            return self.dgt(np.fft.fftshift(w))
        else:
            return self.dgt(self.win)

    def plot_ambiguity_function(self, dynrange=100, fftshift=True):
        """
        Plot the ambiguity function of the window in the current figure.

        Parameters
        ----------
        dynrange : float
            Dynamic range to be displayed
        fftshift : bool
            If true, shift the window in time before computing its DGT.
        """
        plotdgtreal(
            coef=self.compute_ambiguity_function(fftshift=fftshift),
            a=self.hop, M=self.n_bins, fs=self.fs, dynrange=dynrange)


def generate_rectangular_mask(n_bins, hop, sig_len, t_lim, f_lim):
    """
    Generate a rectangular time-frequency mask

    Parameters
    ----------
    n_bins : int
        Number of frequency bins
    hop : int
        Hop size
    sig_len : int
        Signal length
    t_lim : sequence (2,)
        Time boundaries of the mask
    f_lim : sequence (2,)
        Frequency boundaries of the mask

    Returns
    -------
    nd-array
        The boolean 2D array containing the time-frequency mask (True values)
    """
    f_lim = np.array(f_lim)
    t_lim = np.array(t_lim)
    mask = np.zeros((n_bins // 2 + 1, sig_len // hop), dtype=bool)
    if np.issubdtype(f_lim.dtype, np.dtype(float).type):
        f_lim = np.round(f_lim * mask.shape[0]).astype(int)
    if np.issubdtype(t_lim.dtype, np.dtype(float).type):
        t_lim = np.round(t_lim * mask.shape[1]).astype(int)
    mask[f_lim[0]:f_lim[1], t_lim[0]:t_lim[1]] = True
    return mask
