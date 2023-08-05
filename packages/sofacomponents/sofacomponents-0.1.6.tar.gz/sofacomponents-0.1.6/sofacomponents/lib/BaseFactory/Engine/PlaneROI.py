# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PlaneROI

.. autofunction:: PlaneROI

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PlaneROI(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, plane=None, position=None, edges=None, triangles=None, tetrahedra=None, computeEdges=None, computeTriangles=None, computeTetrahedra=None, indices=None, edgeIndices=None, triangleIndices=None, tetrahedronIndices=None, pointsInROI=None, edgesInROI=None, trianglesInROI=None, tetrahedraInROI=None, drawBoxes=None, drawPoints=None, drawEdges=None, drawTriangles=None, drawTetrahedra=None, drawSize=None, **kwargs):
    """
    Find the primitives inside a given plane


    :param name: object name  Default value: PlaneROI

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param plane: Plane defined by 3 points and a depth distance  Default value: [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

    :param position: Rest position coordinates of the degrees of freedom  Default value: []

    :param edges: Edge Topology  Default value: []

    :param triangles: Triangle Topology  Default value: []

    :param tetrahedra: Tetrahedron Topology  Default value: []

    :param computeEdges: If true, will compute edge list and index list inside the ROI.  Default value: 1

    :param computeTriangles: If true, will compute triangle list and index list inside the ROI.  Default value: 1

    :param computeTetrahedra: If true, will compute tetrahedra list and index list inside the ROI.  Default value: 1

    :param indices: Indices of the points contained in the ROI  Default value: [[0]]

    :param edgeIndices: Indices of the edges contained in the ROI  Default value: []

    :param triangleIndices: Indices of the triangles contained in the ROI  Default value: []

    :param tetrahedronIndices: Indices of the tetrahedra contained in the ROI  Default value: []

    :param pointsInROI: Points contained in the ROI  Default value: []

    :param edgesInROI: Edges contained in the ROI  Default value: []

    :param trianglesInROI: Triangles contained in the ROI  Default value: []

    :param tetrahedraInROI: Tetrahedra contained in the ROI  Default value: []

    :param drawBoxes: Draw Box(es)  Default value: 0

    :param drawPoints: Draw Points  Default value: 0

    :param drawEdges: Draw Edges  Default value: 0

    :param drawTriangles: Draw Triangles  Default value: 0

    :param drawTetrahedra: Draw Tetrahedra  Default value: 0

    :param drawSize: rendering size for box and topological elements  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, plane=plane, position=position, edges=edges, triangles=triangles, tetrahedra=tetrahedra, computeEdges=computeEdges, computeTriangles=computeTriangles, computeTetrahedra=computeTetrahedra, indices=indices, edgeIndices=edgeIndices, triangleIndices=triangleIndices, tetrahedronIndices=tetrahedronIndices, pointsInROI=pointsInROI, edgesInROI=edgesInROI, trianglesInROI=trianglesInROI, tetrahedraInROI=tetrahedraInROI, drawBoxes=drawBoxes, drawPoints=drawPoints, drawEdges=drawEdges, drawTriangles=drawTriangles, drawTetrahedra=drawTetrahedra, drawSize=drawSize)
    return "PlaneROI", params
