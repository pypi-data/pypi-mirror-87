# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component LinearVelocityConstraint

.. autofunction:: LinearVelocityConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def LinearVelocityConstraint(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, group=None, endTime=None, indices=None, keyTimes=None, velocities=None, coordinates=None, **kwargs):
    """
    apply velocity to given particles


    :param name: object name  Default value: LinearVelocityConstraint

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param group: ID of the group containing this constraint. This ID is used to specify which constraints are solved by which solver, by specifying in each solver which groups of constraints it should handle.  Default value: 0

    :param endTime: The constraint stops acting after the given value.
Use a negative value for infinite constraints  Default value: -1.0

    :param indices: Indices of the constrained points  Default value: [[0]]

    :param keyTimes: key times for the movements  Default value: [[0.0]]

    :param velocities: velocities corresponding to the key times  Default value: [[0.0, 0.0, 0.0]]

    :param coordinates: coordinates on which to apply velocities  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, group=group, endTime=endTime, indices=indices, keyTimes=keyTimes, velocities=velocities, coordinates=coordinates)
    return "LinearVelocityConstraint", params
