# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component FixedPlaneConstraint

.. autofunction:: FixedPlaneConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def FixedPlaneConstraint(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, group=None, endTime=None, direction=None, dmin=None, dmax=None, indices=None, **kwargs):
    """
    Project particles on a given plane


    :param name: object name  Default value: FixedPlaneConstraint

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param group: ID of the group containing this constraint. This ID is used to specify which constraints are solved by which solver, by specifying in each solver which groups of constraints it should handle.  Default value: 0

    :param endTime: The constraint stops acting after the given value.
Use a negative value for infinite constraints  Default value: -1.0

    :param direction: normal direction of the plane  Default value: [[0.0, 0.0, 0.0]]

    :param dmin: Minimum plane distance from the origin  Default value: 0.0

    :param dmax: Maximum plane distance from the origin  Default value: 0.0

    :param indices: Indices of the fixed points  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, group=group, endTime=endTime, direction=direction, dmin=dmin, dmax=dmax, indices=indices)
    return "FixedPlaneConstraint", params
