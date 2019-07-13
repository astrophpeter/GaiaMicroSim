#####################################
# Module containing functions
# to plot and store the ouputs of the 
# microlensing deflection
# calculations.
#####################################


import matplotlib.pyplot as plt 
from numpy import ndarray
import numpy as np

DEG_TO_MAS = 36000.0*1000.0

def plot_source_trajectories(output_dir: str,ras: ndarray,decs: ndarray,
                             deflected_ras: ndarray,deflected_decs: ndarray,
                             ra_ref: float ,dec_ref: float) -> None:
    """Plots the tracjectory of the lensed and unlensed positions of the
    background source.

    :param ouput_dir: Output directory when the plot is to be saved.
    :param ras: Unlensed RA positions of the source. Has shape (num data,) [deg].
    :param decs: Unlensed DEC positions of the source. Has shape (num data,) [deg].
    :param deflected_ras: Lensed RA positions of the source. Has shape (num data,) [deg].
    :param deflected_decs: Lensed DEC positions of the source. Has shape (num data,) [deg].
    :params ref_ra: reference RA, center of the plot.
    :paramss ref_dec: refernce DEC, center of the plot.
    :returns : None, saves the plot in output_dir.
    """

    rel_ras = (ras - ra_ref) * DEG_TO_MAS
    rel_decs = (decs - dec_ref) *DEG_TO_MAS

    rel_ras_d = (deflected_ras - ra_ref) * DEG_TO_MAS
    rel_decs_d = (deflected_decs - dec_ref) * DEG_TO_MAS

    plt.clf()
    plt.scatter(rel_ras,rel_decs,color='blue',label='Unlensed Positions')
    plt.scatter(rel_ras_d,rel_decs_d,color='orange',label='Lensed Positions')

    plt.xlim(-50,50)
    plt.ylim(-50,50)
    
    plt.xlabel(r'$\Delta$ RA [mas *cos($\delta$)]')
    plt.ylabel(r'$\Delta$ DEC [mas]')

    plt.legend()

    plt.savefig(output_dir+'trajectories.png',dpi=200)
    
    

def plot_lens_source_sep(output_dir: str,seps: ndarray,times: ndarray) -> None:
    """Plots the true lens source sepratation.

    :param ouput_dir: Output directory when the plot is to be saved.
    :param seps: Separations of the lens and source. Has shape (num data,) [mas].
    :param times: Times of the separations [Jyear]
    :returns : None, saves the plot in output_dir.
    """
    plt.clf()
    plt.scatter(times,seps,c='blue',label='Unlensed Separation')
    plt.xlabel('Time [Julian Year]')
    plt.ylabel('Lens source Separation [mas]')
    plt.legend()
    plt.savefig(output_dir+'separations.png',dpi=200)

def save_positions(file_name: str,times: ndarray,ras: ndarray,decs: ndarray) -> None:
    """Saves a file with postiions and times.
    
    :param file_name: Name of the file where the data should be saved.
    :param times: List of times. Has shape (num data points,) [Jyear].
    :param ras: List of RAs. Has shape (num data points,) [deg].
    :param decs: List of Decs. Has shape (num data points,) [deg].
    :parma times: List of the correspond times. Has Shape(num data points,) [Jyear].
    :returns : None, saved the data to file_name.
    """
    out = np.transpose(np.vstack((times,ras,decs)))
    np.savetxt(file_name,out,delimiter=",")

