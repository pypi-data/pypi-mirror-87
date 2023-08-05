# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PartialFixedConstraint

.. autofunction:: PartialFixedConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PartialFixedConstraint(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, group=None, endTime=None, indices=None, fixAll=None, showObject=None, drawSize=None, activate_projectVelocity=None, fixedDirections=None, **kwargs):
    """
    Attach given particles to their initial positions


    :param name: object name  Default value: PartialFixedConstraint

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param group: ID of the group containing this constraint. This ID is used to specify which constraints are solved by which solver, by specifying in each solver which groups of constraints it should handle.  Default value: 0

    :param endTime: The constraint stops acting after the given value.
Use a negative value for infinite constraints  Default value: -1.0

    :param indices: Indices of the fixed points  Default value: [[0], [0]]

    :param fixAll: filter all the DOF to implement a fixed object  Default value: 0

    :param showObject: draw or not the fixed constraints  Default value: 1

    :param drawSize: 0 -> point based rendering, >0 -> radius of spheres  Default value: 0.0

    :param activate_projectVelocity: activate project velocity to set velocity  Default value: 0

    :param fixedDirections: for each direction, 1 if fixed, 0 if free  Default value: [[1, 1, 1]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, group=group, endTime=endTime, indices=indices, fixAll=fixAll, showObject=showObject, drawSize=drawSize, activate_projectVelocity=activate_projectVelocity, fixedDirections=fixedDirections)
    return "PartialFixedConstraint", params
