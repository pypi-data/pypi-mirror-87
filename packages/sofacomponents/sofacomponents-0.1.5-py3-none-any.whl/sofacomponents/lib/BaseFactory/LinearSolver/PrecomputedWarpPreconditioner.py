# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PrecomputedWarpPreconditioner

.. autofunction:: PrecomputedWarpPreconditioner

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PrecomputedWarpPreconditioner(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, jmjt_twostep=None, verbose=None, use_file=None, share_matrix=None, solverName=None, use_rotations=None, draw_rotations_scale=None, **kwargs):
    """
    Linear system solver based on a precomputed inverse matrix, wrapped by a per-node rotation matrix


    :param name: object name  Default value: PrecomputedWarpPreconditioner

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param jmjt_twostep: Use two step algorithm to compute JMinvJt  Default value: 1

    :param verbose: Dump system state at each iteration  Default value: 0

    :param use_file: Dump system matrix in a file  Default value: 1

    :param share_matrix: Share the compliance matrix in memory if they are related to the same file (WARNING: might require to reload Sofa when opening a new scene...)  Default value: 1

    :param solverName: Name of the solver to use to precompute the first matrix  Default value: 

    :param use_rotations: Use Rotations around the preconditioner  Default value: 1

    :param draw_rotations_scale: Scale rotations in draw function  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, jmjt_twostep=jmjt_twostep, verbose=verbose, use_file=use_file, share_matrix=share_matrix, solverName=solverName, use_rotations=use_rotations, draw_rotations_scale=draw_rotations_scale)
    return "PrecomputedWarpPreconditioner", params
