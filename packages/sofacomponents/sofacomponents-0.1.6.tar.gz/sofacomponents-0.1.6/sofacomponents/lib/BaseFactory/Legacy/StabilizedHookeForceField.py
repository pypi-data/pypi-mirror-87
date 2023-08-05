# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component StabilizedHookeForceField

.. autofunction:: StabilizedHookeForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def StabilizedHookeForceField(self, **kwargs):
    """
    Hooke's Law for isotropic homogeneous materials, stabilized for principal stretches



    """
    params = dict()
    return "StabilizedHookeForceField", params
