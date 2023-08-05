# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ShewchukPCGLinearSolver

.. autofunction:: ShewchukPCGLinearSolver

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ShewchukPCGLinearSolver(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, iterations=None, tolerance=None, use_precond=None, update_step=None, build_precond=None, preconditioners=None, graph=None, **kwargs):
    """
    Linear system solver using the conjugate gradient iterative algorithm


    :param name: object name  Default value: ShewchukPCGLinearSolver

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param iterations: maximum number of iterations of the Conjugate Gradient solution  Default value: 25

    :param tolerance: desired precision of the Conjugate Gradient Solution (ratio of current residual norm over initial residual norm)  Default value: 1e-05

    :param use_precond: Use preconditioner  Default value: 1

    :param update_step: Number of steps before the next refresh of precondtioners  Default value: 1

    :param build_precond: Build the preconditioners, if false build the preconditioner only at the initial step  Default value: 1

    :param preconditioners: If not empty: path to the solvers to use as preconditioners  Default value: 

    :param graph: Graph of residuals at each iteration  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, iterations=iterations, tolerance=tolerance, use_precond=use_precond, update_step=update_step, build_precond=build_precond, preconditioners=preconditioners, graph=graph)
    return "ShewchukPCGLinearSolver", params
