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

import numpy as np

from tffpy.datasets import get_mix
from tffpy.interpolation_solver import solve_by_interpolation


class TestInterpolationSolver(unittest.TestCase):
    def test_interpolation_solver(self):
        win_type = 'gauss'
        win_dur = 256 / 8000
        hop_ratio = 1 / 4
        n_bins_ratio = 4
        delta_mix_db = 0
        delta_loc_db = 30
        n_iter_closing = n_iter_opening = 3
        wb_to_loc_ratio_db = 8
        closing_first = True
        or_mask = True

        fig_dir = 'test_fig_interpolation'

        x_mix, dgt_params, signal_params, mask, x_bird, x_engine = \
            get_mix(loc_source='bird', wideband_src='car', crop=4096,
                    wb_to_loc_ratio_db=wb_to_loc_ratio_db,
                    win_dur=win_dur, win_type=win_type,
                    hop_ratio=hop_ratio, n_bins_ratio=n_bins_ratio,
                    n_iter_closing=n_iter_closing,
                    n_iter_opening=n_iter_opening,
                    closing_first=closing_first,
                    delta_mix_db=delta_mix_db, delta_loc_db=delta_loc_db,
                    or_mask=or_mask, fig_dir=fig_dir)

        x_est = solve_by_interpolation(x_mix, mask, dgt_params, signal_params,
                                       fig_dir)
        np.testing.assert_array_equal(x_est.shape, x_mix.shape)

        x_est = solve_by_interpolation(x_mix, mask, dgt_params, signal_params)
        np.testing.assert_array_equal(x_est.shape, x_mix.shape)
