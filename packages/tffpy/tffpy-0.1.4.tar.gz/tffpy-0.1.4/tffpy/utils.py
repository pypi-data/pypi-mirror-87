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
"""Utils classes and functions for tffpy.

.. moduleauthor:: Valentin Emiya
"""
import os
from pathlib import Path
from configparser import ConfigParser
import numpy as np
import matplotlib.pyplot as plt

from ltfatpy import plotdgtreal, dgtreal, idgtreal


def plot_mask(mask, hop, n_bins, fs):
    """
    Plot time-frequency mask

    Parameters
    ----------
    mask : nd-array
        Time-frequency mask
    hop : int
        Hop size
    n_bins : int
        Number of frequency bins
    fs : int
        Sampling frequency
    """
    plotdgtreal(coef=mask.astype(float), a=hop, M=n_bins, fs=fs,
                normalization='lin')


def plot_win(win, fs, label=None):
    """
    Plot window

    Parameters
    ----------
    win : nd-array
        Window array
    fs : int
        Sampling frequency
    label : str or None
        If not None, label to be assigned to the curve.
    """
    x_range = np.fft.fftshift(np.arange(win.size) / fs)
    x_range[x_range > x_range[-1]] -= x_range.size / fs
    if label is None:
        plt.plot(x_range, np.fft.fftshift(win))
    else:
        plt.plot(x_range, np.fft.fftshift(win), label=str(label))
        plt.legend()
    plt.xlabel('Time (s)')
    plt.grid()


def plot_spectrogram(x, dgt_params, fs, dynrange=100, clim=None):
    """
    Plot spectrogram of a signal

    Parameters
    ----------
    x : nd-array
        Signal
    dgt_params : dict
        DGT parameters (see `tffpy.tf_tools.get_dgt_params`)
    fs : int
        Sampling frequency
    dynrange : float
        Dynamic range to be displayed.
    clim : sequence
        Min and max values for the colorbar. If both `clim` and `dynrange` are
        specified, then clim takes precedence.
    """
    tf_mat = dgt(x, dgt_params=dgt_params)
    plotdgtreal(coef=tf_mat, a=dgt_params['hop'], M=dgt_params['n_bins'],
                fs=fs, dynrange=dynrange, clim=clim)


def db(x):
    """
    Linear to decibel (dB) conversion

    Parameters
    ----------
    x : scalar or nd-array
        Values to be converted

    Returns
    -------
    scalar or nd-array
        Conversion of input `x` in dB.
    """
    return 20 * np.log10(np.abs(x))


def sdr(x_ref, x_est):
    """
    Signal to distortion ratio

    Parameters
    ----------
    x_ref : nd-array
        Reference signal
    x_est : nd-array
        Estimation of the reference signal

    Returns
    -------
    float
    """
    return snr(x_signal=x_ref, x_noise=x_est - x_ref)


def snr(x_signal, x_noise):
    """
    Signal to noise ratio

    Parameters
    ----------
    x_signal : nd-array
        Signal of interest
    x_noise : nd-array
        Noise signal

    Returns
    -------
    float
    """
    return db(np.linalg.norm(x_signal)) - db(np.linalg.norm(x_noise))


def is_div_spectrum(x_ref, x_est):
    """
    Itakura-Saito divergence computed via discrete Fourier transform

    Parameters
    ----------
    x_ref : nd-array
        Reference signal
    x_est : nd-array
        Estimation of the reference signal

    Returns
    -------
    float
    """
    return is_div(x_ref=np.abs(np.fft.fft(x_ref)),
                  x_est=np.abs(np.fft.fft(x_est)))


def is_div(x_ref, x_est):
    """
    Itakura-Saito divergence

    Parameters
    ----------
    x_ref : nd-array
        Reference array
    x_est : nd-array
        Estimation of the reference array

    Returns
    -------
    float
    """
    x_ratio = x_ref / x_est
    return np.sum(x_ratio - np.log(x_ratio)) - np.size(x_ratio)


def dgt(sig, dgt_params):
    """
    Discrete Gabor transform of a signal

    Parameters
    ----------
    sig : nd-array
        Input signal
    dgt_params : dict
        DGT parameters (see `tffpy.tf_tools.get_dgt_params`)

    Returns
    -------
    nd-array
        DGT coefficients
    """
    return dgtreal(f=sig, g=dgt_params['win'], a=dgt_params['hop'],
                   M=dgt_params['n_bins'], L=sig.shape[0],
                   pt=dgt_params['phase_conv'])[0]


def idgt(tf_mat, dgt_params, sig_len):
    """
    Inverse discrete Gabor transform

    Parameters
    ----------
    tf_mat : nd-array
        DGT coefficients
    dgt_params : dict
        DGT parameters (see `tffpy.tf_tools.get_dgt_params`)
    sig_len : int
        Signal length

    Returns
    -------
    nd-array
        Reconstructed signal
    """
    return idgtreal(coef=tf_mat, g=dgt_params['win'], a=dgt_params['hop'],
                    M=dgt_params['n_bins'], Ls=sig_len,
                    pt=dgt_params['phase_conv'])[0]


def get_config_file():
    """
    User configuration file

    Returns
    -------
    Path
    """
    return Path(os.path.expanduser('~')) / '.config' / 'tffpy.conf'


def generate_config():
    """
    Generate an empty configuration file.
    """

    config = ConfigParser(allow_no_value=True)

    config.add_section('DATA')
    config.set('DATA', '# path to data')
    config.set('DATA', 'data_path', '/to/be/completed/tffpy/data')
    config_file = get_config_file()
    with open(config_file, 'w') as file:
        config.write(file)
    print('Configuration file created: {}. Please update it with your data '
          'path.'.format(config_file))


def get_data_path():
    """
    Read data folder from user configuration file.

    Returns
    -------
    Path
    """
    config_file = get_config_file()
    if not config_file.exists():
        raise Exception('Configuration file does not exists. To create it, '
                        'execute tffpy.utils.generate_config()')
    config = ConfigParser()
    config.read(config_file)
    data_path = Path(config['DATA']['data_path'])
    if not data_path.exists():
        raise Exception('Invalid data path: {}. Update configuration file {}'
                        .format(data_path, config_file))
    return data_path
