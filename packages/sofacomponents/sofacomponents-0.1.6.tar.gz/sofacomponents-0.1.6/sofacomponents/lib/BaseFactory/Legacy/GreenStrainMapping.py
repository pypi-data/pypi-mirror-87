# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component GreenStrainMapping

.. autofunction:: GreenStrainMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def GreenStrainMapping(self, **kwargs):
    """
    Map Deformation Gradients to Green Lagrangian Strain (large deformations).



    """
    params = dict()
    return "GreenStrainMapping", params
