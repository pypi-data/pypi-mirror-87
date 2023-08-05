# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component NullForceFeedbackT

.. autofunction:: NullForceFeedbackT

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def NullForceFeedbackT(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, activate=None, indice=None, **kwargs):
    """
    Null force feedback for haptic feedback device


    :param name: object name  Default value: NullForceFeedbackT

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param activate: boolean to activate or deactivate the forcefeedback  Default value: 0

    :param indice: Tool indice in the OmniDriver  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, activate=activate, indice=indice)
    return "NullForceFeedbackT", params
