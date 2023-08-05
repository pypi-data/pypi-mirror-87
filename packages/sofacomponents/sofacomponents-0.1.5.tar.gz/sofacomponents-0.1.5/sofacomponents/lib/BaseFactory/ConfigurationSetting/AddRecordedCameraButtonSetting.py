# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component AddRecordedCameraButtonSetting

.. autofunction:: AddRecordedCameraButtonSetting

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def AddRecordedCameraButtonSetting(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, button=None, **kwargs):
    """
    Save Camera's View Point Button configuration


    :param name: object name  Default value: AddRecordedCameraButtonSetting

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param button: Mouse button used  Default value: Left


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, button=button)
    return "AddRecordedCameraButtonSetting", params
