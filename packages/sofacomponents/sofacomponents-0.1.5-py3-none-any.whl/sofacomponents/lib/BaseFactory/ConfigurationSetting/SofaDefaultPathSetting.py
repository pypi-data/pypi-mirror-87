# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SofaDefaultPathSetting

.. autofunction:: SofaDefaultPathSetting

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SofaDefaultPathSetting(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, recordPath=None, gnuplotPath=None, **kwargs):
    """
    Default Paths for Sofa Application


    :param name: object name  Default value: SofaDefaultPathSetting

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param recordPath: Path where will be saved the data of the recorded simulation  Default value: 

    :param gnuplotPath: Path where will be saved the gnuplot files  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, recordPath=recordPath, gnuplotPath=gnuplotPath)
    return "SofaDefaultPathSetting", params
