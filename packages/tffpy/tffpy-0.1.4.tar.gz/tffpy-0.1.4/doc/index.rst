##########################
:mod:`tffpy` documentation
##########################

Overview
========
:py:mod:`tffpy`: time-frequency fading problem and solvers using Gabor
multipliers, based paper
*Time-frequency fading algorithms based on Gabor multipliers*
by M. Kreme, V. Emiya, C. Chaux and B. Torrésani in 2020.

The package :py:mod:`tffpy` includes in particular:

* class :py:class:`tffpy.tf_fading.GabMulTff` that implements the proposed
  solver for reconstructing a source from a mixture and a time-frequency
  binary mask.

* class :py:class:`tffpy.experiments.exp_solve_tff.SolveTffExperiment` to
  conduct the main experiment on mixtures of real sounds, with time-frequency
  masks generated automatically, using the proposed solutions and baseline
  solvers. Script `tffpy.scripts.script_exp_solve_tff` provide example of
  code to handle the experiment (configuring, running on a computer grid or a
  single computer, display results).

Similar and complementary code is available in Matlab.

Documentation
=============

.. only:: html

    :Release: |version|
    :Date: |today|

.. toctree::
    :maxdepth: 1

    installation
    references
    tutorials
    credits


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
