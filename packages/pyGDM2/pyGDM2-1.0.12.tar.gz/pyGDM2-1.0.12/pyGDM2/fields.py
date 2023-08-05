# encoding: utf-8
#
#Copyright (C) 2017-2020, P. R. Wiecha
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
"""
Collection of incident fields
"""

from __future__ import print_function
from __future__ import absolute_import

import itertools
import warnings
import cmath

import numpy as np








#==============================================================================
# Incident field container class
#==============================================================================
class efield(object):
    """incident electromagnetic field container class
    
    Defines an incident electric field including information about wavelengths,
    polarizations, focal spot or whatever optional parameter is supported by
    the used field generator.
    
    Parameters
    ----------
    field_generator : `callable`
        field generator function. Mandatory arguments are 
         - `struct` (instance of :class:`.structures.struct`)
         - `wavelength` (list of wavelengths)
    
    wavelengths : list
        list of wavelengths (wavelengths in nm)
    
    kwargs : list of dict or dict
        possible additional keyword arguments, passed to `field_generator`.
        Either dict or list of dicts.
         - If list of dicts, each entry must correspond exactly to one 
           parameters-set for `field-generator`.
         - If dict, maybe contain lists for configurations of the parameters. 
           In that case, all possible parameter-permutations will be generated.
    
    Examples
    --------
    >>> kwargs = dict(theta = [0.0,45,90])
    [{'theta': 0.0}, {'theta': 45.0}, {'theta': 90.0}]
    
    is equivalent to:
    
    >>> kwargs = [dict(theta=0.0), dict(theta=45.0), dict(theta=90.0)]
    [{'theta': 0.0}, {'theta': 45.0}, {'theta': 90.0}]
    
    """
    def __init__(self, field_generator, wavelengths, kwargs):
        """initialize field container"""
        self.field_generator = field_generator
        self.wavelengths = np.array(wavelengths)
        self.kwargs = kwargs
        
        ## --- generate parameter-sets for field-generator
        if type(kwargs) == dict:
            ## --- integer parameters to list
            for key in kwargs:
                if type(kwargs[key]) not in [list, np.ndarray]:
                    kwargs[key] = [kwargs[key]]
            
            ## --- generate all permutations of kwargs for direct use in field_generator
            varNames = sorted(kwargs)
            self.kwargs_permutations = [dict(zip(varNames, prod)) for 
                                    prod in itertools.product(*(kwargs[varName] 
                                                for varName in varNames))]
        elif type(kwargs) == list:
            self.kwargs_permutations = []
            for kw in kwargs:
                self.kwargs_permutations.append(kw)
                if type(kw) != dict:
                    raise ValueError("Wrong input for 'kwargs': Must be either dict or list of dicts.")
                
        else:
            raise ValueError("Wrong input for 'kwargs': Must be either dict or list of dicts.")
        
        ## set precision to single by default
        self.setDtype(np.float32, np.complex64)
    
    
    def setDtype(self, dtypef, dtypec):
        """set dtype of arrays"""
        self.dtypef = dtypef
        self.dtypec = dtypec
        self.wavelengths = np.asfortranarray(self.wavelengths, dtype=dtypef)










        

#==============================================================================
# Electric field generator functions
#==============================================================================
def nullfield(struct, wavelength, returnField='E'):
    """Zero-Field
    
    Parameters
    ----------
    struct : :class:`.structures.struct`
        structure definition, including environment setup
    
    wavelength : float
        Wavelength in nm
    
    Returns:
    ----------
      E0:       Complex zero at each position defined in struct
    """
    E0 = np.zeros((len(struct.geometry), 3), dtype=struct.dtypec)
    
    return np.asfortranarray(E0)




##----------------------------------------------------------------------
##                      INCIDENT FIELDS
##----------------------------------------------------------------------
def planewave(struct, wavelength, theta=None, polarization_state=None, 
              kSign=-1, consider_substrate_reflection=False, 
              returnField='E'):
    """Normally incident (along Z) planewave
    
    polarization is defined by one of the two kwargs:
     - theta: linear polarization angle in degrees, theta=0 --> along X. 
              Amplitude = 1 for both, E and B 
     - polarization state. tuple (E0x, E0y, Dphi, phi): manually 
              define x and y amplitudes, phase difference and 
              absolute phase of plane wave.
    
    Parameters
    ----------
    struct : :class:`.structures.struct`
        structure definition, including environment setup
    
    wavelength : float
        Wavelength in nm
    
    theta : float, default: None
        either 'theta' or 'polarization_state' must be given.
        linear polarization angle in degrees, 0deg = 0X direction.
    
    polarization_state : 4-tuple of float, default: None
        either 'theta' or 'polarization_state' must be given.
        polarization state with field amplitudes and phases, tuple of 4 float:
        (E0x, E0y, Dphi, Aphi): E0X amplitde, E0Y amplitde, phase difference 
        between X and Y components (in rad), absolute phase of plane wave (in rad).
        The field is then calculated as E = (E0x, E0y*exp(i*Dphi*z), 0)*exp(i*Aphi*z).
            Dphi : 
                - positive: left hand rotating polarization
                - negative: right hand rotating polarization 
                - example: left circular pol. with (1, 1, np.pi/2., 0)
    
    kSign : int, default: -1
        sign of wavenumber. 
        +1: propagation from bottom to top (towards increasing z)
        -1: propagation from top to bottom (towards smaller z, default)
        either kSign or k0 must be given.
    
    consider_substrate_reflection : bool, default: False
        Whether to consider the reflection / transmission coefficient at the
        substrate for adjusting the field amplitude
    
    returnField : str, default: 'E'
        if 'E': returns electric field; if 'B': magnetic field
    
    Returns
    -------
      E0 (B0):       Complex E-(B-)Field at each dipole position as 
                     list of (complex) 3-tuples: [(Ex1, Ey1, Ez1), ...]
    """    
    if (theta is None and polarization_state is None) or (theta is not None and polarization_state is not None):
        raise ValueError("exactly one argument of 'theta' and 'polarization_state' must be given.")
    if theta is not None:
        polarization_state = (1.0 * np.cos(theta * np.pi/180.), 
                              1.0 * np.sin(theta * np.pi/180.), 
                              0, 0)
    
    xm, ym, zm = np.transpose(struct.geometry)
    cn1 = struct.n1
    cn2 = struct.n2
    
    ## --- reflection and transmission coefficients
    if kSign == 1:
        t01 = 2.*cn1 / (cn1+cn2)
        r01 = (cn1-cn2) / (cn1+cn2)
    elif kSign == -1:
        t01 = 2.*cn2 / (cn1+cn2)
        r01 = (cn2-cn1) / (cn1+cn2)
    else:
        raise ValueError("planewave: kSign must be either +1 or -1!")
    
    ## constant parameters
    E0x = polarization_state[0]
    E0y = polarization_state[1]
    Dphi = polarization_state[2]
    Aphi = polarization_state[3]
    
    kz = kSign*cn2 * (2*np.pi / wavelength)    #incidence from positive Z
    
    ## amplitude and polarization
    ##  --------- Electric field --------- 
    E = np.ones((len(zm), 3), dtype=struct.dtypec)
    if returnField in ['e', 'E']:
        abs_phase = np.exp(1j * (kz*zm + Aphi))     # absolute phase
        E.T[0] *= E0x * abs_phase
        E.T[1] *= E0y*np.exp(1j * Dphi) * abs_phase
        E.T[2] *= 0 * abs_phase
    ##  --------- Magnetic field --------- 
    else:
        abs_phase = -1*np.exp(1j * (kz*zm + Aphi))     # absolute phase
        E.T[0] *= -1*E0y*np.exp(1j * Dphi) * abs_phase
        E.T[1] *= E0x * abs_phase
        E.T[2] *= 0 * abs_phase
    
    
