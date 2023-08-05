# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ProjectivePressureConstraint

.. autofunction:: ProjectivePressureConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ProjectivePressureConstraint(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, group=None, endTime=None, optimiser=None, tagMeca=None, tagSolver=None, FFNames=None, phaseNew=None, updateSteps=None, **kwargs):
    """
    Correction the pressure force field for the heart ventricles


    :param name: object name  Default value: ProjectivePressureConstraint

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param group: ID of the group containing this constraint. This ID is used to specify which constraints are solved by which solver, by specifying in each solver which groups of constraints it should handle.  Default value: 0

    :param endTime: The constraint stops acting after the given value.
Use a negative value for infinite constraints  Default value: -1.0

    :param optimiser: if the correction should be optimized  Default value: 0

    :param tagMeca: tagMeca  Default value: meca

    :param tagSolver: Tag of the Solver Object  Default value: solver

    :param FFNames: Names of the pressure forcefields  Default value: []

    :param phaseNew: phaseNew  Default value: []

    :param updateSteps: the number of steps after which the projection should be updated  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, group=group, endTime=endTime, optimiser=optimiser, tagMeca=tagMeca, tagSolver=tagSolver, FFNames=FFNames, phaseNew=phaseNew, updateSteps=updateSteps)
    return "ProjectivePressureConstraint", params
