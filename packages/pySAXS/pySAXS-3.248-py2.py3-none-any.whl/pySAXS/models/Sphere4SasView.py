r"""
For information about polarised and magnetic scattering, see
the :ref:`magnetism` documentation.

Definition
----------

The 1D scattering intensity is calculated in the following way [Guinier1955]_

.. math::

    I(q) = \frac{\text{scale}}{V} \cdot \left[
        3V(\Delta\rho) \cdot \frac{\sin(qr) - qr\cos(qr))}{(qr)^3}
        \right]^2 + \text{background}

where *scale* is a volume fraction, $V$ is the volume of the scatterer,
$r$ is the radius of the sphere, *background* is the background level and
*sld* and *sld_solvent* are the scattering length densities (SLDs) of the
scatterer and the solvent respectively.

Note that if your data is in absolute scale, the *scale* should represent
the volume fraction (which is unitless) if you have a good fit. If not,
it should represent the volume fraction times a factor (by which your data
might need to be rescaled).

The 2D scattering intensity is the same as above, regardless of the
orientation of $\vec q$.

Validation
----------

Validation of our code was done by comparing the output of the 1D model
to the output of the software provided by the NIST (Kline, 2006).

References
----------

.. [Guinier1955] A Guinier and G. Fournet, *Small-Angle Scattering of X-Rays*,
   John Wiley and Sons, New York, (1955)

Authorship and Verification
----------------------------

* **Author: P Kienzle**
* **Last Modified by:**
* **Last Reviewed by:** S King and P Parker **Date:** 2013/09/09 and 2014/01/06
"""

import numpy as np
from numpy import pi, inf, sin, cos, sqrt, log

category = "shape:sphere"

#             ["name", "units", default, [lower, upper], "type","description"],
parameters = [["sld", "1/cm^2", 2e+11, [-inf, inf], "",
               "Layer scattering length density"],
              ["sld_solvent", "1/cm^2", 9.39594e+10, [-inf, inf], "",
               "Solvent scattering length density"],
              ["diameter", "nm", 50, [0, inf], "volume",
               "Sphere diameter"],
              ["concentration", "1/cm^3", 1e14, [0, inf], "",
               "Sphere concentration"],
             ]


def form_volume(radius):
    """Calculate volume for sphere"""
    return 1.333333333333333 * pi * radius ** 3

def radius_effective(mode, radius):
    """Calculate R_eff for sphere"""
    return radius if mode else 0.

def Iq(q, sld, sld_solvent, diameter,concentration):
    """Calculate I(q) for sphere"""
    #print "q",q
    #print "sld,r",sld,sld_solvent,radius
    #qr = q * radius
    #sn, cn = sin(qr), cos(qr)
    ## The natural expression for the bessel function is the following:
    ##     bes = 3 * (sn-qr*cn)/qr**3 if qr>0 else 1
    ## however, to support vector q values we need to handle the conditional
    ## as a vector, which we do by first evaluating the full expression
    ## everywhere, then fixing it up where it is broken.   We should probably
    ## set numpy to ignore the 0/0 error before we do though...
    #bes = 3 * (sn - qr * cn) / qr ** 3 # may be 0/0 but we fix that next line
    #bes[qr == 0] = 1
    #fq = bes * (sld - sld_solvent) * form_volume(radius)
    return sphere(q,[diameter,sld,sld_solvent,concentration])
Iq.vectorized = True  # Iq accepts an array of q values

##
## Form factor (Pedersen notations) P1,P2, etc...
## These are the normalized P ie P(0)=1.
##

def P1(q,R):
    """
    This function returns the form factor of a sphere of radius R for q
    """
    
    return F1(q,R)**2

def F1(q,R):
    """
    This function returns a scattering amplitude of a sphere of radius R for q
    """
    return (3.0*(sin(q*R)-q*R*cos(q*R)))/(q*R)**3.0

def sphere(q,par):
    '''
    par[0] diameter of the sphere (nm)
    par[1] scattering length density of sphere (cm-2)
    par[2] scattering length density of outside (cm-2)
    par[3] concentration of sphere (cm-3)
    '''
    diameter=par[0]
    radiusA=(diameter/2)*10.
    I=par[3]*(par[1]-par[2])**2.*form_volume(radiusA)**2*1e-48*P1(q,radiusA)
    return I

