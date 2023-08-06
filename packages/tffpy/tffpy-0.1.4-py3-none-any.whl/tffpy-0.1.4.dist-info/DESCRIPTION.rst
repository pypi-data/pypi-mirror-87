tffpy
=====

A Python package for time-frequency fading using Gabor multipliers based on
the work in paper *Time-frequency fading algorithms based on Gabor
multipliers* by A. Marina Krémé, Valentin Emiya, Caroline
Chaux and Bruno Torré́sani, 2020.

Install
-------

Install the current release with ``pip``::

    pip install tffpy

Download the data from `this link <https://gitlab.lis-lab.fr/skmad-suite/tff2020/-/archive/master/tff2020-master.zip?path=data>`_.

Then run function `tffpy.utils.generate_config` in order to create
a configuration file and modify it to specify the path to your data folder.
The location of the configuration file is given by function
`tffpy.utils.get_config_file`.

For additional details, see doc/install.rst.

Usage
-----

See the `documentation <http://skmad-suite.pages.lis-lab.fr/tff2020/>`_.

Bugs
----

Please report any bugs that you find through the `tffpy GitLab project
<https://gitlab.lis-lab.fr/skmad-suite/tff2020/issues>`_.

You can also fork the repository and create a merge request.

Source code
-----------

The source code of tffpy is available via its `GitLab project
<https://gitlab.lis-lab.fr/skmad-suite/tff2020>`_.

You can clone the git repository of the project using the command::

    git clone git@gitlab.lis-lab.fr:skmad-suite/tff2020.git

Copyright © 2020
----------------

* `Laboratoire d'Informatique et Systèmes <http://www.lis-lab.fr/>`_
* `Université d'Aix-Marseille <http://www.univ-amu.fr/>`_
* `Centre National de la Recherche Scientifique <http://www.cnrs.fr/>`_
* `Université de Toulon <http://www.univ-tln.fr/>`_

Contributors
------------

* `Valentin Emiya <mailto:valentin.emiya@lis-lab.fr>`_
* `Ama Marina Krémé <mailto:ama-marina.kreme@lis-lab.fr>`_

License
-------

Released under the GNU General Public License version 3 or later
(see `LICENSE.txt`).


