# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ParabolicConstraint

.. autofunction:: ParabolicConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ParabolicConstraint(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, group=None, endTime=None, indices=None, P1=None, P2=None, P3=None, BeginTime=None, EndTime=None, **kwargs):
    """
    Apply a parabolic trajectory to given points


    :param name: object name  Default value: ParabolicConstraint

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param group: ID of the group containing this constraint. This ID is used to specify which constraints are solved by which solver, by specifying in each solver which groups of constraints it should handle.  Default value: 0

    :param endTime: The constraint stops acting after the given value.
Use a negative value for infinite constraints  Default value: -1.0

    :param indices: Indices of the constrained points  Default value: []

    :param P1: first point of the parabol  Default value: [[0.0, 0.0, 0.0]]

    :param P2: second point of the parabol  Default value: [[0.0, 0.0, 0.0]]

    :param P3: third point of the parabol  Default value: [[0.0, 0.0, 0.0]]

    :param BeginTime: Begin Time of the motion  Default value: 0.0

    :param EndTime: End Time of the motion  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, group=group, endTime=endTime, indices=indices, P1=P1, P2=P2, P3=P3, BeginTime=BeginTime, EndTime=EndTime)
    return "ParabolicConstraint", params
