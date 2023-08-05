# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component LMConstraintSolver

.. autofunction:: LMConstraintSolver

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def LMConstraintSolver(self, numIterations=None, maxError=None, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, constraintAcc=None, constraintVel=None, constraintPos=None, graphGSError=None, traceKineticEnergy=None, graphKineticEnergy=None, **kwargs):
    """
    A Constraint Solver working specifically with LMConstraint based components


    :param name: object name  Default value: LMConstraintSolver

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param constraintAcc: Constraint the acceleration  Default value: 0

    :param constraintVel: Constraint the velocity  Default value: 1

    :param constraintPos: Constraint the position  Default value: 1

    :param numIterations: Number of iterations for Gauss-Seidel when solving the Constraints  Default value: 25

    :param maxError: threshold for the residue of the Gauss-Seidel algorithm  Default value: 1e-07

    :param graphGSError: Graph of residuals at each iteration  Default value: 

    :param traceKineticEnergy: Trace the evolution of the Kinetic Energy throughout the solution of the system  Default value: 0

    :param graphKineticEnergy: Graph of the kinetic energy of the system  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, constraintAcc=constraintAcc, constraintVel=constraintVel, constraintPos=constraintPos, numIterations=numIterations, maxError=maxError, graphGSError=graphGSError, traceKineticEnergy=traceKineticEnergy, graphKineticEnergy=graphKineticEnergy)
    return "LMConstraintSolver", params
