# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component VolumeMapping

.. autofunction:: VolumeMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def VolumeMapping(self, **kwargs):
    """
    Compute volume from positions and mesh topology



    """
    params = dict()
    return "VolumeMapping", params
