# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TriangularBiquadraticSpringsForceField

.. autofunction:: TriangularBiquadraticSpringsForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TriangularBiquadraticSpringsForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, triangleInfo=None, edgeInfo=None, initialPoints=None, poissonRatio=None, youngModulus=None, dampingRatio=None, useAngularSprings=None, compressible=None, matrixRegularization=None, **kwargs):
    """
    Biquadratic Springs on a Triangular Mesh


    :param name: object name  Default value: TriangularBiquadraticSpringsForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param triangleInfo: Internal triangle data  Default value: 

    :param edgeInfo: Internal edge data  Default value: 

    :param initialPoints: Initial Position  Default value: []

    :param poissonRatio: Poisson ratio in Hooke's law  Default value: 0.3

    :param youngModulus: Young modulus in Hooke's law  Default value: 1000.0

    :param dampingRatio: Ratio damping/stiffness  Default value: 0.0

    :param useAngularSprings: If Angular Springs should be used or not  Default value: 1

    :param compressible: If additional energy penalizing compressibility should be used  Default value: 1

    :param matrixRegularization: Regularization of the Stiffnes Matrix (between 0 and 1)  Default value: 0.4


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, triangleInfo=triangleInfo, edgeInfo=edgeInfo, initialPoints=initialPoints, poissonRatio=poissonRatio, youngModulus=youngModulus, dampingRatio=dampingRatio, useAngularSprings=useAngularSprings, compressible=compressible, matrixRegularization=matrixRegularization)
    return "TriangularBiquadraticSpringsForceField", params
