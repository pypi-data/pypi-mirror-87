# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component Tetra2TriangleTopologicalMapping

.. autofunction:: Tetra2TriangleTopologicalMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def Tetra2TriangleTopologicalMapping(self, **kwargs):
    """
    Special case of mapping where TetrahedronSetTopology is converted to TriangleSetTopology



    """
    params = dict()
    return "Tetra2TriangleTopologicalMapping", params
