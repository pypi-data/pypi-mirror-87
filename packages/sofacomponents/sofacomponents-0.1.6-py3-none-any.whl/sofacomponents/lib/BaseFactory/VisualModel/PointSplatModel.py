# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PointSplatModel

.. autofunction:: PointSplatModel

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PointSplatModel(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, radius=None, textureSize=None, alpha=None, color=None, pointData=None, **kwargs):
    """
    A simple visualization for a cloud of points.


    :param name: object name  Default value: PointSplatModel

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param radius: Radius of the spheres.  Default value: 1.0

    :param textureSize: Size of the billboard texture.  Default value: 32

    :param alpha: Opacity of the billboards. 1.0 is 100% opaque.  Default value: 1.0

    :param color: Billboard color.(default=[1.0,1.0,1.0,1.0])  Default value: [[1.0, 1.0, 1.0, 1.0]]

    :param pointData: scalar field modulating point colors  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, radius=radius, textureSize=textureSize, alpha=alpha, color=color, pointData=pointData)
    return "PointSplatModel", params
