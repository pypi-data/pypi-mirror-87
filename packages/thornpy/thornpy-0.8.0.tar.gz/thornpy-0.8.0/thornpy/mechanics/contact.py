"""Module for contact mechanics solutions.

"""
#pylint: disable=invalid-name

def spherical(r_1, r_2, E_1, E_2, vu_1, vu_2, P_guess=None):    
    """Returns the contact parameters for two spheres in contact or for a sphere in contact with a flat surface.  In the case of a flat surface, enter None for the radius.
    
    Parameters
    ----------
    r_1 : {None, float}
        Radius of sphere 1
    r_2 : float or None
        Radius of sphere 2
    E_1 : float
        Modulus of sphere 1
    E_2 : float
        Modulus of sphere 2
    vu_1 : float
        Poisson's ratio for sphere 1
    vu_2 : float
        Poisson's ratio for sphere 2
    P_guess : float, optional
        Estimate of the applied load, by default None
    
    Returns
    -------
    float
        stiffness
    float
        stiffness exponent
    float
        contact area (Only if P_guess is given)
    float 
        max penetration parameter for use in an MSC Adams model. (Only if P_guess is given)

    Raises
    ------
    ValueError
        Raised if both radiuses are none

    """    
    # Effective radius
    if r_1 is None:
        R = r_2
    elif r_2 is None:
        R = r_1
    elif r_1 is None and r_2 is None:
        raise ValueError('At least one radius must be provided!')
    else:        
        R = (r_1**-1 + r_2**-1)**-1

    # Effective Modulus
    E = ((1-vu_1**2)/E_1 + (1-vu_2**2)/E_2)**-1

    # Contact Stiffness
    k = 4/3*E*R**.5

    # Stiffness Exponent
    e = 3/2

    if P_guess is not None:
        d = (9*P_guess**2/(16*r_1*E**2))**(1/3)
        d_max = 0.3*d
        a = (3*P_guess*R/4/E)**(1/3)        
        return k, e, a, d_max

    else:
        return k, e
