# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component Edge2QuadTopologicalMapping

.. autofunction:: Edge2QuadTopologicalMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def Edge2QuadTopologicalMapping(self, **kwargs):
    """
    Special case of mapping where EdgeSetTopology is converted to QuadSetTopology



    """
    params = dict()
    return "Edge2QuadTopologicalMapping", params
