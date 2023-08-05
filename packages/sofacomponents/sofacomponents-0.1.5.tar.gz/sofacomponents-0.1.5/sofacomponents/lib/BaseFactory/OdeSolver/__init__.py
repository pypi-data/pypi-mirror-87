# -*- coding: utf-8 -*-


"""
Module OdeSolver

Content of the module
**********************

Summary:
========
.. autosummary::
     :toctree: _autosummary

    EulerImplicitSolver

    RungeKutta2Solver

    CentralDifferenceSolver

    StaticSolver

    DampVelocitySolver

    RungeKutta4Solver

    NewmarkImplicitSolver

    VariationalSymplecticSolver

    EulerExplicitSolver



Content:
========

.. automodule::

    EulerImplicitSolver

    RungeKutta2Solver

    CentralDifferenceSolver

    StaticSolver

    DampVelocitySolver

    RungeKutta4Solver

    NewmarkImplicitSolver

    VariationalSymplecticSolver

    EulerExplicitSolver



Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
# __all__=['EulerImplicitSolver', 'RungeKutta2Solver', 'CentralDifferenceSolver', 'StaticSolver', 'DampVelocitySolver', 'RungeKutta4Solver', 'NewmarkImplicitSolver', 'VariationalSymplecticSolver', 'EulerExplicitSolver']
class OdeSolver:
    from .EulerImplicitSolver import EulerImplicitSolver
    from .RungeKutta2Solver import RungeKutta2Solver
    from .CentralDifferenceSolver import CentralDifferenceSolver
    from .StaticSolver import StaticSolver
    from .DampVelocitySolver import DampVelocitySolver
    from .RungeKutta4Solver import RungeKutta4Solver
    from .NewmarkImplicitSolver import NewmarkImplicitSolver
    from .VariationalSymplecticSolver import VariationalSymplecticSolver
    from .EulerExplicitSolver import EulerExplicitSolver
