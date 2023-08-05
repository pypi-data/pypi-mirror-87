# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ConstantForceField

.. autofunction:: ConstantForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ConstantForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, indices=None, indexFromEnd=None, forces=None, force=None, totalForce=None, showArrowSize=None, showColor=None, **kwargs):
    """
    Constant forces applied to given degrees of freedom
Constant forces applied to given degrees of freedom
Constant forces applied to given degrees of freedom


    :param name: object name  Default value: ConstantForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param indices: indices where the forces are applied  Default value: []

    :param indexFromEnd: Concerned DOFs indices are numbered from the end of the MState DOFs vector. (default=false)  Default value: 0

    :param forces: applied forces at each point  Default value: []

    :param force: applied force to all points if forces attribute is not specified  Default value: [[0.0, 0.0, 0.0]]

    :param totalForce: total force for all points, will be distributed uniformly over points  Default value: [[0.0, 0.0, 0.0]]

    :param showArrowSize: Size of the drawn arrows (0->no arrows, sign->direction of drawing. (default=0)  Default value: 0.0

    :param showColor: Color for object display (default: [0.2,0.9,0.3,1.0])  Default value: [[0.20000000298023224, 0.8999999761581421, 0.30000001192092896, 1.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, indices=indices, indexFromEnd=indexFromEnd, forces=forces, force=force, totalForce=totalForce, showArrowSize=showArrowSize, showColor=showColor)
    return "ConstantForceField", params
