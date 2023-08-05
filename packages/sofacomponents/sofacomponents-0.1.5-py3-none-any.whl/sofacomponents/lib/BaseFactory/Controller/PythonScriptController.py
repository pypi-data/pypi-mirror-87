# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PythonScriptController

.. autofunction:: PythonScriptController

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PythonScriptController(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, handleEventTriggersUpdate=None, filename=None, classname=None, variables=None, timingEnabled=None, autoreload=None, **kwargs):
    """
    A Sofa controller scripted in python


    :param name: object name  Default value: PythonScriptController

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param handleEventTriggersUpdate: Event handling frequency controls the controller update frequency  Default value: 0

    :param filename: Python script filename  Default value: 

    :param classname: Python class implemented in the script to instanciate for the controller  Default value: 

    :param variables: Array of string variables (equivalent to a c-like argv)  Default value: []

    :param timingEnabled: Set this attribute to true or false to activate/deactivate the gathering of timing statistics on the python execution time. Default value is setto true.  Default value: 1

    :param autoreload: Automatically reload the file when the source code is changed. Default value is set to false  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, handleEventTriggersUpdate=handleEventTriggersUpdate, filename=filename, classname=classname, variables=variables, timingEnabled=timingEnabled, autoreload=autoreload)
    return "PythonScriptController", params
