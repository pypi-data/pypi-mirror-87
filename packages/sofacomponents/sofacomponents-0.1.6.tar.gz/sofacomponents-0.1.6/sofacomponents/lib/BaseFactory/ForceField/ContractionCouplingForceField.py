# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ContractionCouplingForceField

.. autofunction:: ContractionCouplingForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ContractionCouplingForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, tetraInfo=None, tetraContractivityParam=None, depolarisationTimes=None, uniquedepolarisationTimes=None, APD=None, APDVT=None, TdVT=None, withVT=None, useVerdandi=None, n0=None, alpha=None, StarlingEffect=None, n1=None, n2=None, tagMechanics=None, useSimple=None, withFile=None, file=None, **kwargs):
    """
    Coupling for contraction on heart


    :param name: object name  Default value: ContractionCouplingForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param tetraInfo: Data to handle topology on tetrahedra  Default value: 

    :param tetraContractivityParam: <Contractivity,stiffness,contractionRate,relaxationrate> by tetra  Default value: []

    :param depolarisationTimes: depolarisationTimes at each node  Default value: []

    :param uniquedepolarisationTimes: depolarisationTimes at each node  Default value: 0.0

    :param APD: APD at each node  Default value: []

    :param APDVT: APDVT  Default value: []

    :param TdVT: TdVT  Default value: []

    :param withVT: if VT TD are used  Default value: 0

    :param useVerdandi: if used with verdandi  Default value: 0

    :param n0: reduction parameter between 0 and 1  Default value: 0.0

    :param alpha: alpha  Default value: 0.0

    :param StarlingEffect: if used with verdandi  Default value: 0

    :param n1: reduction parameter between 0 and 1  Default value: 0.0

    :param n2: reduction parameter between 0 and 1  Default value: 0.0

    :param tagMechanics: Tag of the Mechanical Object  Default value: meca

    :param useSimple: If the model should be simplified  Default value: 0

    :param withFile: if the electrophysiology is precomputed  Default value: 0

    :param file: File where to store the Monitoring  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, tetraInfo=tetraInfo, tetraContractivityParam=tetraContractivityParam, depolarisationTimes=depolarisationTimes, uniquedepolarisationTimes=uniquedepolarisationTimes, APD=APD, APDVT=APDVT, TdVT=TdVT, withVT=withVT, useVerdandi=useVerdandi, n0=n0, alpha=alpha, StarlingEffect=StarlingEffect, n1=n1, n2=n2, tagMechanics=tagMechanics, useSimple=useSimple, withFile=withFile, file=file)
    return "ContractionCouplingForceField", params
