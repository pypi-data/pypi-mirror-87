# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component WriteTopology

.. autofunction:: WriteTopology

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def WriteTopology(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, writeContainers=None, writeShellContainers=None, interval=None, time=None, period=None, **kwargs):
    """
    Write topology containers informations to file at each timestep


    :param name: object name  Default value: WriteTopology

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param filename: output file name  Default value: 

    :param writeContainers: flag enabling output of common topology containers.  Default value: 1

    :param writeShellContainers: flag enabling output of specific shell topology containers.  Default value: 0

    :param interval: time duration between outputs  Default value: 0.0

    :param time: set time to write outputs  Default value: []

    :param period: period between outputs  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, writeContainers=writeContainers, writeShellContainers=writeShellContainers, interval=interval, time=time, period=period)
    return "WriteTopology", params
