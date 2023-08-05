# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component Quad2TriangleTopologicalMapping

.. autofunction:: Quad2TriangleTopologicalMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def Quad2TriangleTopologicalMapping(self, **kwargs):
    """
    Special case of mapping where QuadSetTopology is converted to TriangleSetTopology



    """
    params = dict()
    return "Quad2TriangleTopologicalMapping", params
