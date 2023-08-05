# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component StaticSolver

.. autofunction:: StaticSolver

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def StaticSolver(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, newton_iterations=None, correction_tolerance_threshold=None, residual_tolerance_threshold=None, should_diverge_when_residual_is_growing=None, **kwargs):
    """
    Static ODE Solver


    :param name: object name  Default value: StaticSolver

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param newton_iterations: Number of newton iterations between each load increments (normally, one load increment per simulation time-step.  Default value: 1

    :param correction_tolerance_threshold: Convergence criterion: The newton iterations will stop when the norm of correction |du| reach this threshold.  Default value: 1e-05

    :param residual_tolerance_threshold: Convergence criterion: The newton iterations will stop when the norm of the residual |f - K(u)| reach this threshold. Use a negative value to disable this criterion.  Default value: 1e-05

    :param should_diverge_when_residual_is_growing: Divergence criterion: The newton iterations will stop when the residual is greater than the one from the previous iteration.  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, newton_iterations=newton_iterations, correction_tolerance_threshold=correction_tolerance_threshold, residual_tolerance_threshold=residual_tolerance_threshold, should_diverge_when_residual_is_growing=should_diverge_when_residual_is_growing)
    return "StaticSolver", params
