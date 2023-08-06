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
# TODO check if eigs(, 1) can be replaced by Halko to run faster
from pathlib import Path
import warnings
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label
from scipy.sparse.linalg import eigs

from tffpy.utils import plot_mask
from tffpy.tf_tools import GaborMultiplier


def create_subregions(mask_bool, dgt_params, signal_params, tol,
                      fig_dir=None, return_norms=False):
    """
    Create sub-regions from boolean mask and tolerance on sub-region distance.

    See Algorithm 3 *Finding sub-regions for TFF-P* in the reference paper.

    Parameters
    ----------
    mask_bool : nd-array
        Time-frequency boolean mask
    dgt_params : dict
        DGT parameters
    signal_params : dict
        Signal parameters
    tol : float
        Tolerance on sub-region distance (spectral norm of the composition
        of the Gabor multipliers related to two candidate sub-regions).
    fig_dir : Path
        If not None, folder where figures are stored. If None, figures are
        not plotted.
    return_norms : bool
        If True, the final distance matrix is returned as a second output.

    Returns
    -------
    mask_labeled : nd-array
        Time-frequency mask with one positive integer for each sub-region
        and zeros outside sub-regions.
    pq_norms : nd-array
        Matrix of distances between sub-regions.
    """
    mask_labeled, n_labels = label(mask_bool)
    pq_norms = _get_pq_norms(mask=mask_labeled,
                             dgt_params=dgt_params, signal_params=signal_params)

    if fig_dir is not None:
        fig_dir = Path(fig_dir)
        fig_dir.mkdir(parents=True, exist_ok=True)

        plt.figure()
        plot_mask(mask=mask_labeled, hop=dgt_params['hop'],
                  n_bins=dgt_params['n_bins'], fs=signal_params['fs'])
        plt.set_cmap('nipy_spectral')
        plt.title('Initial subregions')
        plt.savefig(fig_dir / 'initial_subregions.pdf')

        # from matplotlib.colors import LogNorm
        plt.figure()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            plt.imshow(np.log10(pq_norms+pq_norms.T), origin='lower')
        plt.ylabel('Sub-region index')
        plt.xlabel('Sub-region index')
        plt.colorbar()
        plt.set_cmap('viridis')
        plt.title('Initial norms of Gabor multiplier composition')
        plt.savefig(fig_dir / 'initial_norms.pdf')
        n_labels_max = n_labels

    while pq_norms.max() > tol:
        # Merge each pair (p, q), q < p, such that pq_norms[p, q] > tol
        to_be_updated = [False] * n_labels
        while pq_norms.max() > tol:
            i_p, i_q = np.unravel_index(np.argmax(pq_norms, axis=None),
                                        pq_norms.shape)
            mask_labeled, pq_norms = _merge_subregions(mask=mask_labeled,
                                                       pq_norms=pq_norms,
                                                       i_p=i_p, i_q=i_q)
            to_be_updated[i_q] = True
            to_be_updated[i_p] = to_be_updated[-1]
            to_be_updated = to_be_updated[:-1]
            n_labels -= 1
        for i_p in range(n_labels):
            if to_be_updated[i_p]:
                _update_pq_norms(mask=mask_labeled,
                                 pq_norms=pq_norms, i_p=i_p,
                                 dgt_params=dgt_params,
                                 signal_params=signal_params)
        # print('Merge sub-region p={}'.format(i_p))

        if fig_dir is not None:
            plt.figure()
            plot_mask(mask=mask_labeled, hop=dgt_params['hop'],
                      n_bins=dgt_params['n_bins'], fs=signal_params['fs'])
            plt.title('subregions')
            plt.set_cmap('nipy_spectral')
            plt.savefig(fig_dir / 'subregions_i{}.pdf'
                        .format(n_labels_max-n_labels))

            plt.figure()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                plt.imshow(np.log10(pq_norms+pq_norms.T), origin='lower')
            plt.ylabel('Sub-region index')
            plt.xlabel('Sub-region index')
            plt.colorbar()
            plt.set_cmap('viridis')
            plt.title('norms of Gabor multiplier composition')
            plt.savefig(fig_dir / 'norms__i{}.pdf'
                        .format(n_labels_max-n_labels))

    if fig_dir is not None:
        plt.figure()
        plot_mask(mask=mask_labeled, hop=dgt_params['hop'],
                  n_bins=dgt_params['n_bins'], fs=signal_params['fs'])
        plt.title('Final subregions')
        plt.set_cmap('nipy_spectral')
        plt.savefig(fig_dir / 'final_subregions.pdf')

        plt.figure()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            plt.imshow(np.log10(pq_norms+pq_norms.T), origin='lower')
        plt.ylabel('Sub-region index')
        plt.xlabel('Sub-region index')
        plt.colorbar()
        plt.set_cmap('viridis')
        plt.title('Final norms of Gabor multiplier composition')
        plt.savefig(fig_dir / 'final_norms.pdf')

    if return_norms:
        return mask_labeled, pq_norms
    else:
        return mask_labeled


