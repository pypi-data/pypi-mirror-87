# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component NormalsFromPoints

.. autofunction:: NormalsFromPoints

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def NormalsFromPoints(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, position=None, triangles=None, quads=None, normals=None, invertNormals=None, useAngles=None, **kwargs):
    """
    Compute vertex normals by averaging face normals


    :param name: object name  Default value: NormalsFromPoints

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param position: Vertices of the mesh  Default value: []

    :param triangles: Triangles of the mesh  Default value: []

    :param quads: Quads of the mesh  Default value: []

    :param normals: Computed vertex normals of the mesh  Default value: []

    :param invertNormals: Swap normals  Default value: 0

    :param useAngles: Use incident angles to weight faces normal contributions at each vertex  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, position=position, triangles=triangles, quads=quads, normals=normals, invertNormals=invertNormals, useAngles=useAngles)
    return "NormalsFromPoints", params
