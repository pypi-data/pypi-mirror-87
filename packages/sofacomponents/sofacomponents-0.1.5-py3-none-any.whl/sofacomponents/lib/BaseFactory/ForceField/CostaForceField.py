# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component CostaForceField

.. autofunction:: CostaForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def CostaForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, matrixRegularization=None, tensorDirections=None, fiberDirections=None, ParameterSet=None, tetrahedronInfo=None, edgeInfo=None, file=None, **kwargs):
    """
    Costa's law in Tetrahedral finite elements


    :param name: object name  Default value: CostaForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param matrixRegularization: Regularization of the Stiffness Matrix (true or false)  Default value: 0

    :param tensorDirections:  file with DTI tensor at each tetra  Default value: []

    :param fiberDirections:  file with fibers at each tetra  Default value: []

    :param ParameterSet: The global parameters specifying the material  Default value: []

    :param tetrahedronInfo: Data to handle topology on tetrahedra  Default value: 

    :param edgeInfo: Data to handle topology on edges  Default value: 

    :param file: File where to store the Jacobian  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, matrixRegularization=matrixRegularization, tensorDirections=tensorDirections, fiberDirections=fiberDirections, ParameterSet=ParameterSet, tetrahedronInfo=tetrahedronInfo, edgeInfo=edgeInfo, file=file)
    return "CostaForceField", params
