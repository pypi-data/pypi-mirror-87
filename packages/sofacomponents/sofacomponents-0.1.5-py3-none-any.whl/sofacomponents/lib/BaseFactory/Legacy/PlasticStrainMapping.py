# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PlasticStrainMapping

.. autofunction:: PlasticStrainMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PlasticStrainMapping(self, **kwargs):
    """
    Map a total strain to an elastic strain + a plastic strain.



    """
    params = dict()
    return "PlasticStrainMapping", params
