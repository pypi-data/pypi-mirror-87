# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component DefaultContactManager

.. autofunction:: DefaultContactManager

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def DefaultContactManager(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, response=None, responseParams=None, **kwargs):
    """
    Default class to create reactions to the collisions


    :param name: object name  Default value: DefaultContactManager

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param response: contact response class  Default value: default

    :param responseParams: contact response parameters (syntax: name1=value1&name2=value2&...)  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, response=response, responseParams=responseParams)
    return "DefaultContactManager", params
