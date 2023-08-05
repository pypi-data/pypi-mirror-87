# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TorsionForceField

.. autofunction:: TorsionForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TorsionForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, indices=None, torque=None, axis=None, origin=None, **kwargs):
    """
    Applies a torque to specified points


    :param name: object name  Default value: TorsionForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param indices: indices of the selected points  Default value: []

    :param torque: torque to apply  Default value: 0.0

    :param axis: direction of the axis (will be normalized)  Default value: [[0.0, 0.0, 0.0]]

    :param origin: origin of the axis  Default value: [[0.0, 0.0, 0.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, indices=indices, torque=torque, axis=axis, origin=origin)
    return "TorsionForceField", params
