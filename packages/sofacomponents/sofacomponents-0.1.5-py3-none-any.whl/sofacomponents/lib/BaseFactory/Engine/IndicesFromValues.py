# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component IndicesFromValues

.. autofunction:: IndicesFromValues

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def IndicesFromValues(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, values=None, indices=None, otherIndices=None, recursiveSearch=None, **kwargs):
    """
    Find the indices of a list of values within a larger set of values


    :param name: object name  Default value: IndicesFromValues

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param values: input values  Default value: []

    :param global: Global values, in which the input values are searched (NB: use the kwargs syntax as name is a reserved word in python)

    :param indices: Output indices of the given values, searched in global  Default value: []

    :param otherIndices: Output indices of the other values, (NOT the given ones) searched in global  Default value: []

    :param recursiveSearch: if set to true, output are indices of the "global" data matching with one of the values  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, values=values, indices=indices, otherIndices=otherIndices, recursiveSearch=recursiveSearch)
    return "IndicesFromValues", params
