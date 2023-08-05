# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component LinearForceField

.. autofunction:: LinearForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def LinearForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, points=None, force=None, times=None, forces=None, arrowSizeCoef=None, **kwargs):
    """
    Linearly interpolated force applied to given degrees of freedom


    :param name: object name  Default value: LinearForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param points: points where the force is applied  Default value: []

    :param force: applied force to all points  Default value: 1.0

    :param times: key times for the interpolation  Default value: []

    :param forces: forces corresponding to the key times  Default value: []

    :param arrowSizeCoef: Size of the drawn arrows (0->no arrows, sign->direction of drawing  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, points=points, force=force, times=times, forces=forces, arrowSizeCoef=arrowSizeCoef)
    return "LinearForceField", params
