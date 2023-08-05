# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component AffineMovementConstraint

.. autofunction:: AffineMovementConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def AffineMovementConstraint(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, group=None, endTime=None, meshIndices=None, indices=None, beginConstraintTime=None, endConstraintTime=None, rotation=None, quaternion=None, translation=None, drawConstrainedPoints=None, **kwargs):
    """
    Constraint the movement by a rigid transform.


    :param name: object name  Default value: AffineMovementConstraint

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param group: ID of the group containing this constraint. This ID is used to specify which constraints are solved by which solver, by specifying in each solver which groups of constraints it should handle.  Default value: 0

    :param endTime: The constraint stops acting after the given value.
Use a negative value for infinite constraints  Default value: -1.0

    :param meshIndices: Indices of the mesh  Default value: []

    :param indices: Indices of the constrained points  Default value: []

    :param beginConstraintTime: Begin time of the bilinear constraint  Default value: 0.0

    :param endConstraintTime: End time of the bilinear constraint  Default value: 20.0

    :param rotation: rotation applied to border points  Default value: [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

    :param quaternion: quaternion applied to border points  Default value: [[0.0, 0.0, 0.0, 1.0]]

    :param translation: translation applied to border points  Default value: [[0.0, 0.0, 0.0]]

    :param drawConstrainedPoints: draw constrained points  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, group=group, endTime=endTime, meshIndices=meshIndices, indices=indices, beginConstraintTime=beginConstraintTime, endConstraintTime=endConstraintTime, rotation=rotation, quaternion=quaternion, translation=translation, drawConstrainedPoints=drawConstrainedPoints)
    return "AffineMovementConstraint", params
