.. _Modeling:

*********
Modeling
*********
This chapter focus on the input data structures required to simulate any home energy system with ``GILDA-OPTS``. The simulation setup requires case definition files containing the parameters of the input elements.

``GILDA-OPTS`` employs standard models typically used for household appliances. Comprehensive information about the element parameters, their definitions and models, the variables introduced by each element, and the output data types can be found in the following sections.

Numbers can be in English format (using a point to separate decimals) or in scientific notation (e.g., 1e3). It is recommended that element names do not include spaces or non-ASCII characters.

============
Data Formats
============

The data files used by ``GILDA-OPTS`` are ``.json`` files which define and return a single structure. The json-file format is plain text and can be edited with any standard text editor.

===============================
Configure the Planning Horizon
===============================

The planning horizon is segmented into multiple independent time blocks, which can be as short as an hour or less, according to the temporal resolution. The ``block`` parameters are shown below:

.. table:: ``Block`` input parameters
   :widths: auto
   :align: center

   +----------+-------+-------+---------+--------------------------------------------------+
   |  field   | kind  | units | default |                description                       |
   +==========+=======+=======+=========+==================================================+
   | duration | float | hour  |    1    | Block time duration                              |
   +----------+-------+-------+---------+--------------------------------------------------+
   | discount | float | p.u.  |    1    | Discount factor to be used in the LP formulation |
   +----------+-------+-------+---------+--------------------------------------------------+


===============
System Elements
===============

-----
Bus
-----
The ``bus`` element corresponds to the electric bus where the electric elements are connected. The ``bus`` parameters are depicted below :

.. table:: ``Bus`` input parameters
   :widths: auto
   :align: center

   +----------+-------+-------+---------+--------------------------------------------------+
   |  field   | kind  | units | default |                description                       |
   +==========+=======+=======+=========+==================================================+
   | uid      | int   |       |   -1    | Bus unique identifier                            |
   +----------+-------+-------+---------+--------------------------------------------------+
   | name     | str   |       |    1    | Bus name                                         |
   +----------+-------+-------+---------+--------------------------------------------------+


----
Grid
----
``Grid`` element contains the basic grid electric provider. The attributes for the ``Grid`` element are listed below:

.. table:: ``Grid`` input parameters
   :widths: auto
   :align: center

   +-----------------+-------+---------+---------+-----------------------------------------------+
   |     field       | kind  | units   | default |                description                    |
   +=================+=======+=========+=========+===============================================+
   | uid             | int   |         |   -1    | Grid unique identifier                        |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   | name            |  str  |         |    1    | Grid provider name                            |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   |capacity         | float |   KW    |    0    | Connection Capacity                           |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   |energy_buy_price_sched   | float | $/KWh   |         |  List of energy tariff values                 |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   |power_tariff     | float | $/KW    |    0    | Power tariff                                  |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   |power_factor_sched    | float | p.u.    |         | List of power factor values                   |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   |emission_factor_sched | float | gCO2/KWh|         | List of emission factors                      |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   | emission_cost   | float | $/gCO2  |    0    | Emission cost                                 |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   | energy_sell_price_sched   | float | $/KWh   |         | Energy purchase price                    |
   +-----------------+-------+---------+---------+-----------------------------------------------+


------
Demand
------
``Demand`` element represents a base electric load in the scheduling problem. The ``demand`` is modeled as a specified quantity of real power consumed at a ``bus``. The parameters for the ``Demand`` element are listed below.

.. table:: ``Demand`` input parameters
   :widths: auto
   :align: center

   +-----------------+-------+---------+---------+-----------------------------------------------+
   |     field       | kind  | units   | default |                description                    |
   +=================+=======+=========+=========+===============================================+
   | uid             | int   |         |   -1    | Load unique identifier                        |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   | name            |  str  |         |         | Load name                                     |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   |bus_uid          | int   |         |   -1    | Bus uid to be connected to                    |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   |load             | float | KW      |         | List of load values                           |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   |cfail            | float |         |    0    | Cost of fail to supply the load               |
   +-----------------+-------+---------+---------+-----------------------------------------------+


----------------------------------------
Time Shiftable Smart Appliances - (TSSA)
----------------------------------------
``TSSA`` module represents a Time Shiftable Smart Appliance load in the scheduling problem. The attributes for the ``TSSA`` element are showed below:

.. table:: ``TSSA`` input parameters
   :widths: auto
   :align: center

   +-----------------+-------+---------+---------+-------------------------------------------------------------------+
   |     field       | kind  | units   | default |                description                                        |
   +=================+=======+=========+=========+===================================================================+
   | uid             | int   |         |   -1    | TSSA unique identifier                                            |
   +-----------------+-------+---------+---------+-------------------------------------------------------------------+
   | name            |  str  |         |         | TSSA name                                                         |
   +-----------------+-------+---------+---------+-------------------------------------------------------------------+
   |bus_uid          | int   |         |   -1    | Bus uid to be connected to                                        |
   +-----------------+-------+---------+---------+-------------------------------------------------------------------+
   |load             | float |  KW     |    0    | Load value                                                        |
   +-----------------+-------+---------+---------+-------------------------------------------------------------------+
   |on_period        | float |   H     |    0    | 'On' continuous period time                                       |
   +-----------------+-------+---------+---------+-------------------------------------------------------------------+
   |off_indexes      | int   |   H     |         | List of block index where the on-off variable value is set to off |
   +-----------------+-------+---------+---------+-------------------------------------------------------------------+


----------------------------------------
Battery Energy Storage System - (BESS)
----------------------------------------
``BESS`` module represents a Battery Energy Storage System. The parameters for the ``BESS`` element are showed below.

.. table:: ``BESS`` input parameters
   :widths: auto
   :align: center

   +-----------------+-------+---------+---------+-----------------------------------------------+
   |     field       | kind  | units   | default |                description                    |
   +=================+=======+=========+=========+===============================================+
   | uid             | int   |         |   -1    | BESS unique identifier                        |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   | name            |  str  |         |         | BESS name                                     |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   |bus_uid          | int   |         |   -1    | Bus uid to be connected to                    |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   |capacity         | float | KWh     |    0    | Storage capacity                              |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   |max_flow         | float | KW      |    0    | Max In & Out flow                             |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   |efficiency       | float | p.u.    |    1    | In&Out efficiency                             |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   |eini             | float | KWh     |    0    | Start energy stored                           |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   |efin             | float | KWh     |    0    | End energy stored                             |
   +-----------------+-------+---------+---------+-----------------------------------------------+
   |efin_price       | float | $/KWh   |    0    | Energy value at the end of the period         |
   +-----------------+-------+---------+---------+-----------------------------------------------+

-------------
Local Source
-------------
``Local_Source`` module contains the basic local energy source, such as PV or Wind. The attributes for the ``Local_Source`` element are showed below:

.. table:: ``Local_Source`` input parameters
   :widths: auto
   :align: center

   +-----------------+-------+---------+---------+-------------------------------------------------------------------+
   |     field       | kind  | units   | default |                description                                        |
   +=================+=======+=========+=========+===================================================================+
   | uid             | int   |         |   -1    | LocalSource unique identifier                                     |
   +-----------------+-------+---------+---------+-------------------------------------------------------------------+
   | name            |  str  |         |         | LocalSource provider name                                         |
   +-----------------+-------+---------+---------+-------------------------------------------------------------------+
   |capacity         | float |  KW     |   0     | Connection Capacity                                               |
   +-----------------+-------+---------+---------+-------------------------------------------------------------------+
   |generation_profile_sched | float |  p.u. |    0    | Potential generation profile value,as a factor of the capacity    |
   +-----------------+-------+---------+---------+-------------------------------------------------------------------+


------------------------------------------
Single Room Thermal System - (SRTS)
------------------------------------------
``SRTS`` module represents a Single Room Thermal System in the scheduling problem. The parameters for the ``SRTS`` element are showed below.

.. table:: ``SRTS`` input parameters
   :widths: auto
   :align: center

   +-----------------+-------+---------+---------+---------------------------------------------+
   |     field       | kind  | units   | default |            description                      |
   +=================+=======+=========+=========+=============================================+
   | uid             | int   |         |   -1    | SRTS unique identifier                      |
   +-----------------+-------+---------+---------+---------------------------------------------+
   | name            |  str  |         |         | SRTS name                                   |
   +-----------------+-------+---------+---------+---------------------------------------------+
   |bus_uid          |  int  |         |   -1    | Bus uid to be connected to                  |
   +-----------------+-------+---------+---------+---------------------------------------------+