# =============================================================================
#     TODO: CORRECT REFLECTED PART WAVEVEKTOR SIGN!
# =============================================================================
    if consider_substrate_reflection:
        if kSign == 1:  # bottom to top
            E[zm>0] *= t01
            E[zm<=0] += r01 * E[zm<=0]
        else:           # top to bottom
            E[zm<=0] *= t01
            E[zm>0] += r01 * E[zm>0]
    
    return np.asfortranarray(E, dtype=struct.dtypec)
    

    
def evanescent_planewave_fortran(struct, wavelength, theta_inc=0.0, polar='s',
                         returnField='E'):
    """oblique incident planewave, only linear polarization
    
    Oblique incidence (from bottom to top) through n1/n2/n3 layer interfaces. 
    May be used to simulate evanescent fields in the total internal 
    reflection configuration. Linear polarization.
    Amplitude = 1 for both, E and B.
    
    Using former fortran implementation (incidence limited to lower half space)
    
    Parameters
    ----------
    struct : :class:`.structures.struct`
        structure definition, including environment setup
    
    wavelength : float
        Wavelength in nm
    
    theta_inc : float, default: 0
        incident angle in the XZ plane with respect to e_z, in degrees.
         - 0deg = along Z (form neg to pos Z)
         - 90deg = along X  (form pos to neg X)
    
    polar : str, default: 's'
        incident linear polarization. Either 's' or 'p'. 
        At 0 degree incident angle, 's' is polarized in x/z plane, 'p' along y.
    
    returnField : str, default: 'E'
        if 'E': returns electric field; if 'B': magnetic field
    
    Returns
    -------
      E0 (B0):       Complex E-(B-)Field at each dipole position as 
                     list of (complex) 3-tuples: [(Ex1, Ey1, Ez1), ...]
    """
    from pyGDM2.pyGDMfor import evanescentfield as forevanescentfield
    
    spacing = struct.spacing
    xm, ym, zm = np.transpose(struct.geometry)
    posObj = np.transpose([xm,ym,zm])
    
    cn1 = struct.n1
    cn2 = struct.n2
    cn3 = struct.n3
    
    if polar == 's':
        idx_pol = 0
    elif polar == 'p':
        idx_pol = 1
    else:
        raise ValueError("'polar' must be either 's' or 'p'.")
    
    Ex = np.asfortranarray( np.zeros(len(xm)), dtype=struct.dtypec)
    Ey = np.asfortranarray( np.zeros(len(xm)), dtype=struct.dtypec)
    Ez = np.asfortranarray( np.zeros(len(xm)), dtype=struct.dtypec)
    
    for i,R in enumerate(posObj):
        x,y,z = R
        ex,ey,ez, bx,by,bz = forevanescentfield(wavelength, theta_inc, spacing, 
                                                x,y,z, cn1,cn2,cn3)
        
        if returnField.lower() == 'e':
            Ex[i], Ey[i], Ez[i] = ex[idx_pol], ey[idx_pol], ez[idx_pol]
        else:
            Ex[i], Ey[i], Ez[i] = bx[idx_pol], by[idx_pol], bz[idx_pol]
        
    Evec = np.transpose([Ex, Ey, Ez])
    return np.asfortranarray(Evec, dtype=struct.dtypec)





def _three_layer_field(wavelength, theta_inc, polar, z_d, spacing, n1, n2, n3, x, y, z):
    """oblique incident planewave, only linear polarization
    
    Oblique incidence (from bottom to top) through n1/n2/n3 layer interfaces. 
    May be used to simulate evanescent fields in the total internal 
    reflection configuration. Linear polarization.
    Amplitude = 1 for both, E and B.
    
    Original code by Ch. Girard, python implementation by C. Majorel
    
    Parameters
    ----------
    wavelength : float
        Wavelength in nm
    
    theta_inc : float, default: 0
        incident angle in the XZ plane with respect to e_z, in degrees.
         - 0deg = along Z (from neg to pos Z)
         - 90deg = along X  (from pos to neg X)
         - 180deg = along Z  (from pos to neg Z)
         - 270deg = along X  (from neg to pos X)
    
    polar : str, default: 's'
        incident linear polarization. Either 's' or 'p'. 
        At 0 degree incident angle, 's' is polarized along x, 'p' along y.
    
    z_d : float
        bottom interface position (along z) between media 1 and 2
    
    spacing : float
        spacing between bottom interface (between media 1 and 2) and 
        top interface position (between media 2 and 3)
    
    n1, n2, n3 : complex
        (complex) refractive index of each media 
    
    x, y, z : float
        x/y/z coordinates for computation of the fields
    
    Returns
    -------
      E0, B0:       Complex E-B-Fields at each dipole position as 
                    6 lists of the (complex) components: 
                    Ex, Ey, Ez, Bx, By, Bz
    """
