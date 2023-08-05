# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component JoinPoints

.. autofunction:: JoinPoints

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def JoinPoints(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, points=None, distance=None, mergedPoints=None, **kwargs):
    """
    ?


    :param name: object name  Default value: JoinPoints

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param points: Points  Default value: []

    :param distance: Distance to merge points  Default value: 0.0

    :param mergedPoints: Merged Points  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, points=points, distance=distance, mergedPoints=mergedPoints)
    return "JoinPoints", params
