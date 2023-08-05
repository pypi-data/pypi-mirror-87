# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component RecordedCamera

.. autofunction:: RecordedCamera

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def RecordedCamera(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, position=None, orientation=None, lookAt=None, distance=None, fieldOfView=None, zNear=None, zFar=None, computeZClip=None, minBBox=None, maxBBox=None, widthViewport=None, heightViewport=None, projectionType=None, activated=None, fixedLookAt=None, modelViewMatrix=None, projectionMatrix=None, zoomSpeed=None, panSpeed=None, pivot=None, startTime=None, endTime=None, rotationMode=None, translationMode=None, navigationMode=None, rotationSpeed=None, rotationCenter=None, rotationStartPoint=None, rotationLookAt=None, rotationAxis=None, cameraUp=None, drawRotation=None, drawTranslation=None, cameraPositions=None, cameraOrientations=None, **kwargs):
    """
    A camera that is moving along a predetermined path.


    :param name: object name  Default value: RecordedCamera

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param position: Camera's position  Default value: [[0.0, 0.0, 0.0]]

    :param orientation: Camera's orientation  Default value: [[0.0, 0.0, 0.0, 1.0]]

    :param lookAt: Camera's look at  Default value: [[0.0, 0.0, 0.0]]

    :param distance: Distance between camera and look at  Default value: 0.0

    :param fieldOfView: Camera's FOV  Default value: 45.0

    :param zNear: Camera's zNear  Default value: 0.01

    :param zFar: Camera's zFar  Default value: 100.0

    :param computeZClip: Compute Z clip planes (Near and Far) according to the bounding box  Default value: 1

    :param minBBox: minBBox  Default value: [[0.0, 0.0, 0.0]]

    :param maxBBox: maxBBox  Default value: [[1.0, 1.0, 1.0]]

    :param widthViewport: widthViewport  Default value: 800

    :param heightViewport: heightViewport  Default value: 600

    :param projectionType: Camera Type (0 = Perspective, 1 = Orthographic)  Default value: Perspective

    :param activated: Camera activated ?  Default value: 1

    :param fixedLookAt: keep the lookAt point always fixed  Default value: 0

    :param modelViewMatrix: ModelView Matrix  Default value: [[0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0]]

    :param projectionMatrix: Projection Matrix  Default value: [[0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0]]

    :param zoomSpeed: Zoom Speed  Default value: 250.0

    :param panSpeed: Pan Speed  Default value: 0.1

    :param pivot: Pivot (0 => Scene center, 1 => World Center  Default value: 0

    :param startTime: Time when the camera moves will start  Default value: 0.0

    :param endTime: Time when the camera moves will end (or loop)  Default value: 200.0

    :param rotationMode: If true, rotation will be performed  Default value: 0

    :param translationMode: If true, translation will be performed  Default value: 0

    :param navigationMode: If true, navigation will be performed  Default value: 0

    :param rotationSpeed: rotation Speed  Default value: 0.1

    :param rotationCenter: Rotation center coordinates  Default value: [[0.0, 0.0, 0.0]]

    :param rotationStartPoint: Rotation start position coordinates  Default value: [[0.0, 0.0, 0.0]]

    :param rotationLookAt: Position to be focused during rotation  Default value: [[0.0, 0.0, 0.0]]

    :param rotationAxis: Rotation axis  Default value: [[0.0, 1.0, 0.0]]

    :param cameraUp: Camera Up axis  Default value: [[0.0, 0.0, 0.0]]

    :param drawRotation: If true, will draw the rotation path  Default value: 0

    :param drawTranslation: If true, will draw the translation path  Default value: 0

    :param cameraPositions: Intermediate camera's positions  Default value: []

    :param cameraOrientations: Intermediate camera's orientations  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, position=position, orientation=orientation, lookAt=lookAt, distance=distance, fieldOfView=fieldOfView, zNear=zNear, zFar=zFar, computeZClip=computeZClip, minBBox=minBBox, maxBBox=maxBBox, widthViewport=widthViewport, heightViewport=heightViewport, projectionType=projectionType, activated=activated, fixedLookAt=fixedLookAt, modelViewMatrix=modelViewMatrix, projectionMatrix=projectionMatrix, zoomSpeed=zoomSpeed, panSpeed=panSpeed, pivot=pivot, startTime=startTime, endTime=endTime, rotationMode=rotationMode, translationMode=translationMode, navigationMode=navigationMode, rotationSpeed=rotationSpeed, rotationCenter=rotationCenter, rotationStartPoint=rotationStartPoint, rotationLookAt=rotationLookAt, rotationAxis=rotationAxis, cameraUp=cameraUp, drawRotation=drawRotation, drawTranslation=drawTranslation, cameraPositions=cameraPositions, cameraOrientations=cameraOrientations)
    return "RecordedCamera", params