#    ## -- convert the angle to put theta=0° as downward normal incidence
#    if theta in (-np.pi/2., np.pi/2.):
#        theta += 180.
#    else :
#        theta -= 180.
    
    ## -- convert angles 90 and 270 close to horizontal angles to avoid divergence
    if theta_inc in [-90, 90, -270, 270] and (n1!=n2 or n2!=n3):
        warnings.warn("Using interface with horizontal angle of incidence!" + 
                      "Please make sure if horizontal incidence makes sense in presence of an interface.")
    
    if theta_inc in [-90, 90]:
        theta_inc += 0.05
    if theta_inc in [-270, 270]:
        theta_inc -= 0.05
    
    z_u = z_d + spacing             # z position of upper interface
    r = np.array([x, y, z])         # eval. position
    theta_r = theta_inc*np.pi/180.  # inc. angle in rad 
    k0 = 2*np.pi/wavelength         # wavevector in vacuum
    
    ## -- permittivities    
    eps1 = n1**2
    eps2 = n2**2
    eps3 = n3**2
    
    if theta_r > np.pi/2. and theta_r < 3*np.pi/2.:
    ## -- Different wavevectors    
        k1 = np.array([-n3*k0*cmath.sin(theta_r), 0. , -k0*cmath.sqrt(eps1-eps3*cmath.sin(theta_r)**2)])        ## -- transmitted wavevector in medium 1 (bottom layer)
        k2 = np.array([-n3*k0*cmath.sin(theta_r), 0. , -k0*cmath.sqrt(eps2-eps3*cmath.sin(theta_r)**2)])        ## -- transmitted wavevector in medium 2 (middle layer)
        k2p = np.array([-n3*k0*cmath.sin(theta_r), 0. , k0*cmath.sqrt(eps2-eps3*cmath.sin(theta_r)**2)])        ## -- reflected wavevector in medium 2 (middle layer)
        k3 = np.array([-n3*k0*cmath.sin(theta_r), 0. , n3*k0*cmath.cos(theta_r)])                               ## -- incident wavevector in medium 3 (top layer)
        k3p = np.array([-n3*k0*cmath.sin(theta_r), 0. , -n3*k0*cmath.cos(theta_r)])                             ## -- reflected wavevector in medium 3 (top layer)
        
    ## -- Phase terms    
        c1p = cmath.exp(1.0j*k1[2]*z_d)
        c1m = cmath.exp(-1.0j*k1[2]*z_d)
        c2p = cmath.exp(1.0j*k2[2]*z_d)
        c2m = cmath.exp(-1.0j*k2[2]*z_d)
        c2pp = cmath.exp(1.0j*k2[2]*z_u)
        c2pm = cmath.exp(-1.0j*k2[2]*z_u)
        c3pp = cmath.exp(1.0j*k3[2]*z_u)
        c3pm = cmath.exp(-1.0j*k3[2]*z_u)
        
    ## -- z - components of the wavevector/eps for magnetic modulus    
        k1gz = k1[2]/eps1
        k2gz = k2[2]/eps2
        k3gz = k3[2]/eps3               
        
    ### --- modulus electric field in s-polarized mode    
        delta = c3pm*c1p*(c2m*c2pp*(k2[2]**2+k1[2]*k3[2]+k3[2]*k2[2]+k1[2]*k2[2])+
                c2p*c2pm*(-k2[2]**2-k1[2]*k3[2]+k1[2]*k2[2]+k3[2]*k2[2]))
        
        delta3 = c3pp*c1p*(c2m*c2pp*(-k2[2]**2-k2[2]*k1[2]+k1[2]*k3[2]+k2[2]*k3[2])+
                  c2p*c2pm*(k2[2]**2-k2[2]*k1[2]+k2[2]*k3[2]-k1[2]*k3[2]))
        
        delta2 = 2.*c2m*c1p*(k1[2]*k3[2]+k3[2]*k2[2])
        
        delta2p = 2.*c2p*c1p*(k2[2]*k3[2]-k1[2]*k3[2])
        
        delta1 = 4.*k2[2]*k3[2]
        
        cep3 = delta3/delta
        ce2 = delta2/delta
        cep2 = delta2p/delta
        ce1 = delta1/delta
        
        
    ### --- modulus magnetic field in p-polarized mode
        deltam = c3pm*c1p*(c2m*c2pp*(k2gz**2+k1gz*k3gz+k3gz*k2gz+k1gz*k2gz)+
                c2p*c2pm*(-k2gz**2-k1gz*k3gz+k1gz*k2gz+k3gz*k2gz))
        
        delta3m = c3pp*c1p*(c2m*c2pp*(-k2gz**2-k2gz*k1gz+k1gz*k3gz+k2gz*k3gz)+
                  c2p*c2pm*(k2gz**2-k2gz*k1gz+k2gz*k3gz-k1gz*k3gz))
        
        delta2m = 2.*c2m*c1p*(k1gz*k3gz+k3gz*k2gz)
        
        delta2pm = 2.*c2p*c1p*(k2gz*k3gz-k1gz*k3gz)
        
        delta1m = 4.*k2gz*k3gz
        
        cmagp3 = delta3m/deltam
        cmag2 = delta2m/deltam
        cmagp2 = delta2pm/deltam
        cmag1 = delta1m/deltam


    ### --- Determination of the differents electric and magnetic field    
        if z>z_u:
            cphase3 = cmath.exp(1.0j*np.dot(k3,r))
            cphase3p = cmath.exp(1.0j*np.dot(k3p,r))
                
            if polar=='s':
                Ex = 0.
                Ey = cphase3+cep3*cphase3p
                Ez = 0.
                
                Bx = -cphase3*k3[2]/k0-(cep3*cphase3p*k3p[2]/k0)
                By = 0.
                Bz = cphase3*k3[0]/k0+(cep3*cphase3p*k3p[0]/k0)
                
            if polar=='p':
                Ex = n3*(-cphase3*k3[2]/(eps3*k0)-cmagp3*cphase3p*k3p[2]/(eps3*k0))
                Ey = 0.
                Ez = n3*(cphase3*k3[0]/(eps3*k0)+cmagp3*cphase3p*k3p[0]/(eps3*k0))
                
                Bx = 0.
                By = -cphase3-cmagp3*cphase3p
                Bz = 0.
                
        elif z_d<z<z_u:
            cphase2 = cmath.exp(1.0j*np.dot(k2,r))
            cphase2p = cmath.exp(1.0j*np.dot(k2p,r))
                
            if polar=='s':
                Ex = 0.
                Ey = ce2*cphase2+cep2*cphase2p
                Ez = 0.
    
                Bx = -ce2*cphase2*k2[2]/k0-cep2*cphase2p*k2p[2]/k0
                By = 0.
                Bz = ce2*cphase2*k2[0]/k0+cep2*cphase2p*k2p[0]/k0
                
            if polar=='p':
                Ex = n3*(-cmag2*cphase2*k2[2]/(eps2*k0)-cmagp2*cphase2p*k2p[2]/(eps2*k0))
                Ey = 0.
                Ez = n3*(cmag2*cphase2*k2[0]/(eps2*k0)+cmagp2*cphase2p*k2p[0]/(eps2*k0))
                
                Bx = 0.
                By = -cmag2*cphase2-cmagp2*cphase2p
                Bz = 0.
                
        else:
            cphase1 = cmath.exp(1.0j*np.dot(k1,r))
            
            if polar=='s':
                Ex = 0.
                Ey = ce1*cphase1
                Ez = 0.
                
                Bx = -ce1*cphase1*k1[2]/k0
                By = 0.
                Bz = ce1*cphase1*k1[0]/k0
            
            if polar=='p':
                Ex = n3*(-cmag1*cphase1*k1[2]/(eps1*k0))
                Ey = 0.
                # Ez = 1./n3*(cmag1*cphase1*k1[0]/(eps1*k0))  # <-- this was probably wrong
                Ez = n3*(cmag1*cphase1*k1[0]/(eps1*k0))
                
                Bx = 0.
                By = -cmag1*cphase1
                Bz = 0.

    else :    
    ## -- Different wavevectors    
        k1 = np.array([-n1*k0*cmath.sin(theta_r), 0. , n1*k0*cmath.cos(theta_r)])                              ## -- incident wavevector in medium 1 (bottom layer)
        k1p = np.array([-n1*k0*cmath.sin(theta_r), 0. , -n1*k0*cmath.cos(theta_r)])                            ## -- reflected wavevector in medium 1 (bottom layer)
        k2 = np.array([-n1*k0*cmath.sin(theta_r), 0. , k0*cmath.sqrt(eps2-eps1*cmath.sin(theta_r)**2)])        ## -- transmitted wavevector in medium 2 (middle layer)
        k2p = np.array([-n1*k0*cmath.sin(theta_r), 0. , -k0*cmath.sqrt(eps2-eps1*cmath.sin(theta_r)**2)])      ## -- reflected wavevector in medium 2 (middle layer)
        k3 = np.array([-n1*k0*cmath.sin(theta_r), 0. , k0*cmath.sqrt(eps3-eps1*cmath.sin(theta_r)**2)])        ## -- transmitted wavevector in medium 3 (top layer)
        
    ## -- Phase terms    
        c1p = cmath.exp(1.0j*k1[2]*z_d)
        c1m = cmath.exp(-1.0j*k1[2]*z_d)
        c2p = cmath.exp(1.0j*k2[2]*z_d)
        c2m = cmath.exp(-1.0j*k2[2]*z_d)
        c2pp = cmath.exp(1.0j*k2[2]*z_u)
        c2pm = cmath.exp(-1.0j*k2[2]*z_u)
        c3pp = cmath.exp(1.0j*k3[2]*z_u)
        c3pm = cmath.exp(-1.0j*k3[2]*z_u)
        
    ## -- z - components of the wavevector/eps for magnetic modulus    
        k1gz = k1[2]/eps1
        k2gz = k2[2]/eps2
        k3gz = k3[2]/eps3
        
    ### --- modulus electric field in s-polarized mode    
        delta = c3pp*c1m*(c2m*c2pp*(-k2[2]**2-k3[2]*k1[2]+k2[2]*k3[2]+k2[2]*k1[2])+
                c2p*c2pm*(k1[2]*k2[2]+k3[2]*k1[2]+k3[2]*k2[2]+k2[2]**2))
        
        delta1 = c3pp*c1p*(c2m*c2pp*(k2[2]**2-k3[2]*k2[2]+k1[2]*k2[2]-k1[2]*k3[2])+
                  c2p*c2pm*(-k2[2]**2-k3[2]*k2[2]+k1[2]*k3[2]+k1[2]*k2[2]))
        
        delta2 = 2.*c3pp*c2pm*(k1[2]*k2[2]+k1[2]*k3[2])
        
        delta2p = 2.*c3pp*c2pp*(k1[2]*k2[2]-k1[2]*k3[2])
        
        delta3 = 4.*k1[2]*k2[2]
        
        cep1 = delta1/delta
        ce2 = delta2/delta
        cep2 = delta2p/delta
        ce3 = delta3/delta
        
        
    ### --- modulus magnetic field in p-polarized mode
        deltam = c3pp*c1m*(c2m*c2pp*(-k2gz**2-k3gz*k1gz+k2gz*k3gz+k2gz*k1gz)+
                c2p*c2pm*(k1gz*k2gz+k3gz*k1gz+k3gz*k2gz+k2gz**2))
        
        delta1m = c3pp*c1p*(c2m*c2pp*(k2gz**2-k3gz*k2gz+k1gz*k2gz-k1gz*k3gz)+
                  c2p*c2pm*(-k2gz**2-k3gz*k2gz+k1gz*k3gz+k1gz*k2gz))
        
        delta2m = 2.*c3pp*c2pm*(k1gz*k2gz+k1gz*k3gz)
        
        delta2pm = 2.*c3pp*c2pp*(k1gz*k2gz-k1gz*k3gz)
        
        delta3m = 4.*k1gz*k2gz
        
        cmagp1 = delta1m/deltam
        cmag2 = delta2m/deltam
        cmagp2 = delta2pm/deltam
        cmag3 = delta3m/deltam
    
    ### --- Determination of the differents electric and magnetic field    
        if z<z_d:
            cphase1 = cmath.exp(1.0j*np.dot(k1,r))
            cphase1p = cmath.exp(1.0j*np.dot(k1p,r))
                
            if polar=='s':
                Ex = 0.
                Ey = cphase1+cep1*cphase1p
                Ez = 0.
                
                Bx = -cphase1*k1[2]/k0-(cep1*cphase1p*k1p[2]/k0)
                By = 0.
                Bz = cphase1*k1[0]/k0+(cep1*cphase1p*k1p[0]/k0)
                
            if polar=='p':
                Ex = n1*(-cphase1*k1[2]/(eps1*k0)-cmagp1*cphase1p*k1p[2]/(eps1*k0))
                Ey = 0.
                Ez = n1*(cphase1*k1[0]/(eps1*k0)+cmagp1*cphase1p*k1p[0]/(eps1*k0))
                
                Bx = 0.
                By = -cphase1-cmagp1*cphase1p
                Bz = 0.
                
        elif z_d<z<z_u:
            cphase2 = cmath.exp(1.0j*np.dot(k2,r))
            cphase2p = cmath.exp(1.0j*np.dot(k2p,r))
                
            if polar=='s':
                Ex = 0.
                Ey = ce2*cphase2+cep2*cphase2p
                Ez = 0.
                
                Bx = -ce2*cphase2*k2[2]/k0-cep2*cphase2p*k2p[2]/k0
                By = 0.
                Bz = ce2*cphase2*k2[0]/k0+cep2*cphase2p*k2p[0]/k0
            
            if polar=='p':
                Ex = n1*(-cmag2*cphase2*k2[2]/(eps2*k0)-cmagp2*cphase2p*k2p[2]/(eps2*k0))
                Ey = 0.
                Ez = n1*(cmag2*cphase2*k2[0]/(eps2*k0)+cmagp2*cphase2p*k2p[0]/(eps2*k0))
                
                Bx = 0.
                By = -cmag2*cphase2-cmagp2*cphase2p
                Bz = 0.
                
                
        else:
            cphase3 = cmath.exp(1.0j*np.dot(k3,r))
            
            if polar=='s':
                Ex = 0.
                Ey = ce3*cphase3
                Ez = 0.
               
                Bx = -ce3*cphase3*k3[2]/k0
                By = 0.
                Bz = ce3*cphase3*k3[0]/k0
            
            if polar=='p':
                Ex = n1*(-cmag3*cphase3*k3[2]/(eps3*k0))
                Ey = 0.
                # Ez = 1./n1*(cmag3*cphase3*k3[0]/(eps3*k0))  # <-- this was probably wrong
                Ez = n1*(cmag3*cphase3*k3[0]/(eps3*k0))
                
                Bx = 0.
                By = -cmag3*cphase3
                Bz = 0.
    
    return Ex, Ey, Ez, Bx, By, Bz


