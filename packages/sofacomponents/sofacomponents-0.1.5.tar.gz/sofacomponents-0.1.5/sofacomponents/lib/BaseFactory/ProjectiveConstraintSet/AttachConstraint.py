# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component AttachConstraint

.. autofunction:: AttachConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def AttachConstraint(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, group=None, endTime=None, indices1=None, indices2=None, twoWay=None, freeRotations=None, lastFreeRotation=None, restRotations=None, lastPos=None, lastDir=None, clamp=None, minDistance=None, positionFactor=None, velocityFactor=None, responseFactor=None, constraintFactor=None, **kwargs):
    """
    Attach given pair of particles, projecting the positions of the second particles to the first ones


    :param name: object name  Default value: AttachConstraint

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param group: ID of the group containing this constraint. This ID is used to specify which constraints are solved by which solver, by specifying in each solver which groups of constraints it should handle.  Default value: 0

    :param endTime: The constraint stops acting after the given value.
Use a negative value for infinite constraints  Default value: -1.0

    :param indices1: Indices of the source points on the first model  Default value: []

    :param indices2: Indices of the fixed points on the second model  Default value: []

    :param twoWay: true if forces should be projected back from model2 to model1  Default value: 0

    :param freeRotations: true to keep rotations free (only used for Rigid DOFs)  Default value: 0

    :param lastFreeRotation: true to keep rotation of the last attached point free (only used for Rigid DOFs)  Default value: 0

    :param restRotations: true to use rest rotations local offsets (only used for Rigid DOFs)  Default value: 0

    :param lastPos: position at which the attach constraint should become inactive  Default value: [[0.0, 0.0, 0.0]]

    :param lastDir: direction from lastPos at which the attach coustraint should become inactive  Default value: [[0.0, 0.0, 0.0]]

    :param clamp: true to clamp particles at lastPos instead of freeing them.  Default value: 0

    :param minDistance: the constraint become inactive if the distance between the points attached is bigger than minDistance.  Default value: -1.0

    :param positionFactor: IN: Factor applied to projection of position  Default value: 1.0

    :param velocityFactor: IN: Factor applied to projection of velocity  Default value: 1.0

    :param responseFactor: IN: Factor applied to projection of force/acceleration  Default value: 1.0

    :param constraintFactor: Constraint factor per pair of points constrained. 0 -> the constraint is released. 1 -> the constraint is fully constrained  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, group=group, endTime=endTime, indices1=indices1, indices2=indices2, twoWay=twoWay, freeRotations=freeRotations, lastFreeRotation=lastFreeRotation, restRotations=restRotations, lastPos=lastPos, lastDir=lastDir, clamp=clamp, minDistance=minDistance, positionFactor=positionFactor, velocityFactor=velocityFactor, responseFactor=responseFactor, constraintFactor=constraintFactor)
    return "AttachConstraint", params
