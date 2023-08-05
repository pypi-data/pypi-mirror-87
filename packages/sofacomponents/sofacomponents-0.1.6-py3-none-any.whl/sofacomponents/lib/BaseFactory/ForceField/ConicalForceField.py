# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ConicalForceField

.. autofunction:: ConicalForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ConicalForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, coneCenter=None, coneHeight=None, coneAngle=None, stiffness=None, damping=None, color=None, **kwargs):
    """
    Repulsion applied by a cone toward the exterior


    :param name: object name  Default value: ConicalForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param coneCenter: cone center  Default value: [[0.0, 0.0, 0.0]]

    :param coneHeight: cone height  Default value: [[0.0, 0.0, 0.0]]

    :param coneAngle: cone angle  Default value: 10.0

    :param stiffness: force stiffness  Default value: 500.0

    :param damping: force damping  Default value: 5.0

    :param color: cone color. (default=0.0,0.0,0.0,1.0,1.0)  Default value: [[0.0, 0.0, 1.0, 1.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, coneCenter=coneCenter, coneHeight=coneHeight, coneAngle=coneAngle, stiffness=stiffness, damping=damping, color=color)
    return "ConicalForceField", params