# =============================================================================
# Modification of the pyGDM class to use the function defined above
# =============================================================================

def evanescent_planewave(struct, wavelength, theta_inc=0, polar='s',
                         returnField='E'):
    """oblique incident planewave, only linear polarization
    
    Oblique incidence (from bottom to top) through n1/n2/n3 layer interfaces. 
    May be used to simulate evanescent fields in the total internal 
    reflection configuration. Linear polarization.
    Amplitude = 1 for both, E and B.
    
    Original code by Ch. Girard, python implementation by C. Majorel
    
    Parameters
    ----------
    struct : :class:`.structures.struct`
        structure definition, including environment setup
    
    wavelength : float
        Wavelength in nm
    
    theta_inc : float, default: 0
        incident angle in the XZ plane with respect to e_z, in degrees.
         - 0deg = along Z (from neg to pos Z)
         - 90deg = along X  (from pos to neg X)
         - 180deg = along Z  (from pos to neg Z)
         - 270deg = along X  (from neg to pos X)
    
    polar : str, default: 's'
        incident linear polarization. Either 's' or 'p'. 
        At 0 degree incident angle, 's' is polarized along x, 'p' along y.
    
    returnField : str, default: 'E'
        if 'E': returns electric field; if 'B': magnetic field
    
    Returns
    -------
      E0 (B0):       Complex E-(B-)Field at each dipole position as 
                    list of (complex) 3-tuples: [(Ex1, Ey1, Ez1), ...]
    """
    
    spacing = struct.spacing
    z_d = 0   # position of lower interface
    xm, ym, zm = np.transpose(struct.geometry)
    posObj = np.transpose([xm,ym,zm])
    
    cn1 = struct.n1
    cn2 = struct.n2
    cn3 = struct.n3
    
    if polar.lower() not in ['s', 'p']:
        raise ValueError("'polar' must be either 's' or 'p'.")
    
    Ex = np.asfortranarray( np.zeros(len(xm)), dtype=struct.dtypec)
    Ey = np.asfortranarray( np.zeros(len(xm)), dtype=struct.dtypec)
    Ez = np.asfortranarray( np.zeros(len(xm)), dtype=struct.dtypec)
    
    for i,R in enumerate(posObj):
        x,y,z = R
        ex,ey,ez, bx,by,bz = _three_layer_field(wavelength, theta_inc, polar.lower(), 
                                                z_d, spacing, cn1, cn2, cn3, x, y, z)
        
        if returnField.lower() == 'e':
            Ex[i], Ey[i], Ez[i] = ex, ey, ez
        else:
            Ex[i], Ey[i], Ez[i] = bx, by, bz
        
    Evec = np.transpose([Ex, Ey, Ez])
    return np.asfortranarray(Evec, dtype=struct.dtypec)





    
    
