# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SubsetTopologicalMapping

.. autofunction:: SubsetTopologicalMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SubsetTopologicalMapping(self, **kwargs):
    """
    This class is a specific implementation of TopologicalMapping where the destination topology is a subset of the source topology. The implementation currently assumes that both topologies have been initialized correctly.



    """
    params = dict()
    return "SubsetTopologicalMapping", params
