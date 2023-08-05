# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PositionBasedDynamicsConstraint

.. autofunction:: PositionBasedDynamicsConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PositionBasedDynamicsConstraint(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, group=None, endTime=None, stiffness=None, position=None, velocity=None, old_position=None, **kwargs):
    """
    Position-based dynamics


    :param name: object name  Default value: PositionBasedDynamicsConstraint

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param group: ID of the group containing this constraint. This ID is used to specify which constraints are solved by which solver, by specifying in each solver which groups of constraints it should handle.  Default value: 0

    :param endTime: The constraint stops acting after the given value.
Use a negative value for infinite constraints  Default value: -1.0

    :param stiffness: Blending between current pos and target pos.  Default value: 1.0

    :param position: Target positions.  Default value: []

    :param velocity: Velocities.  Default value: []

    :param old_position: Old positions.  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, group=group, endTime=endTime, stiffness=stiffness, position=position, velocity=velocity, old_position=old_position)
    return "PositionBasedDynamicsConstraint", params