def focused_planewave(struct, wavelength, theta=None, polarization_state=None, 
                      xSpot=0.0, ySpot=0.0, 
                      NA=-1.0, spotsize=-1.0, kSign=-1, phase=0.0,
                      consider_substrate_reflection=False, returnField='E'):
    """Normally incident (along Z) planewave with gaussian intensity profile
    
    focused at (x0,y0)
    
    polarization is defined by one of the two kwargs:
     - theta: linear polarization angle in degrees, theta=0 --> along X. 
              Amplitude = 1 for both, E and B 
     - polarization state. tuple (E0x, E0y, Dphi, phi): manually 
              define x and y amplitudes, phase difference and 
              absolute phase of plane wave.
    
    Parameters
    ----------
    struct : :class:`.structures.struct`
        structure definition, including environment setup
    
    wavelength : float
        Wavelength in nm
    
    theta : float, default: None
        either 'theta' or 'polarization_state' must be given.
        linear polarization angle in degrees, 0deg = 0X direction
    
    polarization_state : 4-tuple of float, default: None
        either 'theta' or 'polarization_state' must be given.
        polarization state with field amplitudes and phases, tuple of 4 float:
        (E0x, E0y, Dphi, Aphi): E0X amplitde, E0Y amplitde, phase difference 
        between X and Y components (in rad), absolute phase of plane wave (in rad).
        The field is then calculated as E = (E0x, E0y*exp(i*Dphi*z), 0)*exp(i*Aphi*z).
            Dphi : 
                - positive: left hand rotating polarization
                - negative: right hand rotating polarization 
                - example: left circular pol. with (E0x=1, E0y=1, Dphi=np.pi/2., phi=0)
    
    xSpot, ySpot : float, float, default: 0, 0
        focal spot position (in nm)
    
    kSign : int, default: -1
        sign of wavenumber. 
        +1: propagation from bottom to top (towards increasing z)
        -1: propagation from top to bottom (towards smaller z, default)
       
    phase : float, default: 0
          additional phase of the beam, in degrees
          
    consider_substrate_reflection : bool, default: False
        Whether to consider the reflection / transmission coefficient at the
        substrate for adjusting the field amplitude
        
    returnField : str, default: 'E'
        if 'E': returns electric field; if 'B' or 'H': magnetic field
    
    Returns
    -------
      E0 (B0):       Complex E-(B-)Field at each dipole position as 
                     list of (complex) 3-tuples: [(Ex1, Ey1, Ez1), ...]
    """
    E = planewave(struct, wavelength=wavelength, theta=theta, 
                  polarization_state=polarization_state, kSign=kSign, 
                  consider_substrate_reflection=consider_substrate_reflection, 
                  returnField=returnField)
    
    
    xm, ym, zm = np.transpose(struct.geometry)
    
    ## beamwaist
    if spotsize == NA == -1:
        raise ValueError("Focused Beam Error! Either spotsize or NA must be given.")
    elif spotsize == -1:
        w0 = 2*wavelength/(NA*np.pi)
    else:
        w0 = spotsize
    
    I_gaussian =  np.exp( -1.0 * (((xm-xSpot)**2 + (ym-ySpot)**2) / (w0**2)))
    
    E = np.prod([E.T,[I_gaussian]], axis=0).T
    
    return np.asfortranarray(E, dtype=struct.dtypec)



