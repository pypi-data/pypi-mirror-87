# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PostProcessManager

.. autofunction:: PostProcessManager

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PostProcessManager(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, zNear=None, zFar=None, **kwargs):
    """
    PostProcessManager


    :param name: object name  Default value: PostProcessManager

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param zNear: Set zNear distance (for Depth Buffer)  Default value: 1.0

    :param zFar: Set zFar distance (for Depth Buffer)  Default value: 100.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, zNear=zNear, zFar=zFar)
    return "PostProcessManager", params
