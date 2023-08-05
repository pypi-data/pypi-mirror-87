# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TriangleStrainAverageMapping

.. autofunction:: TriangleStrainAverageMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TriangleStrainAverageMapping(self, **kwargs):
    """
    Compute deformation gradients in triangles



    """
    params = dict()
    return "TriangleStrainAverageMapping", params
