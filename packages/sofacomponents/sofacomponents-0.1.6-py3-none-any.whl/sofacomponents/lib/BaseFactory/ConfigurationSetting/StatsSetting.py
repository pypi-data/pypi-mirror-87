# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component StatsSetting

.. autofunction:: StatsSetting

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def StatsSetting(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, dumpState=None, logTime=None, exportState=None, **kwargs):
    """
    Stats settings


    :param name: object name  Default value: StatsSetting

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param dumpState: Dump state vectors at each time step of the simulation  Default value: 0

    :param logTime: Output in the console an average of the time spent during different stages of the simulation  Default value: 0

    :param exportState: Create GNUPLOT files with the positions, velocities and forces of all the simulated objects of the scene  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, dumpState=dumpState, logTime=logTime, exportState=exportState)
    return "StatsSetting", params
