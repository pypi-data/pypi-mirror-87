# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component OgdenForceField

.. autofunction:: OgdenForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def OgdenForceField(self, **kwargs):
    """
    Ogden's Law for isotropic homogeneous materials



    """
    params = dict()
    return "OgdenForceField", params
