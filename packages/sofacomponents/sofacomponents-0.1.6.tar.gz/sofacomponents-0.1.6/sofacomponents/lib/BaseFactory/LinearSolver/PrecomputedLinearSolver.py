# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PrecomputedLinearSolver

.. autofunction:: PrecomputedLinearSolver

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PrecomputedLinearSolver(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, jmjt_twostep=None, verbose=None, use_file=None, **kwargs):
    """
    Linear system solver based on a precomputed inverse matrix


    :param name: object name  Default value: PrecomputedLinearSolver

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param jmjt_twostep: Use two step algorithm to compute JMinvJt  Default value: 1

    :param verbose: Dump system state at each iteration  Default value: 0

    :param use_file: Dump system matrix in a file  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, jmjt_twostep=jmjt_twostep, verbose=verbose, use_file=use_file)
    return "PrecomputedLinearSolver", params
