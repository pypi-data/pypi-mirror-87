# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component NonUniformHexahedralFEMForceFieldAndMass

.. autofunction:: NonUniformHexahedralFEMForceFieldAndMass

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def NonUniformHexahedralFEMForceFieldAndMass(self, poissonRatio=None, youngModulus=None, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, separateGravity=None, rayleighMass=None, method=None, hexahedronInfo=None, density=None, lumpedMass=None, massMatrices=None, totalMass=None, particleMasses=None, lumpedMasses=None, recursive=None, useMBK=None, **kwargs):
    """
    Non uniform Hexahedral finite elements


    :param name: object name  Default value: NonUniformHexahedralFEMForceFieldAndMass

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param separateGravity: add separately gravity to velocity computation  Default value: 0

    :param rayleighMass: Rayleigh damping - mass matrix coefficient  Default value: 0.0

    :param method: "large" or "polar" displacements  Default value: large

    :param poissonRatio: (No help available)  Default value: 0.449999988079

    :param youngModulus: (No help available)  Default value: 5000.0

    :param hexahedronInfo: Internal hexahedron data  Default value: 

    :param density: density == volumetric mass in english (kg.m-3)  Default value: 1.0

    :param lumpedMass: Does it use lumped masses?  Default value: 0

    :param massMatrices: Mass matrices per element (M_i)  Default value: []

    :param totalMass: Total mass per element  Default value: []

    :param particleMasses: Mass per particle  Default value: []

    :param lumpedMasses: Lumped masses  Default value: []

    :param recursive: Use recursive matrix computation  Default value: 0

    :param useMBK: compute MBK and use it in addMBKdx, instead of using addDForce and addMDx.  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, separateGravity=separateGravity, rayleighMass=rayleighMass, method=method, poissonRatio=poissonRatio, youngModulus=youngModulus, hexahedronInfo=hexahedronInfo, density=density, lumpedMass=lumpedMass, massMatrices=massMatrices, totalMass=totalMass, particleMasses=particleMasses, lumpedMasses=lumpedMasses, recursive=recursive, useMBK=useMBK)
    return "NonUniformHexahedralFEMForceFieldAndMass", params
