# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component CorotationalMeshMapping

.. autofunction:: CorotationalMeshMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def CorotationalMeshMapping(self, **kwargs):
    """
    Rigidly aligns positions to rest positions for each element



    """
    params = dict()
    return "CorotationalMeshMapping", params
