# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component LinearSolverConstraintCorrection

.. autofunction:: LinearSolverConstraintCorrection

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def LinearSolverConstraintCorrection(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, wire_optimization=None, solverName=None, **kwargs):
    """
    

    :param name: object name  Default value: LinearSolverConstraintCorrection

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param wire_optimization: constraints are reordered along a wire-like topology (from tip to base)  Default value: 0

    :param solverName: search for the following names upward the scene graph  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, wire_optimization=wire_optimization, solverName=solverName)
    return "LinearSolverConstraintCorrection", params
