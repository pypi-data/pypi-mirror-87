# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PartialLinearMovementConstraint

.. autofunction:: PartialLinearMovementConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PartialLinearMovementConstraint(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, group=None, endTime=None, indices=None, keyTimes=None, movements=None, showMovement=None, linearMovementBetweenNodesInIndices=None, mainIndice=None, minDepIndice=None, maxDepIndice=None, imposedDisplacmentOnMacroNodes=None, X0=None, Y0=None, Z0=None, movedDirections=None, **kwargs):
    """
    translate given particles


    :param name: object name  Default value: PartialLinearMovementConstraint

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param group: ID of the group containing this constraint. This ID is used to specify which constraints are solved by which solver, by specifying in each solver which groups of constraints it should handle.  Default value: 0

    :param endTime: The constraint stops acting after the given value.
Use a negative value for infinite constraints  Default value: -1.0

    :param indices: Indices of the constrained points  Default value: [[0]]

    :param keyTimes: key times for the movements  Default value: [[0.0]]

    :param movements: movements corresponding to the key times  Default value: [[0.0, 0.0, 0.0]]

    :param showMovement: Visualization of the movement to be applied to constrained dofs.  Default value: 0

    :param linearMovementBetweenNodesInIndices: Take into account the linear movement between the constrained points  Default value: 0

    :param mainIndice: The main indice node in the list of constrained nodes, it defines how to apply the linear movement between this constrained nodes   Default value: 0

    :param minDepIndice: The indice node in the list of constrained nodes, which is imposed the minimum displacment   Default value: 0

    :param maxDepIndice: The indice node in the list of constrained nodes, which is imposed the maximum displacment   Default value: 0

    :param imposedDisplacmentOnMacroNodes: The imposed displacment on macro nodes  Default value: []

    :param X0: Size of specimen in X-direction  Default value: 0.0

    :param Y0: Size of specimen in Y-direction  Default value: 0.0

    :param Z0: Size of specimen in Z-direction  Default value: 0.0

    :param movedDirections: for each direction, 1 if moved, 0 if free  Default value: [[1, 1, 1]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, group=group, endTime=endTime, indices=indices, keyTimes=keyTimes, movements=movements, showMovement=showMovement, linearMovementBetweenNodesInIndices=linearMovementBetweenNodesInIndices, mainIndice=mainIndice, minDepIndice=minDepIndice, maxDepIndice=maxDepIndice, imposedDisplacmentOnMacroNodes=imposedDisplacmentOnMacroNodes, X0=X0, Y0=Y0, Z0=Z0, movedDirections=movedDirections)
    return "PartialLinearMovementConstraint", params
