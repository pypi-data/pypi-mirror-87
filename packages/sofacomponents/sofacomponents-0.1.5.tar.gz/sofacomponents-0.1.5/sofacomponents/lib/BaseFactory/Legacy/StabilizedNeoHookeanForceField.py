# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component StabilizedNeoHookeanForceField

.. autofunction:: StabilizedNeoHookeanForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def StabilizedNeoHookeanForceField(self, **kwargs):
    """
    StabilizedNeoHookean's Law for isotropic homogeneous materials



    """
    params = dict()
    return "StabilizedNeoHookeanForceField", params
