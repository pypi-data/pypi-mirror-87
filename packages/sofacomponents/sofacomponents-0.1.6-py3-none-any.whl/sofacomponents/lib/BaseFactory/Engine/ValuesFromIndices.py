# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ValuesFromIndices

.. autofunction:: ValuesFromIndices

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ValuesFromIndices(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, indices=None, out=None, outStr=None, **kwargs):
    """
    Find the values given a list of indices


    :param name: object name  Default value: ValuesFromIndices

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param in: input values (NB: use the kwargs syntax as name is a reserved word in python)

    :param indices: Indices of the values  Default value: []

    :param out: Output values corresponding to the indices  Default value: []

    :param outStr: Output values corresponding to the indices, converted as a string  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, indices=indices, out=out, outStr=outStr)
    return "ValuesFromIndices", params
