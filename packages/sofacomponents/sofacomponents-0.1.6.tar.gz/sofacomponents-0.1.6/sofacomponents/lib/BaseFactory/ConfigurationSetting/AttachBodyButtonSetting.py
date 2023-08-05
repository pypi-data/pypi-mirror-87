# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component AttachBodyButtonSetting

.. autofunction:: AttachBodyButtonSetting

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def AttachBodyButtonSetting(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, button=None, stiffness=None, arrowSize=None, showFactorSize=None, **kwargs):
    """
    Attach Body Button configuration


    :param name: object name  Default value: AttachBodyButtonSetting

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param button: Mouse button used  Default value: Left

    :param stiffness: Stiffness of the spring to attach a particule  Default value: 1000.0

    :param arrowSize: Size of the drawn spring: if >0 an arrow will be drawn  Default value: 0.0

    :param showFactorSize: Show factor size of the JointSpringForcefield  when interacting with rigids  Default value: 1.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, button=button, stiffness=stiffness, arrowSize=arrowSize, showFactorSize=showFactorSize)
    return "AttachBodyButtonSetting", params
