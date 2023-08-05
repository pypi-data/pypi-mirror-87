# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component Mesh2PointTopologicalMapping

.. autofunction:: Mesh2PointTopologicalMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def Mesh2PointTopologicalMapping(self, **kwargs):
    """
    This class maps any mesh primitive (point, edge, triangle...) into a point using a relative position from the primitive



    """
    params = dict()
    return "Mesh2PointTopologicalMapping", params
