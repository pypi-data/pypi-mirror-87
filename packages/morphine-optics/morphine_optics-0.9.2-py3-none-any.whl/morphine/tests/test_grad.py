import jax.numpy as np
import numpy as onp
from jax import grad, jit, vmap
from jax import random
import matplotlib.pyplot as plt

import poppy

import os
TESTDIR = os.path.abspath(os.path.dirname(__file__))
ddir = os.path.join(TESTDIR,'../data/')


import logging
_log = logging.getLogger('poppy_tests')


def test_propagate():

    osys = poppy.OpticalSystem()
    osys.add_pupil(poppy.CircularAperture(radius=3))    # pupil radius in meters
    osys.add_detector(pixelscale=0.025, fov_arcsec=0.75)  # image plane coordinates in arcseconds

    def objective(wavelength):
        psf,intermediate = osys.propagate_mono(wavelength*1e-6)   
        return (np.sum(psf.amplitude**2.))

    output = objective(2.)
    assert (output-0.96685994)<0.00001
    print('Propagation worked!')

def test_grad():
    osys = poppy.OpticalSystem()
    osys.add_pupil(poppy.CircularAperture(radius=3))    # pupil radius in meters
    osys.add_detector(pixelscale=0.025, fov_arcsec=0.75)  # image plane coordinates in arcseconds

    def objective(wavelength):
        psf,intermediate = osys.propagate_mono(wavelength*1e-6)   
        return (np.sum(psf.amplitude**2.))

    thisgrad = grad(objective)
    output = thisgrad(2.0)
    assert(output - -0.01927825) < 0.0000001
    print('Gradient worked!')
