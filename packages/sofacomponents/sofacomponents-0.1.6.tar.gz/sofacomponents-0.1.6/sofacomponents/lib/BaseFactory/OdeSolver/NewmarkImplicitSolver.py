# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component NewmarkImplicitSolver

.. autofunction:: NewmarkImplicitSolver

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def NewmarkImplicitSolver(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, rayleighStiffness=None, rayleighMass=None, vdamping=None, gamma=None, beta=None, threadSafeVisitor=None, **kwargs):
    """
    Implicit time integratorusing Newmark scheme


    :param name: object name  Default value: NewmarkImplicitSolver

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param rayleighStiffness: Rayleigh damping coefficient related to stiffness  Default value: 0.0

    :param rayleighMass: Rayleigh damping coefficient related to mass  Default value: 0.0

    :param vdamping: Velocity decay coefficient (no decay if null)  Default value: 0.0

    :param gamma: Newmark scheme gamma coefficient  Default value: 0.5

    :param beta: Newmark scheme beta coefficient  Default value: 0.25

    :param threadSafeVisitor: If true, do not use realloc and free visitors in fwdInteractionForceField.  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, rayleighStiffness=rayleighStiffness, rayleighMass=rayleighMass, vdamping=vdamping, gamma=gamma, beta=beta, threadSafeVisitor=threadSafeVisitor)
    return "NewmarkImplicitSolver", params
