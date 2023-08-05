# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MergeMeshes

.. autofunction:: MergeMeshes

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MergeMeshes(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, nbMeshes=None, npoints=None, position=None, edges=None, triangles=None, quads=None, polygons=None, tetrahedra=None, hexahedra=None, position1=None, position2=None, edges1=None, edges2=None, triangles1=None, triangles2=None, quads1=None, quads2=None, tetrahedra1=None, tetrahedra2=None, hexahedra1=None, hexahedra2=None, **kwargs):
    """
    Merge several meshes


    :param name: object name  Default value: MergeMeshes

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param nbMeshes: number of meshes to merge  Default value: 2

    :param npoints: Number Of out points  Default value: 0

    :param position: Output Vertices of the merged mesh  Default value: []

    :param edges: Output Edges of the merged mesh  Default value: []

    :param triangles: Output Triangles of the merged mesh  Default value: []

    :param quads: Output Quads of the merged mesh  Default value: []

    :param polygons: Output Polygons of the merged mesh  Default value: []

    :param tetrahedra: Output Tetrahedra of the merged mesh  Default value: []

    :param hexahedra: Output Hexahedra of the merged mesh  Default value: []

    :param position1: input positions for mesh 1  Default value: []

    :param position2: input positions for mesh 2  Default value: []

    :param edges1: input edges for mesh 1  Default value: []

    :param edges2: input edges for mesh 2  Default value: []

    :param triangles1: input triangles for mesh 1  Default value: []

    :param triangles2: input triangles for mesh 2  Default value: []

    :param quads1: input quads for mesh 1  Default value: []

    :param quads2: input quads for mesh 2  Default value: []

    :param tetrahedra1: input tetrahedra for mesh 1  Default value: []

    :param tetrahedra2: input tetrahedra for mesh 2  Default value: []

    :param hexahedra1: input hexahedra for mesh 1  Default value: []

    :param hexahedra2: input hexahedra for mesh 2  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, nbMeshes=nbMeshes, npoints=npoints, position=position, edges=edges, triangles=triangles, quads=quads, polygons=polygons, tetrahedra=tetrahedra, hexahedra=hexahedra, position1=position1, position2=position2, edges1=edges1, edges2=edges2, triangles1=triangles1, triangles2=triangles2, quads1=quads1, quads2=quads2, tetrahedra1=tetrahedra1, tetrahedra2=tetrahedra2, hexahedra1=hexahedra1, hexahedra2=hexahedra2)
    return "MergeMeshes", params
