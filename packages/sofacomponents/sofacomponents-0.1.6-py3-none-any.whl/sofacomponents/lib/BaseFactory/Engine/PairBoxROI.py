# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PairBoxROI

.. autofunction:: PairBoxROI

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PairBoxROI(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, inclusiveBox=None, includedBox=None, position=None, meshPosition=None, indices=None, pointsInROI=None, drawInclusiveBox=None, drawInclusdedBx=None, drawPoints=None, drawSize=None, **kwargs):
    """
    Find the primitives (vertex/edge/triangle/tetrahedron) inside a given box


    :param name: object name  Default value: PairBoxROI

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param inclusiveBox: Inclusive box defined by xmin,ymin,zmin, xmax,ymax,zmax  Default value: [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

    :param includedBox: Included box defined by xmin,ymin,zmin, xmax,ymax,zmax  Default value: [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

    :param position: Rest position coordinates of the degrees of freedom  Default value: []

    :param meshPosition: Vertices of the mesh loaded  Default value: []

    :param indices: Indices of the points contained in the ROI  Default value: []

    :param pointsInROI: Points contained in the ROI  Default value: []

    :param drawInclusiveBox: Draw Inclusive Box  Default value: 0

    :param drawInclusdedBx: Draw Included Box  Default value: 0

    :param drawPoints: Draw Points  Default value: 0

    :param drawSize: Draw Size  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, inclusiveBox=inclusiveBox, includedBox=includedBox, position=position, meshPosition=meshPosition, indices=indices, pointsInROI=pointsInROI, drawInclusiveBox=drawInclusiveBox, drawInclusdedBx=drawInclusdedBx, drawPoints=drawPoints, drawSize=drawSize)
    return "PairBoxROI", params
