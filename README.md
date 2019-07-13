# GaiaMicroSim
Simulations of Gaia Microlensing Events

## Structure of the Repository

* `GOST_data/` data from Gaia Observation Forecast Tool is stored here. Each file has the name corresponding to the background source of the event. "\<Gaia DR2 backgound source id\>_GOST.csv."
* `astrometry_util.py` Contains helper functions that deal with calculating the projected postions of stars and astrometric microlensing deflections.
* `query_util.py` Contains helper functions that deal with getting astrometric data on the source and lens from the Gaia DR2 catalog and mass estimates of the lenses.
* `plot_util.py` Contains helper functions that deal with plotting and saving the output of a simulated event.
* `get_deflection_positions.py` This is the main program. Will calculate the predicted deflected positions of the background source for a microlensing event. And store the results in `outputs/`. Details on how to use this script are outlined below in the usage section.
* `outputs/` This contains the results of the microlensing simulations. Results for a particular event are stored in sub directories with names "\<Gaia DR2 background source id\>_\<Gaia DR2 lens id\>/". 
* `outputs/<Gaia DR2 background source id>_<Gaia DR2 lens id>/lensed_positions.csv` File containing times the background source was seen by Gaia [Juluian years], Right ascension [Degrees], Declination [Degrees] of the background source inlcuding the microlensing deflection.
* `outputs/<Gaia DR2 background source id>_<Gaia DR2 lens id>/unlensed_positions.csv` File containing times the background source was seen by Gaia [Juluian years], Right ascension [Degrees], Declination [Degrees] of the background source **NOT** inlcuding the microlensing deflection.
* `outputs/<Gaia DR2 background source id>_<Gaia DR2 lens id>/separation.png` A plot of the true lens source separation at the times Gaia observed the event.
* `outputs/<Gaia DR2 background source id>_<Gaia DR2 lens id>/trajectorys.png` A plot of the lensed and unlensed source trajectories at the times Gaia observed the event. Zommed in to 500 mas square around the event maximum.

## Installation

Before being able to run the code you will need to install the following packages.

* Astropy `pip install astropy`
* Astroquery `pip install astroquery`
* Pandas `pip install panadas`


## Example Usage

To generate the output for a single microlensing event where the background source has Gaia DR2 source id = source_id, and the lens has a Gaia DR2 source id = lens_id. You run `python get_deflection_position.py source_id lens_id`.

For example for the candidate event where the background source has id = 5254061535052907008 and the lens has id = 5254061535097566848, running `python get_deflection_position.py 5254061535052907008 5254061535097566848` will populate the `outputs/5254061535052907008_5254061535097566848/` directory with the simulation results.
