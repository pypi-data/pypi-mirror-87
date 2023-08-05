# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SimpleTesselatedTetraTopologicalMapping

.. autofunction:: SimpleTesselatedTetraTopologicalMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SimpleTesselatedTetraTopologicalMapping(self, **kwargs):
    """
    Special case of mapping where TetrahedronSetTopology is converted into a finer TetrahedronSetTopology



    """
    params = dict()
    return "SimpleTesselatedTetraTopologicalMapping", params
