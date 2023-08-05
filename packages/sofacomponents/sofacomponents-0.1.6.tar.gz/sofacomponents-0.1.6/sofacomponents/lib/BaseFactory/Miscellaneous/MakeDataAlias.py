# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MakeDataAlias

.. autofunction:: MakeDataAlias

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MakeDataAlias(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, componentname=None, dataname=None, alias=None, **kwargs):
    """
    This object create an alias to a data field. 


    :param name: object name  Default value: MakeDataAlias

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Invalid

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param componentname: The component class for which to create an alias.  Default value: 

    :param dataname: The data field for which to create an alias.  Default value: 

    :param alias: The alias of the data field.  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, componentname=componentname, dataname=dataname, alias=alias)
    return "MakeDataAlias", params
