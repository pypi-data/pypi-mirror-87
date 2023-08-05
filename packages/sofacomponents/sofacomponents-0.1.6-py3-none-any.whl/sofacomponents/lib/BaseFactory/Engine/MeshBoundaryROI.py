# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MeshBoundaryROI

.. autofunction:: MeshBoundaryROI

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MeshBoundaryROI(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, triangles=None, quads=None, inputROI=None, indices=None, **kwargs):
    """
    Outputs indices of boundary vertices of a triangle/quad mesh


    :param name: object name  Default value: MeshBoundaryROI

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param triangles: input triangles  Default value: []

    :param quads: input quads  Default value: []

    :param inputROI: optional subset of the input mesh  Default value: []

    :param indices: Index lists of the closing vertices  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, triangles=triangles, quads=quads, inputROI=inputROI, indices=indices)
    return "MeshBoundaryROI", params
