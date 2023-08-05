# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MeshTrianLoader

.. autofunction:: MeshTrianLoader

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MeshTrianLoader(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, position=None, polylines=None, edges=None, triangles=None, quads=None, polygons=None, highOrderEdgePositions=None, highOrderTrianglePositions=None, highOrderQuadPositions=None, tetrahedra=None, hexahedra=None, pentahedra=None, highOrderTetrahedronPositions=None, highOrderHexahedronPositions=None, pyramids=None, normals=None, edgesGroups=None, trianglesGroups=None, quadsGroups=None, polygonsGroups=None, tetrahedraGroups=None, hexahedraGroups=None, pentahedraGroups=None, pyramidsGroups=None, flipNormals=None, triangulate=None, createSubelements=None, onlyAttachedPoints=None, translation=None, rotation=None, scale3d=None, transformation=None, trian2=None, neighborTable=None, edgesOnBorder=None, trianglesOnBorderList=None, **kwargs):
    """
    Specific mesh loader for trian (only triangulations) file format.


    :param name: object name  Default value: MeshTrianLoader

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Invalid

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param filename: Filename of the object  Default value: 

    :param position: Vertices of the mesh loaded  Default value: []

    :param polylines: Polylines of the mesh loaded  Default value: []

    :param edges: Edges of the mesh loaded  Default value: []

    :param triangles: Triangles of the mesh loaded  Default value: []

    :param quads: Quads of the mesh loaded  Default value: []

    :param polygons: Polygons of the mesh loaded  Default value: []

    :param highOrderEdgePositions: High order edge points of the mesh loaded  Default value: []

    :param highOrderTrianglePositions: High order triangle points of the mesh loaded  Default value: []

    :param highOrderQuadPositions: High order quad points of the mesh loaded  Default value: []

    :param tetrahedra: Tetrahedra of the mesh loaded  Default value: []

    :param hexahedra: Hexahedra of the mesh loaded  Default value: []

    :param pentahedra: Pentahedra of the mesh loaded  Default value: []

    :param highOrderTetrahedronPositions: High order tetrahedron points of the mesh loaded  Default value: []

    :param highOrderHexahedronPositions: High order hexahedron points of the mesh loaded  Default value: []

    :param pyramids: Pyramids of the mesh loaded  Default value: []

    :param normals: Normals of the mesh loaded  Default value: []

    :param edgesGroups: Groups of Edges  Default value: 

    :param trianglesGroups: Groups of Triangles  Default value: 

    :param quadsGroups: Groups of Quads  Default value: 

    :param polygonsGroups: Groups of Polygons  Default value: 

    :param tetrahedraGroups: Groups of Tetrahedra  Default value: 

    :param hexahedraGroups: Groups of Hexahedra  Default value: 

    :param pentahedraGroups: Groups of Pentahedra  Default value: 

    :param pyramidsGroups: Groups of Pyramids  Default value: 

    :param flipNormals: Flip Normals  Default value: 0

    :param triangulate: Divide all polygons into triangles  Default value: 0

    :param createSubelements: Divide all n-D elements into their (n-1)-D boundary elements (e.g. tetrahedra to triangles)  Default value: 0

    :param onlyAttachedPoints: Only keep points attached to elements of the mesh  Default value: 0

    :param translation: Translation of the DOFs  Default value: [[0.0, 0.0, 0.0]]

    :param rotation: Rotation of the DOFs  Default value: [[0.0, 0.0, 0.0]]

    :param scale3d: Scale of the DOFs in 3 dimensions  Default value: [[1.0, 1.0, 1.0]]

    :param transformation: 4x4 Homogeneous matrix to transform the DOFs (when present replace any)  Default value: [[1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

    :param trian2: Set to true if the mesh is a trian2 format.  Default value: 0

    :param neighborTable: Table of neighborhood triangle indices for each triangle.  Default value: []

    :param edgesOnBorder: List of edges which are on the border of the mesh loaded.  Default value: []

    :param trianglesOnBorderList: List of triangle indices which are on the border of the mesh loaded.  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, position=position, polylines=polylines, edges=edges, triangles=triangles, quads=quads, polygons=polygons, highOrderEdgePositions=highOrderEdgePositions, highOrderTrianglePositions=highOrderTrianglePositions, highOrderQuadPositions=highOrderQuadPositions, tetrahedra=tetrahedra, hexahedra=hexahedra, pentahedra=pentahedra, highOrderTetrahedronPositions=highOrderTetrahedronPositions, highOrderHexahedronPositions=highOrderHexahedronPositions, pyramids=pyramids, normals=normals, edgesGroups=edgesGroups, trianglesGroups=trianglesGroups, quadsGroups=quadsGroups, polygonsGroups=polygonsGroups, tetrahedraGroups=tetrahedraGroups, hexahedraGroups=hexahedraGroups, pentahedraGroups=pentahedraGroups, pyramidsGroups=pyramidsGroups, flipNormals=flipNormals, triangulate=triangulate, createSubelements=createSubelements, onlyAttachedPoints=onlyAttachedPoints, translation=translation, rotation=rotation, scale3d=scale3d, transformation=transformation, trian2=trian2, neighborTable=neighborTable, edgesOnBorder=edgesOnBorder, trianglesOnBorderList=trianglesOnBorderList)
    return "MeshTrianLoader", params
