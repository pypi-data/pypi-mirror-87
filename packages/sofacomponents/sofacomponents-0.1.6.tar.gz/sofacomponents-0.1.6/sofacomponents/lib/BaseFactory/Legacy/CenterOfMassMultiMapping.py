# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component CenterOfMassMultiMapping

.. autofunction:: CenterOfMassMultiMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def CenterOfMassMultiMapping(self, **kwargs):
    """
    Set the point to the center of mass of the DOFs it is attached to



    """
    params = dict()
    return "CenterOfMassMultiMapping", params
