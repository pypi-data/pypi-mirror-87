# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component FlexibleCorotationalFEMForceField

.. autofunction:: FlexibleCorotationalFEMForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def FlexibleCorotationalFEMForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, nbRef=None, position=None, tolerance=None, method=None, order=None, youngModulus=None, poissonRatio=None, viscosity=None, geometricStiffness=None, **kwargs):
    """
    Flexible Tetrahedral finite elements


    :param name: object name  Default value: FlexibleCorotationalFEMForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param nbRef: maximum number of parents per child  Default value: 4

    :param position: position of parent nodes  Default value: []

    :param tolerance: minimum weight (allows for mapping outside elements)  Default value: -1.0

    :param method: Decomposition method  Default value: svd

    :param order: Order of quadrature method  Default value: 1

    :param youngModulus: Young Modulus  Default value: 5000.0

    :param poissonRatio: Poisson Ratio  Default value: 0.0

    :param viscosity: Viscosity (stress/strainRate)  Default value: 0.0

    :param geometricStiffness: Should geometricStiffness be considered?  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, nbRef=nbRef, position=position, tolerance=tolerance, method=method, order=order, youngModulus=youngModulus, poissonRatio=poissonRatio, viscosity=viscosity, geometricStiffness=geometricStiffness)
    return "FlexibleCorotationalFEMForceField", params
