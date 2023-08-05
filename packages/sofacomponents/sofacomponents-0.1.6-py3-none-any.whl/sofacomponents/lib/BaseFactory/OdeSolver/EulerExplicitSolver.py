# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component EulerExplicitSolver

.. autofunction:: EulerExplicitSolver

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def EulerExplicitSolver(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, symplectic=None, optimizedForDiagonalMatrix=None, threadSafeVisitor=None, **kwargs):
    """
    A simple explicit time integrator


    :param name: object name  Default value: EulerExplicitSolver

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param symplectic: If true, the velocities are updated before the positions and the method is symplectic (more robust). If false, the positions are updated before the velocities (standard Euler, less robust).  Default value: 1

    :param optimizedForDiagonalMatrix: If true, solution to the system Ax=b can be directly found by computing x = f/m. Must be set to false if M is sparse.  Default value: 1

    :param threadSafeVisitor: If true, do not use realloc and free visitors in fwdInteractionForceField.  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, symplectic=symplectic, optimizedForDiagonalMatrix=optimizedForDiagonalMatrix, threadSafeVisitor=threadSafeVisitor)
    return "EulerExplicitSolver", params
