# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SubsetTopology

.. autofunction:: SubsetTopology

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SubsetTopology(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, box=None, centers=None, radii=None, direction=None, normal=None, edgeAngle=None, triAngle=None, rest_position=None, edges=None, triangles=None, quads=None, tetrahedra=None, hexahedra=None, tetrahedraInput=None, indices=None, edgeIndices=None, triangleIndices=None, quadIndices=None, tetrahedronIndices=None, hexahedronIndices=None, pointsInROI=None, pointsOutROI=None, edgesInROI=None, edgesOutROI=None, trianglesInROI=None, trianglesOutROI=None, quadsInROI=None, quadsOutROI=None, tetrahedraInROI=None, tetrahedraOutROI=None, hexahedraInROI=None, hexahedraOutROI=None, nbrborder=None, localIndices=None, drawROI=None, drawPoints=None, drawEdges=None, drawTriangle=None, drawTetrahedra=None, drawSize=None, **kwargs):
    """
    Engine used to create subset topology given box, sphere, plan, ...


    :param name: object name  Default value: SubsetTopology

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param box: Box defined by xmin,ymin,zmin, xmax,ymax,zmax  Default value: [[0.0, 0.0, 0.0, 1.0, 1.0, 1.0]]

    :param centers: Center(s) of the sphere(s)  Default value: []

    :param radii: Radius(i) of the sphere(s)  Default value: []

    :param direction: Edge direction(if edgeAngle > 0)  Default value: [[0.0, 0.0, 0.0]]

    :param normal: Normal direction of the triangles (if triAngle > 0)  Default value: [[0.0, 0.0, 0.0]]

    :param edgeAngle: Max angle between the direction of the selected edges and the specified direction  Default value: 0.0

    :param triAngle: Max angle between the normal of the selected triangle and the specified normal direction  Default value: 0.0

    :param rest_position: Rest position coordinates of the degrees of freedom  Default value: []

    :param edges: Edge Topology  Default value: []

    :param triangles: Triangle Topology  Default value: []

    :param quads: Quad Topology  Default value: []

    :param tetrahedra: Tetrahedron Topology  Default value: []

    :param hexahedra: Hexahedron Topology  Default value: []

    :param tetrahedraInput: Indices of the tetrahedra to keep  Default value: []

    :param indices: Indices of the points contained in the ROI  Default value: [[0]]

    :param edgeIndices: Indices of the edges contained in the ROI  Default value: []

    :param triangleIndices: Indices of the triangles contained in the ROI  Default value: []

    :param quadIndices: Indices of the quads contained in the ROI  Default value: []

    :param tetrahedronIndices: Indices of the tetrahedra contained in the ROI  Default value: []

    :param hexahedronIndices: Indices of the hexahedra contained in the ROI  Default value: []

    :param pointsInROI: Points contained in the ROI  Default value: []

    :param pointsOutROI: Points out of the ROI  Default value: []

    :param edgesInROI: Edges contained in the ROI  Default value: []

    :param edgesOutROI: Edges out of the ROI  Default value: []

    :param trianglesInROI: Triangles contained in the ROI  Default value: []

    :param trianglesOutROI: Triangles out of the ROI  Default value: []

    :param quadsInROI: Quads contained in the ROI  Default value: []

    :param quadsOutROI: Quads out of the ROI  Default value: []

    :param tetrahedraInROI: Tetrahedra contained in the ROI  Default value: []

    :param tetrahedraOutROI: Tetrahedra out of the ROI  Default value: []

    :param hexahedraInROI: Hexahedra contained in the ROI  Default value: []

    :param hexahedraOutROI: Hexahedra out of the ROI  Default value: []

    :param nbrborder: If localIndices option is activated, will give the number of vertices on the border of the ROI (being the n first points of each output Topology).   Default value: 0

    :param localIndices: If true, will compute local dof indices in topological elements  Default value: 0

    :param drawROI: Draw ROI  Default value: 0

    :param drawPoints: Draw Points  Default value: 0

    :param drawEdges: Draw Edges  Default value: 0

    :param drawTriangle: Draw Triangles  Default value: 0

    :param drawTetrahedra: Draw Tetrahedra  Default value: 0

    :param drawSize: rendering size for box and topological elements  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, box=box, centers=centers, radii=radii, direction=direction, normal=normal, edgeAngle=edgeAngle, triAngle=triAngle, rest_position=rest_position, edges=edges, triangles=triangles, quads=quads, tetrahedra=tetrahedra, hexahedra=hexahedra, tetrahedraInput=tetrahedraInput, indices=indices, edgeIndices=edgeIndices, triangleIndices=triangleIndices, quadIndices=quadIndices, tetrahedronIndices=tetrahedronIndices, hexahedronIndices=hexahedronIndices, pointsInROI=pointsInROI, pointsOutROI=pointsOutROI, edgesInROI=edgesInROI, edgesOutROI=edgesOutROI, trianglesInROI=trianglesInROI, trianglesOutROI=trianglesOutROI, quadsInROI=quadsInROI, quadsOutROI=quadsOutROI, tetrahedraInROI=tetrahedraInROI, tetrahedraOutROI=tetrahedraOutROI, hexahedraInROI=hexahedraInROI, hexahedraOutROI=hexahedraOutROI, nbrborder=nbrborder, localIndices=localIndices, drawROI=drawROI, drawPoints=drawPoints, drawEdges=drawEdges, drawTriangle=drawTriangle, drawTetrahedra=drawTetrahedra, drawSize=drawSize)
    return "SubsetTopology", params
