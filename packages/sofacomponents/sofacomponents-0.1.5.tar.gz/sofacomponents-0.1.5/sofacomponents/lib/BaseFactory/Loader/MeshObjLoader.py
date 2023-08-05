# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MeshObjLoader

.. autofunction:: MeshObjLoader

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MeshObjLoader(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, position=None, polylines=None, edges=None, triangles=None, quads=None, polygons=None, highOrderEdgePositions=None, highOrderTrianglePositions=None, highOrderQuadPositions=None, tetrahedra=None, hexahedra=None, pentahedra=None, highOrderTetrahedronPositions=None, highOrderHexahedronPositions=None, pyramids=None, normals=None, edgesGroups=None, trianglesGroups=None, quadsGroups=None, polygonsGroups=None, tetrahedraGroups=None, hexahedraGroups=None, pentahedraGroups=None, pyramidsGroups=None, flipNormals=None, triangulate=None, createSubelements=None, onlyAttachedPoints=None, translation=None, rotation=None, scale3d=None, transformation=None, handleSeams=None, loadMaterial=None, defaultMaterial=None, materials=None, faceList=None, texcoordsIndex=None, positionsDefinition=None, texcoordsDefinition=None, normalsIndex=None, normalsDefinition=None, texcoords=None, computeMaterialFaces=None, vertPosIdx=None, vertNormIdx=None, **kwargs):
    """
    Specific mesh loader for Obj file format.


    :param name: object name  Default value: MeshObjLoader

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

    :param handleSeams: Preserve UV and normal seams information (vertices with multiple UV and/or normals)  Default value: 0

    :param loadMaterial: Load the related MTL file or use a default one?  Default value: 1

    :param defaultMaterial: Default material  Default value: Default Diffuse 1 0.75 0.75 0.75 1 Ambient 1 0.2 0.2 0.2 1 Specular 0 1 1 1 1 Emissive 0 0 0 0 0 Shininess 0 45 

    :param materials: List of materials  Default value: 

    :param faceList: List of face definitions.  Default value: []

    :param texcoordsIndex: Indices of textures coordinates used in faces definition.  Default value: []

    :param positionsDefinition: Vertex positions definition  Default value: []

    :param texcoordsDefinition: Texture coordinates definition  Default value: []

    :param normalsIndex: List of normals of elements of the mesh loaded.  Default value: []

    :param normalsDefinition: Normals definition  Default value: []

    :param texcoords: Texture coordinates of all faces, to be used as the parent data of a VisualModel texcoords data  Default value: []

    :param computeMaterialFaces: True to activate export of Data instances containing list of face indices for each material  Default value: 0

    :param vertPosIdx: If vertices have multiple normals/texcoords stores vertices position indices  Default value: []

    :param vertNormIdx: If vertices have multiple normals/texcoords stores vertices normal indices  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, position=position, polylines=polylines, edges=edges, triangles=triangles, quads=quads, polygons=polygons, highOrderEdgePositions=highOrderEdgePositions, highOrderTrianglePositions=highOrderTrianglePositions, highOrderQuadPositions=highOrderQuadPositions, tetrahedra=tetrahedra, hexahedra=hexahedra, pentahedra=pentahedra, highOrderTetrahedronPositions=highOrderTetrahedronPositions, highOrderHexahedronPositions=highOrderHexahedronPositions, pyramids=pyramids, normals=normals, edgesGroups=edgesGroups, trianglesGroups=trianglesGroups, quadsGroups=quadsGroups, polygonsGroups=polygonsGroups, tetrahedraGroups=tetrahedraGroups, hexahedraGroups=hexahedraGroups, pentahedraGroups=pentahedraGroups, pyramidsGroups=pyramidsGroups, flipNormals=flipNormals, triangulate=triangulate, createSubelements=createSubelements, onlyAttachedPoints=onlyAttachedPoints, translation=translation, rotation=rotation, scale3d=scale3d, transformation=transformation, handleSeams=handleSeams, loadMaterial=loadMaterial, defaultMaterial=defaultMaterial, materials=materials, faceList=faceList, texcoordsIndex=texcoordsIndex, positionsDefinition=positionsDefinition, texcoordsDefinition=texcoordsDefinition, normalsIndex=normalsIndex, normalsDefinition=normalsDefinition, texcoords=texcoords, computeMaterialFaces=computeMaterialFaces, vertPosIdx=vertPosIdx, vertNormIdx=vertNormIdx)
    return "MeshObjLoader", params
