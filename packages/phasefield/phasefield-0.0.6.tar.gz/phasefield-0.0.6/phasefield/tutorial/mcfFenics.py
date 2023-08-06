import phasefield.useFenics
from phasefield import PhaseStepper, PhaseModel
from ufl import as_vector, conditional, SpatialCoordinate
from fenics import plot, File, project
import matplotlib.pyplot as plt

class SharpMCF():
    """Sharp definition for mean curvature flow."""
    mobility = 1

    omega = ([-2, -2], [2, 2], [200, 200])
    endTime = 0.32

    def gamma(nu):
        return [[0,1],[1,0]]

    def initial(x):
        return [[conditional(x[0]*x[0]+x[1]*x[1] < 0.8, 1, 0),
                conditional(x[0]*x[0]+x[1]*x[1] > 0.8, 1, 0)]]

phaseField = PhaseModel(SharpMCF, epsilon = 0.05, dt = 0.001)
fempyBase = PhaseStepper(phaseField)
solution = fempyBase.solution
vtkfile = File('mcf.pvd')
vtkfile << project(solution[0])
while fempyBase.time < SharpMCF.endTime:
    fempyBase.nextTime()
    print(fempyBase.time)
    vtkfile << project(solution[0])
