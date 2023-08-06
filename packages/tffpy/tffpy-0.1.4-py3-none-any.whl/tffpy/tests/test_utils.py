import unittest
from unittest.mock import patch
import tempfile
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
from pathlib import Path
from configparser import ConfigParser

from tffpy.utils import generate_config, get_data_path


class TestGenerateConfig(unittest.TestCase):
    def test_generate_config(self):
        with patch('tffpy.utils.get_config_file') as mock:
            mock.return_value = Path(tempfile.mkdtemp()) / 'tffpy.conf'
            config_file = mock.return_value
            self.assertFalse(config_file.exists())
            generate_config()
            self.assertTrue(config_file.exists())


class TestGetDataPath(unittest.TestCase):
    def test_get_data_path(self):
        with patch('tffpy.utils.get_config_file') as mock:
            mock.return_value = Path(tempfile.mkdtemp()) / 'tffpy.conf'
            config_file = mock.return_value

            self.assertFalse(config_file.exists())
            with self.assertRaises(Exception):
                get_data_path()

            generate_config()
            with self.assertRaises(Exception):
                get_data_path()

            config = ConfigParser()
            config.read(config_file)
            true_data_path = Path(__file__).absolute().parents[3] / 'data'
            print(true_data_path)
            self.assertTrue(true_data_path.exists())
            print('Data path:', str(true_data_path))
            config.set('DATA', 'data_path', str(true_data_path))
            config.write(open(config_file, 'w'))
            tested_data_path = get_data_path()
            self.assertEqual(tested_data_path, true_data_path)
