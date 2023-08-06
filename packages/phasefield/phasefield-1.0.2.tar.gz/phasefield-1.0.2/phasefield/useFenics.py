from fenics import Constant, DirichletBC
from fenics import RectangleMesh, Point, refine
from fenics import VectorElement, VectorFunctionSpace, Function, project, TestFunction
from fenics import solve as _solve

from ufl import Cell, replace
from ufl.algorithms.analysis import extract_arguments_and_coefficients

from phasefield.external import External

#### mynote: need to way to set the constants in the model for the user
def constant(value,name):
    return Constant(value)
def dirichletBC(space,values,part):
    return DirichletBC(space,values,part)
def uflSpace(dimDomain, dimRange):
    return VectorElement("Lagrange", Cell("triangle", 2), 1, dimRange)
    if dimRange == 1:
        return FunctionSpace("Lagrange", Cell("triangle", 2), 1, dimRange)
    else:
        return VectorElement("Lagrange", Cell("triangle", 2), 1, dimRange)
External.constant = constant
External.dirichletBC = dirichletBC
External.uflSpace = uflSpace

def mesh(domain):
    return RectangleMesh(Point(domain[0]),Point(domain[1]),domain[2][0],domain[2][1])
def adaptMesh(persistentDF, indicator, *args):
    mark(indicator, *args)
    adapt(persistentDF)
    loadBalance(persistentDF)
def globalRefine(mesh,steps):
    for i in range(int(steps/2)):
        print(i,mesh)
        mesh = refine(mesh)
    return mesh
External.mesh = mesh
External.adaptMesh = adaptMesh
External.globalRefine = globalRefine

def discreteFunctionSpace(mesh,dimRange,order,storage):
    return VectorFunctionSpace( mesh, "Lagrange", order, dim=dimRange )
def discreteFunction(space,name):
    return Function(space)
def interpolate(df,expr):
    df.interpolate(project(expr,V=df.function_space()))
def assign(fromDF,toDF):
    toDF.assign(fromDF)
External.discreteFunctionSpace = discreteFunctionSpace
External.discreteFunction = discreteFunction
External.interpolate = interpolate
External.assign = assign

def scheme(equation, dirichletBCs, solver, parameters):
    return [equation.lhs, equation.rhs, dirichletBCs]
def solve(scheme,target):
    phi = TestFunction(target.function_space())
    args, coeffs = extract_arguments_and_coefficients(scheme[0])
    lhs = replace(scheme[0], {args[1]:target, args[0]:phi})
    args, coeffs = extract_arguments_and_coefficients(scheme[1])
    rhs = replace(scheme[1], {args[1]:target, args[0]:phi})
    args, coeffs = extract_arguments_and_coefficients(lhs-rhs)
    return _solve(lhs - rhs == 0, target, scheme[2])
External.scheme = scheme
External.solve = solve
