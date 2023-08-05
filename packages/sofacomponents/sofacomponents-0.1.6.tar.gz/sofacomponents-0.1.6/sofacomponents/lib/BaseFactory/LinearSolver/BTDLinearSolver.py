# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component BTDLinearSolver

.. autofunction:: BTDLinearSolver

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def BTDLinearSolver(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, verbose=None, showProblem=None, subpartSolve=None, verification=None, test_perf=None, blockSize=None, **kwargs):
    """
    Linear system solver using Thomas Algorithm for Block Tridiagonal matrices


    :param name: object name  Default value: BTDLinearSolver

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param verbose: Dump system state at each iteration  Default value: 0

    :param showProblem: display debug informations about subpartSolve computation  Default value: 0

    :param subpartSolve: Allows for the computation of a subpart of the system  Default value: 0

    :param verification: verification of the subpartSolve  Default value: 0

    :param test_perf: verification of performance  Default value: 0

    :param blockSize: dimension of the blocks in the matrix  Default value: 6


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, verbose=verbose, showProblem=showProblem, subpartSolve=subpartSolve, verification=verification, test_perf=test_perf, blockSize=blockSize)
    return "BTDLinearSolver", params
