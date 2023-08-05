# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component CorotationalStrainMapping

.. autofunction:: CorotationalStrainMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def CorotationalStrainMapping(self, **kwargs):
    """
    Map Deformation Gradients to Corotational Strain (small local deformations).



    """
    params = dict()
    return "CorotationalStrainMapping", params
