# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SimpleTesselatedHexaTopologicalMapping

.. autofunction:: SimpleTesselatedHexaTopologicalMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SimpleTesselatedHexaTopologicalMapping(self, **kwargs):
    """
    Special case of mapping where HexahedronSetTopology is converted into a finer HexahedronSetTopology



    """
    params = dict()
    return "SimpleTesselatedHexaTopologicalMapping", params
