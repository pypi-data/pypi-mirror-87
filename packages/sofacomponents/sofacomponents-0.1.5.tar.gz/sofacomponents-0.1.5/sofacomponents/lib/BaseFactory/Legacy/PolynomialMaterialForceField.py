# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PolynomialMaterialForceField

.. autofunction:: PolynomialMaterialForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PolynomialMaterialForceField(self, **kwargs):
    """
    Polynomial Material Law for isotropic homogeneous materials



    """
    params = dict()
    return "PolynomialMaterialForceField", params
