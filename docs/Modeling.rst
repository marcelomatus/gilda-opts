.. _Modeling:

*********
Modeling
*********
This chapter focus on the input data structures required to simulate any home energy system with GILDA-OPTS. The simulation setup requires case definition files, in ``json`` format, containing the parameters of the input elements. 

``GILDA-OPTS`` employs standard models typically used for household appliances. Comprehensive information about the element parameters, their definitions and models, the variables introduced by each element, and the output data types can be found in the following sections.

Numbers can be in English format (using a point to separate decimals) or in scientific notation (e.g., 1e3). It is recommended that element names do not include spaces or non-ASCII characters.

============
Data Formats
============

The data files used by ``GILDA-OPTS`` are ``.json`` files which define and return a single structure. The json-file format is plain text and can be edited with any standard text editor.

===============================
Configure the Planning Horizon
===============================

Block

===============
System Elements
===============

-----
Bus
-----

----
Grid
----

------
Demand
------

----------------------------------------
Time Shiftable Smart Appliances - (TSSA)
----------------------------------------

----------------------------------------
Battery Energy Storage System - (BESS)
----------------------------------------

-------------
Local Source
-------------

------------------------------------------
Simplified Building Thermal Model - (SBTM)
------------------------------------------
