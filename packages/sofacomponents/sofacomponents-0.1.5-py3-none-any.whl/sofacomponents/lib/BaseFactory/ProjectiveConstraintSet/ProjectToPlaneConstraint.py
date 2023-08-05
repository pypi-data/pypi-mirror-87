# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ProjectToPlaneConstraint

.. autofunction:: ProjectToPlaneConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ProjectToPlaneConstraint(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, group=None, endTime=None, indices=None, origin=None, normal=None, drawSize=None, **kwargs):
    """
    Attach given particles to their initial positions


    :param name: object name  Default value: ProjectToPlaneConstraint

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param group: ID of the group containing this constraint. This ID is used to specify which constraints are solved by which solver, by specifying in each solver which groups of constraints it should handle.  Default value: 0

    :param endTime: The constraint stops acting after the given value.
Use a negative value for infinite constraints  Default value: -1.0

    :param indices: Indices of the fixed points  Default value: [[0]]

    :param origin: A point in the plane  Default value: [[0.0, 0.0, 0.0]]

    :param normal: Normal vector to the plane  Default value: [[0.0, 0.0, 0.0]]

    :param drawSize: 0 -> point based rendering, >0 -> radius of spheres  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, group=group, endTime=endTime, indices=indices, origin=origin, normal=normal, drawSize=drawSize)
    return "ProjectToPlaneConstraint", params
