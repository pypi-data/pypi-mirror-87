# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component Hexa2TetraTopologicalMapping

.. autofunction:: Hexa2TetraTopologicalMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def Hexa2TetraTopologicalMapping(self, **kwargs):
    """
    Special case of mapping where HexahedronSetTopology is converted to TetrahedronSetTopology



    """
    params = dict()
    return "Hexa2TetraTopologicalMapping", params
