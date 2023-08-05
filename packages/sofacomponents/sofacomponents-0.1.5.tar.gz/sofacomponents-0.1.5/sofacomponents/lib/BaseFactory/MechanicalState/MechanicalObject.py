# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MechanicalObject

.. autofunction:: MechanicalObject

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MechanicalObject(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, position=None, velocity=None, force=None, rest_position=None, externalForce=None, derivX=None, free_position=None, free_velocity=None, constraint=None, mappingJacobian=None, reset_position=None, reset_velocity=None, restScale=None, useTopology=None, showObject=None, showObjectScale=None, showIndices=None, showIndicesScale=None, showVectors=None, showVectorsScale=None, drawMode=None, showColor=None, translation=None, rotation=None, scale3d=None, translation2=None, rotation2=None, size=None, reserve=None, **kwargs):
    """
    mechanical state vectors
mechanical state vectors
Mechanical state vectors
mechanical state vectors
mechanical state vectors


    :param name: object name  Default value: MechanicalObject

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param position: position coordinates of the degrees of freedom  Default value: [[0.0, 0.0, 0.0]]

    :param velocity: velocity coordinates of the degrees of freedom  Default value: [[0.0, 0.0, 0.0]]

    :param force: force vector of the degrees of freedom  Default value: [[0.0, 0.0, 0.0]]

    :param rest_position: rest position coordinates of the degrees of freedom  Default value: []

    :param externalForce: externalForces vector of the degrees of freedom  Default value: [[0.0, 0.0, 0.0]]

    :param derivX: dx vector of the degrees of freedom  Default value: []

    :param free_position: free position coordinates of the degrees of freedom  Default value: []

    :param free_velocity: free velocity coordinates of the degrees of freedom  Default value: []

    :param constraint: constraints applied to the degrees of freedom  Default value: 

    :param mappingJacobian: mappingJacobian applied to the degrees of freedom  Default value: 

    :param reset_position: reset position coordinates of the degrees of freedom  Default value: []

    :param reset_velocity: reset velocity coordinates of the degrees of freedom  Default value: []

    :param restScale: optional scaling of rest position coordinates (to simulated pre-existing internal tension).(default = 1.0)  Default value: 1.0

    :param useTopology: Shall this object rely on any active topology to initialize its size and positions  Default value: 1

    :param showObject: Show objects. (default=false)  Default value: 0

    :param showObjectScale: Scale for object display. (default=0.1)  Default value: 0.10000000149

    :param showIndices: Show indices. (default=false)  Default value: 0

    :param showIndicesScale: Scale for indices display. (default=0.02)  Default value: 0.019999999553

    :param showVectors: Show velocity. (default=false)  Default value: 0

    :param showVectorsScale: Scale for vectors display. (default=0.0001)  Default value: 9.99999974738e-05

    :param drawMode: The way vectors will be drawn:
- 0: Line
- 1:Cylinder
- 2: Arrow.

The DOFS will be drawn:
- 0: point
- >1: sphere. (default=0)  Default value: 0

    :param showColor: Color for object display. (default=[1 1 1 1])  Default value: [[1.0, 1.0, 1.0, 1.0]]

    :param translation: Translation of the DOFs  Default value: [[0.0, 0.0, 0.0]]

    :param rotation: Rotation of the DOFs  Default value: [[0.0, 0.0, 0.0]]

    :param scale3d: Scale of the DOFs in 3 dimensions  Default value: [[1.0, 1.0, 1.0]]

    :param translation2: Translation of the DOFs, applied after the rest position has been computed  Default value: [[0.0, 0.0, 0.0]]

    :param rotation2: Rotation of the DOFs, applied the after the rest position has been computed  Default value: [[0.0, 0.0, 0.0]]

    :param size: Size of the vectors  Default value: 1

    :param reserve: Size to reserve when creating vectors. (default=0)  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, position=position, velocity=velocity, force=force, rest_position=rest_position, externalForce=externalForce, derivX=derivX, free_position=free_position, free_velocity=free_velocity, constraint=constraint, mappingJacobian=mappingJacobian, reset_position=reset_position, reset_velocity=reset_velocity, restScale=restScale, useTopology=useTopology, showObject=showObject, showObjectScale=showObjectScale, showIndices=showIndices, showIndicesScale=showIndicesScale, showVectors=showVectors, showVectorsScale=showVectorsScale, drawMode=drawMode, showColor=showColor, translation=translation, rotation=rotation, scale3d=scale3d, translation2=translation2, rotation2=rotation2, size=size, reserve=reserve)
    return "MechanicalObject", params