def gaussian(struct, wavelength, theta=None, polarization_state=None, 
             xSpot=0.0, ySpot=0.0, zSpot=0.0, 
             NA=-1.0, spotsize=-1.0, kSign=-1.0, 
             paraxial=False, phase=0.0, returnField='E'):
    """Normal incident (along Z) Gaussian Beam Field
    
    obligatory "einKwargs" are one of 'theta' or 'polarization_state' and 
    one of 'NA' or 'spotsize'
    
    polarization is defined by one of the two kwargs:
     - theta: linear polarization angle in degrees, theta=0 --> along X. 
              Amplitude = 1 for both, E and B 
     - polarization_state. tuple (E0x, E0y, Dphi, phi): manually 
              define x and y amplitudes, phase difference and 
              absolute phase of plane wave.
    
    
    Parameters
    ----------
      struct : :class:`.structures.struct`
          structure object including environment
      
      wavelength : float
          Wavelength in nm
    
      theta : float, default: None
        either 'theta' or 'polarization_state' must be given.
        linear polarization angle in degrees, 0deg = 0X direction
    
    polarization_state : 4-tuple of float, default: None
        either 'theta' or 'polarization_state' must be given.
        polarization state with field amplitudes and phases, tuple of 4 float:
        (E0x, E0y, Dphi, Aphi): E0X amplitde, E0Y amplitde, phase difference 
        between X and Y components (in rad), absolute phase of plane wave (in rad).
        The field is then calculated as E = (E0x, E0y*exp(i*Dphi*z), 0)*exp(i*Aphi*z).
            Dphi : 
                - positive: left hand rotating polarization
                - negative: right hand rotating polarization 
                - example: left circular pol. with (E0x=1, E0y=1, Dphi=np.pi/2., phi=0)
        
      xSpot,ySpot,zSpot : float, default: 0,0,0
          x/y/z coordinates of focal point
      
      NA : float
          Numerical aperture to calculate beamwaist
      
      spotsize : float (optional)
          Gaussian beamwaist (overrides "NA")
      
      kSign : float, default: -1
          Direction of Beam. -1: top to Bottom, 1 Bottom to top
      
      paraxial : bool, default: False
          Use paraxial Gaussian beam: No longitudinal fields.
          If "False", longitudinal components are obtained using Maxwell 
          equation div(E)=0 as condition
         
      phase : float, default: 0
          additional phase of the beam, in degrees
      
      returnField : str, default: 'E'
          if 'E': returns electric field; if 'B': magnetic field
    
    Returns
    -------
      E0:       Complex E-Field at each dipole position
      
    
    Notes
    -----
     - paraxial correction : 
         see: Novotny & Hecht. "Principles of nano-optics". Cambridge University Press (2006)

    
    """
    if (theta is None and polarization_state is None) or (theta is not None and polarization_state is not None):
        raise ValueError("exactly one argument of 'theta' and 'polarization_state' must be given.")
    if theta is not None:
        polarization_state = (1.0 * np.cos(theta * np.pi/180.), 
                              1.0 * np.sin(theta * np.pi/180.), 
                              0, 0)
        
    xm, ym, zm = np.transpose(struct.geometry)
    cn1 = struct.n1     # only consider environmental refindex
    cn2 = struct.n2     # only consider environmental refindex
    cn3 = struct.n3     # only consider environmental refindex
    
    if zm.min()<0 and cn1 != cn2:
        warnings.warn("Evaluating field in substrate with index n1 != n2. This is not implemented yet and might give false reults.")
    if zm.min() > struct.spacing and cn2 != cn3:
        warnings.warn("Evaluating field in cladding with index n2 != n3. This is not implemented yet and might give false reults.")
    
    Ex = np.asfortranarray( np.zeros(len(xm)), dtype=struct.dtypec)
    Ey = np.asfortranarray( np.zeros(len(xm)), dtype=struct.dtypec)
    Ez = np.asfortranarray( np.zeros(len(xm)), dtype=struct.dtypec)
    
    
    ## beamwaist
    if spotsize == NA == -1:
        raise ValueError("Focused Beam Error! Either spotsize or NA must be given.")
    elif spotsize == -1:
        w0 = 2*wavelength/(NA*np.pi)
    else:
        w0 = spotsize
    
    ## waist, curvature and gouy-phase
    def w(z, zR, w0):
        return w0 * np.sqrt(1 + (z/zR)**2)
    
    def R(z, zR):
        return z*( 1 + (zR/z)**2 )
    
    def gouy(z, zR):
        return np.arctan2(z,zR)
    ## constant parameters
    E0 = complex(1,0)
    k = kSign*cn2 * (2*np.pi / wavelength)    #incidence from positive Z
    zR = np.pi*w0**2 / wavelength
    
    r2 = (xm-xSpot)**2+(ym-ySpot)**2
    z = zm-zSpot
    
    
    ## amplitude and polarization
    E0x = polarization_state[0]
    E0y = polarization_state[1]
    Dphi = polarization_state[2]
    Aphi = polarization_state[3]
    
    
    ##  --------- Electric field --------- 
    E = E0 * (w0/w(z,zR,w0) * 
            np.exp(-r2 / w(z,zR,w0)**2 ) * 
            np.exp(1j * (k*z + k*r2/(2*R(z,zR)) - gouy(z, zR)) )) * np.exp(1j*phase*np.pi/180.)
    
    if returnField in ['e', 'E']:
        abs_phase = np.exp(1j * Aphi)     # add an absolute phase
        Ex = E * E0x * abs_phase
        Ey = E * E0y * np.exp(1j * Dphi) * abs_phase
    else:
    ##  --------- Magnetic field --------- 
        abs_phase = -1*np.exp(1j * Aphi)     # add an absolute phase
        Ex = -1*E * E0y*np.exp(1j * Dphi) * abs_phase
        Ey = E * E0x * abs_phase        
    
    ## obtained longitudinal component using condition div(E)==0
    if paraxial:
        Ez = np.zeros(len(E))   # <-- paraxial gaussian beam: No longitudinal E-component
    else:
        Ez = (-1j * 2 / (k * w(z,zR,w0)**2)) * \
                ((xm-xSpot) * Ex + (ym-ySpot) * Ey)
    
    Evec = np.transpose([Ex, Ey, Ez])
    return np.asfortranarray(Evec, dtype=struct.dtypec)




