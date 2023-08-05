# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MinResLinearSolver

.. autofunction:: MinResLinearSolver

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MinResLinearSolver(self, iterations=None, tolerance=None, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, verbose=None, graph=None, **kwargs):
    """
    Linear system solver using the MINRES iterative algorithm


    :param name: object name  Default value: MinResLinearSolver

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param iterations: maximum number of iterations of the Conjugate Gradient solution  Default value: 25

    :param tolerance: desired precision of the Conjugate Gradient Solution (ratio of current residual norm over initial residual norm)  Default value: 1e-05

    :param verbose: Dump system state at each iteration  Default value: 0

    :param graph: Graph of residuals at each iteration  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, iterations=iterations, tolerance=tolerance, verbose=verbose, graph=graph)
    return "MinResLinearSolver", params
