# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component Vertex2Frame

.. autofunction:: Vertex2Frame

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def Vertex2Frame(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, position=None, texCoords=None, normals=None, frames=None, useNormals=None, invertNormals=None, rotation=None, rotationAngle=None, **kwargs):
    """
    

    :param name: object name  Default value: Vertex2Frame

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param position: Vertices of the mesh loaded  Default value: []

    :param texCoords: TexCoords of the mesh loaded  Default value: []

    :param normals: Normals of the mesh loaded  Default value: []

    :param frames: Frames at output  Default value: []

    :param useNormals: Use normals to compute the orientations; if disabled the direction of the x axisof a vertice is the one from this vertice to the next one  Default value: 1

    :param invertNormals: Swap normals  Default value: 0

    :param rotation: Apply a local rotation on the frames. If 0 a x-axis rotation is applied. If 1 a y-axis rotation is applied, If 2 a z-axis rotation is applied.  Default value: 0

    :param rotationAngle: Angle rotation  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, position=position, texCoords=texCoords, normals=normals, frames=frames, useNormals=useNormals, invertNormals=invertNormals, rotation=rotation, rotationAngle=rotationAngle)
    return "Vertex2Frame", params
