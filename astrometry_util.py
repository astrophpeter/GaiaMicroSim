##############################
# Module containing functions
# to calculate the microlensing
# astrometric deflections
##############################


from astropy.coordinates import get_body_barycentric
from astropy.time import Time
import astropy.units as un
import numpy as np
from numpy import ndarray

DEG_TO_MAS = 3600.0*1000.0

def getRaDecAtEpoch(ra_0,dec_0,pmra,pmdec,parallax,epoch_0,epoch):
    """Returns the apparent position of a star as seen from 
    earth at a given epoch,including parallax motion. Does not 
    account for relativistic effects. All coordinates/proper 
    motions/parallaxs should be on the ICRF.
     
    If parrallax is < 0.0 , it is set equal to 0.0. 
      
      Args:
      ----
         ra_0 (double) : initial position of the star in Right ascension [Deg].
         dec_0 (double) : initial position of the star in delcination [Deg].
         pmra (double) : proper motion in RA [mas/yr].
         pmdec (double) : proper motion in DEC [mas/yr].
         parallax (double) : annual stellar parallax [mas].
         epoch_0 (double) : reference epoch (Gaia DR2 2015.5) [Julian Years].
         epoch (double) : epoch to compute position [Juluian Years].
     
     Returns:
     -----
         (ra,dec) (double,double) : position in ra, dec at time = epoch. [deg].
    """
    
    if parallax < 0.0:
        paralax = 0.0  

    MAS_TO_DEG = 1.0 / 3600000.0
   
    cos_ra_0 = np.cos(np.deg2rad(ra_0))
    cos_dec_0 = np.cos(np.deg2rad(dec_0))
    sin_ra_0 = np.sin(np.deg2rad(ra_0))
    sin_dec_0 = np.sin(np.deg2rad(dec_0))

    #get barycentric position of the earth in astonmical units.
    R = get_body_barycentric('earth',Time(epoch, format='jyear', scale='utc'), ephemeris='jpl')
    X = (R.x.to(un.AU)).value
    Y = (R.y.to(un.AU)).value
    Z = (R.z.to(un.AU)).value

    #compute motion due to proper motion in mas
    d_ra_pm = (epoch-epoch_0) * pmra  / cos_dec_0
    d_dec_pm = (epoch-epoch_0) * pmdec

    #compute motion due to parallax in mas. 
    #(See Section 7.2.2.3 in Urban & Seidelmann 2013)
    d_ra_plx = parallax *(1.0 / cos_dec_0)*(sin_ra_0 * X - cos_ra_0 *Y)
    d_dec_plx = parallax * (X*cos_ra_0*sin_dec_0 + Y*sin_ra_0*sin_dec_0 - Z*cos_dec_0)
  
    #compute postion at epoch
    ra_final = ra_0 + (d_ra_pm + d_ra_plx) * MAS_TO_DEG
    dec_final = dec_0 + (d_dec_pm + d_dec_plx) * MAS_TO_DEG
   
    return (ra_final,dec_final)


def getSep(ra_1,dec_1,ra_2,dec_2):
    """Calculates the angular sepratation of two objects
    on the sky.

    :param ra_1: Right ascension of object 1 [Deg]
    :param dec_1: Declination of object 1 [Deg]
    :param ra_2: Right ascension of object 2 [Deg]
    :param dec_2: Declination of object 2 [Deg]
    :return : Angular separation [mas]
    """
    dec_avg = 0.5*(dec_1+dec_2)   

    delta_dec = (dec_2-dec_1)*DEG_TO_MAS
    delta_ra = (ra_2-ra_1)*DEG_TO_MAS*abs(np.cos(np.deg2rad(dec_avg)))

    return np.hypot(delta_dec,delta_ra)

def getAngle(ra_1: float,dec_1: float,ra_2: float ,dec_2: float) -> float:
    """Calculates the angle north of east between
    two objects.
    
    For microlensing object 2 must be the source to get the direction of
    the deflection right (always away from the lens)

    :param ra_1: Right ascension of object 1 [Deg]
    :param dec_1: Declination of object 1 [Deg]
    :param ra_2: Right ascension of object 2 [Deg]
    :param dec_2: Declination of object 2 [Deg]
    :return: angle north of east between the two objects [Rad]
    """

    dec_avg = 0.5*(dec_1+dec_2)
    delta_dec = (dec_2-dec_1)*DEG_TO_MAS
    delta_ra = (ra_2-ra_1)*DEG_TO_MAS*abs(np.cos(np.deg2rad(dec_avg)))

    return np.arctan2(delta_dec,delta_ra)

def getEinsteinRaduis(mass: float,lens_parallax: float,source_parallax) -> float:
    """Calculates the Angular Einestien Radius for
    a lens and source configuation.

    This does assume that 1/parallax is a good estimator
    of distance. 

    Will set negative source parallaxes to zero.

    :param mass: Lenss mass [Msol]
    :param lens_parallax: lens parallax [mas]
    :param source_parallax: source parallax [mas]
    :return : Angular Einstian Radius [mas]
    """
    if source_parallax < 0.0:
        source_parallax = 0.0   

    return 2.854*np.sqrt(mass*(lens_parallax-source_parallax))

def getPartiallyResolvedMicrolensingShiftMag(separation: float,
    EinsteinRadius: float) -> float:
    """Calucations the magnitude of the astrometric microlensing deflection
    in the partially resolved regime.
    
    \theta_E = angular Einstein Radius

    deflection = (1/2) * (sqrt(u^2+4)-u)*\theta_E

    See e.g. "Relativistic deflection of background starlight measures
    the mass of a nearby white dwarf star" by Kailash C. Sahu et al (2017)
    https://arxiv.org/abs/1706.02037.    

    :param separation: Angular separation of the lens and source [mas].
    :param EienstienRadius: Eienstien radius of the lens source system [mas].
    :return : Microlensing deflection magnitude [mas].
    """

    u = separation / EinsteinRadius
    
    return 0.5*(np.sqrt(u**2+4)-u)*EinsteinRadius

def getDeflectionVector(deflectionMag: float,angle: float) -> ndarray:
    """Calculates the deflection vector in Right acsesnion and declination

    :param deflectionMag : Magnitude of the astrometric deflection [mas]
    :param angle : angle of the deflection [rad]
    :return : deflection vector shape (2,) [ra*cos(dec) offset, dec ofset]
    """

    return (1.0/DEG_TO_MAS)*deflectionMag*np.array([np.cos(angle),np.sin(angle)])



