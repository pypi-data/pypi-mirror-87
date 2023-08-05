# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SphereQuadTopology

.. autofunction:: SphereQuadTopology

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SphereQuadTopology(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, position=None, edges=None, triangles=None, quads=None, tetrahedra=None, hexahedra=None, uv=None, drawEdges=None, drawTriangles=None, drawQuads=None, drawTetrahedra=None, drawHexahedra=None, nx=None, ny=None, nz=None, internalPoints=None, splitNormals=None, min=None, max=None, center=None, radius=None, **kwargs):
    """
    Sphere topology constructed with deformed quads


    :param name: object name  Default value: SphereQuadTopology

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

    :param nx: x grid resolution  Default value: 0

    :param ny: y grid resolution  Default value: 0

    :param nz: z grid resolution  Default value: 0

    :param internalPoints: include internal points (allow a one-to-one mapping between points from RegularGridTopology and CubeTopology)  Default value: 0

    :param splitNormals: split corner points to have planar normals  Default value: 0

    :param min: Min  Default value: [[0.0, 0.0, 0.0]]

    :param max: Max  Default value: [[1.0, 1.0, 1.0]]

    :param center: Center of the sphere  Default value: [[0.0, 0.0, 0.0]]

    :param radius: Radius of the sphere  Default value: 1.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, position=position, edges=edges, triangles=triangles, quads=quads, tetrahedra=tetrahedra, hexahedra=hexahedra, uv=uv, drawEdges=drawEdges, drawTriangles=drawTriangles, drawQuads=drawQuads, drawTetrahedra=drawTetrahedra, drawHexahedra=drawHexahedra, nx=nx, ny=ny, nz=nz, internalPoints=internalPoints, splitNormals=splitNormals, min=min, max=max, center=center, radius=radius)
    return "SphereQuadTopology", params
