# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component Hexa2QuadTopologicalMapping

.. autofunction:: Hexa2QuadTopologicalMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def Hexa2QuadTopologicalMapping(self, **kwargs):
    """
    Special case of mapping where HexahedronSetTopology is converted to QuadSetTopology



    """
    params = dict()
    return "Hexa2QuadTopologicalMapping", params
