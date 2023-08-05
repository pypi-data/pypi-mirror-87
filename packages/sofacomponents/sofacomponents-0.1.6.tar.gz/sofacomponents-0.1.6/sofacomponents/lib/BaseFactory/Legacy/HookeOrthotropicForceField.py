# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component HookeOrthotropicForceField

.. autofunction:: HookeOrthotropicForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def HookeOrthotropicForceField(self, **kwargs):
    """
    Hooke's Law for Orthotropic homogeneous materials



    """
    params = dict()
    return "HookeOrthotropicForceField", params
