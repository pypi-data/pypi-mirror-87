# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TriangularTensorMassForceField

.. autofunction:: TriangularTensorMassForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TriangularTensorMassForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, edgeInfo=None, poissonRatio=None, youngModulus=None, **kwargs):
    """
    Linear Elastic Membrane on a Triangular Mesh


    :param name: object name  Default value: TriangularTensorMassForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param edgeInfo: Internal edge data  Default value: 

    :param poissonRatio: Poisson ratio in Hooke's law  Default value: 0.3

    :param youngModulus: Young modulus in Hooke's law  Default value: 1000.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, edgeInfo=edgeInfo, poissonRatio=poissonRatio, youngModulus=youngModulus)
    return "TriangularTensorMassForceField", params
