# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component OglColorMap

.. autofunction:: OglColorMap

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def OglColorMap(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, paletteSize=None, colorScheme=None, showLegend=None, legendOffset=None, legendTitle=None, min=None, max=None, legendRangeScale=None, **kwargs):
    """
    Provides color palette and support for conversion of numbers to colors.


    :param name: object name  Default value: OglColorMap

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param paletteSize: How many colors to use  Default value: 256

    :param colorScheme: Color scheme to use  Default value: HSV

    :param showLegend: Activate rendering of color scale legend on the side  Default value: 0

    :param legendOffset: Draw the legend on screen with an x,y offset  Default value: [[10.0, 5.0]]

    :param legendTitle: Add a title to the legend  Default value: 

    :param min: min value for drawing the legend without the need to actually use the range with getEvaluator method wich sets the min  Default value: 0.0

    :param max: max value for drawing the legend without the need to actually use the range with getEvaluator method wich sets the max  Default value: 0.0

    :param legendRangeScale: to change the unit of the min/max value of the legend  Default value: 1.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, paletteSize=paletteSize, colorScheme=colorScheme, showLegend=showLegend, legendOffset=legendOffset, legendTitle=legendTitle, min=min, max=max, legendRangeScale=legendRangeScale)
    return "OglColorMap", params
