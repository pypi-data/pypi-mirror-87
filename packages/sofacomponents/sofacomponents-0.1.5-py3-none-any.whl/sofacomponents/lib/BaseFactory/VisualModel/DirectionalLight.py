# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component DirectionalLight

.. autofunction:: DirectionalLight

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def DirectionalLight(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, color=None, shadowTextureSize=None, drawSource=None, zNear=None, zFar=None, shadowsEnabled=None, softShadows=None, shadowFactor=None, VSMLightBleeding=None, VSMMinVariance=None, textureUnit=None, modelViewMatrix=None, projectionMatrix=None, direction=None, **kwargs):
    """
    A directional light illuminating the scene with parallel rays of light (can cast shadows).


    :param name: object name  Default value: DirectionalLight

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param color: Set the color of the light. (default=[1.0,1.0,1.0,1.0])  Default value: [[1.0, 1.0, 1.0, 1.0]]

    :param shadowTextureSize: [Shadowing] Set size for shadow texture   Default value: 0

    :param drawSource: Draw Light Source  Default value: 0

    :param zNear: [Shadowing] Light's ZNear  Default value: 0.0

    :param zFar: [Shadowing] Light's ZFar  Default value: 0.0

    :param shadowsEnabled: [Shadowing] Enable Shadow from this light  Default value: 1

    :param softShadows: [Shadowing] Turn on Soft Shadow from this light  Default value: 0

    :param shadowFactor: [Shadowing] Shadow Factor (decrease/increase darkness)  Default value: 1.0

    :param VSMLightBleeding: [Shadowing] (VSM only) Light bleeding paramter  Default value: 0.0500000007451

    :param VSMMinVariance: [Shadowing] (VSM only) Minimum variance parameter  Default value: 0.0010000000475

    :param textureUnit: [Shadowing] Texture unit for the genereated shadow texture  Default value: 1

    :param modelViewMatrix: [Shadowing] ModelView Matrix  Default value: [[0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0]]

    :param projectionMatrix: [Shadowing] Projection Matrix  Default value: [[0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0]]

    :param direction: Set the direction of the light  Default value: [[0.0, 0.0, -1.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, color=color, shadowTextureSize=shadowTextureSize, drawSource=drawSource, zNear=zNear, zFar=zFar, shadowsEnabled=shadowsEnabled, softShadows=softShadows, shadowFactor=shadowFactor, VSMLightBleeding=VSMLightBleeding, VSMMinVariance=VSMMinVariance, textureUnit=textureUnit, modelViewMatrix=modelViewMatrix, projectionMatrix=projectionMatrix, direction=direction)
    return "DirectionalLight", params
