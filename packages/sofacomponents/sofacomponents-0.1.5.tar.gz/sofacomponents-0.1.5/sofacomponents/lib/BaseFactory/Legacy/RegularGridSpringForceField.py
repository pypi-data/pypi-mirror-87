# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component RegularGridSpringForceField

.. autofunction:: RegularGridSpringForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def RegularGridSpringForceField(self, **kwargs):
    """
    Spring acting on the edges and faces of a regular grid



    """
    params = dict()
    return "RegularGridSpringForceField", params
