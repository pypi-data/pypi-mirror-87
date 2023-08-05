# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component BilateralInteractionConstraint

.. autofunction:: BilateralInteractionConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def BilateralInteractionConstraint(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, group=None, constraintIndex=None, endTime=None, first_point=None, second_point=None, rest_vector=None, numericalTolerance=None, activateAtIteration=None, merge=None, derivative=None, keepOrientationDifference=None, **kwargs):
    """
    TODO-BilateralInteractionConstraint


    :param name: object name  Default value: BilateralInteractionConstraint

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param group: ID of the group containing this constraint. This ID is used to specify which constraints are solved by which solver, by specifying in each solver which groups of constraints it should handle.  Default value: 0

    :param constraintIndex: Constraint index (first index in the right hand term resolution vector)  Default value: 0

    :param endTime: The constraint stops acting after the given value.
Use a negative value for infinite constraints  Default value: -1.0

    :param first_point: index of the constraint on the first model  Default value: []

    :param second_point: index of the constraint on the second model  Default value: []

    :param rest_vector: Relative position to maintain between attached points (optional)  Default value: []

    :param numericalTolerance: a real value specifying the tolerance during the constraint solving. (optional, default=0.0001)  Default value: 0.0001

    :param activateAtIteration: activate constraint at specified interation (0 = always enabled, -1=disabled)  Default value: 0

    :param merge: TEST: merge the bilateral constraints in a unique constraint  Default value: 0

    :param derivative: TEST: derivative  Default value: 0

    :param keepOrientationDifference: keep the initial difference in orientation (only for rigids)  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, group=group, constraintIndex=constraintIndex, endTime=endTime, first_point=first_point, second_point=second_point, rest_vector=rest_vector, numericalTolerance=numericalTolerance, activateAtIteration=activateAtIteration, merge=merge, derivative=derivative, keepOrientationDifference=keepOrientationDifference)
    return "BilateralInteractionConstraint", params
