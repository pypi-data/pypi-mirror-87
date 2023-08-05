# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component HexahedronCompositeFEMMapping

.. autofunction:: HexahedronCompositeFEMMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def HexahedronCompositeFEMMapping(self, **kwargs):
    """
    Set the point to the center of mass of the DOFs it is attached to



    """
    params = dict()
    return "HexahedronCompositeFEMMapping", params
