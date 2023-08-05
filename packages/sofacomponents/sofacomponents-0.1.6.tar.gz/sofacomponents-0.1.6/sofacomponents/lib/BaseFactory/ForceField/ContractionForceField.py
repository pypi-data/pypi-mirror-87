# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ContractionForceField

.. autofunction:: ContractionForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ContractionForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, viscosityParameter=None, heartPeriod=None, addElastometry=None, useCoupling=None, useVerdandi=None, DesactivateElastoIfNoElec=None, tagContraction=None, tagSolver=None, elasticModulus=None, tetraPloted=None, graph=None, graph2=None, fiberDirections=None, tetraContractivityParam=None, depolarisationTimes=None, APD=None, calculateStress=None, stressFile=None, SecSPK_passive=None, tetrahedronInfo=None, edgeInfo=None, file=None, **kwargs):
    """
    Contraction Force for heart beating


    :param name: object name  Default value: ContractionForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param viscosityParameter: for passive relaxation  Default value: 0.0

    :param heartPeriod: heart Period  Default value: 0.0

    :param addElastometry: If we want the elastic component in series  Default value: 0

    :param useCoupling: if the contraction is couple  Default value: 0

    :param useVerdandi: useVerdandi  Default value: 0

    :param DesactivateElastoIfNoElec: set to 1 for calculating the cauchy stress  Default value: 0

    :param tagContraction: Tag of the contraction node  Default value: tagContraction

    :param tagSolver: Tag of the Solver Object  Default value: solver

    :param elasticModulus: modulus for the elastic component in series  Default value: 0.0

    :param tetraPloted: tetra index of values display in graph for each iteration.  Default value: 0

    :param graph: Vertex state value per iteration  Default value: 

    :param graph2: Vertex state value per iteration  Default value: 

    :param fiberDirections:  file with fibers at each tetra  Default value: []

    :param tetraContractivityParam: <Contractivity,contractionRate,relaxationrate> by tetra  Default value: []

    :param depolarisationTimes: depolarisationTimes at each node  Default value: []

    :param APD: APD at each node  Default value: []

    :param calculateStress: set to 1 for calculating the cauchy stress  Default value: 0

    :param stressFile: name of the output cauchy stress file  Default value: CauchyStress.txt

    :param SecSPK_passive: second piola kirshoff tensor of passive part  Default value: []

    :param tetrahedronInfo: Data to handle topology on tetrahedra  Default value: 

    :param edgeInfo: Data to handle topology on edges  Default value: 

    :param file: File where to store the Monitoring  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, viscosityParameter=viscosityParameter, heartPeriod=heartPeriod, addElastometry=addElastometry, useCoupling=useCoupling, useVerdandi=useVerdandi, DesactivateElastoIfNoElec=DesactivateElastoIfNoElec, tagContraction=tagContraction, tagSolver=tagSolver, elasticModulus=elasticModulus, tetraPloted=tetraPloted, graph=graph, graph2=graph2, fiberDirections=fiberDirections, tetraContractivityParam=tetraContractivityParam, depolarisationTimes=depolarisationTimes, APD=APD, calculateStress=calculateStress, stressFile=stressFile, SecSPK_passive=SecSPK_passive, tetrahedronInfo=tetrahedronInfo, edgeInfo=edgeInfo, file=file)
    return "ContractionForceField", params
