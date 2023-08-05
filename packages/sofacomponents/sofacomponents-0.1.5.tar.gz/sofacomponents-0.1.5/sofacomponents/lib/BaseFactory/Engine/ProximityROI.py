# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ProximityROI

.. autofunction:: ProximityROI

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ProximityROI(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, centers=None, radii=None, N=None, position=None, indices=None, pointsInROI=None, distance=None, indicesOut=None, drawSphere=None, drawPoints=None, drawSize=None, **kwargs):
    """
    Find the N closest primitives from a given position


    :param name: object name  Default value: ProximityROI

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param centers: Center(s) of the sphere(s)  Default value: []

    :param radii: Radius(i) of the sphere(s)  Default value: []

    :param N: Maximum number of points to select  Default value: 0

    :param position: Rest position coordinates of the degrees of freedom  Default value: []

    :param indices: Indices of the points contained in the ROI  Default value: [[0]]

    :param pointsInROI: Points contained in the ROI  Default value: []

    :param distance: distance between the points contained in the ROI and the closest center.  Default value: []

    :param indicesOut: Indices of the points not contained in the ROI  Default value: []

    :param drawSphere: Draw shpere(s)  Default value: 0

    :param drawPoints: Draw Points  Default value: 0

    :param drawSize: rendering size for box and topological elements  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, centers=centers, radii=radii, N=N, position=position, indices=indices, pointsInROI=pointsInROI, distance=distance, indicesOut=indicesOut, drawSphere=drawSphere, drawPoints=drawPoints, drawSize=drawSize)
    return "ProximityROI", params
