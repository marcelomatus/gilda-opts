***************
Getting Started
***************

===================
System Requirements
===================

To use Gilda-opts you will need:
Phyton 3.9
Phython libraries or packages:
   pip 19.2.3

For the hardware requirements, please refer to the system requirements for the version of ``Python`` that you are using.

============
Installation
============

The sources for FESOP can be downloaded from the `Github repository`_.

1. You can either clone the public repository:

   ``>git clone https://github.com/marcelomatus/gilda-opts.git``

2. Once you have a copy of the source, you can install it running this command in your terminal:

   ``> pip install gilda-opts``

This is the preferred method to install ``gilda-opts``, as it will always install the most recent stable release.

====================
Running a Simulation
====================
To run a simulation, you must follow three steps. First, prepare the input data to define all of the relevant system parameters. Then invoke the function to run the simulation. Finally, you can access the results saved in output data files.

^^^^^^^^^^^^^^^^^^^^^^^^^
Preparing Case Input Data
^^^^^^^^^^^^^^^^^^^^^^^^^
The full details of the input data files are documented in Chapter x. The GILDA-OPTS distribution also includes some examples described a bit further in Chapter Y.

^^^^^^^^^^^^^^^^
Solving the Case
^^^^^^^^^^^^^^^^
The solver is invoked by calling the main simulation function ``gilda-opts`` followed by the name of the case file. For example, to run the system case defined through the ``demand_grid.json`` file, type at the command ``shell`` or ``prompt``:

> gilda_opts -i cases/demand_grid.json

The following message will be generated:

^^^^^^^^^^^^^^^^^^^^
Accesing the Results
^^^^^^^^^^^^^^^^^^^^
The simulation results are saved to several output files located at the directory


.. _Github repository: https://github.com/marcelomatus/gilda-opts
