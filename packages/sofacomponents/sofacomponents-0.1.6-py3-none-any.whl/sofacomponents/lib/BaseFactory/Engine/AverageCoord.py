# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component AverageCoord

.. autofunction:: AverageCoord

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def AverageCoord(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, indices=None, vecId=None, average=None, **kwargs):
    """
    Compute the average of coordinates


    :param name: object name  Default value: AverageCoord

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param indices: indices of the coordinates to average  Default value: []

    :param vecId: index of the vector (default value corresponds to core::VecCoordId::position() )  Default value: 1

    :param average: average of the values with the given indices in the given coordinate vector 
(default value corresponds to the average coord of the mechanical context)  Default value: [[0.0, 0.0, 0.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, indices=indices, vecId=vecId, average=average)
    return "AverageCoord", params
