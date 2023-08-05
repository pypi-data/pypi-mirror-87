# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TriangularFEMForceFieldOptim

.. autofunction:: TriangularFEMForceFieldOptim

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TriangularFEMForceFieldOptim(self, poissonRatio=None, youngModulus=None, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, triangleInfo=None, triangleState=None, vertexInfo=None, edgeInfo=None, damping=None, restScale=None, showStressVector=None, showStressMaxValue=None, **kwargs):
    """
    Corotational Triangular finite elements


    :param name: object name  Default value: TriangularFEMForceFieldOptim

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param triangleInfo: Internal triangle data (persistent)  Default value: 

    :param triangleState: Internal triangle data (time-dependent)  Default value: 

    :param vertexInfo: Internal point data  Default value: 

    :param edgeInfo: Internal edge data  Default value: 

    :param poissonRatio: Poisson ratio in Hooke's law  Default value: 0.45

    :param youngModulus: Young modulus in Hooke's law  Default value: 1000.0

    :param damping: Ratio damping/stiffness  Default value: 0.0

    :param restScale: Scale factor applied to rest positions (to simulate pre-stretched materials)  Default value: 1.0

    :param showStressVector: Flag activating rendering of stress directions within each triangle  Default value: 0

    :param showStressMaxValue: Max value for rendering of stress values  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, triangleInfo=triangleInfo, triangleState=triangleState, vertexInfo=vertexInfo, edgeInfo=edgeInfo, poissonRatio=poissonRatio, youngModulus=youngModulus, damping=damping, restScale=restScale, showStressVector=showStressVector, showStressMaxValue=showStressMaxValue)
    return "TriangularFEMForceFieldOptim", params
