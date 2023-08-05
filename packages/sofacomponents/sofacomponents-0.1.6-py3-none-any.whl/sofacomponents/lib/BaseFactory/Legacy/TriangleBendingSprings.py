# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TriangleBendingSprings

.. autofunction:: TriangleBendingSprings

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TriangleBendingSprings(self, **kwargs):
    """
    Springs added to a traingular mesh to prevent bending



    """
    params = dict()
    return "TriangleBendingSprings", params
