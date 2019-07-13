##################################
# Script to obtain the positions
# of a background source including
# a microlenisng signal as seen by
# Gaia.
##################################


import query_util as query
import astrometry_util as ast
import numpy as np
import plot_util as plot 
import os 
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('source_dr2_id', type=int,
                     help='Gaia DR2 source id for the lensed object.')
parser.add_argument('lens_dr2_id', type=int,
                     help='Gaia DR2 source id for the lens.')

args = parser.parse_args()
source_dr2_id = args.source_dr2_id
lens_dr2_id = args.lens_dr2_id

output_dir = "outputs/" + str(source_dr2_id) + "_" + str(lens_dr2_id) + "/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Getting backgound source data...")
source_data = query.get_ast_data(source_dr2_id)

print("Getting lens data...")
lens_data = query.get_ast_data(lens_dr2_id)

print("Getting GOST times...")
gost_times = query.get_gost_times(source_dr2_id)

print("Getting Lens mass estimate..")
lens_mass = query.get_lens_mass(lens_dr2_id)

#Keep track of a bunch of important things
deflected_ras = np.array([])
deflected_decs = np.array([])
ras = np.array([])
decs = np.array([])
separations = np.array([])


# Get the Einstein Radius for the lens source system
EinsteinRadius = ast.getEinsteinRaduis(lens_mass,lens_data['parallax'][0],
                                    source_data['parallax'][0])

#Cycle over all of the GOST times
for t in gost_times:

    # Get the position of the source at time t
    source_ra,source_dec = ast.getRaDecAtEpoch(source_data['ra'][0],source_data['dec'][0],
                                               source_data['pmra'][0],source_data['pmdec'][0],
                                               source_data['parallax'][0],source_data['ref_epoch'][0],t)
    # Get the position of the lens at time t
    lens_ra,lens_dec = ast.getRaDecAtEpoch(lens_data['ra'][0],lens_data['dec'][0],
                                                lens_data['pmra'][0],lens_data['pmdec'][0],
                                                lens_data['parallax'][0],lens_data['ref_epoch'][0],t)

    # Define the reference declination at the average of the lens and source
    ref_dec = 0.5*(source_dec+lens_dec)

    # Calculate the lens and source angular separation
    separation = ast.getSep(lens_ra,lens_dec,source_ra,source_dec)
    
    # Calculate the angle between the lens and source (direction of deflection)
    angle = ast.getAngle(lens_ra,lens_dec,source_ra,source_dec)

    # Calculate the microlensing deflection magnitude 
    deflectionMag = ast.getPartiallyResolvedMicrolensingShiftMag(separation,EinsteinRadius)
    
    # Calculate the ra*cos(dec), dec deflection offset
    deflectionVector = ast.getDeflectionVector(deflectionMag,angle)

    # Calculate the position of the source including the microlenising deflection
    deflected_ras = np.append(deflected_ras,source_ra+deflectionVector[0]/np.cos(np.deg2rad(ref_dec)))
    deflected_decs = np.append(deflected_decs,source_dec+deflectionVector[0])

    #store the un deflections position and lens source separation.
    ras = np.append(ras,source_ra)
    decs = np.append(decs,source_dec)
    separations = np.append(separations,separation)

#find a good reference point to center plots on. 
min_ind = np.argmin(separations)
plot_ra_ref = ras[min_ind]
plot_dec_ref = decs[min_ind]

#plot and store outputs
plot.plot_source_trajectories(output_dir,ras,decs,deflected_ras,deflected_decs,plot_ra_ref,plot_dec_ref)
plot.plot_lens_source_sep(output_dir,separations,gost_times)
plot.save_positions(output_dir+"unlensed_posistions.csv",gost_times,ras,decs)
plot.save_positions(output_dir+"lensed_positions.csv",gost_times,deflected_ras,deflected_decs)










