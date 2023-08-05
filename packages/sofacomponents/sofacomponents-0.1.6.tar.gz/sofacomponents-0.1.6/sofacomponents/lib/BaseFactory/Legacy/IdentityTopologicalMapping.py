# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component IdentityTopologicalMapping

.. autofunction:: IdentityTopologicalMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def IdentityTopologicalMapping(self, **kwargs):
    """
    This class is a specific implementation of TopologicalMapping where the destination topology should be kept identical to the source topology. The implementation currently assumes that both topology have been initialized identically.



    """
    params = dict()
    return "IdentityTopologicalMapping", params
