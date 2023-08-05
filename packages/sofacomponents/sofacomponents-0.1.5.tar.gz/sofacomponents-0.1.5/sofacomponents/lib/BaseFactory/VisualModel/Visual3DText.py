# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component Visual3DText

.. autofunction:: Visual3DText

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def Visual3DText(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, text=None, position=None, scale=None, color=None, depthTest=None, **kwargs):
    """
    Display 3D camera-oriented text


    :param name: object name  Default value: Visual3DText

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param text: Test to display  Default value: 

    :param position: 3d position  Default value: [[0.0, 0.0, 0.0]]

    :param scale: text scale  Default value: 1.0

    :param color: text color. (default=[1.0,1.0,1.0,1.0])  Default value: [[1.0, 1.0, 1.0, 1.0]]

    :param depthTest: perform depth test  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, text=text, position=position, scale=scale, color=color, depthTest=depthTest)
    return "Visual3DText", params
