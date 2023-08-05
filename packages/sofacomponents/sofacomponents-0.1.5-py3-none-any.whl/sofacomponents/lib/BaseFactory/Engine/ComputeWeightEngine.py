# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ComputeWeightEngine

.. autofunction:: ComputeWeightEngine

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ComputeWeightEngine(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, indices=None, weights=None, **kwargs):
    """
    Computes the weight and indices of a set of vertices of an VisualModelImpl using a given shape function.


    :param name: object name  Default value: ComputeWeightEngine

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param indices: Indices  Default value: []

    :param weights: Weights  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, indices=indices, weights=weights)
    return "ComputeWeightEngine", params
