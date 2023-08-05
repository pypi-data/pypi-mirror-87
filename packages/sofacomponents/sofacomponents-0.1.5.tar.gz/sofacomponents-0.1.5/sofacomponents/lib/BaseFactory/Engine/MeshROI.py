# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MeshROI

.. autofunction:: MeshROI

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MeshROI(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, position=None, edges=None, triangles=None, tetrahedra=None, ROIposition=None, ROIedges=None, ROItriangles=None, computeEdges=None, computeTriangles=None, computeTetrahedra=None, computeMeshROI=None, box=None, indices=None, edgeIndices=None, triangleIndices=None, tetrahedronIndices=None, pointsInROI=None, edgesInROI=None, trianglesInROI=None, tetrahedraInROI=None, pointsOutROI=None, edgesOutROI=None, trianglesOutROI=None, tetrahedraOutROI=None, indicesOut=None, edgeOutIndices=None, triangleOutIndices=None, tetrahedronOutIndices=None, drawOut=None, drawMesh=None, drawBox=None, drawPoints=None, drawEdges=None, drawTriangles=None, drawTetrahedra=None, drawSize=None, doUpdate=None, **kwargs):
    """
    Find the primitives (vertex/edge/triangle/tetrahedron) inside a given mesh


    :param name: object name  Default value: MeshROI

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param position: Rest position coordinates of the degrees of freedom  Default value: []

    :param edges: Edge Topology  Default value: []

    :param triangles: Triangle Topology  Default value: []

    :param tetrahedra: Tetrahedron Topology  Default value: []

    :param ROIposition: ROI position coordinates of the degrees of freedom  Default value: []

    :param ROIedges: ROI Edge Topology  Default value: []

    :param ROItriangles: ROI Triangle Topology  Default value: []

    :param computeEdges: If true, will compute edge list and index list inside the ROI.  Default value: 1

    :param computeTriangles: If true, will compute triangle list and index list inside the ROI.  Default value: 1

    :param computeTetrahedra: If true, will compute tetrahedra list and index list inside the ROI.  Default value: 1

    :param computeMeshROI: Compute with the mesh (not only bounding box)  Default value: 1

    :param box: Bounding box defined by xmin,ymin,zmin, xmax,ymax,zmax  Default value: [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

    :param indices: Indices of the points contained in the ROI  Default value: [[0]]

    :param edgeIndices: Indices of the edges contained in the ROI  Default value: []

    :param triangleIndices: Indices of the triangles contained in the ROI  Default value: []

    :param tetrahedronIndices: Indices of the tetrahedra contained in the ROI  Default value: []

    :param pointsInROI: Points contained in the ROI  Default value: []

    :param edgesInROI: Edges contained in the ROI  Default value: []

    :param trianglesInROI: Triangles contained in the ROI  Default value: []

    :param tetrahedraInROI: Tetrahedra contained in the ROI  Default value: []

    :param pointsOutROI: Points not contained in the ROI  Default value: []

    :param edgesOutROI: Edges not contained in the ROI  Default value: []

    :param trianglesOutROI: Triangles not contained in the ROI  Default value: []

    :param tetrahedraOutROI: Tetrahedra not contained in the ROI  Default value: []

    :param indicesOut: Indices of the points not contained in the ROI  Default value: []

    :param edgeOutIndices: Indices of the edges not contained in the ROI  Default value: []

    :param triangleOutIndices: Indices of the triangles not contained in the ROI  Default value: []

    :param tetrahedronOutIndices: Indices of the tetrahedra not contained in the ROI  Default value: []

    :param drawOut: Draw the data not contained in the ROI  Default value: 0

    :param drawMesh: Draw Mesh used for the ROI  Default value: 0

    :param drawBox: Draw the Bounding box around the mesh used for the ROI  Default value: 0

    :param drawPoints: Draw Points  Default value: 0

    :param drawEdges: Draw Edges  Default value: 0

    :param drawTriangles: Draw Triangles  Default value: 0

    :param drawTetrahedra: Draw Tetrahedra  Default value: 0

    :param drawSize: rendering size for mesh and topological elements  Default value: 0.0

    :param doUpdate: Update the computation (not only at the init)  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, position=position, edges=edges, triangles=triangles, tetrahedra=tetrahedra, ROIposition=ROIposition, ROIedges=ROIedges, ROItriangles=ROItriangles, computeEdges=computeEdges, computeTriangles=computeTriangles, computeTetrahedra=computeTetrahedra, computeMeshROI=computeMeshROI, box=box, indices=indices, edgeIndices=edgeIndices, triangleIndices=triangleIndices, tetrahedronIndices=tetrahedronIndices, pointsInROI=pointsInROI, edgesInROI=edgesInROI, trianglesInROI=trianglesInROI, tetrahedraInROI=tetrahedraInROI, pointsOutROI=pointsOutROI, edgesOutROI=edgesOutROI, trianglesOutROI=trianglesOutROI, tetrahedraOutROI=tetrahedraOutROI, indicesOut=indicesOut, edgeOutIndices=edgeOutIndices, triangleOutIndices=triangleOutIndices, tetrahedronOutIndices=tetrahedronOutIndices, drawOut=drawOut, drawMesh=drawMesh, drawBox=drawBox, drawPoints=drawPoints, drawEdges=drawEdges, drawTriangles=drawTriangles, drawTetrahedra=drawTetrahedra, drawSize=drawSize, doUpdate=doUpdate)
    return "MeshROI", params
