# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component GridTopology

.. autofunction:: GridTopology

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def GridTopology(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, position=None, edges=None, triangles=None, quads=None, tetrahedra=None, hexahedra=None, uv=None, drawEdges=None, drawTriangles=None, drawQuads=None, drawTetrahedra=None, drawHexahedra=None, n=None, computeHexaList=None, computeQuadList=None, computeTriangleList=None, computeEdgeList=None, computePointList=None, createTexCoords=None, **kwargs):
    """
    Base class fo a regular grid in 3D


    :param name: object name  Default value: GridTopology

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param filename: Filename of the mesh  Default value: 

    :param position: List of point positions  Default value: []

    :param edges: List of edge indices  Default value: [[1, 3], [3, 0], [0, 1], [3, 2], [2, 0], [5, 7], [7, 4], [4, 5], [7, 6], [6, 4], [1, 5], [5, 0], [4, 0], [3, 7], [7, 2], [6, 2], [6, 0], [7, 1]]

    :param triangles: List of triangle indices  Default value: [[0, 1, 3], [0, 3, 2], [4, 5, 7], [4, 7, 6], [0, 1, 5], [0, 5, 4], [2, 3, 7], [2, 7, 6], [0, 2, 6], [0, 6, 4], [1, 3, 7], [1, 7, 5]]

    :param quads: List of quad indices  Default value: [[0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4], [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5]]

    :param tetrahedra: List of tetrahedron indices  Default value: []

    :param hexahedra: List of hexahedron indices  Default value: [[0, 1, 3, 2, 4, 5, 7, 6]]

    :param uv: List of uv coordinates  Default value: []

    :param drawEdges: if true, draw the topology Edges  Default value: 0

    :param drawTriangles: if true, draw the topology Triangles  Default value: 0

    :param drawQuads: if true, draw the topology Quads  Default value: 0

    :param drawTetrahedra: if true, draw the topology Tetrahedra  Default value: 0

    :param drawHexahedra: if true, draw the topology hexahedra  Default value: 0

    :param n: grid resolution. (default = 2 2 2)  Default value: [[2, 2, 2]]

    :param computeHexaList: put true if the list of Hexahedra is needed during init (default=true)  Default value: 1

    :param computeQuadList: put true if the list of Quad is needed during init (default=true)  Default value: 1

    :param computeTriangleList: put true if the list of triangle is needed during init (default=true)  Default value: 1

    :param computeEdgeList: put true if the list of Lines is needed during init (default=true)  Default value: 1

    :param computePointList: put true if the list of Points is needed during init (default=true)  Default value: 1

    :param createTexCoords: If set to true, virtual texture coordinates will be generated using 3D interpolation (default=false).  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, position=position, edges=edges, triangles=triangles, quads=quads, tetrahedra=tetrahedra, hexahedra=hexahedra, uv=uv, drawEdges=drawEdges, drawTriangles=drawTriangles, drawQuads=drawQuads, drawTetrahedra=drawTetrahedra, drawHexahedra=drawHexahedra, n=n, computeHexaList=computeHexaList, computeQuadList=computeQuadList, computeTriangleList=computeTriangleList, computeEdgeList=computeEdgeList, computePointList=computePointList, createTexCoords=createTexCoords)
    return "GridTopology", params
