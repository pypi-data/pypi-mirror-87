# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component RigidMapping

.. autofunction:: RigidMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def RigidMapping(self, **kwargs):
    """
    Set the positions and velocities of points attached to a rigid parent



    """
    params = dict()
    return "RigidMapping", params
