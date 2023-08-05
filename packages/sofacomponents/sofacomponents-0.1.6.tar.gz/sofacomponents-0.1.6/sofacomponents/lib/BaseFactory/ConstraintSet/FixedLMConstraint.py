# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component FixedLMConstraint

.. autofunction:: FixedLMConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def FixedLMConstraint(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, group=None, constraintIndex=None, object1=None, object2=None, indices=None, drawSize=None, **kwargs):
    """
    Maintain a set of particle to a fixed position using LMConstraint


    :param name: object name  Default value: FixedLMConstraint

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param group: ID of the group containing this constraint. This ID is used to specify which constraints are solved by which solver, by specifying in each solver which groups of constraints it should handle.  Default value: 0

    :param constraintIndex: Constraint index (first index in the right hand term resolution vector)  Default value: 0

    :param object1: First Object to constrain  Default value: 

    :param object2: Second Object to constrain  Default value: 

    :param indices: List of the index of particles to be fixed  Default value: []

    :param drawSize: 0 -> point based rendering, >0 -> radius of spheres  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, group=group, constraintIndex=constraintIndex, object1=object1, object2=object2, indices=indices, drawSize=drawSize)
    return "FixedLMConstraint", params
