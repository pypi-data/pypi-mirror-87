# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ConstraintAnimationLoop

.. autofunction:: ConstraintAnimationLoop

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ConstraintAnimationLoop(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, displayTime=None, tolerance=None, maxIterations=None, doCollisionsFirst=None, doubleBuffer=None, scaleTolerance=None, allVerified=None, sor=None, schemeCorrection=None, realTimeCompensation=None, graphErrors=None, graphConstraints=None, graphForces=None, **kwargs):
    """
    Constraint animation loop manager


    :param name: object name  Default value: ConstraintAnimationLoop

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param displayTime: Display time for each important step of ConstraintAnimationLoop.  Default value: 0

    :param tolerance: Tolerance of the Gauss-Seidel  Default value: 1e-05

    :param maxIterations: Maximum number of iterations of the Gauss-Seidel  Default value: 1000

    :param doCollisionsFirst: Compute the collisions first (to support penality-based contacts)  Default value: 0

    :param doubleBuffer: Buffer the constraint problem in a double buffer to be accessible with an other thread  Default value: 0

    :param scaleTolerance: Scale the error tolerance with the number of constraints  Default value: 1

    :param allVerified: All contraints must be verified (each constraint's error < tolerance)  Default value: 0

    :param sor: Successive Over Relaxation parameter (0-2)  Default value: 1.0

    :param schemeCorrection: Apply new scheme where compliance is progressively corrected  Default value: 0

    :param realTimeCompensation: If the total computational time T < dt, sleep(dt-T)  Default value: 0

    :param graphErrors: Sum of the constraints' errors at each iteration  Default value: 

    :param graphConstraints: Graph of each constraint's error at the end of the resolution  Default value: 

    :param graphForces: Graph of each constraint's force at each step of the resolution  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, displayTime=displayTime, tolerance=tolerance, maxIterations=maxIterations, doCollisionsFirst=doCollisionsFirst, doubleBuffer=doubleBuffer, scaleTolerance=scaleTolerance, allVerified=allVerified, sor=sor, schemeCorrection=schemeCorrection, realTimeCompensation=realTimeCompensation, graphErrors=graphErrors, graphConstraints=graphConstraints, graphForces=graphForces)
    return "ConstraintAnimationLoop", params
