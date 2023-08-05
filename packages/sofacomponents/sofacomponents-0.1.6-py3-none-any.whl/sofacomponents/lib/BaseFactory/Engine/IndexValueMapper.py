# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component IndexValueMapper

.. autofunction:: IndexValueMapper

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def IndexValueMapper(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, inputValues=None, indices=None, value=None, outputValues=None, defaultValue=None, **kwargs):
    """
    Input values to output values mapper. Includes indices rules, such as replacement, resize


    :param name: object name  Default value: IndexValueMapper

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param inputValues: Already existing values (can be empty)   Default value: []

    :param indices: Indices to map value on   Default value: []

    :param value: Value to map indices on   Default value: 0.0

    :param outputValues: New map between indices and values  Default value: []

    :param defaultValue: Default value for indices without any value  Default value: 1.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, inputValues=inputValues, indices=indices, value=value, outputValues=outputValues, defaultValue=defaultValue)
    return "IndexValueMapper", params
