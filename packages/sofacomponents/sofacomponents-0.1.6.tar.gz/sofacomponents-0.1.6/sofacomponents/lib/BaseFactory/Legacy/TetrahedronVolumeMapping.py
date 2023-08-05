# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TetrahedronVolumeMapping

.. autofunction:: TetrahedronVolumeMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TetrahedronVolumeMapping(self, **kwargs):
    """
    Map deformation gradients to the invariants of the right Cauchy Green deformation tensor: I1, I2 and J



    """
    params = dict()
    return "TetrahedronVolumeMapping", params
