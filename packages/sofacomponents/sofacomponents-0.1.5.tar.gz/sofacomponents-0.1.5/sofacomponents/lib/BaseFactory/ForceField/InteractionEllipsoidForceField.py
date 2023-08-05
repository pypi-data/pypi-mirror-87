# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component InteractionEllipsoidForceField

.. autofunction:: InteractionEllipsoidForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def InteractionEllipsoidForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, contacts=None, center=None, vradius=None, stiffness=None, damping=None, color=None, draw=None, object2_dof_index=None, object2_forces=None, object2_invert=None, **kwargs):
    """
    Repulsion applied by an ellipsoid toward the exterior or the interior


    :param name: object name  Default value: InteractionEllipsoidForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param contacts: Contacts  Default value: 

    :param center: ellipsoid center  Default value: []

    :param vradius: ellipsoid radius  Default value: []

    :param stiffness: force stiffness (positive to repulse outward, negative inward)  Default value: 500.0

    :param damping: force damping  Default value: 5.0

    :param color: ellipsoid color. (default=[0.0,0.5,1.0,1.0])  Default value: [[0.0, 0.5, 1.0, 1.0]]

    :param draw: enable/disable drawing of the ellipsoid  Default value: 1

    :param object2_dof_index: Dof index of object 2 where the forcefield is attached  Default value: 0

    :param object2_forces: enable/disable propagation of forces to object 2  Default value: 1

    :param object2_invert: inverse transform from object 2 (use when object 1 is in local coordinates within a frame defined by object 2)  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, contacts=contacts, center=center, vradius=vradius, stiffness=stiffness, damping=damping, color=color, draw=draw, object2_dof_index=object2_dof_index, object2_forces=object2_forces, object2_invert=object2_invert)
    return "InteractionEllipsoidForceField", params
