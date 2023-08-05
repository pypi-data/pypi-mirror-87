# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component HexahedronFEMForceField

.. autofunction:: HexahedronFEMForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def HexahedronFEMForceField(self, poissonRatio=None, youngModulus=None, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, method=None, updateStiffnessMatrix=None, assembling=None, gatherPt=None, gatherBsize=None, drawing=None, drawPercentageOffset=None, stiffnessMatrices=None, initialPoints=None, **kwargs):
    """
    Hexahedral finite elements


    :param name: object name  Default value: HexahedronFEMForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param method: "large" or "polar" or "small" displacements  Default value: large

    :param poissonRatio: (No help available)  Default value: 0.449999988079

    :param youngModulus: (No help available)  Default value: 5000.0

    :param updateStiffnessMatrix: (No help available)  Default value: 0

    :param assembling: (No help available)  Default value: 0

    :param gatherPt: number of dof accumulated per threads during the gather operation (Only use in GPU version)  Default value:  

    :param gatherBsize: number of dof accumulated per threads during the gather operation (Only use in GPU version)  Default value:  

    :param drawing:  draw the forcefield if true  Default value: 1

    :param drawPercentageOffset: size of the hexa  Default value: 0.15

    :param stiffnessMatrices: Stiffness matrices per element (K_i)  Default value: []

    :param initialPoints: Initial Position  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, method=method, poissonRatio=poissonRatio, youngModulus=youngModulus, updateStiffnessMatrix=updateStiffnessMatrix, assembling=assembling, gatherPt=gatherPt, gatherBsize=gatherBsize, drawing=drawing, drawPercentageOffset=drawPercentageOffset, stiffnessMatrices=stiffnessMatrices, initialPoints=initialPoints)
    return "HexahedronFEMForceField", params