def _get_pq_norms(mask, dgt_params, signal_params):
    """
    Compute distance matrix between sub-regions.

    Parameters
    ----------
    mask : nd-array
        Time-frequency mask with one positive integer for each sub-region
        and zeros outside sub-regions.
    dgt_params : dict
        DGT parameters
    signal_params : dict
        Signal parameters

    Returns
    -------
    pq_norms : nd-array
        Matrix of distances between sub-regions.
    """
    n_labels = np.unique(mask).size - 1
    pq_norms = np.zeros((n_labels, n_labels))
    for i_p in range(n_labels):
        for i_q in range(i_p):
            gabmul_p = GaborMultiplier(mask=(mask == i_p + 1),
                                       dgt_params=dgt_params,
                                       signal_params=signal_params)
            gabmul_q = GaborMultiplier(mask=(mask == i_q + 1),
                                       dgt_params=dgt_params,
                                       signal_params=signal_params)
            gabmul_pq = gabmul_p @ gabmul_q
            pq_norms[i_p, i_q] = \
                np.real(eigs(A=gabmul_pq, k=1, return_eigenvectors=False)[0])
    return pq_norms


def _update_pq_norms(mask, pq_norms, i_p, dgt_params, signal_params):
    """
    Update (in-place) distance between one particular sub-region and all
    sub-regions in distance matrix.

    Parameters
    ----------
    mask : nd-array
        Time-frequency mask with one positive integer for each sub-region
        and zeros outside sub-regions.
    pq_norms : nd-array
        Matrix of distances between sub-regions, updated in-place.
    i_p : int
        Index of sub-region to be updated
    dgt_params : dict
        DGT parameters
    signal_params : dict
        Signal parameters

    """
    n_labels = pq_norms.shape[0]
    gabmul_p = GaborMultiplier(mask=(mask == i_p + 1),
                               dgt_params=dgt_params,
                               signal_params=signal_params)
    for i_q in range(n_labels):
        if i_p == i_q:
            continue
        gabmul_q = GaborMultiplier(mask=(mask == i_q + 1),
                                   dgt_params=dgt_params,
                                   signal_params=signal_params)
        gabmul_pq = gabmul_p @ gabmul_q
        gabmul_pq_norm = \
            np.real(eigs(A=gabmul_pq, k=1, return_eigenvectors=False)[0])
        if i_q < i_p:
            pq_norms[i_p, i_q] = gabmul_pq_norm
        else:
            pq_norms[i_q, i_p] = gabmul_pq_norm


def _merge_subregions(mask, pq_norms, i_p, i_q):
    """
    Merge two sub-regions indexed by `i_p` and `i_q`


    In the time-frequency mask, the label of the region indexed by `i_p`
    will be replace by the label of the region indexed by `i_q` and index
    `i_p` will be used to relabel the region with highest label.

    In the distance matrix, rows and columns will be moved consequently. The
    distance between the new, merged sub-region and all other sub-regions is
    not updated; it can be done by calling :py:func:`_update_pq_norms`.

    Parameters
    ----------
    mask : nd-array
        Time-frequency mask with one positive integer for each sub-region
        and zeros outside sub-regions.
    pq_norms : nd-array
        Matrix of distances between sub-regions.
    i_p : int
        Index of sub-region that will be removed after merging.
    i_q : int
        Index of sub-region that will receive the result.
    Returns
    -------
    mask : nd-array
        Updated time-frequency mask with one positive integer for each
        sub-region and zeros outside sub-regions.
    pq_norms : nd-array
        Updated distance matrix (except for distance with the new sub-region).

    """
    p = i_p + 1
    q = i_q + 1

    n_labels = pq_norms.shape[0]
    mask[mask == p] = q
    mask[mask == n_labels] = p
    pq_norms[i_p, :i_p - 1] = pq_norms[-1, :i_p - 1]
    pq_norms[i_p:, i_p] = pq_norms[-1, i_p:]
    pq_norms = pq_norms[:-1, :-1]
    return mask, pq_norms
