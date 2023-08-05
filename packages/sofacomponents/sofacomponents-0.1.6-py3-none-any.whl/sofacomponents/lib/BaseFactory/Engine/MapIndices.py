# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MapIndices

.. autofunction:: MapIndices

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MapIndices(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, indices=None, out=None, outStr=None, transpose=None, **kwargs):
    """
    Apply a permutation to a set of indices


    :param name: object name  Default value: MapIndices

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param in: input indices (NB: use the kwargs syntax as name is a reserved word in python)

    :param indices: array containing in ith cell the input index corresponding to the output index i (or reversively if transpose=true)  Default value: []

    :param out: Output indices  Default value: []

    :param outStr: Output indices, converted as a string  Default value: 

    :param transpose: Should the transposed mapping be used ?  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, indices=indices, out=out, outStr=outStr, transpose=transpose)
    return "MapIndices", params
