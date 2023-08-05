# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component HermiteSplineConstraint

.. autofunction:: HermiteSplineConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def HermiteSplineConstraint(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, group=None, endTime=None, indices=None, BeginTime=None, EndTime=None, X0=None, dX0=None, X1=None, dX1=None, SX0=None, SX1=None, **kwargs):
    """
    Apply a hermite cubic spline trajectory to given points


    :param name: object name  Default value: HermiteSplineConstraint

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param group: ID of the group containing this constraint. This ID is used to specify which constraints are solved by which solver, by specifying in each solver which groups of constraints it should handle.  Default value: 0

    :param endTime: The constraint stops acting after the given value.
Use a negative value for infinite constraints  Default value: -1.0

    :param indices: Indices of the constrained points  Default value: []

    :param BeginTime: Begin Time of the motion  Default value: 0.0

    :param EndTime: End Time of the motion  Default value: 0.0

    :param X0: first control point  Default value: [[0.0, 0.0, 0.0]]

    :param dX0: first control tangente  Default value: [[0.0, 0.0, 0.0]]

    :param X1: second control point  Default value: [[0.0, 0.0, 0.0]]

    :param dX1: sceond control tangente  Default value: [[0.0, 0.0, 0.0]]

    :param SX0: first interpolation vector  Default value: [[0.0, 0.0]]

    :param SX1: second interpolation vector  Default value: [[0.0, 0.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, group=group, endTime=endTime, indices=indices, BeginTime=BeginTime, EndTime=EndTime, X0=X0, dX0=dX0, X1=X1, dX1=dX1, SX0=SX0, SX1=SX1)
    return "HermiteSplineConstraint", params
