# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MeshMatrixMass

.. autofunction:: MeshMatrixMass

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MeshMatrixMass(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, separateGravity=None, rayleighMass=None, vertexMass=None, massDensity=None, totalMass=None, vertexMassInfo=None, edgeMassInfo=None, edgeMass=None, computeMassOnRest=None, showGravityCenter=None, showAxisSizeFactor=None, lumping=None, printMass=None, graph=None, **kwargs):
    """
    Define a specific mass for each particle


    :param name: object name  Default value: MeshMatrixMass

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param separateGravity: add separately gravity to velocity computation  Default value: 0

    :param rayleighMass: Rayleigh damping - mass matrix coefficient  Default value: 0.0

    :param vertexMass: Specify a vector giving the mass of each vertex. 
If unspecified or wrongly set, another mass information is used.  Default value: []

    :param massDensity: Specify real and strictly positive value(s) for the mass density. 
If unspecified or wrongly set, the totalMass information is used.  Default value: []

    :param totalMass: Specify the total mass resulting from all particles. 
If unspecified or wrongly set, the default value is used: totalMass = 1.0  Default value: 1.0

    :param vertexMassInfo: internal values of the particles masses on vertices, supporting topological changes  Default value: []

    :param edgeMassInfo: internal values of the particles masses on edges, supporting topological changes  Default value: []

    :param edgeMass: values of the particles masses on edges  Default value: []

    :param computeMassOnRest: If true, the mass of every element is computed based on the rest position rather than the position  Default value: 0

    :param showGravityCenter: display the center of gravity of the system  Default value: 0

    :param showAxisSizeFactor: factor length of the axis displayed (only used for rigids)  Default value: 1.0

    :param lumping: boolean if you need to use a lumped mass matrix  Default value: 0

    :param printMass: boolean if you want to check the mass conservation  Default value: 0

    :param graph: Graph of the controlled potential  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, separateGravity=separateGravity, rayleighMass=rayleighMass, vertexMass=vertexMass, massDensity=massDensity, totalMass=totalMass, vertexMassInfo=vertexMassInfo, edgeMassInfo=edgeMassInfo, edgeMass=edgeMass, computeMassOnRest=computeMassOnRest, showGravityCenter=showGravityCenter, showAxisSizeFactor=showAxisSizeFactor, lumping=lumping, printMass=printMass, graph=graph)
    return "MeshMatrixMass", params
