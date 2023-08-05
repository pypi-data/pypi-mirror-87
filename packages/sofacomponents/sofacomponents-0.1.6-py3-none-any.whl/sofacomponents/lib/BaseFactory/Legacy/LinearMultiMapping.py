# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component LinearMultiMapping

.. autofunction:: LinearMultiMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def LinearMultiMapping(self, **kwargs):
    """
    Map child positions as a linear combination of parents.



    """
    params = dict()
    return "LinearMultiMapping", params
