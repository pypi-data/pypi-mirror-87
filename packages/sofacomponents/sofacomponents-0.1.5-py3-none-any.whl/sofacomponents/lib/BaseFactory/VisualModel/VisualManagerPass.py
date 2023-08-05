# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component VisualManagerPass

.. autofunction:: VisualManagerPass

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def VisualManagerPass(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, factor=None, renderToScreen=None, outputName=None, **kwargs):
    """
    VisualManagerPass


    :param name: object name  Default value: VisualManagerPass

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param factor: set the resolution factor for the output pass. default value:1.0  Default value: 1.0

    :param renderToScreen: if true, this pass will be displayed on screen (only one renderPass in the scene must be defined as renderToScreen)  Default value: 0

    :param outputName: name the output texture  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, factor=factor, renderToScreen=renderToScreen, outputName=outputName)
    return "VisualManagerPass", params