## ---------- Setup incident field
def double_gaussian(struct, wavelength, 
                    theta1, theta2,
                    xSpot1, ySpot1, zSpot1, xSpot2, ySpot2, zSpot2,
                    phase1=0.0, phase2=0.0,
                    beam1_amplitude=1.0, beam2_amplitude=1.0,
                    paraxial=True, spotsize=-1.0, kSign=-1,
                    returnField='E'):
    """Two focused beams, based on :func:`.gaussian`
    
    Parameters
    ----------
    theta1, theta2 : float
        polarization angle of beam 1 and 2
    
    xSpot1, ySpot1, zSpot1 : float
        beam 1 focal spot
    
    xSpot2, ySpot2, zSpot2 : float
        beam 2 focal spot
    
    phase1, phase2 : float, default: 0
        relative phase, in degrees
                  
    beam1_amplitude, beam2_amplitude : float, default: 1
        max. amplitude of beam 1, beam 2
    
    For the other parameters, see :func:`.gaussian`
    
    
    Returns
    -------
      E0:       Complex E-Field at each dipole position ( (Ex,Ey,Ez)-tuples )
    """

    ## --- evaluate focused beam twice using the two focal positions
    Efield1 = gaussian(struct, wavelength, theta1,
                               xSpot1, ySpot1, zSpot1,
                               spotsize=spotsize, kSign=kSign,
                               paraxial=paraxial, phase=phase1,
                               returnField=returnField)
    Efield2 = gaussian(struct, wavelength, theta2,
                               xSpot2, ySpot2, zSpot2,
                               spotsize=spotsize, kSign=kSign,
                               paraxial=paraxial, phase=phase2,
                               returnField=returnField)

    ## --- get the complex x/y/z field components as individual arrays for summation
    Ex1, Ey1, Ez1 = Efield1.T
    Ex2, Ey2, Ez2 = Efield2.T

    ## --- add both beams
    Ex = Ex1*beam1_amplitude + Ex2*beam2_amplitude
    Ey = Ey1*beam1_amplitude + Ey2*beam2_amplitude
    Ez = Ez1*beam1_amplitude + Ez2*beam2_amplitude

    ## --- return as fortran array to avoid copying of arrays in memory
    return np.asfortranarray(np.transpose([Ex, Ey, Ez]))



def dipole_electric(struct, wavelength, x0,y0,z0, mx,my,mz, returnField='E'):
    """field emitted by an electric dipole at (x0,y0,z0) with complex amplitude (mx,my,mz)
    
    obligatory kwargs are: wavelength, x0,y0,z0, mx,my,mz
    
    From:  G. S. Agarwal, Phys. Rev. A, 11, 230 (1975). (Eqs. 4.5/4.6)
    
    Parameters
    ----------
      struct : :class:`.structures.struct`
          structure object including environment
     
      wavelength : float
          wavelength in nm
    
      x0,y0,z0 : float
          x/y/z coordinates of electric dipole position
          
      mx,my,mz : float
          x/y/z amplitude of elec. dipole vector
          
      returnField : str, default: 'E'
          if 'E': returns electric field; if 'B': magnetic field
    
    Returns
    -------
      E0:       Complex E-Field at each dipole position ( (Ex,Ey,Ez)-tuples )
    """
    from pyGDM2.pyGDMfor import elecmag0_full as forelecmag0_full
    from pyGDM2.pyGDMfor import magmag0_full as formagmag0_full
    
    xm, ym, zm = np.transpose(struct.geometry)
    cn1 = struct.n1
    cn2 = struct.n2
    cn3 = struct.n3
    
    if zm.min()<0 and cn1 != cn2:
        warnings.warn("Evaluating field in substrate with index n1 != n2. This is not implemented yet and might give false reults.")
    if zm.min() > struct.spacing and cn2 != cn3:
        warnings.warn("Evaluating field in cladding with index n2 != n3. This is not implemented yet and might give false reults.")
    
    Ex = np.asfortranarray( np.zeros(len(xm)), dtype=struct.dtypec)
    Ey = np.asfortranarray( np.zeros(len(xm)), dtype=struct.dtypec)
    Ez = np.asfortranarray( np.zeros(len(xm)), dtype=struct.dtypec)
    posObj = np.transpose([xm,ym,zm])
    
    ak0 = 2.*np.pi / wavelength
    
    ## get propagator S0
    for i,R in enumerate(posObj):
        xObs = R[0]
        yObs = R[1]
        zObs = R[2]
        if returnField in ['E','e']:
            ## magmag = elecelec
            cxx,cxy,cxz,\
                cyx,cyy,cyz,\
                czx,czy,czz\
                = formagmag0_full(ak0,xObs,yObs,zObs,
                                       x0,y0,z0,
                                       cn1,cn2,cn3)
            Ex[i] = cxx*mx + cxy*my + cxz*mz
            Ey[i] = cyx*mx + cyy*my + cyz*mz
            Ez[i] = czx*mx + czy*my + czz*mz
        else:
            cxx,cxy,cxz,\
                cyx,cyy,cyz,\
                czx,czy,czz\
                = forelecmag0_full(ak0,xObs,yObs,zObs,
                                       x0,y0,z0,
                                       cn1,cn2,cn3)
            Ex[i] = -1*cxx*mx + -1*cxy*my + -1*cxz*mz
            Ey[i] = -1*cyx*mx + -1*cyy*my + -1*cyz*mz
            Ez[i] = -1*czx*mx + -1*czy*my + -1*czz*mz
    
    Evec = np.transpose([Ex, Ey, Ez])
    return np.asfortranarray(Evec, dtype=struct.dtypec)



