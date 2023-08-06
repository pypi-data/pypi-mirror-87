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
"""Test of the module :module:`tffpy.datasets`

.. moduleauthor:: Valentin Emiya
"""
import unittest
import numpy as np

from tffpy.datasets import get_mix, get_dataset
from tffpy.utils import snr


class TestGetMix(unittest.TestCase):

    def setUp(self):
        dataset = get_dataset()
        self.loc_source_list = list(dataset['localized'].keys())
        self.wb_source_list = list(dataset['wideband'].keys())

    def test_snr(self):
        loc_source = self.loc_source_list[0]
        wb_source = self.wb_source_list[0]
        for wb_to_loc_ratio_db in [-10, -3, 0, 6]:
            x_mix, dgt_params, signal_params, mask, x_loc, x_wb = \
                get_mix(loc_source=loc_source, wideband_src=wb_source,
                        wb_to_loc_ratio_db=wb_to_loc_ratio_db,
                        win_dur=128 / 8000, win_type='gauss',
                        hop_ratio=1 / 4, n_bins_ratio=4, n_iter_closing=2,
                        n_iter_opening=2, delta_mix_db=0, delta_loc_db=30,
                        closing_first=True, fig_dir=None)
            np.testing.assert_array_almost_equal(x_mix, x_loc + x_wb)
            np.testing.assert_almost_equal(snr(x_signal=x_wb, x_noise=x_loc),
                                           wb_to_loc_ratio_db)

