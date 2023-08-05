# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component EvalPointsDistance

.. autofunction:: EvalPointsDistance

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def EvalPointsDistance(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, draw=None, isToPrint=None, filename=None, period=None, distance=None, distMean=None, distMin=None, distMax=None, distDev=None, rdistMean=None, rdistMin=None, rdistMax=None, rdistDev=None, **kwargs):
    """
    Periodically compute the distance between 2 set of points


    :param name: object name  Default value: EvalPointsDistance

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param draw: activate rendering of lines between associated points  Default value: 1

    :param isToPrint: suppress somes data before using save as function  Default value: 0

    :param filename: output file name  Default value: 

    :param period: period between outputs  Default value: 0.0

    :param distance: distances (OUTPUT)  Default value: []

    :param distMean: mean distance (OUTPUT)  Default value: 1.0

    :param distMin: min distance (OUTPUT)  Default value: 1.0

    :param distMax: max distance (OUTPUT)  Default value: 1.0

    :param distDev: distance standard deviation (OUTPUT)  Default value: 1.0

    :param rdistMean: mean relative distance (OUTPUT)  Default value: 1.0

    :param rdistMin: min relative distance (OUTPUT)  Default value: 1.0

    :param rdistMax: max relative distance (OUTPUT)  Default value: 1.0

    :param rdistDev: relative distance standard deviation (OUTPUT)  Default value: 1.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, draw=draw, isToPrint=isToPrint, filename=filename, period=period, distance=distance, distMean=distMean, distMin=distMin, distMax=distMax, distDev=distDev, rdistMean=rdistMean, rdistMin=rdistMin, rdistMax=rdistMax, rdistDev=rdistDev)
    return "EvalPointsDistance", params
