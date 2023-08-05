# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component BoxStiffSpringForceField

.. autofunction:: BoxStiffSpringForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def BoxStiffSpringForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, stiffness=None, damping=None, showArrowSize=None, drawMode=None, spring=None, indices1=None, indices2=None, length=None, box_object1=None, box_object2=None, factorRestLength=None, forceOldBehavior=None, **kwargs):
    """
    Set Spring between the points inside a given box


    :param name: object name  Default value: BoxStiffSpringForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param stiffness: uniform stiffness for the all springs  Default value: 100.0

    :param damping: uniform damping for the all springs  Default value: 5.0

    :param showArrowSize: size of the axis  Default value: 0.00999999977648

    :param drawMode: The way springs will be drawn:
- 0: Line
- 1:Cylinder
- 2: Arrow  Default value: 0

    :param spring: pairs of indices, stiffness, damping, rest length  Default value: 

    :param indices1: Indices of the source points on the first model  Default value: []

    :param indices2: Indices of the fixed points on the second model  Default value: []

    :param length: uniform length of all springs  Default value: 0.0

    :param box_object1: Box for the object1 where springs will be attached  Default value: [[0.0, 0.0, 0.0, 1.0, 1.0, 1.0]]

    :param box_object2: Box for the object2 where springs will be attached  Default value: [[0.0, 0.0, 0.0, 1.0, 1.0, 1.0]]

    :param factorRestLength: Factor used to compute the rest length of the springs generated  Default value: 1.0

    :param forceOldBehavior: Keep using the old behavior  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, stiffness=stiffness, damping=damping, showArrowSize=showArrowSize, drawMode=drawMode, spring=spring, indices1=indices1, indices2=indices2, length=length, box_object1=box_object1, box_object2=box_object2, factorRestLength=factorRestLength, forceOldBehavior=forceOldBehavior)
    return "BoxStiffSpringForceField", params
