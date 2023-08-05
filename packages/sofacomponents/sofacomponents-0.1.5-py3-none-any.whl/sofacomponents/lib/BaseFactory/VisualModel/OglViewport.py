# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component OglViewport

.. autofunction:: OglViewport

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def OglViewport(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, screenPosition=None, screenSize=None, cameraPosition=None, cameraOrientation=None, cameraRigid=None, zNear=None, zFar=None, fovy=None, enabled=None, advancedRendering=None, useFBO=None, swapMainView=None, drawCamera=None, **kwargs):
    """
    OglViewport


    :param name: object name  Default value: OglViewport

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param screenPosition: Viewport position  Default value: [[0, 0]]

    :param screenSize: Viewport size  Default value: [[0, 0]]

    :param cameraPosition: Camera's position in eye's space  Default value: [[0.0, 0.0, 0.0]]

    :param cameraOrientation: Camera's orientation  Default value: [[0.0, 0.0, 0.0, 1.0]]

    :param cameraRigid: Camera's rigid coord  Default value: [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

    :param zNear: Camera's ZNear  Default value: 0.0

    :param zFar: Camera's ZFar  Default value: 0.0

    :param fovy: Field of View (Y axis)  Default value: 60.0

    :param enabled: Enable visibility of the viewport  Default value: 1

    :param advancedRendering: If true, viewport will be hidden if advancedRendering visual flag is not enabled  Default value: 0

    :param useFBO: Use a FBO to render the viewport  Default value: 1

    :param swapMainView: Swap this viewport with the main view  Default value: 0

    :param drawCamera: Draw a frame representing the camera (see it in main viewport)  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, screenPosition=screenPosition, screenSize=screenSize, cameraPosition=cameraPosition, cameraOrientation=cameraOrientation, cameraRigid=cameraRigid, zNear=zNear, zFar=zFar, fovy=fovy, enabled=enabled, advancedRendering=advancedRendering, useFBO=useFBO, swapMainView=swapMainView, drawCamera=drawCamera)
    return "OglViewport", params
