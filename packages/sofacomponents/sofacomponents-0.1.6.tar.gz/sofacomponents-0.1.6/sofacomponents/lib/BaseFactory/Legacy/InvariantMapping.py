# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component InvariantMapping

.. autofunction:: InvariantMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def InvariantMapping(self, **kwargs):
    """
    Map deformation gradients to the invariants of the right Cauchy Green deformation tensor: I1, I2 and J



    """
    params = dict()
    return "InvariantMapping", params
