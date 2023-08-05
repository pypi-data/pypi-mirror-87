# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TetrahedronFEMForceField

.. autofunction:: TetrahedronFEMForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TetrahedronFEMForceField(self, poissonRatio=None, youngModulus=None, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, initialPoints=None, method=None, localStiffnessFactor=None, updateStiffnessMatrix=None, computeGlobalMatrix=None, plasticMaxThreshold=None, plasticYieldThreshold=None, plasticCreep=None, gatherPt=None, gatherBsize=None, drawHeterogeneousTetra=None, drawAsEdges=None, computeVonMisesStress=None, vonMisesPerElement=None, vonMisesPerNode=None, vonMisesStressColors=None, showStressColorMap=None, showStressAlpha=None, showVonMisesStressPerNode=None, updateStiffness=None, **kwargs):
    """
    Tetrahedral finite elements


    :param name: object name  Default value: TetrahedronFEMForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param initialPoints: Initial Position  Default value: []

    :param method: "small", "large" (by QR), "polar" or "svd" displacements  Default value: large

    :param poissonRatio: FEM Poisson Ratio [0,0.5[  Default value: 0.449999988079

    :param youngModulus: FEM Young Modulus  Default value: [[5000.0]]

    :param localStiffnessFactor: Allow specification of different stiffness per element. If there are N element and M values are specified, the youngModulus factor for element i would be localStiffnessFactor[i*M/N]  Default value: []

    :param updateStiffnessMatrix: (No help available)  Default value: 0

    :param computeGlobalMatrix: (No help available)  Default value: 0

    :param plasticMaxThreshold: Plastic Max Threshold (2-norm of the strain)  Default value: 0.0

    :param plasticYieldThreshold: Plastic Yield Threshold (2-norm of the strain)  Default value: 9.99999974738e-05

    :param plasticCreep: Plastic Creep Factor * dt [0,1]. Warning this factor depends on dt.  Default value: 0.899999976158

    :param gatherPt: number of dof accumulated per threads during the gather operation (Only use in GPU version)  Default value:  

    :param gatherBsize: number of dof accumulated per threads during the gather operation (Only use in GPU version)  Default value:  

    :param drawHeterogeneousTetra: Draw Heterogeneous Tetra in different color  Default value: 0

    :param drawAsEdges: Draw as edges instead of tetrahedra  Default value: 0

    :param computeVonMisesStress: compute and display von Mises stress: 0: no computations, 1: using corotational strain, 2: using full Green strain  Default value: 0

    :param vonMisesPerElement: von Mises Stress per element  Default value: []

    :param vonMisesPerNode: von Mises Stress per node  Default value: []

    :param vonMisesStressColors: Vector of colors describing the VonMises stress  Default value: []

    :param showStressColorMap: Color map used to show stress values  Default value: 

    :param showStressAlpha: Alpha for vonMises visualisation  Default value: 1.0

    :param showVonMisesStressPerNode: draw points  showing vonMises stress interpolated in nodes  Default value: 0

    :param updateStiffness: udpate structures (precomputed in init) using stiffness parameters in each iteration (set listening=1)  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, initialPoints=initialPoints, method=method, poissonRatio=poissonRatio, youngModulus=youngModulus, localStiffnessFactor=localStiffnessFactor, updateStiffnessMatrix=updateStiffnessMatrix, computeGlobalMatrix=computeGlobalMatrix, plasticMaxThreshold=plasticMaxThreshold, plasticYieldThreshold=plasticYieldThreshold, plasticCreep=plasticCreep, gatherPt=gatherPt, gatherBsize=gatherBsize, drawHeterogeneousTetra=drawHeterogeneousTetra, drawAsEdges=drawAsEdges, computeVonMisesStress=computeVonMisesStress, vonMisesPerElement=vonMisesPerElement, vonMisesPerNode=vonMisesPerNode, vonMisesStressColors=vonMisesStressColors, showStressColorMap=showStressColorMap, showStressAlpha=showStressAlpha, showVonMisesStressPerNode=showVonMisesStressPerNode, updateStiffness=updateStiffness)
    return "TetrahedronFEMForceField", params
