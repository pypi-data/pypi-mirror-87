# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component CauchyStrainMapping

.. autofunction:: CauchyStrainMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def CauchyStrainMapping(self, **kwargs):
    """
    Map Deformation Gradients to Linear/Cauchy Strain (small displacements)



    """
    params = dict()
    return "CauchyStrainMapping", params
