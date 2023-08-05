# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MakeAlias

.. autofunction:: MakeAlias

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MakeAlias(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, targetcomponent=None, alias=None, **kwargs):
    """
    This object create an alias to a component name to make the scene more readable. 


    :param name: object name  Default value: MakeAlias

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Invalid

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param targetcomponent: The component class for which to create an alias.  Default value: 

    :param alias: The new alias of the component.  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, targetcomponent=targetcomponent, alias=alias)
    return "MakeAlias", params
