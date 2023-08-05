# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component RelativeStrainMapping

.. autofunction:: RelativeStrainMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def RelativeStrainMapping(self, **kwargs):
    """
    Map a total strain to an elastic strain + offset



    """
    params = dict()
    return "RelativeStrainMapping", params
