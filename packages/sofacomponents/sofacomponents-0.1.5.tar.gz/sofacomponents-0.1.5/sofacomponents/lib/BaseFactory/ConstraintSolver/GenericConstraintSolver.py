# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component GenericConstraintSolver

.. autofunction:: GenericConstraintSolver

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def GenericConstraintSolver(self, maxIterations=None, tolerance=None, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, displayTime=None, sor=None, scaleTolerance=None, allVerified=None, schemeCorrection=None, unbuilt=None, computeGraphs=None, graphErrors=None, graphConstraints=None, graphForces=None, graphViolations=None, currentNumConstraints=None, currentNumConstraintGroups=None, currentIterations=None, currentError=None, reverseAccumulateOrder=None, constraintForces=None, computeConstraintForces=None, **kwargs):
    """
    A Generic Constraint Solver using the Linear Complementarity Problem formulation to solve Constraint based components


    :param name: object name  Default value: GenericConstraintSolver

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param displayTime: Display time for each important step of GenericConstraintSolver.  Default value: 0

    :param maxIterations: maximal number of iterations of the Gauss-Seidel algorithm  Default value: 1000

    :param tolerance: residual error threshold for termination of the Gauss-Seidel algorithm  Default value: 0.001

    :param sor: Successive Over Relaxation parameter (0-2)  Default value: 1.0

    :param scaleTolerance: Scale the error tolerance with the number of constraints  Default value: 1

    :param allVerified: All contraints must be verified (each constraint's error < tolerance)  Default value: 0

    :param schemeCorrection: Apply new scheme where compliance is progressively corrected  Default value: 0

    :param unbuilt: Compliance is not fully built  Default value: 0

    :param computeGraphs: Compute graphs of errors and forces during resolution  Default value: 0

    :param graphErrors: Sum of the constraints' errors at each iteration  Default value: 

    :param graphConstraints: Graph of each constraint's error at the end of the resolution  Default value: 

    :param graphForces: Graph of each constraint's force at each step of the resolution  Default value: 

    :param graphViolations: Graph of each constraint's violation at each step of the resolution  Default value: 

    :param currentNumConstraints: OUTPUT: current number of constraints  Default value: 0

    :param currentNumConstraintGroups: OUTPUT: current number of constraints  Default value: 0

    :param currentIterations: OUTPUT: current number of constraint groups  Default value: 0

    :param currentError: OUTPUT: current error  Default value: 0.0

    :param reverseAccumulateOrder: True to accumulate constraints from nodes in reversed order (can be necessary when using multi-mappings or interaction constraints not following the node hierarchy)  Default value: 0

    :param constraintForces: OUTPUT: constraint forces (stored only if computeConstraintForces=True)  Default value: []

    :param computeConstraintForces: enable the storage of the constraintForces (default = False).  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, displayTime=displayTime, maxIterations=maxIterations, tolerance=tolerance, sor=sor, scaleTolerance=scaleTolerance, allVerified=allVerified, schemeCorrection=schemeCorrection, unbuilt=unbuilt, computeGraphs=computeGraphs, graphErrors=graphErrors, graphConstraints=graphConstraints, graphForces=graphForces, graphViolations=graphViolations, currentNumConstraints=currentNumConstraints, currentNumConstraintGroups=currentNumConstraintGroups, currentIterations=currentIterations, currentError=currentError, reverseAccumulateOrder=reverseAccumulateOrder, constraintForces=constraintForces, computeConstraintForces=computeConstraintForces)
    return "GenericConstraintSolver", params
