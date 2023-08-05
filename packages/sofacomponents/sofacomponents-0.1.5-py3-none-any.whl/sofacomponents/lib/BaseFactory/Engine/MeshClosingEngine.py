# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MeshClosingEngine

.. autofunction:: MeshClosingEngine

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MeshClosingEngine(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, inputPosition=None, inputTriangles=None, inputQuads=None, position=None, triangles=None, quads=None, indices=None, closingPosition=None, closingTriangles=None, **kwargs):
    """
    Merge several meshes


    :param name: object name  Default value: MeshClosingEngine

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param inputPosition: input vertices  Default value: []

    :param inputTriangles: input triangles  Default value: []

    :param inputQuads: input quads  Default value: []

    :param position: Vertices of closed mesh  Default value: []

    :param triangles: Triangles of closed mesh  Default value: []

    :param quads: Quads of closed mesh (=input quads with current method)  Default value: []

    :param indices: Index lists of the closing parts  Default value: 

    :param closingPosition: Vertices of the closing parts  Default value: []

    :param closingTriangles: Triangles of the closing parts  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, inputPosition=inputPosition, inputTriangles=inputTriangles, inputQuads=inputQuads, position=position, triangles=triangles, quads=quads, indices=indices, closingPosition=closingPosition, closingTriangles=closingTriangles)
    return "MeshClosingEngine", params
