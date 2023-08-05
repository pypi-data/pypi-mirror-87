# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component VolumePreservationForceField

.. autofunction:: VolumePreservationForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def VolumePreservationForceField(self, **kwargs):
    """
    volume Preservation law for isotropic homogeneous materials



    """
    params = dict()
    return "VolumePreservationForceField", params
