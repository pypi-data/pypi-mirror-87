# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component VisualManagerSecondaryPass

.. autofunction:: VisualManagerSecondaryPass

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def VisualManagerSecondaryPass(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, factor=None, renderToScreen=None, outputName=None, input_tags=None, output_tags=None, fragFilename=None, **kwargs):
    """
    VisualManagerSecondaryPass


    :param name: object name  Default value: VisualManagerSecondaryPass

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param factor: set the resolution factor for the output pass. default value:1.0  Default value: 1.0

    :param renderToScreen: if true, this pass will be displayed on screen (only one renderPass in the scene must be defined as renderToScreen)  Default value: 0

    :param outputName: name the output texture  Default value: 

    :param input_tags: list of input passes used as source textures  Default value: []

    :param output_tags: output reference tag (use it if the resulting fbo is used as a source for another secondary pass)  Default value: []

    :param fragFilename: Set the fragment shader filename to load  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, factor=factor, renderToScreen=renderToScreen, outputName=outputName, input_tags=input_tags, output_tags=output_tags, fragFilename=fragFilename)
    return "VisualManagerSecondaryPass", params
