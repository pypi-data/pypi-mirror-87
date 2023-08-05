# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component OglLabel

.. autofunction:: OglLabel

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def OglLabel(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, prefix=None, label=None, suffix=None, x=None, y=None, fontsize=None, color=None, selectContrastingColor=None, updateLabelEveryNbSteps=None, visible=None, **kwargs):
    """
    Display 2D text in the viewport.


    :param name: object name  Default value: OglLabel

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param prefix: The prefix of the text to display  Default value: 

    :param label: The text to display  Default value: 

    :param suffix: The suffix of the text to display  Default value: 

    :param x: The x position of the text on the screen  Default value: 10

    :param y: The y position of the text on the screen  Default value: 10

    :param fontsize: The size of the font used to display the text on the screen  Default value: 14

    :param color: The color of the text to display. (default='gray')  Default value: [[0.5, 0.5, 0.5, 1.0]]

    :param selectContrastingColor: Overide the color value but one that contrast with the background color  Default value: 0

    :param updateLabelEveryNbSteps: Update the display of the label every nb of time steps  Default value: 0

    :param visible: Is label displayed  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, prefix=prefix, label=label, suffix=suffix, x=x, y=y, fontsize=fontsize, color=color, selectContrastingColor=selectContrastingColor, updateLabelEveryNbSteps=updateLabelEveryNbSteps, visible=visible)
    return "OglLabel", params
