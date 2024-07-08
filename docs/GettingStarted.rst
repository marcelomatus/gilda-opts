***************
Getting Started
***************

===================
System Requirements
===================

To use ``GILDA-OPTS`` you will need:

* Phyton 3.11.9
* Phython libraries or packages:

  * pip 24.0
  * Sphinx 7.3.7
  * pyomo
  * numpy

* A mixed integer linear programming solver (as CBC, Gurobi)

For the hardware requirements, please refer to the system requirements for the version of ``Python`` that you are using.

============
Installation
============

The sources for ``GILDA-OPTS`` can be downloaded from the `Github repository`_.

1. You can either clone the public repository:

   ``>git clone https://github.com/marcelomatus/gilda-opts.git``

2. Once you have a copy of the source, you can install it running this command in your terminal:

   ``> pip install gilda-opts``

This is the preferred method to install ``GILDA-OPTS``, as it will always install the most recent stable release.

Once installed, you can verify that ``GILDA-OPTS`` is available by executing:

   ``> gilda_opts -h``

This should display the following ``GILDA-OPTS`` options:

=======================================  ================================================= 
-h, --help                               show this help message and exit
--version                                show program's version number and exit
-i INFILE_NAME, --infile INFILE_NAME     Json input file. Stdinp is used if not provided.
-o OUTFILE_NAME, --outfile OUTFILE_NAME  Json output file. Stdout is used if not provided.
-v, --verbose                            set loglevel to INFO
-vv, --very-verbose                      set loglevel to DEBUG
-k, --keepfiles                          If included, the solver keepfiles option is used
-s SOLVER, --solver SOLVER               Defines the solver to be used (default: cbc)
=======================================  =================================================

====================
Running a Simulation
====================
To run a simulation, you must follow three steps. First, prepare the input data to define all of the relevant system parameters. Then invoke the function to run the simulation. Finally, you can access the results saved in output data files.

^^^^^^^^^^^^^^^^^^^^^^^^^
Preparing Case Input Data
^^^^^^^^^^^^^^^^^^^^^^^^^
The full details of the input data files are documented in :any:`Modelling`. The ``GILDA-OPTS`` distribution also includes some `Examples`_ that illustrate how to accurately input data to construct and simulate the system.

^^^^^^^^^^^^^^^^
Solving the Case
^^^^^^^^^^^^^^^^
The solver is invoked by calling the main simulation function ``GILDA-OPTS`` followed by the name of the case file. For example, to run the system case defined through the ``demand_grid.json`` file, type at the command ``shell`` or ``prompt``:

> gilda_opts -i cases/demand_grid.json

The results of the simulation will be printed on the screen.

^^^^^^^^^^^^^^^^^^^^
Accesing the Results
^^^^^^^^^^^^^^^^^^^^
The simulation results are printed on the screen and saved to several output files located at the directory ??


.. _Github repository: https://github.com/marcelomatus/gilda-opts
