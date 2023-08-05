# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component HookeTransverseForceField

.. autofunction:: HookeTransverseForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def HookeTransverseForceField(self, **kwargs):
    """
    Hooke's Law for Transversely isotropic homogeneous materials (symmetry about X axis)



    """
    params = dict()
    return "HookeTransverseForceField", params
