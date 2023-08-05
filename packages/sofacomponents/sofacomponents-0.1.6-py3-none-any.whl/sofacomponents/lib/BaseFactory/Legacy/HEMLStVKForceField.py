# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component HEMLStVKForceField

.. autofunction:: HEMLStVKForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def HEMLStVKForceField(self, **kwargs):
    """
    St Venant-Kirchhoff (Hooke's Law for isotropic homogeneous materials)



    """
    params = dict()
    return "HEMLStVKForceField", params
