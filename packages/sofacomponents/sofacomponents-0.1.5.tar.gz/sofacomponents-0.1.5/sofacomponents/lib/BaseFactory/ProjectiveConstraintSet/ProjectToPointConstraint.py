# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ProjectToPointConstraint

.. autofunction:: ProjectToPointConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ProjectToPointConstraint(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, group=None, endTime=None, indices=None, point=None, fixAll=None, drawSize=None, **kwargs):
    """
    Project particles to a point
Project particles to a point
Project particles to a point


    :param name: object name  Default value: ProjectToPointConstraint

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param group: ID of the group containing this constraint. This ID is used to specify which constraints are solved by which solver, by specifying in each solver which groups of constraints it should handle.  Default value: 0

    :param endTime: The constraint stops acting after the given value.
Use a negative value for infinite constraints  Default value: -1.0

    :param indices: Indices of the points to project  Default value: [[0]]

    :param point: Target of the projection  Default value: [[0.0, 0.0, 0.0]]

    :param fixAll: filter all the DOF to implement a fixed object  Default value: 0

    :param drawSize: 0 -> point based rendering, >0 -> radius of spheres  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, group=group, endTime=endTime, indices=indices, point=point, fixAll=fixAll, drawSize=drawSize)
    return "ProjectToPointConstraint", params
