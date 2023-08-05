# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component LinearStrainMapping

.. autofunction:: LinearStrainMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def LinearStrainMapping(self, **kwargs):
    """
    Map strain positions as a linear combination of strains, for smoothing.



    """
    params = dict()
    return "LinearStrainMapping", params
