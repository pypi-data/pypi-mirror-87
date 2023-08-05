# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ArticulatedSystemMapping

.. autofunction:: ArticulatedSystemMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ArticulatedSystemMapping(self, **kwargs):
    """
    Mapping between a set of 6D DOF's and a set of angles (µ) using an articulated hierarchy container. 



    """
    params = dict()
    return "ArticulatedSystemMapping", params
