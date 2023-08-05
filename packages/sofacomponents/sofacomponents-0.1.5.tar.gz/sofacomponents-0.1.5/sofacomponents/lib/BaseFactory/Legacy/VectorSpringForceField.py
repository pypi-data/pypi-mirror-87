# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component VectorSpringForceField

.. autofunction:: VectorSpringForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def VectorSpringForceField(self, **kwargs):
    """
    Spring force field acting along the edges of a mesh



    """
    params = dict()
    return "VectorSpringForceField", params
