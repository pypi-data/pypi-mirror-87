# -*- coding: utf-8 -*-


"""
Module LinearSolver

Content of the module
**********************

Summary:
========
.. autosummary::
     :toctree: _autosummary

    MinResLinearSolver

    SparseLDLSolver

    ShewchukPCGLinearSolver

    LULinearSolver

    WarpPreconditioner

    SVDLinearSolver

    PrecomputedLinearSolver

    CGLinearSolver

    CholeskySolver

    BTDLinearSolver

    JacobiPreconditioner

    SparseCholeskySolver

    BlockJacobiPreconditioner

    PrecomputedWarpPreconditioner

    SparseLUSolver

    SSORPreconditioner



Content:
========

.. automodule::

    MinResLinearSolver

    SparseLDLSolver

    ShewchukPCGLinearSolver

    LULinearSolver

    WarpPreconditioner

    SVDLinearSolver

    PrecomputedLinearSolver

    CGLinearSolver

    CholeskySolver

    BTDLinearSolver

    JacobiPreconditioner

    SparseCholeskySolver

    BlockJacobiPreconditioner

    PrecomputedWarpPreconditioner

    SparseLUSolver

    SSORPreconditioner



Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
# __all__=['MinResLinearSolver', 'SparseLDLSolver', 'ShewchukPCGLinearSolver', 'LULinearSolver', 'WarpPreconditioner', 'SVDLinearSolver', 'PrecomputedLinearSolver', 'CGLinearSolver', 'CholeskySolver', 'BTDLinearSolver', 'JacobiPreconditioner', 'SparseCholeskySolver', 'BlockJacobiPreconditioner', 'PrecomputedWarpPreconditioner', 'SparseLUSolver', 'SSORPreconditioner']
class LinearSolver:
    from .MinResLinearSolver import MinResLinearSolver
    from .SparseLDLSolver import SparseLDLSolver
    from .ShewchukPCGLinearSolver import ShewchukPCGLinearSolver
    from .LULinearSolver import LULinearSolver
    from .WarpPreconditioner import WarpPreconditioner
    from .SVDLinearSolver import SVDLinearSolver
    from .PrecomputedLinearSolver import PrecomputedLinearSolver
    from .CGLinearSolver import CGLinearSolver
    from .CholeskySolver import CholeskySolver
    from .BTDLinearSolver import BTDLinearSolver
    from .JacobiPreconditioner import JacobiPreconditioner
    from .SparseCholeskySolver import SparseCholeskySolver
    from .BlockJacobiPreconditioner import BlockJacobiPreconditioner
    from .PrecomputedWarpPreconditioner import PrecomputedWarpPreconditioner
    from .SparseLUSolver import SparseLUSolver
    from .SSORPreconditioner import SSORPreconditioner
