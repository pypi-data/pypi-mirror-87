# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MechanicalMatrixMapper

.. autofunction:: MechanicalMatrixMapper

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MechanicalMatrixMapper(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, forceFieldList=None, stopAtNodeToParse=None, skipJ1tKJ1=None, skipJ2tKJ2=None, **kwargs):
    """
    This component allows to map the stiffness (and mass) matrix through a mapping.


    :param name: object name  Default value: MechanicalMatrixMapper

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param forceFieldList: List of ForceField Names to work on (by default will take all)  Default value: []

    :param stopAtNodeToParse: Boolean to choose whether forceFields in children Nodes of NodeToParse should be considered.  Default value: 0

    :param skipJ1tKJ1: Boolean to choose whether to skip J1tKJ1 to avoid 2 contributions, in case 2 MechanicalMatrixMapper are used  Default value: 0

    :param skipJ2tKJ2: Boolean to choose whether to skip J2tKJ2 to avoid 2 contributions, in case 2 MechanicalMatrixMapper are used  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, forceFieldList=forceFieldList, stopAtNodeToParse=stopAtNodeToParse, skipJ1tKJ1=skipJ1tKJ1, skipJ2tKJ2=skipJ2tKJ2)
    return "MechanicalMatrixMapper", params
