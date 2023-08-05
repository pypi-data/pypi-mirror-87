# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component BoxROI

.. autofunction:: BoxROI

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def BoxROI(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, box=None, orientedBox=None, position=None, edges=None, triangles=None, tetrahedra=None, hexahedra=None, quad=None, computeEdges=None, computeTriangles=None, computeTetrahedra=None, computeHexahedra=None, computeQuad=None, strict=None, indices=None, edgeIndices=None, triangleIndices=None, tetrahedronIndices=None, hexahedronIndices=None, quadIndices=None, pointsInROI=None, edgesInROI=None, trianglesInROI=None, tetrahedraInROI=None, hexahedraInROI=None, quadInROI=None, nbIndices=None, drawBoxes=None, drawPoints=None, drawEdges=None, drawTriangles=None, drawTetrahedra=None, drawHexahedra=None, drawQuads=None, drawSize=None, doUpdate=None, rest_position=None, isVisible=None, **kwargs):
    """
    Find the primitives (vertex/edge/triangle/quad/tetrahedron/hexahedron) inside given boxes
Find the primitives (vertex/edge/triangle/tetrahedron) inside a given box
Find the primitives (vertex/edge/triangle/tetrahedron) inside a given box


    :param name: object name  Default value: BoxROI

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param box: List of boxes defined by xmin,ymin,zmin, xmax,ymax,zmax  Default value: []

    :param orientedBox: List of boxes defined by 3 points (p0, p1, p2) and a depth distance 
A parallelogram will be defined by (p0, p1, p2, p3 = p0 + (p2-p1)). 
The box will finaly correspond to the parallelogram extrusion of depth/2 
along its normal and depth/2 in the opposite direction.   Default value: []

    :param position: Rest position coordinates of the degrees of freedom. 
If empty the positions from a MechanicalObject then a MeshLoader are searched in the current context. 
If none are found the parent's context is searched for MechanicalObject.  Default value: []

    :param edges: Edge Topology  Default value: []

    :param triangles: Triangle Topology  Default value: []

    :param tetrahedra: Tetrahedron Topology  Default value: []

    :param hexahedra: Hexahedron Topology  Default value: []

    :param quad: Quad Topology  Default value: []

    :param computeEdges: If true, will compute edge list and index list inside the ROI. (default = true)  Default value: 1

    :param computeTriangles: If true, will compute triangle list and index list inside the ROI. (default = true)  Default value: 1

    :param computeTetrahedra: If true, will compute tetrahedra list and index list inside the ROI. (default = true)  Default value: 1

    :param computeHexahedra: If true, will compute hexahedra list and index list inside the ROI. (default = true)  Default value: 1

    :param computeQuad: If true, will compute quad list and index list inside the ROI. (default = true)  Default value: 1

    :param strict: If true, an element is inside the box iif all of its nodes are inside. If False, only the center point of the element is checked. (default = true)  Default value: 1

    :param indices: Indices of the points contained in the ROI  Default value: [[0]]

    :param edgeIndices: Indices of the edges contained in the ROI  Default value: []

    :param triangleIndices: Indices of the triangles contained in the ROI  Default value: []

    :param tetrahedronIndices: Indices of the tetrahedra contained in the ROI  Default value: []

    :param hexahedronIndices: Indices of the hexahedra contained in the ROI  Default value: []

    :param quadIndices: Indices of the quad contained in the ROI  Default value: []

    :param pointsInROI: Points contained in the ROI  Default value: []

    :param edgesInROI: Edges contained in the ROI  Default value: []

    :param trianglesInROI: Triangles contained in the ROI  Default value: []

    :param tetrahedraInROI: Tetrahedra contained in the ROI  Default value: []

    :param hexahedraInROI: Hexahedra contained in the ROI  Default value: []

    :param quadInROI: Quad contained in the ROI  Default value: []

    :param nbIndices: Number of selected indices  Default value: 0

    :param drawBoxes: Draw Boxes. (default = false)  Default value: 0

    :param drawPoints: Draw Points. (default = false)  Default value: 0

    :param drawEdges: Draw Edges. (default = false)  Default value: 0

    :param drawTriangles: Draw Triangles. (default = false)  Default value: 0

    :param drawTetrahedra: Draw Tetrahedra. (default = false)  Default value: 0

    :param drawHexahedra: Draw Tetrahedra. (default = false)  Default value: 0

    :param drawQuads: Draw Quads. (default = false)  Default value: 0

    :param drawSize: rendering size for box and topological elements  Default value: 0.0

    :param doUpdate: If true, updates the selection at the beginning of simulation steps. (default = true)  Default value: 1

    :param rest_position: (deprecated) Replaced with the attribute 'position'  Default value: []

    :param isVisible: (deprecated)Replaced with the attribute 'drawBoxes'  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, box=box, orientedBox=orientedBox, position=position, edges=edges, triangles=triangles, tetrahedra=tetrahedra, hexahedra=hexahedra, quad=quad, computeEdges=computeEdges, computeTriangles=computeTriangles, computeTetrahedra=computeTetrahedra, computeHexahedra=computeHexahedra, computeQuad=computeQuad, strict=strict, indices=indices, edgeIndices=edgeIndices, triangleIndices=triangleIndices, tetrahedronIndices=tetrahedronIndices, hexahedronIndices=hexahedronIndices, quadIndices=quadIndices, pointsInROI=pointsInROI, edgesInROI=edgesInROI, trianglesInROI=trianglesInROI, tetrahedraInROI=tetrahedraInROI, hexahedraInROI=hexahedraInROI, quadInROI=quadInROI, nbIndices=nbIndices, drawBoxes=drawBoxes, drawPoints=drawPoints, drawEdges=drawEdges, drawTriangles=drawTriangles, drawTetrahedra=drawTetrahedra, drawHexahedra=drawHexahedra, drawQuads=drawQuads, drawSize=drawSize, doUpdate=doUpdate, rest_position=rest_position, isVisible=isVisible)
    return "BoxROI", params
