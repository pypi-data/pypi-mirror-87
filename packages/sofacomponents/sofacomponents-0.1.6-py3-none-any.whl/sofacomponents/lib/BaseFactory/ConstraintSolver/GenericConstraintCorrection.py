# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component GenericConstraintCorrection

.. autofunction:: GenericConstraintCorrection

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def GenericConstraintCorrection(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, solverName=None, ODESolverName=None, complianceFactor=None, **kwargs):
    """
    

    :param name: object name  Default value: GenericConstraintCorrection

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param solverName: name of the constraint solver  Default value: []

    :param ODESolverName: name of the ode solver  Default value: 

    :param complianceFactor: Factor applied to the position factor and velocity factor used to calculate compliance matrix  Default value: 1.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, solverName=solverName, ODESolverName=ODESolverName, complianceFactor=complianceFactor)
    return "GenericConstraintCorrection", params
