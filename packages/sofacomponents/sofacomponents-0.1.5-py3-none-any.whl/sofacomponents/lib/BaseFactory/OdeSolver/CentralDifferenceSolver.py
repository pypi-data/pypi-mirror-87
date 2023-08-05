# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component CentralDifferenceSolver

.. autofunction:: CentralDifferenceSolver

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def CentralDifferenceSolver(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, rayleighMass=None, threadSafeVisitor=None, **kwargs):
    """
    Explicit time integrator using central difference (also known as Verlet of Leap-frop)


    :param name: object name  Default value: CentralDifferenceSolver

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param rayleighMass: Rayleigh damping coefficient related to mass  Default value: 0.0

    :param threadSafeVisitor: If true, do not use realloc and free visitors in fwdInteractionForceField.  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, rayleighMass=rayleighMass, threadSafeVisitor=threadSafeVisitor)
    return "CentralDifferenceSolver", params
