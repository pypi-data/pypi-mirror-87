# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SelectConnectedLabelsROI

.. autofunction:: SelectConnectedLabelsROI

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SelectConnectedLabelsROI(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, nbLabels=None, connectLabels=None, indices=None, **kwargs):
    """
    Select a subset of points or cells labeled from different sources, that are connected given a list of connection pairs


    :param name: object name  Default value: SelectConnectedLabelsROI

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param nbLabels: number of label lists  Default value: 0

    :param connectLabels: Pairs of label to be connected accross different label lists  Default value: []

    :param indices: selected point/cell indices  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, nbLabels=nbLabels, connectLabels=connectLabels, indices=indices)
    return "SelectConnectedLabelsROI", params
