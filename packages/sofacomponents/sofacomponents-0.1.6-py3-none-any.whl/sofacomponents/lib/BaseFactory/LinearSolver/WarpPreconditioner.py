# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component WarpPreconditioner

.. autofunction:: WarpPreconditioner

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def WarpPreconditioner(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, solverName=None, useRotationFinder=None, **kwargs):
    """
    Linear system solver wrapping another (precomputed) linear solver by a per-node rotation matrix


    :param name: object name  Default value: WarpPreconditioner

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param solverName: Name of the solver/preconditioner to warp  Default value: 

    :param useRotationFinder: Which rotation Finder to use  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, solverName=solverName, useRotationFinder=useRotationFinder)
    return "WarpPreconditioner", params
