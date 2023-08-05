# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component WriteState

.. autofunction:: WriteState

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def WriteState(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, writeX=None, writeX0=None, writeV=None, writeF=None, time=None, period=None, DOFsX=None, DOFsV=None, stopAt=None, keperiod=None, **kwargs):
    """
    Write State vectors to file at each timestep


    :param name: object name  Default value: WriteState

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param filename: output file name  Default value: 

    :param writeX: flag enabling output of X vector  Default value: 1

    :param writeX0: flag enabling output of X0 vector  Default value: 0

    :param writeV: flag enabling output of V vector  Default value: 0

    :param writeF: flag enabling output of F vector  Default value: 0

    :param time: set time to write outputs (by default export at t=0)  Default value: []

    :param period: period between outputs  Default value: 0.0

    :param DOFsX: set the position DOFs to write  Default value: []

    :param DOFsV: set the velocity DOFs to write  Default value: []

    :param stopAt: stop the simulation when the given threshold is reached  Default value: 0.0

    :param keperiod: set the period to measure the kinetic energy increase  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, writeX=writeX, writeX0=writeX0, writeV=writeV, writeF=writeF, time=time, period=period, DOFsX=DOFsX, DOFsV=DOFsV, stopAt=stopAt, keperiod=keperiod)
    return "WriteState", params
