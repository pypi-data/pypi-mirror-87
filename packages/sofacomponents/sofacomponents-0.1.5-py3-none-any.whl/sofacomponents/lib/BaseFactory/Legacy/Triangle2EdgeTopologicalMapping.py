# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component Triangle2EdgeTopologicalMapping

.. autofunction:: Triangle2EdgeTopologicalMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def Triangle2EdgeTopologicalMapping(self, **kwargs):
    """
    Special case of mapping where TriangleSetTopology is converted to EdgeSetTopology



    """
    params = dict()
    return "Triangle2EdgeTopologicalMapping", params
