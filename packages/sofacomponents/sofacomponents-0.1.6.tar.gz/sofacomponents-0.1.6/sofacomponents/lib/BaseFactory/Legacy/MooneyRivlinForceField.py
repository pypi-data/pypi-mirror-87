# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MooneyRivlinForceField

.. autofunction:: MooneyRivlinForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MooneyRivlinForceField(self, **kwargs):
    """
    MooneyRivlin's Law for isotropic homogeneous materials



    """
    params = dict()
    return "MooneyRivlinForceField", params
