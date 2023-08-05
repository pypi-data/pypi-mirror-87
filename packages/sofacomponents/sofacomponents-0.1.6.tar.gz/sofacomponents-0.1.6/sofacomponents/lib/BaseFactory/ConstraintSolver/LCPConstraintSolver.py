# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component LCPConstraintSolver

.. autofunction:: LCPConstraintSolver

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def LCPConstraintSolver(self, tolerance=None, maxIt=None, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, displayDebug=None, displayTime=None, initial_guess=None, build_lcp=None, mu=None, minW=None, maxF=None, multi_grid=None, multi_grid_levels=None, merge_method=None, merge_spatial_step=None, merge_local_levels=None, group=None, graph=None, showLevels=None, showCellWidth=None, showTranslation=None, showLevelTranslation=None, **kwargs):
    """
    A Constraint Solver using the Linear Complementarity Problem formulation to solve BaseConstraint based components


    :param name: object name  Default value: LCPConstraintSolver

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param displayDebug: Display debug information.  Default value: 0

    :param displayTime: Display time for each important step of LCPConstraintSolver.  Default value: 0

    :param initial_guess: activate LCP results history to improve its resolution performances.  Default value: 1

    :param build_lcp: LCP is not fully built to increase performance in some case.  Default value: 1

    :param tolerance: residual error threshold for termination of the Gauss-Seidel algorithm  Default value: 0.001

    :param maxIt: maximal number of iterations of the Gauss-Seidel algorithm  Default value: 1000

    :param mu: Friction coefficient  Default value: 0.6

    :param minW: If not zero, constraints whose self-compliance (i.e. the corresponding value on the diagonal of W) is smaller than this threshold will be ignored  Default value: 0.0

    :param maxF: If not zero, constraints whose response force becomes larger than this threshold will be ignored  Default value: 0.0

    :param multi_grid: activate multi_grid resolution (NOT STABLE YET)  Default value: 0

    :param multi_grid_levels: if multi_grid is active: how many levels to create (>=2)  Default value: 2

    :param merge_method: if multi_grid is active: which method to use to merge constraints (0 = compliance-based, 1 = spatial coordinates)  Default value: 0

    :param merge_spatial_step: if merge_method is 1: grid size reduction between multigrid levels  Default value: 2

    :param merge_local_levels: if merge_method is 1: up to the specified level of the multigrid, constraints are grouped locally, i.e. separately within each contact pairs, while on upper levels they are grouped globally independently of contact pairs.  Default value: 2

    :param group: list of ID of groups of constraints to be handled by this solver.  Default value: [[0]]

    :param graph: Graph of residuals at each iteration  Default value: 

    :param showLevels: Number of constraint levels to display  Default value: 0

    :param showCellWidth: Distance between each constraint cells  Default value: 0.0

    :param showTranslation: Position of the first cell  Default value: [[0.0, 0.0, 0.0]]

    :param showLevelTranslation: Translation between levels  Default value: [[0.0, 0.0, 0.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, displayDebug=displayDebug, displayTime=displayTime, initial_guess=initial_guess, build_lcp=build_lcp, tolerance=tolerance, maxIt=maxIt, mu=mu, minW=minW, maxF=maxF, multi_grid=multi_grid, multi_grid_levels=multi_grid_levels, merge_method=merge_method, merge_spatial_step=merge_spatial_step, merge_local_levels=merge_local_levels, group=group, graph=graph, showLevels=showLevels, showCellWidth=showCellWidth, showTranslation=showTranslation, showLevelTranslation=showLevelTranslation)
    return "LCPConstraintSolver", params
