# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component BarycentricMapping

.. autofunction:: BarycentricMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def BarycentricMapping(self, **kwargs):
    """
    Mapping using barycentric coordinates of the child with respect to cells of its parent



    """
    params = dict()
    return "BarycentricMapping", params