def dipole_magnetic(struct, wavelength, x0,y0,z0, mx,my,mz, returnField='E'):
    """field emitted by a magnetic dipole at (x0,y0,z0) with complex amplitude (mx,my,mz)
    
    obligatory "einKwargs" are: wavelength, x0,y0,z0, mx,my,mz
    
    From:  G. S. Agarwal, Phys. Rev. A, 11, 230 (1975). (Eqs. 4.5/4.6)
    
    Parameters
    ----------
      struct : :class:`.structures.struct`
          structure object including environment
     
      wavelength : float
        Wavelength in nm
    
      x0,y0,z0 : float
          x/y/z coordinates of magnetic dipole position
          
      mx,my,mz : float
          x/y/z amplitude of mag. dipole vector
          
      returnField : str, default: 'E'
          if 'E': returns electric field; if 'B': magnetic field
    
    Returns
    -------
      E0:       Complex E-Field at each dipole position ( (Ex,Ey,Ez)-tuples )
      
    """
    from pyGDM2.pyGDMfor import elecmag0_full as forelecmag0_full
    from pyGDM2.pyGDMfor import magmag0_full as formagmag0_full
    
    xm, ym, zm = np.transpose(struct.geometry)
    cn1 = struct.n1
    cn2 = struct.n2
    cn3 = struct.n3
    
    if zm.min()<0 and cn1 != cn2:
        warnings.warn("Evaluating field in substrate with index n1 != n2. This is not implemented yet and might give false reults.")
    if zm.min() > struct.spacing and cn2 != cn3:
        warnings.warn("Evaluating field in cladding with index n2 != n3. This is not implemented yet and might give false reults.")
    
    
    Ex = np.asfortranarray( np.zeros(len(xm)), dtype=struct.dtypec)
    Ey = np.asfortranarray( np.zeros(len(xm)), dtype=struct.dtypec)
    Ez = np.asfortranarray( np.zeros(len(xm)), dtype=struct.dtypec)
    posObj = np.transpose([xm,ym,zm])
    
    ak0 = 2.*np.pi / wavelength
    
    ## get propagator S0
    for i,R in enumerate(posObj):
        xObs = R[0]
        yObs = R[1]
        zObs = R[2]
        if returnField in ['E','e']:
#            raise ValueError("E not implemented")
            cxx,cxy,cxz,\
                cyx,cyy,cyz,\
                czx,czy,czz\
                = forelecmag0_full(ak0,xObs,yObs,zObs,
                                       x0,y0,z0,
                                       cn1,cn2,cn3)
            Ex[i] = -1*cxx*mx + -1*cxy*my + -1*cxz*mz
            Ey[i] = -1*cyx*mx + -1*cyy*my + -1*cyz*mz
            Ez[i] = -1*czx*mx + -1*czy*my + -1*czz*mz
        else:
            cxx,cxy,cxz,\
                cyx,cyy,cyz,\
                czx,czy,czz\
                = formagmag0_full(ak0,xObs,yObs,zObs,
                                       x0,y0,z0,
                                       cn1,cn2,cn3)
            Ex[i] = cxx*mx + cxy*my + cxz*mz
            Ey[i] = cyx*mx + cyy*my + cyz*mz
            Ez[i] = czx*mx + czy*my + czz*mz
    
    
    Evec = np.transpose([Ex, Ey, Ez])
    return np.asfortranarray(Evec, dtype=struct.dtypec)









if __name__ == "__main__":
    ## ---------- Module Doc
    #print forEplanewave.__doc__
#    print forEfocused.__doc__
    
    
    ## TEST INCIDENT FIELD ROUTINE
    from mayavi import mlab
    from pyGDM2 import structures
    
    posX=0;posY=0;posZ=1000
    MAXDIST=200
    xm,ym,zm = structures.rectwire(10,20,20,20).T
    zm += 50   ## z-offset
    dist = np.sqrt((xm-posX)**2 + (ym-posY)**2 + (zm-posZ)**2)
    xm = xm[dist>MAXDIST]
    ym = ym[dist>MAXDIST]
    zm = zm[dist>MAXDIST]
    
    simDict = {'elambda':[800], 'atheta':[0], 
               'xm':xm, 'ym':ym, 'zm':zm,
               'n1':1,'n2':1,'n3':1}
    
    
#    FIELD = focused(simDict, 1,1, 100,100, NA=1.)
#    FIELD = np.reshape(FIELD, (len(FIELD)/3, 3))
#    X,Y,Z = FIELD.T
#    
#    mlab.figure()
#    mlab.quiver3d(xm,ym,zm, X.real, Y.real, Z.real)
#    mlab.orientation_axes()
#    mlab.axes()
#    mlab.title("Focused Planewave")
    
    
    
    fieldtype = 'e'
    FIELD = planewave(simDict,  800,0,   returnField=fieldtype)
#    FIELD = magDipole(simDict,  800,0,   posX,posY,posZ,   1,0,0,  returnField=fieldtype)
#    FIELD = elecDipole(simDict,  800,0,   posX,posY,posZ,   1,0,0,  returnField=fieldtype)
    FIELD = np.reshape(FIELD, (len(FIELD)/3, 3))
    X,Y,Z = FIELD.T
    
    
    
    
#    from pyGDM.visu.common import animateNearfield3D
#    NF = np.array([xm,ym,zm, X.real,X.imag, Y.real,Y.imag, Z.real,Z.imag]).T
#    animateNearfield3D(NF)
    
    
    
#    fig = mlab.figure(size=(1000,1000))
    mlab.quiver3d(xm,ym,zm, X.real, Y.real, Z.real)
    mlab.orientation_axes()
    mlab.axes()
    if fieldtype=='E':
        mlab.title("mag. dipole - Efield")
##        mlab.savefig("mag_dp_Efield.png")
    if fieldtype=='B':
        mlab.title("mag. dipole - Bfield")
##        mlab.savefig("mag_dp_Bfield.png")
#    
    mlab.show()




## -- list of all available incident field generators
FIELDS_LIST = [planewave, evanescent_planewave, focused_planewave,
               gaussian, double_gaussian,
               dipole_electric, dipole_magnetic]


