# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component QuadBendingSprings

.. autofunction:: QuadBendingSprings

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def QuadBendingSprings(self, **kwargs):
    """
    Springs added to a quad mesh to prevent bending



    """
    params = dict()
    return "QuadBendingSprings", params
