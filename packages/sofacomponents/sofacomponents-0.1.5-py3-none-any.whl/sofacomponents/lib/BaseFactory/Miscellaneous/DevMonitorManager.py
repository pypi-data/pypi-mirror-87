# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component DevMonitorManager

.. autofunction:: DevMonitorManager

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def DevMonitorManager(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, period=None, indices=None, **kwargs):
    """
    DevMonitorManager


    :param name: object name  Default value: DevMonitorManager

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param period: period between outputs  Default value: 1.0

    :param indices: Indices of the points which will be monitored  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, period=period, indices=indices)
    return "DevMonitorManager", params
