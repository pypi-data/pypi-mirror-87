# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TriangularFEMForceField

.. autofunction:: TriangularFEMForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TriangularFEMForceField(self, poissonRatio=None, youngModulus=None, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, triangleInfo=None, vertexInfo=None, edgeInfo=None, method=None, damping=None, rotatedInitialElements=None, initialTransformation=None, fracturable=None, hosfordExponant=None, criteriaValue=None, showStressValue=None, showStressVector=None, showFracturableTriangles=None, computePrincipalStress=None, **kwargs):
    """
    Corotational Triangular finite elements


    :param name: object name  Default value: TriangularFEMForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param triangleInfo: Internal triangle data  Default value: 

    :param vertexInfo: Internal point data  Default value: 

    :param edgeInfo: Internal edge data  Default value: 

    :param method: large: large displacements, small: small displacements  Default value: large

    :param poissonRatio: Poisson ratio in Hooke's law (vector)  Default value: [[0.45]]

    :param youngModulus: Young modulus in Hooke's law (vector)  Default value: [[1000.0]]

    :param damping: Ratio damping/stiffness  Default value: 0.0

    :param rotatedInitialElements: Flag activating rendering of stress directions within each triangle  Default value: []

    :param initialTransformation: Flag activating rendering of stress directions within each triangle  Default value: []

    :param fracturable: the forcefield computes the next fracturable Edge  Default value: 0

    :param hosfordExponant: Exponant in the Hosford yield criteria  Default value: 1.0

    :param criteriaValue: Fracturable threshold used to draw fracturable triangles  Default value: 1e+15

    :param showStressValue: Flag activating rendering of stress values as a color in each triangle  Default value: 0

    :param showStressVector: Flag activating rendering of stress directions within each triangle  Default value: 0

    :param showFracturableTriangles: Flag activating rendering of triangles to fracture  Default value: 0

    :param computePrincipalStress: Compute principal stress for each triangle  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, triangleInfo=triangleInfo, vertexInfo=vertexInfo, edgeInfo=edgeInfo, method=method, poissonRatio=poissonRatio, youngModulus=youngModulus, damping=damping, rotatedInitialElements=rotatedInitialElements, initialTransformation=initialTransformation, fracturable=fracturable, hosfordExponant=hosfordExponant, criteriaValue=criteriaValue, showStressValue=showStressValue, showStressVector=showStressVector, showFracturableTriangles=showFracturableTriangles, computePrincipalStress=computePrincipalStress)
    return "TriangularFEMForceField", params
