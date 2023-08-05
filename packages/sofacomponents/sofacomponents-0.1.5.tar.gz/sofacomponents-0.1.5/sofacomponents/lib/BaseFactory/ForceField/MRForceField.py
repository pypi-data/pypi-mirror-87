# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MRForceField

.. autofunction:: MRForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MRForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, ParameterSet=None, matrixRegularization=None, file=None, useVerdandi=None, depolarisationTimes=None, APD=None, activeRelaxation=None, MaxPeakActiveRelaxation=None, heartPeriod=None, calculateStress=None, MRStressPK=None, tetrahedronInfo=None, edgeInfo=None, **kwargs):
    """
    MR's law in Tetrahedral finite elements


    :param name: object name  Default value: MRForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param ParameterSet: The global parameters specifying the Mooney-rivlin material  Default value: []

    :param matrixRegularization: Regularization of the Stiffness Matrix (true or false)  Default value: 0

    :param file: File where to store the Jacobian  Default value: 

    :param useVerdandi: useVerdandi  Default value: 0

    :param depolarisationTimes: depolarisationTimes at each node  Default value: []

    :param APD: APD at each node  Default value: []

    :param activeRelaxation: Use or not an active relaxation triggering after the end of depolarisation  Default value: 0

    :param MaxPeakActiveRelaxation: Multiplicative factor in front of each c1 c2 I in active realxation  Default value: 5.0

    :param heartPeriod: heart Period  Default value: 0.0

    :param calculateStress: set to 1 for calculating the cauchy stress  Default value: 0

    :param MRStressPK: Second Piola-Kirshoff stress from MR part (= passive part)  Default value: []

    :param tetrahedronInfo: Data to handle topology on tetrahedra  Default value: 

    :param edgeInfo: Data to handle topology on edges  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, ParameterSet=ParameterSet, matrixRegularization=matrixRegularization, file=file, useVerdandi=useVerdandi, depolarisationTimes=depolarisationTimes, APD=APD, activeRelaxation=activeRelaxation, MaxPeakActiveRelaxation=MaxPeakActiveRelaxation, heartPeriod=heartPeriod, calculateStress=calculateStress, MRStressPK=MRStressPK, tetrahedronInfo=tetrahedronInfo, edgeInfo=edgeInfo)
    return "MRForceField", params
