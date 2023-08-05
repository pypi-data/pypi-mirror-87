# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ComplementaryROI

.. autofunction:: ComplementaryROI

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ComplementaryROI(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, position=None, nbSet=None, indices=None, pointsInROI=None, **kwargs):
    """
    Find the points that are NOT in the input sets


    :param name: object name  Default value: ComplementaryROI

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param position: input positions  Default value: []

    :param nbSet: number of sets to complement  Default value: 0

    :param indices: indices of the point in the ROI  Default value: []

    :param pointsInROI: points in the ROI  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, position=position, nbSet=nbSet, indices=indices, pointsInROI=pointsInROI)
    return "ComplementaryROI", params
