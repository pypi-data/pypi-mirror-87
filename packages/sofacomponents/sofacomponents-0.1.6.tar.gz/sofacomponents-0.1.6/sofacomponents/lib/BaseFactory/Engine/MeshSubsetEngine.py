# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MeshSubsetEngine

.. autofunction:: MeshSubsetEngine

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MeshSubsetEngine(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, inputPosition=None, inputEdges=None, inputTriangles=None, inputQuads=None, indices=None, position=None, edges=None, triangles=None, quads=None, **kwargs):
    """
    Extract a mesh subset based on selected vertices


    :param name: object name  Default value: MeshSubsetEngine

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param inputPosition: input vertices  Default value: []

    :param inputEdges: input edges  Default value: []

    :param inputTriangles: input triangles  Default value: []

    :param inputQuads: input quads  Default value: []

    :param indices: Index lists of the selected vertices  Default value: []

    :param position: Vertices of mesh subset  Default value: []

    :param edges: edges of mesh subset  Default value: []

    :param triangles: Triangles of mesh subset  Default value: []

    :param quads: Quads of mesh subset  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, inputPosition=inputPosition, inputEdges=inputEdges, inputTriangles=inputTriangles, inputQuads=inputQuads, indices=indices, position=position, edges=edges, triangles=triangles, quads=quads)
    return "MeshSubsetEngine", params
