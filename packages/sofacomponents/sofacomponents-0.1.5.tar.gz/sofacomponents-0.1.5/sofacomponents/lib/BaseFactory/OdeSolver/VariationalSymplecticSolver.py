# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component VariationalSymplecticSolver

.. autofunction:: VariationalSymplecticSolver

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def VariationalSymplecticSolver(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, newtonError=None, steps=None, rayleighStiffness=None, rayleighMass=None, verbose=None, saveEnergyInFile=None, explicitIntegration=None, file=None, computeHamiltonian=None, hamiltonianEnergy=None, useIncrementalPotentialEnergy=None, threadSafeVisitor=None, **kwargs):
    """
    Implicit time integrator which conserves linear momentum and mechanical energy


    :param name: object name  Default value: VariationalSymplecticSolver

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param newtonError: Error tolerance for Newton iterations  Default value: 0.01

    :param steps: Maximum number of Newton steps  Default value: 5

    :param rayleighStiffness: Rayleigh damping coefficient related to stiffness, > 0  Default value: 0.0

    :param rayleighMass: Rayleigh damping coefficient related to mass, > 0  Default value: 0.0

    :param verbose: Dump information on the residual errors and number of Newton iterations  Default value: 0

    :param saveEnergyInFile: If kinetic and potential energies should be dumped in a CSV file at each iteration  Default value: 0

    :param explicitIntegration: Use explicit integration scheme  Default value: 0

    :param file: File name where kinetic and potential energies are saved in a CSV file  Default value: 

    :param computeHamiltonian: Compute hamiltonian  Default value: 1

    :param hamiltonianEnergy: hamiltonian energy  Default value: 0.0

    :param useIncrementalPotentialEnergy: use real potential energy, if false use approximate potential energy  Default value: 1

    :param threadSafeVisitor: If true, do not use realloc and free visitors in fwdInteractionForceField.  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, newtonError=newtonError, steps=steps, rayleighStiffness=rayleighStiffness, rayleighMass=rayleighMass, verbose=verbose, saveEnergyInFile=saveEnergyInFile, explicitIntegration=explicitIntegration, file=file, computeHamiltonian=computeHamiltonian, hamiltonianEnergy=hamiltonianEnergy, useIncrementalPotentialEnergy=useIncrementalPotentialEnergy, threadSafeVisitor=threadSafeVisitor)
    return "VariationalSymplecticSolver", params
