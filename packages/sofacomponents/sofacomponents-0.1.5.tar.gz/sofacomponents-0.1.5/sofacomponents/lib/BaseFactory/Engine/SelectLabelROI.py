# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SelectLabelROI

.. autofunction:: SelectLabelROI

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SelectLabelROI(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, labels=None, selectLabels=None, indices=None, **kwargs):
    """
    Select a subset of labeled points or cells stored in (vector<svector<label>>) given certain labels


    :param name: object name  Default value: SelectLabelROI

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param labels: lists of labels associated to each point/cell  Default value: 

    :param selectLabels: list of selected labels  Default value: []

    :param indices: selected point/cell indices  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, labels=labels, selectLabels=selectLabels, indices=indices)
    return "SelectLabelROI", params
