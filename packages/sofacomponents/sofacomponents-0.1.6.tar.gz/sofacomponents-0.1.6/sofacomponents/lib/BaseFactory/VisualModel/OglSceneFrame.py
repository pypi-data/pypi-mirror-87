# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component OglSceneFrame

.. autofunction:: OglSceneFrame

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def OglSceneFrame(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, draw=None, style=None, alignment=None, **kwargs):
    """
    Display a frame at the corner of the scene view


    :param name: object name  Default value: OglSceneFrame

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param draw: Display the frame or not  Default value: 1

    :param style: Style of the frame  Default value: Cylinders

    :param alignment: Alignment of the frame in the view  Default value: BottomRight


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, draw=draw, style=style, alignment=alignment)
    return "OglSceneFrame", params
