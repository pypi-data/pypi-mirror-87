# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MeshSpringForceField

.. autofunction:: MeshSpringForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MeshSpringForceField(self, **kwargs):
    """
    Spring force field acting along the edges of a mesh



    """
    params = dict()
    return "MeshSpringForceField", params
