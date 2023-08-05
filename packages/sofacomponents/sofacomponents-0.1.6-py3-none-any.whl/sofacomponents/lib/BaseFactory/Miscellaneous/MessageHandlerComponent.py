# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MessageHandlerComponent

.. autofunction:: MessageHandlerComponent

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MessageHandlerComponent(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, handler=None, **kwargs):
    """
    This object controls the way Sofa print's info/warning/error/fatal messages. 


    :param name: object name  Default value: MessageHandlerComponent

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param handler: Type of the message handler to use among [sofa, clang                                        //, log                                        , silent].   Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, handler=handler)
    return "MessageHandlerComponent", params
