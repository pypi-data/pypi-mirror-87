# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TriangleFEMForceField

.. autofunction:: TriangleFEMForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TriangleFEMForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, initialPoints=None, method=None, poissonRatio=None, youngModulus=None, thickness=None, planeStrain=None, **kwargs):
    """
    Triangular finite elements


    :param name: object name  Default value: TriangleFEMForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param initialPoints: Initial Position  Default value: []

    :param method: large: large displacements, small: small displacements  Default value: large

    :param poissonRatio: Poisson ratio in Hooke's law  Default value: 0.3

    :param youngModulus: Young modulus in Hooke's law  Default value: 1000.0

    :param thickness: Thickness of the elements  Default value: 1.0

    :param planeStrain: Plane strain or plane stress assumption  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, initialPoints=initialPoints, method=method, poissonRatio=poissonRatio, youngModulus=youngModulus, thickness=thickness, planeStrain=planeStrain)
    return "TriangleFEMForceField", params
