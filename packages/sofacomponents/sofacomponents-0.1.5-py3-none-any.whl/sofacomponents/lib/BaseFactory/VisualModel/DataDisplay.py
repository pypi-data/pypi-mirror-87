# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component DataDisplay

.. autofunction:: DataDisplay

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def DataDisplay(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, position=None, restPosition=None, normal=None, maximalRange=None, pointData=None, triangleData=None, quadData=None, pointTriangleData=None, pointQuadData=None, colorNaN=None, userRange=None, currentMin=None, currentMax=None, shininess=None, **kwargs):
    """
    Rendering of meshes colored by data


    :param name: object name  Default value: DataDisplay

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param position: Vertices coordinates  Default value: []

    :param restPosition: Vertices rest coordinates  Default value: []

    :param normal: Normals of the model  Default value: []

    :param maximalRange: Keep the maximal range through all timesteps  Default value: 1

    :param pointData: Data associated with nodes  Default value: []

    :param triangleData: Data associated with triangles  Default value: []

    :param quadData: Data associated with quads  Default value: []

    :param pointTriangleData: Data associated with nodes per triangle  Default value: []

    :param pointQuadData: Data associated with nodes per quad  Default value: []

    :param colorNaN: Color used for NaN values.(default=[0.0,0.0,0.0,1.0])  Default value: [[0.0, 0.0, 0.0, 1.0]]

    :param userRange: Clamp to this values (if max>min)  Default value: [[1.0, -1.0]]

    :param currentMin: Current min range  Default value: 0.0

    :param currentMax: Current max range  Default value: 0.0

    :param shininess: Shininess for rendering point-based data [0,128].  <0 means no specularity  Default value: -1.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, position=position, restPosition=restPosition, normal=normal, maximalRange=maximalRange, pointData=pointData, triangleData=triangleData, quadData=quadData, pointTriangleData=pointTriangleData, pointQuadData=pointQuadData, colorNaN=colorNaN, userRange=userRange, currentMin=currentMin, currentMax=currentMax, shininess=shininess)
    return "DataDisplay", params
