# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MeshTopology

.. autofunction:: MeshTopology

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MeshTopology(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, position=None, edges=None, triangles=None, quads=None, tetrahedra=None, hexahedra=None, uv=None, drawEdges=None, drawTriangles=None, drawQuads=None, drawTetrahedra=None, drawHexahedra=None, **kwargs):
    """
    Generic mesh topology


    :param name: object name  Default value: MeshTopology

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param filename: Filename of the mesh  Default value: 

    :param position: List of point positions  Default value: []

    :param edges: List of edge indices  Default value: []

    :param triangles: List of triangle indices  Default value: []

    :param quads: List of quad indices  Default value: []

    :param tetrahedra: List of tetrahedron indices  Default value: []

    :param hexahedra: List of hexahedron indices  Default value: []

    :param uv: List of uv coordinates  Default value: []

    :param drawEdges: if true, draw the topology Edges  Default value: 0

    :param drawTriangles: if true, draw the topology Triangles  Default value: 0

    :param drawQuads: if true, draw the topology Quads  Default value: 0

    :param drawTetrahedra: if true, draw the topology Tetrahedra  Default value: 0

    :param drawHexahedra: if true, draw the topology hexahedra  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, position=position, edges=edges, triangles=triangles, quads=quads, tetrahedra=tetrahedra, hexahedra=hexahedra, uv=uv, drawEdges=drawEdges, drawTriangles=drawTriangles, drawQuads=drawQuads, drawTetrahedra=drawTetrahedra, drawHexahedra=drawHexahedra)
    return "MeshTopology", params
