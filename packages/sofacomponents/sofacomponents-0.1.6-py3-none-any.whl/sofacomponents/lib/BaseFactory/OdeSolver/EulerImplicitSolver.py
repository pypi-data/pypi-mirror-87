# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component EulerImplicitSolver

.. autofunction:: EulerImplicitSolver

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def EulerImplicitSolver(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, rayleighStiffness=None, rayleighMass=None, vdamping=None, firstOrder=None, trapezoidalScheme=None, solveConstraint=None, threadSafeVisitor=None, **kwargs):
    """
    Time integrator using implicit backward Euler scheme


    :param name: object name  Default value: EulerImplicitSolver

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param rayleighStiffness: Rayleigh damping coefficient related to stiffness, > 0  Default value: 0.0

    :param rayleighMass: Rayleigh damping coefficient related to mass, > 0  Default value: 0.0

    :param vdamping: Velocity decay coefficient (no decay if null)  Default value: 0.0

    :param firstOrder: Use backward Euler scheme for first order ode system.  Default value: 0

    :param trapezoidalScheme: Optional: use the trapezoidal scheme instead of the implicit Euler scheme and get second order accuracy in time  Default value: 0

    :param solveConstraint: Apply ConstraintSolver (requires a ConstraintSolver in the same node as this solver, disabled by by default for now)  Default value: 0

    :param threadSafeVisitor: If true, do not use realloc and free visitors in fwdInteractionForceField.  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, rayleighStiffness=rayleighStiffness, rayleighMass=rayleighMass, vdamping=vdamping, firstOrder=firstOrder, trapezoidalScheme=trapezoidalScheme, solveConstraint=solveConstraint, threadSafeVisitor=threadSafeVisitor)
    return "EulerImplicitSolver", params
