# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component CenterOfMassMulti2Mapping

.. autofunction:: CenterOfMassMulti2Mapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def CenterOfMassMulti2Mapping(self, **kwargs):
    """
    Set the point to the center of mass of the DOFs it is attached to



    """
    params = dict()
    return "CenterOfMassMulti2Mapping", params
