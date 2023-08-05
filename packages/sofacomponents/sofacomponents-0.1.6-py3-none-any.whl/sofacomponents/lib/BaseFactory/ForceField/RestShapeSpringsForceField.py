# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component RestShapeSpringsForceField

.. autofunction:: RestShapeSpringsForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def RestShapeSpringsForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, points=None, stiffness=None, angularStiffness=None, pivot_points=None, external_points=None, recompute_indices=None, drawSpring=None, springColor=None, **kwargs):
    """
    Elastic springs generating forces on degrees of freedom between their current and rest shape position
Spring attached to rest position
Spring attached to rest position


    :param name: object name  Default value: RestShapeSpringsForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param points: points controlled by the rest shape springs  Default value: []

    :param stiffness: stiffness values between the actual position and the rest shape position  Default value: []

    :param angularStiffness: angularStiffness assigned when controlling the rotation of the points  Default value: []

    :param pivot_points: global pivot points used when translations instead of the rigid mass centers  Default value: []

    :param external_points: points from the external Mechancial State that define the rest shape springs  Default value: []

    :param recompute_indices: Recompute indices (should be false for BBOX)  Default value: 1

    :param drawSpring: draw Spring  Default value: 0

    :param springColor: spring color. (default=[0.0,1.0,0.0,1.0])  Default value: [[0.0, 1.0, 0.0, 1.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, points=points, stiffness=stiffness, angularStiffness=angularStiffness, pivot_points=pivot_points, external_points=external_points, recompute_indices=recompute_indices, drawSpring=drawSpring, springColor=springColor)
    return "RestShapeSpringsForceField", params
