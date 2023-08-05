# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component LightManager

.. autofunction:: LightManager

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def LightManager(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, shadows=None, softShadows=None, ambient=None, debugDraw=None, **kwargs):
    """
    Manage a set of lights that can cast hard and soft shadows.Soft Shadows is done using Variance Shadow Mapping (http://developer.download.nvidia.com/SDK/10.5/direct3d/Source/VarianceShadowMapping/Doc/VarianceShadowMapping.pdf)


    :param name: object name  Default value: LightManager

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param shadows: Enable Shadow in the scene. (default=0)  Default value: 0

    :param softShadows: If Shadows enabled, Enable Variance Soft Shadow in the scene. (default=0)  Default value: 0

    :param ambient: Ambient lights contribution (Vec4f)(default=[0.0f,0.0f,0.0f,0.0f])  Default value: [[0.0, 0.0, 0.0, 1.0]]

    :param debugDraw: enable/disable drawing of lights shadow textures. (default=false)  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, shadows=shadows, softShadows=softShadows, ambient=ambient, debugDraw=debugDraw)
    return "LightManager", params
