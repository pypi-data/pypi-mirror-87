# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MergeROIs

.. autofunction:: MergeROIs

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MergeROIs(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, nbROIs=None, roiIndices=None, **kwargs):
    """
    Merge a list of ROIs (vector<Indices>) into a single Data (vector<svector<Indices>>)


    :param name: object name  Default value: MergeROIs

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param nbROIs: size of indices/value vector  Default value: 0

    :param roiIndices: Vector of ROIs  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, nbROIs=nbROIs, roiIndices=roiIndices)
    return "MergeROIs", params
