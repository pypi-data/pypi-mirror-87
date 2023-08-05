# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TetrahedralCorotationalFEMForceField

.. autofunction:: TetrahedralCorotationalFEMForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TetrahedralCorotationalFEMForceField(self, poissonRatio=None, youngModulus=None, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, tetrahedronInfo=None, method=None, localStiffnessFactor=None, updateStiffnessMatrix=None, computeGlobalMatrix=None, drawing=None, drawColor1=None, drawColor2=None, drawColor3=None, drawColor4=None, **kwargs):
    """
    Corotational FEM Tetrahedral finite elements


    :param name: object name  Default value: TetrahedralCorotationalFEMForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param tetrahedronInfo: Internal tetrahedron data  Default value: 

    :param method: "small", "large" (by QR) or "polar" displacements  Default value: large

    :param poissonRatio: FEM Poisson Ratio  Default value: 0.449999988079

    :param youngModulus: FEM Young Modulus  Default value: 5000.0

    :param localStiffnessFactor: Allow specification of different stiffness per element. If there are N element and M values are specified, the youngModulus factor for element i would be localStiffnessFactor[i*M/N]  Default value: []

    :param updateStiffnessMatrix: (No help available)  Default value: 0

    :param computeGlobalMatrix: (No help available)  Default value: 0

    :param drawing:  draw the forcefield if true  Default value: 1

    :param drawColor1:  draw color for faces 1  Default value: [[0.0, 0.0, 1.0, 1.0]]

    :param drawColor2:  draw color for faces 2  Default value: [[0.0, 0.5, 1.0, 1.0]]

    :param drawColor3:  draw color for faces 3  Default value: [[0.0, 1.0, 1.0, 1.0]]

    :param drawColor4:  draw color for faces 4  Default value: [[0.5, 1.0, 1.0, 1.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, tetrahedronInfo=tetrahedronInfo, method=method, poissonRatio=poissonRatio, youngModulus=youngModulus, localStiffnessFactor=localStiffnessFactor, updateStiffnessMatrix=updateStiffnessMatrix, computeGlobalMatrix=computeGlobalMatrix, drawing=drawing, drawColor1=drawColor1, drawColor2=drawColor2, drawColor3=drawColor3, drawColor4=drawColor4)
    return "TetrahedralCorotationalFEMForceField", params
