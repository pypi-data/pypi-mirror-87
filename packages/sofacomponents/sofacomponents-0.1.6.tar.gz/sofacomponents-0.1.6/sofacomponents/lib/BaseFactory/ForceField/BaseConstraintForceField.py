# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component BaseConstraintForceField

.. autofunction:: BaseConstraintForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def BaseConstraintForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, useForce=None, normal=None, kn=None, temporaryForce=None, temporaryTimes=None, kp=None, heartPeriod=None, Zone=None, tagSolver=None, loadername=None, **kwargs):
    """
    Spring Constraint on the base for heart simulation


    :param name: object name  Default value: BaseConstraintForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param useForce: if a force has to be added  Default value: 0

    :param normal: vec3d of the normal direction of the spring  Default value: [[0.0, 0.0, 0.0]]

    :param kn: stiffness in the normal direction  Default value: 0.0

    :param temporaryForce: temporaryForce  Default value: 0

    :param temporaryTimes: vec3d of the 3 times of force  Default value: [[0.0, 0.0, 0.0]]

    :param kp: stiffness in the parallel direction  Default value: 0.0

    :param heartPeriod: heart period  Default value: 0.0

    :param Zone: List of tetra on a base  Default value: []

    :param tagSolver: Tag of the Solver Object  Default value: solver

    :param loadername: loader name  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, useForce=useForce, normal=normal, kn=kn, temporaryForce=temporaryForce, temporaryTimes=temporaryTimes, kp=kp, heartPeriod=heartPeriod, Zone=Zone, tagSolver=tagSolver, loadername=loadername)
    return "BaseConstraintForceField", params
