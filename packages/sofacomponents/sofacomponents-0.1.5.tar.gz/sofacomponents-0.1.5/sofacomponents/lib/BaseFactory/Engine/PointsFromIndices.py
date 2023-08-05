# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PointsFromIndices

.. autofunction:: PointsFromIndices

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PointsFromIndices(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, position=None, indices=None, indices_position=None, **kwargs):
    """
    Find the points given a list of indices


    :param name: object name  Default value: PointsFromIndices

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param position: Position coordinates of the degrees of freedom  Default value: []

    :param indices: Indices of the points  Default value: []

    :param indices_position: Coordinates of the points contained in indices  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, position=position, indices=indices, indices_position=indices_position)
    return "PointsFromIndices", params
