# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MergePoints

.. autofunction:: MergePoints

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MergePoints(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, position1=None, position2=None, mappingX2=None, indices1=None, indices2=None, points=None, noUpdate=None, **kwargs):
    """
    Merge 2 cordinate vectors


    :param name: object name  Default value: MergePoints

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param position1: position coordinates of the degrees of freedom of the first object  Default value: []

    :param position2: Rest position coordinates of the degrees of freedom of the second object  Default value: []

    :param mappingX2: Mapping of indices to inject position2 inside position1 vertex buffer  Default value: []

    :param indices1: Indices of the points of the first object  Default value: []

    :param indices2: Indices of the points of the second object  Default value: []

    :param points: position coordinates of the merge  Default value: []

    :param noUpdate: do not update the output at eacth time step (false)  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, position1=position1, position2=position2, mappingX2=mappingX2, indices1=indices1, indices2=indices2, points=points, noUpdate=noUpdate)
    return "MergePoints", params
