# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component IdentityMapping

.. autofunction:: IdentityMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def IdentityMapping(self, **kwargs):
    """
    Special case of mapping where the child points are the same as the parent points
Special case of mapping where the child points are the same as the parent points
Special case of mapping where the child points are the same as the parent points



    """
    params = dict()
    return "IdentityMapping", params
