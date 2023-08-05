# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ViewerSetting

.. autofunction:: ViewerSetting

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ViewerSetting(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, resolution=None, fullscreen=None, cameraMode=None, objectPickingMethod=None, **kwargs):
    """
    Configuration for the Viewer of your application


    :param name: object name  Default value: ViewerSetting

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param resolution: resolution of the Viewer  Default value: [[800, 600]]

    :param fullscreen: Fullscreen mode  Default value: 0

    :param cameraMode: Camera mode  Default value: Perspective

    :param objectPickingMethod: The method used to pick objects  Default value: Ray casting


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, resolution=resolution, fullscreen=fullscreen, cameraMode=cameraMode, objectPickingMethod=objectPickingMethod)
    return "ViewerSetting", params
