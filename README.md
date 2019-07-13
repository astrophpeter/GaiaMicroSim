# GaiaMicroSim
Simulations of Gaia Microlensing Events

## Structure of the Repository

* `GOST_data/` data from Gaia Observation Forecast Tool is stored here. Each file has the name corresponding to the background source of the event. "\<Gaia DR2 backgound source id\>_GOST.csv."
* `astrometry_util.py` Contains helper functions that deal with calculating the projected postions of stars and astrometric microlensing deflections.
* `query_util.py` Contains helper functions that deal with getting astrometric data on the source and lens from the Gaia DR2 catalog and mass estimates of the lenses.
* `plot_util.py` Contains helper functions that deal with plotting and saving the output of a simulated event.
* `get_deflection_positions.py` This is the main program. Will calculate the predicted deflected positions of the background source for a microlensing event. And store the results in `output/`. 
