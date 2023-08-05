# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component DiagonalMass

.. autofunction:: DiagonalMass

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def DiagonalMass(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, separateGravity=None, rayleighMass=None, vertexMass=None, massDensity=None, totalMass=None, computeMassOnRest=None, showGravityCenter=None, showAxisSizeFactor=None, filename=None, **kwargs):
    """
    Define a specific mass for each particle


    :param name: object name  Default value: DiagonalMass

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
If unspecified or wrongly set, the massDensity or totalMass information is used.  Default value: []

    :param massDensity: Specify one single real and positive value for the mass density. 
If unspecified or wrongly set, the totalMass information is used.  Default value: 1.0

    :param totalMass: Specify the total mass resulting from all particles. 
If unspecified or wrongly set, the default value is used: totalMass = 1.0  Default value: 1.0

    :param computeMassOnRest: If true, the mass of every element is computed based on the rest position rather than the position  Default value: 1

    :param showGravityCenter: Display the center of gravity of the system  Default value: 0

    :param showAxisSizeFactor: Factor length of the axis displayed (only used for rigids)  Default value: 1.0

    :param filename: Xsp3.0 file to specify the mass parameters  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, separateGravity=separateGravity, rayleighMass=rayleighMass, vertexMass=vertexMass, massDensity=massDensity, totalMass=totalMass, computeMassOnRest=computeMassOnRest, showGravityCenter=showGravityCenter, showAxisSizeFactor=showAxisSizeFactor, filename=filename)
    return "DiagonalMass", params
