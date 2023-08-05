# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component BackgroundSetting

.. autofunction:: BackgroundSetting

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def BackgroundSetting(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, color=None, image=None, **kwargs):
    """
    Backgrounds setting


    :param name: object name  Default value: BackgroundSetting

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param color: Color of the background  Default value: [[1.0, 1.0, 1.0, 1.0]]

    :param image: Image to be used as background  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, color=color, image=image)
    return "BackgroundSetting", params
