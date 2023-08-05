# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TriangleDeformationMapping

.. autofunction:: TriangleDeformationMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TriangleDeformationMapping(self, **kwargs):
    """
    Compute deformation gradients in triangles



    """
    params = dict()
    return "TriangleDeformationMapping", params
