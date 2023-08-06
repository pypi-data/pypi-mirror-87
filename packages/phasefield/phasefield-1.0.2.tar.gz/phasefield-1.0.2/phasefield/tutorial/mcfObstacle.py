#!/usr/bin/python
"""
Mean curvature flow with obstacle potential well and uniform refinement
"""
from ufl import pi, sqrt, tanh
from phasefield import PhaseStepper, PhaseModel
from phasefield.auxfun import Obstacle

from dune.fem.plotting import plotComponents
from dune.grid import cartesianDomain

from dune.fem.function import integrate

class Mcf:
    """Sharp definition for mean curvature flow"""
    omega = cartesianDomain([-2, -2], [2, 2], [3, 3])
    endTime = 0.125
    saveStep = 0.02
    fileBase = "McfObstacle"

    mobility = 1
    def initial(x):
        """ Initial conditions """
        r0 = 0.5
        epsilon = 0.02
        return [[0.5-0.5*tanh((1/epsilon)*(x[0]*x[0]+x[1]*x[1]-r0*r0)),
                 0.5+0.5*tanh((1/epsilon)*(x[0]*x[0]+x[1]*x[1]-r0*r0))]]

    def gamma(nu):
        """ Matrix of surface tensions """
        return [[0, 1], [1, 0]]

if __name__== "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    # run epsilon from 0.02 to 0.03 in 6 increments
    maxLevel = 20
    dt = 1e-4
    epsilon = 0.02

    phaseField = PhaseModel(Mcf, constrained=True, epsilon=epsilon, dt=dt)

    fempyBase = PhaseStepper(phaseField)

    fempyBase.gridSetup(13, maxLevel)
    fempyBase.defaultRefine = [1.4, 1.2, 4, maxLevel]

    solution = fempyBase.solution
    while fempyBase.time < Mcf.endTime:
        print(fempyBase.time)
        fempyBase.nextTime()
        fempyBase.adapt()
