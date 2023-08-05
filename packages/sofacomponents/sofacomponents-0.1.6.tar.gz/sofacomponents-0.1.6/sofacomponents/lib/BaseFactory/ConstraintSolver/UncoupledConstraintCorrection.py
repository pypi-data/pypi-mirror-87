# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component UncoupledConstraintCorrection

.. autofunction:: UncoupledConstraintCorrection

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def UncoupledConstraintCorrection(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, compliance=None, defaultCompliance=None, verbose=None, correctionVelocityFactor=None, correctionPositionFactor=None, useOdeSolverIntegrationFactors=None, **kwargs):
    """
    Component computing constraint forces within a simulated body using the compliance method.
Component computing contact forces within a simulated body using the compliance method.
Component computing contact forces within a simulated body using the compliance method.


    :param name: object name  Default value: UncoupledConstraintCorrection

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param compliance: compliance value on each dof. If Rigid compliance (7 values): 1st value for translations, 6 others for upper-triangular part of symmetric 3x3 rotation compliance matrix  Default value: []

    :param defaultCompliance: Default compliance value for new dof or if all should have the same (in which case compliance vector should be empty)  Default value: 1e-05

    :param verbose: Dump the constraint matrix at each iteration  Default value: 0

    :param correctionVelocityFactor: Factor applied to the constraint forces when correcting the velocities  Default value: 1.0

    :param correctionPositionFactor: Factor applied to the constraint forces when correcting the positions  Default value: 1.0

    :param useOdeSolverIntegrationFactors: Use odeSolver integration factors instead of correctionVelocityFactor and correctionPositionFactor  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, compliance=compliance, defaultCompliance=defaultCompliance, verbose=verbose, correctionVelocityFactor=correctionVelocityFactor, correctionPositionFactor=correctionPositionFactor, useOdeSolverIntegrationFactors=useOdeSolverIntegrationFactors)
    return "UncoupledConstraintCorrection", params
