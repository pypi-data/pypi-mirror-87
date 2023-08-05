# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SVDLinearSolver

.. autofunction:: SVDLinearSolver

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SVDLinearSolver(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, verbose=None, minSingularValue=None, conditionNumber=None, **kwargs):
    """
    Linear system solver using the conjugate gradient iterative algorithm


    :param name: object name  Default value: SVDLinearSolver

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param verbose: Dump system state at each iteration  Default value: 0

    :param minSingularValue: Thershold under which a singular value is set to 0, for the stabilization of ill-conditioned system.  Default value: 1e-06

    :param conditionNumber: Condition number of the matrix: ratio between the largest and smallest singular values. Computed in method solve.  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, verbose=verbose, minSingularValue=minSingularValue, conditionNumber=conditionNumber)
    return "SVDLinearSolver", params
