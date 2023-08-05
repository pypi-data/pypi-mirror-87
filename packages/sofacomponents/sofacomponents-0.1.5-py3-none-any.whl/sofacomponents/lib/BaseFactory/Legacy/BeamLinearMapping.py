# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component BeamLinearMapping

.. autofunction:: BeamLinearMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def BeamLinearMapping(self, **kwargs):
    """
    Set the positions and velocities of points attached to a beam using linear interpolation between DOFs



    """
    params = dict()
    return "BeamLinearMapping", params
