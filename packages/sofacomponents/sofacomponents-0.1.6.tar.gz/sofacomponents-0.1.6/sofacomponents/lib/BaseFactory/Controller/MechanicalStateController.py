# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MechanicalStateController

.. autofunction:: MechanicalStateController

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MechanicalStateController(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, handleEventTriggersUpdate=None, index=None, onlyTranslation=None, buttonDeviceState=None, mainDirection=None, **kwargs):
    """
    Provides a Mouse & Keyboard user control on a Mechanical State.


    :param name: object name  Default value: MechanicalStateController

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param handleEventTriggersUpdate: Event handling frequency controls the controller update frequency  Default value: 0

    :param index: Index of the controlled DOF  Default value: 0

    :param onlyTranslation: Controlling the DOF only in translation  Default value: 0

    :param buttonDeviceState: state of ths device button  Default value: 0

    :param mainDirection: Main direction and orientation of the controlled DOF  Default value: [[0.0, 0.0, -1.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, handleEventTriggersUpdate=handleEventTriggersUpdate, index=index, onlyTranslation=onlyTranslation, buttonDeviceState=buttonDeviceState, mainDirection=mainDirection)
    return "MechanicalStateController", params
