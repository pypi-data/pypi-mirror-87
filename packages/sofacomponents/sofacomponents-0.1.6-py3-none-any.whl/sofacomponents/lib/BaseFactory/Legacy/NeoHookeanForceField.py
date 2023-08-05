# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component NeoHookeanForceField

.. autofunction:: NeoHookeanForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def NeoHookeanForceField(self, **kwargs):
    """
    NeoHookean's Law for isotropic homogeneous materials



    """
    params = dict()
    return "NeoHookeanForceField", params
