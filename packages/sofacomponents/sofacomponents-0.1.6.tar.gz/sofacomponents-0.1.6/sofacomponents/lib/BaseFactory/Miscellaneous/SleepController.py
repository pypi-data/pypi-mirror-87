# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SleepController

.. autofunction:: SleepController

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SleepController(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, minTimeSinceWakeUp=None, immobileThreshold=None, rotationThreshold=None, **kwargs):
    """
    A controller that puts node into sleep when the objects are not moving, and wake them up again when there are in collision with a moving object


    :param name: object name  Default value: SleepController

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param minTimeSinceWakeUp: Do not do anything before objects have been moving for this duration  Default value: 0.1

    :param immobileThreshold: Speed value under which we consider a particule to be immobile  Default value: 0.001

    :param rotationThreshold: If non null, this is the rotation speed value under which we consider a particule to be immobile  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, minTimeSinceWakeUp=minTimeSinceWakeUp, immobileThreshold=immobileThreshold, rotationThreshold=rotationThreshold)
    return "SleepController", params
