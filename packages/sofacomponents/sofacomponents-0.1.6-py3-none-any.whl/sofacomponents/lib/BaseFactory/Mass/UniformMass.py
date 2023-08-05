# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component UniformMass

.. autofunction:: UniformMass

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def UniformMass(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, separateGravity=None, rayleighMass=None, vertexMass=None, totalMass=None, filename=None, showGravityCenter=None, showAxisSizeFactor=None, compute_mapping_inertia=None, showInitialCenterOfGravity=None, showX0=None, localRange=None, indices=None, handleTopologicalChanges=None, preserveTotalMass=None, **kwargs):
    """
    Define the same mass for all the particles
Define the same mass for all the particles
Define the same mass for all the particles


    :param name: object name  Default value: UniformMass

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param separateGravity: add separately gravity to velocity computation  Default value: 0

    :param rayleighMass: Rayleigh damping - mass matrix coefficient  Default value: 0.0

    :param vertexMass: Specify one single, positive, real value for the mass of each particle. 
If unspecified or wrongly set, the totalMass information is used.  Default value: 1.0

    :param totalMass: Specify the total mass resulting from all particles. 
If unspecified or wrongly set, the default value is used: totalMass = 1.0  Default value: 1.0

    :param filename: File storing the mass parameters [rigid objects only].  Default value: unused

    :param showGravityCenter: display the center of gravity of the system  Default value: 0

    :param showAxisSizeFactor: factor length of the axis displayed (only used for rigids)  Default value: 1.0

    :param compute_mapping_inertia: to be used if the mass is placed under a mapping  Default value: 0

    :param showInitialCenterOfGravity: display the initial center of gravity of the system  Default value: 0

    :param showX0: display the rest positions  Default value: 0

    :param localRange: optional range of local DOF indices. 
Any computation involving only indices outside of this range 
are discarded (useful for parallelization using mesh partitionning)  Default value: [[-1, -1]]

    :param indices: optional local DOF indices. Any computation involving only indices outside of this list are discarded  Default value: []

    :param handleTopologicalChanges: The mass and totalMass are recomputed on particles add/remove.  Default value: 0

    :param preserveTotalMass: Prevent totalMass from decreasing when removing particles.  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, separateGravity=separateGravity, rayleighMass=rayleighMass, vertexMass=vertexMass, totalMass=totalMass, filename=filename, showGravityCenter=showGravityCenter, showAxisSizeFactor=showAxisSizeFactor, compute_mapping_inertia=compute_mapping_inertia, showInitialCenterOfGravity=showInitialCenterOfGravity, showX0=showX0, localRange=localRange, indices=indices, handleTopologicalChanges=handleTopologicalChanges, preserveTotalMass=preserveTotalMass)
    return "UniformMass", params
