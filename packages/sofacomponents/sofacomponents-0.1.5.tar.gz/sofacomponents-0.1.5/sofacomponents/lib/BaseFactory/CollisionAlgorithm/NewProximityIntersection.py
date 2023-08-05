# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component NewProximityIntersection

.. autofunction:: NewProximityIntersection

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def NewProximityIntersection(self, alarmDistance=None, contactDistance=None, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, useLineLine=None, **kwargs):
    """
    Optimized Proximity Intersection based on Triangle-Triangle tests, ignoring Edge-Edge cases


    :param name: object name  Default value: NewProximityIntersection

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param alarmDistance: Proximity detection distance  Default value: 1.0

    :param contactDistance: Distance below which a contact is created  Default value: 0.5

    :param useLineLine: Line-line collision detection enabled  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, alarmDistance=alarmDistance, contactDistance=contactDistance, useLineLine=useLineLine)
    return "NewProximityIntersection", params
