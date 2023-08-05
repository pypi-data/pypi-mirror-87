# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SphereROI

.. autofunction:: SphereROI

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SphereROI(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, centers=None, radii=None, direction=None, normal=None, edgeAngle=None, triAngle=None, position=None, edges=None, triangles=None, quads=None, tetrahedra=None, computeEdges=None, computeTriangles=None, computeQuads=None, computeTetrahedra=None, indices=None, edgeIndices=None, triangleIndices=None, quadIndices=None, tetrahedronIndices=None, pointsInROI=None, edgesInROI=None, trianglesInROI=None, quadsInROI=None, tetrahedraInROI=None, indicesOut=None, drawSphere=None, drawPoints=None, drawEdges=None, drawTriangles=None, drawQuads=None, drawTetrahedra=None, drawSize=None, **kwargs):
    """
    Find the primitives (vertex/edge/triangle/tetrahedron) inside a given sphere


    :param name: object name  Default value: SphereROI

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param centers: Center(s) of the sphere(s)  Default value: []

    :param radii: Radius(i) of the sphere(s)  Default value: []

    :param direction: Edge direction(if edgeAngle > 0)  Default value: [[0.0, 0.0, 0.0]]

    :param normal: Normal direction of the triangles (if triAngle > 0)  Default value: [[0.0, 0.0, 0.0]]

    :param edgeAngle: Max angle between the direction of the selected edges and the specified direction  Default value: 0.0

    :param triAngle: Max angle between the normal of the selected triangle and the specified normal direction  Default value: 0.0

    :param position: Rest position coordinates of the degrees of freedom  Default value: []

    :param edges: Edge Topology  Default value: []

    :param triangles: Triangle Topology  Default value: []

    :param quads: Quads Topology  Default value: []

    :param tetrahedra: Tetrahedron Topology  Default value: []

    :param computeEdges: If true, will compute edge list and index list inside the ROI.  Default value: 1

    :param computeTriangles: If true, will compute triangle list and index list inside the ROI.  Default value: 1

    :param computeQuads: If true, will compute quad list and index list inside the ROI.  Default value: 1

    :param computeTetrahedra: If true, will compute tetrahedra list and index list inside the ROI.  Default value: 1

    :param indices: Indices of the points contained in the ROI  Default value: [[0]]

    :param edgeIndices: Indices of the edges contained in the ROI  Default value: []

    :param triangleIndices: Indices of the triangles contained in the ROI  Default value: []

    :param quadIndices: Indices of the quads contained in the ROI  Default value: []

    :param tetrahedronIndices: Indices of the tetrahedra contained in the ROI  Default value: []

    :param pointsInROI: Points contained in the ROI  Default value: []

    :param edgesInROI: Edges contained in the ROI  Default value: []

    :param trianglesInROI: Triangles contained in the ROI  Default value: []

    :param quadsInROI: Quads contained in the ROI  Default value: []

    :param tetrahedraInROI: Tetrahedra contained in the ROI  Default value: []

    :param indicesOut: Indices of the points not contained in the ROI  Default value: []

    :param drawSphere: Draw shpere(s)  Default value: 0

    :param drawPoints: Draw Points  Default value: 0

    :param drawEdges: Draw Edges  Default value: 0

    :param drawTriangles: Draw Triangles  Default value: 0

    :param drawQuads: Draw Quads  Default value: 0

    :param drawTetrahedra: Draw Tetrahedra  Default value: 0

    :param drawSize: rendering size for box and topological elements  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, centers=centers, radii=radii, direction=direction, normal=normal, edgeAngle=edgeAngle, triAngle=triAngle, position=position, edges=edges, triangles=triangles, quads=quads, tetrahedra=tetrahedra, computeEdges=computeEdges, computeTriangles=computeTriangles, computeQuads=computeQuads, computeTetrahedra=computeTetrahedra, indices=indices, edgeIndices=edgeIndices, triangleIndices=triangleIndices, quadIndices=quadIndices, tetrahedronIndices=tetrahedronIndices, pointsInROI=pointsInROI, edgesInROI=edgesInROI, trianglesInROI=trianglesInROI, quadsInROI=quadsInROI, tetrahedraInROI=tetrahedraInROI, indicesOut=indicesOut, drawSphere=drawSphere, drawPoints=drawPoints, drawEdges=drawEdges, drawTriangles=drawTriangles, drawQuads=drawQuads, drawTetrahedra=drawTetrahedra, drawSize=drawSize)
    return "SphereROI", params
