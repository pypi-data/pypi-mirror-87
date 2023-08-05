# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component HookeForceField

.. autofunction:: HookeForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def HookeForceField(self, **kwargs):
    """
    Hooke's Law for isotropic homogeneous materials



    """
    params = dict()
    return "HookeForceField", params
