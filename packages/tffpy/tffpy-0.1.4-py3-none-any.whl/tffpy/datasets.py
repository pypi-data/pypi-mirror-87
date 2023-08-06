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
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import \
    binary_opening, binary_closing, generate_binary_structure

from madarrays import Waveform
from ltfatpy import plotdgtreal

from tffpy.tf_tools import get_signal_params, get_dgt_params, GaborMultiplier
from tffpy.utils import dgt, db, plot_spectrogram, plot_mask, get_data_path


default_data_root_dir = get_data_path()
default_data_dir = default_data_root_dir / 'data_8000Hz_16384samples'


def get_dataset():
    """
    Get dataset for isolated wideband and localized sources before mixing.

    Returns
    -------
    dataset : dict
        dataset['wideband'] (resp. dataset['localized']) is a dictionary
        containing the :py:class:`~pathlib.Path` object for all the wideband
        (resp. localized) sounds.
    """
    dataset = dict()
    dataset['wideband'] = {
        x.stem: x
        for x in (default_data_dir / 'wide_band_sources').glob('*.wav')
    }
    dataset['localized'] = {
        x.stem: x
        for x in (default_data_dir / 'localized_sources').glob('*.wav')
    }
    return dataset


def get_mix(loc_source, wideband_src, crop=None,
            wb_to_loc_ratio_db=0, win_dur=128 / 8000, win_type='gauss',
            hop_ratio=1/4, n_bins_ratio=4, n_iter_closing=2,
            n_iter_opening=2, delta_mix_db=0, delta_loc_db=30,
            closing_first=True, or_mask=False,
            fig_dir=None, prefix=''):
    """
    Build the mix two sounds and the related time-frequency boolean mask.

    Parameters
    ----------
    loc_source : Path
        Localized sound file.
    wideband_src : Path
        Wideband sound file.
    crop : int or None
        If not None, a cropped, centered portion of the sound will be
        extracted with the specified length, in samples.
    wb_to_loc_ratio_db : float
        Wideband source to localized source energy ratio to be adjusted in
        the mix.
    win_dur : float
        Window duration, in seconds.
    win_type : str
        Window name
    hop_ratio : float
        Ratio of the window length that will be set as hop size for the DGT.
    n_bins_ratio : float
        Factor that will be applied to the window length to compute the
        number of bins in the DGT.
    delta_mix_db : float
        Coefficient energy ratio, in dB, between the wideband source and the
        localized source in the mixture in order to select coefficients in
        the mask.
    delta_loc_db : float
        Dynamic range, in dB, for the localized source in order to select
        coefficients in the mask.
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
    prefix : str
        If not None, this prefix is used when saving the figures.

    Returns
    -------
    x_mix : Waveform
        Mix signal (sum of outputs `x_loc` and `x_wb`)
    dgt_params : dict
        DGT parameters
    signal_params : dict
        Signal parameters
    mask : nd-array
        Time-frequency binary mask
    x_loc : Waveform
        Localized source signal
    x_wb : Waveform
        Wideband source signal
    """
    dataset = get_dataset()

    x_loc = Waveform.from_wavfile(dataset['localized'][loc_source])
    x_wb = Waveform.from_wavfile(dataset['wideband'][wideband_src])
    np.testing.assert_array_equal(x_loc.shape, x_wb.shape)
    if crop is not None:
        x_len = crop
        i_start = (x_loc.shape[0] - x_len) // 2
        x_loc = x_loc[i_start:i_start+x_len]
        x_wb = x_wb[i_start:i_start+x_len]
    signal_params = get_signal_params(sig_len=x_loc.shape[0], fs=x_loc.fs)

    # Unit energy
    x_loc /= np.linalg.norm(x_loc)
    x_wb /= np.linalg.norm(x_wb)
    gain_wb = 1 / (1 + 10 ** (-wb_to_loc_ratio_db / 20))
    x_loc *= (1 - gain_wb)
    x_wb *= gain_wb

    # Build mix
    x_mix = x_loc + x_wb

    # Build dgt
    fs = x_loc.fs
    approx_win_len = int(2 ** np.round(np.log2(win_dur * fs)))
    hop = int(approx_win_len * hop_ratio)
    n_bins = int(approx_win_len * n_bins_ratio)
    sig_len = x_loc.shape[0]
    dgt_params = get_dgt_params(win_type=win_type,
                                approx_win_len=approx_win_len,
                                hop=hop, n_bins=n_bins, sig_len=sig_len)

    tf_mat_loc_db = db(np.abs(dgt(x_loc, dgt_params=dgt_params)))
    tf_mat_wb_db = db(np.abs(dgt(x_wb, dgt_params=dgt_params)))

    # Build mask_raw
    mask_mix = tf_mat_loc_db > tf_mat_wb_db + delta_mix_db
    mask_loc = tf_mat_loc_db > tf_mat_loc_db.max() - delta_loc_db

    if or_mask:
        mask_raw = np.logical_or(mask_mix, mask_loc)
    else:
        mask_raw = np.logical_and(mask_mix, mask_loc)

    struct = generate_binary_structure(2, 1)
    if n_iter_closing > 0:
        if closing_first:
            mask = binary_opening(
                binary_closing(input=mask_raw, structure=struct,
                               iterations=n_iter_closing, border_value=1),
                iterations=n_iter_opening, structure=struct, border_value=0)
        else:
            mask = binary_closing(
                binary_opening(input=mask_raw,structure=struct,
                               iterations=n_iter_opening, border_value=0),
                iterations=n_iter_closing, structure=struct, border_value=1)
    else:
        mask = mask_raw


    if fig_dir is not None:
        fig_dir = Path(fig_dir)
        fig_dir.mkdir(exist_ok=True, parents=True)
        if len(prefix) > 0:
            prefix = prefix + '_'

        plt.figure()
        plot_mask(mask=mask_mix, hop=dgt_params['hop'],
                  n_bins=dgt_params['n_bins'], fs=signal_params['fs'])
        plt.title('Mask Mix - Area: {} ({:.1%})'.format(mask_mix.sum(),
                                                        np.average(mask_mix)))
        plt.tight_layout()
        plt.savefig(fig_dir / 'mask_mix.pdf')

        plt.figure()
        plot_mask(mask=mask_loc, hop=dgt_params['hop'],
                  n_bins=dgt_params['n_bins'], fs=signal_params['fs'])
        plt.title('Mask Loc - Area: {} ({:.1%})'.format(mask_loc.sum(),
                                                        np.average(mask_loc)))
        plt.tight_layout()
        plt.savefig(fig_dir / 'mask_loc.pdf')

        plt.figure()
        plot_spectrogram(x=x_mix, dgt_params=dgt_params, fs=fs)
        plt.title('Mix')
        plt.tight_layout()
        plt.savefig(fig_dir / 'mix_spectrogram.pdf')

        plt.figure()
        plot_mask(mask=mask_raw, hop=dgt_params['hop'],
                  n_bins=dgt_params['n_bins'], fs=fs)
        plt.title('Raw mask')
        plt.tight_layout()
        plt.savefig(fig_dir / 'raw_mask.pdf')

        plt.figure()
        plot_mask(mask=mask, hop=dgt_params['hop'],
                  n_bins=dgt_params['n_bins'], fs=fs)
        plt.tight_layout()
        plt.title('Smoothed mask')
        plt.savefig(fig_dir / 'smoothed_mask.pdf')

        plt.figure()
        plot_spectrogram(x=x_loc, dgt_params=dgt_params, fs=fs)
        plt.title('Loc')
        plt.tight_layout()
        plt.savefig(fig_dir / 'loc_source.pdf')

        plt.figure()
        tf_mat = dgt(x_loc, dgt_params=dgt_params) * mask
        plotdgtreal(coef=tf_mat, a=dgt_params['hop'], M=dgt_params['n_bins'],
                    fs=fs, dynrange=100)
        plt.title('Masked loc')
        plt.tight_layout()
        plt.savefig(fig_dir / 'masked_loc.pdf')

        plt.figure()
        gabmul = GaborMultiplier(mask=~mask,
                                 dgt_params=dgt_params,
                                 signal_params=signal_params)
        x_est = gabmul @ x_wb
        plot_spectrogram(x=x_est, dgt_params=dgt_params, fs=fs)
        plt.title('Filtered wb')
        plt.tight_layout()
        plt.savefig(fig_dir / 'zerofill_spectrogram.pdf'.format(prefix))

    return x_mix, dgt_params, signal_params, mask, x_loc, x_wb
