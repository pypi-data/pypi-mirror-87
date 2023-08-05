# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component LennardJonesForceField

.. autofunction:: LennardJonesForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def LennardJonesForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, aInit=None, alpha=None, beta=None, dmax=None, fmax=None, d0=None, p0=None, damping=None, **kwargs):
    """
    Lennard-Jones forces for fluids


    :param name: object name  Default value: LennardJonesForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param aInit: a for Gravitational FF which corresponds to G*m1*m2 alpha should be equal to 1 and beta to 0.  Default value: 0.0

    :param alpha: Alpha  Default value: 6.0

    :param beta: Beta  Default value: 12.0

    :param dmax: DMax  Default value: 2.0

    :param fmax: FMax  Default value: 1.0

    :param d0: d0  Default value: 1.0

    :param p0: p0  Default value: 1.0

    :param damping: Damping  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, aInit=aInit, alpha=alpha, beta=beta, dmax=dmax, fmax=fmax, d0=d0, p0=p0, damping=damping)
    return "LennardJonesForceField", params
