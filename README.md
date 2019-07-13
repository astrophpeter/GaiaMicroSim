# GaiaMicroSim
Simulations of Gaia Microlensing Events

## Structure of the Repository

* `GOST_data/` data from Gaia Observation Forecast Tool is stored here. Each file has the name corresponding to the background source of the event. "\<Gaia DR2 backgound source id\>_gost.csv."
* `astrometry_util.py Contains helper functoins that deal with calculating the projected postions of stars and astrometric microlensing deflections.
* `query_util.py` Contains helper functions that deal with getting astrometric data on the source and lens from the Gaia DR2 catalog and mass estimates of the lenses.
 
