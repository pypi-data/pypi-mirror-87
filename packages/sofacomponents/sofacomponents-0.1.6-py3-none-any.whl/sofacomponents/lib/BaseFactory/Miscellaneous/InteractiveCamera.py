# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component InteractiveCamera

.. autofunction:: InteractiveCamera

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def InteractiveCamera(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, position=None, orientation=None, lookAt=None, distance=None, fieldOfView=None, zNear=None, zFar=None, computeZClip=None, minBBox=None, maxBBox=None, widthViewport=None, heightViewport=None, projectionType=None, activated=None, fixedLookAt=None, modelViewMatrix=None, projectionMatrix=None, zoomSpeed=None, panSpeed=None, pivot=None, **kwargs):
    """
    InteractiveCamera


    :param name: object name  Default value: InteractiveCamera

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

    :param pivot: Pivot (0 => Camera lookAt, 1 => Camera position, 2 => Scene center, 3 => World center  Default value: 2


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, position=position, orientation=orientation, lookAt=lookAt, distance=distance, fieldOfView=fieldOfView, zNear=zNear, zFar=zFar, computeZClip=computeZClip, minBBox=minBBox, maxBBox=maxBBox, widthViewport=widthViewport, heightViewport=heightViewport, projectionType=projectionType, activated=activated, fixedLookAt=fixedLookAt, modelViewMatrix=modelViewMatrix, projectionMatrix=projectionMatrix, zoomSpeed=zoomSpeed, panSpeed=panSpeed, pivot=pivot)
    return "InteractiveCamera", params
