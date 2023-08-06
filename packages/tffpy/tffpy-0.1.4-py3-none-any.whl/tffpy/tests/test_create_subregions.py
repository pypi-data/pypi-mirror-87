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
import unittest
from tffpy.datasets import get_mix
from tffpy.create_subregions import create_subregions


class TestCreateSubregions(unittest.TestCase):
    def test_create_subregions(self):
        fig_dir = 'fig_create_subregions'
        x_mix, dgt_params, signal_params, mask, x_loc, x_wb = \
            get_mix(loc_source='bird',
                    wideband_src='car',
                    crop=4096,
                    win_dur=256 / 8000,
                    win_type='gauss',
                    hop_ratio=1 / 4,
                    n_bins_ratio=4,
                    n_iter_closing=3,
                    n_iter_opening=3,
                    closing_first=True,
                    delta_mix_db=0,
                    delta_loc_db=20,
                    wb_to_loc_ratio_db=16,
                    or_mask=True,
                    fig_dir=None)
        tol = 1e-9
        mask_with_subregions, norms = create_subregions(
            mask_bool=mask, dgt_params=dgt_params, signal_params=signal_params,
            tol=tol, fig_dir=fig_dir, return_norms=True)

        tol = 1e-5
        mask_with_subregions = create_subregions(
            mask_bool=mask, dgt_params=dgt_params, signal_params=signal_params,
            tol=tol, fig_dir=None, return_norms=False)
