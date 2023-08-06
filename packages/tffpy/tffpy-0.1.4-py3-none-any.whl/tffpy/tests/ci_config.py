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
    Create configuration files for continuous integration.

.. moduleauthor:: Valentin Emiya
"""
from configparser import ConfigParser
from pathlib import Path
import os

from yafe.utils import ConfigParser as YafeConfigParser

from tffpy.utils import get_config_file, generate_config


def create_config_files():
    config_file = get_config_file()
    if not config_file.exists():
        generate_config()
        config = ConfigParser()
        config.read(config_file)
        data_path = Path(__file__).absolute().parents[3] / 'data'
        print('Data path:', str(data_path))
        config.set('DATA', 'data_path', str(data_path))
        config.write(open(config_file, 'w'))

    yafe_config_file = YafeConfigParser._config_path
    print('Yafe configuration file:', yafe_config_file)
    if not yafe_config_file.exists():
        yafe_user_path = Path(os.path.expanduser('~')) / 'yafe_user_path'
        yafe_logger_path = Path(os.path.expanduser('~')) / 'yafe_logger_path'
        print(yafe_user_path)
        print(yafe_logger_path)
        yafe_user_path.mkdir(parents=True, exist_ok=True)
        yafe_logger_path.mkdir(parents=True, exist_ok=True)
        YafeConfigParser.generate_config()
        yafe_config_parser = YafeConfigParser()
        yafe_config_parser.set('USER', 'data_path', str(yafe_user_path))
        yafe_config_parser.set('LOGGER', 'path', str(yafe_logger_path))
        yafe_config_parser.write(open(yafe_config_file, 'w'))

if __name__ == '__main__':
    create_config_files()