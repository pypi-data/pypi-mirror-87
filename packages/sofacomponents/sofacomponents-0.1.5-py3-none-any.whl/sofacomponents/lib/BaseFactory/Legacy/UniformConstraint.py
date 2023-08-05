# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component UniformConstraint

.. autofunction:: UniformConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def UniformConstraint(self, **kwargs):
    """
    A constraint equation applied on all dofs.



    """
    params = dict()
    return "UniformConstraint", params
