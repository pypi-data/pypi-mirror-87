# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MeshSplittingEngine

.. autofunction:: MeshSplittingEngine

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MeshSplittingEngine(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, position=None, edges=None, triangles=None, quads=None, tetrahedra=None, hexahedra=None, nbInputs=None, indexPairs=None, position1=None, **kwargs):
    """
    This class breaks a mesh in multiple parts, based on selected vertices or cells.


    :param name: object name  Default value: MeshSplittingEngine

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param position: input vertices  Default value: []

    :param edges: input edges  Default value: []

    :param triangles: input triangles  Default value: []

    :param quads: input quads  Default value: []

    :param tetrahedra: input tetrahedra  Default value: []

    :param hexahedra: input hexahedra  Default value: []

    :param nbInputs: Number of input vectors  Default value: 0

    :param indexPairs: couples for input vertices: ROI index + index in the ROI  Default value: []

    :param position1: output vertices(1)  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, position=position, edges=edges, triangles=triangles, quads=quads, tetrahedra=tetrahedra, hexahedra=hexahedra, nbInputs=nbInputs, indexPairs=indexPairs, position1=position1)
    return "MeshSplittingEngine", params
