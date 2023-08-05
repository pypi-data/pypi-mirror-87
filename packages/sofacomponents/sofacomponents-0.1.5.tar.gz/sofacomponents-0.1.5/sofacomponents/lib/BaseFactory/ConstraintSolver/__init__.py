# -*- coding: utf-8 -*-


"""
Module ConstraintSolver

Content of the module
**********************

Summary:
========
.. autosummary::
     :toctree: _autosummary

    LMConstraintSolver

    LCPConstraintSolver

    PrecomputedConstraintCorrection

    LinearSolverConstraintCorrection

    LMConstraintDirectSolver

    GenericConstraintSolver

    GenericConstraintCorrection

    UncoupledConstraintCorrection



Content:
========

.. automodule::

    LMConstraintSolver

    LCPConstraintSolver

    PrecomputedConstraintCorrection

    LinearSolverConstraintCorrection

    LMConstraintDirectSolver

    GenericConstraintSolver

    GenericConstraintCorrection

    UncoupledConstraintCorrection



Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
# __all__=['LMConstraintSolver', 'LCPConstraintSolver', 'PrecomputedConstraintCorrection', 'LinearSolverConstraintCorrection', 'LMConstraintDirectSolver', 'GenericConstraintSolver', 'GenericConstraintCorrection', 'UncoupledConstraintCorrection']
class ConstraintSolver:
    from .LMConstraintSolver import LMConstraintSolver
    from .LCPConstraintSolver import LCPConstraintSolver
    from .PrecomputedConstraintCorrection import PrecomputedConstraintCorrection
    from .LinearSolverConstraintCorrection import LinearSolverConstraintCorrection
    from .LMConstraintDirectSolver import LMConstraintDirectSolver
    from .GenericConstraintSolver import GenericConstraintSolver
    from .GenericConstraintCorrection import GenericConstraintCorrection
    from .UncoupledConstraintCorrection import UncoupledConstraintCorrection
