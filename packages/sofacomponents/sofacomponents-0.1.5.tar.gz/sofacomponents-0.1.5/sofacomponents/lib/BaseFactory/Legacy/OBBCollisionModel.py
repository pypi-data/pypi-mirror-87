# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component OBBCollisionModel

.. autofunction:: OBBCollisionModel

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def OBBCollisionModel(self, **kwargs):
    """
    Collision model which represents a set of OBBs



    """
    params = dict()
    return "OBBCollisionModel", params
