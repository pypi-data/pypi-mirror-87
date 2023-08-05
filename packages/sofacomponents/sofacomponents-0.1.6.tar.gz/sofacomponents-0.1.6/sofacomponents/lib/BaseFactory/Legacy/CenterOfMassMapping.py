# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component CenterOfMassMapping

.. autofunction:: CenterOfMassMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def CenterOfMassMapping(self, **kwargs):
    """
    Set the point to the center of mass of the DOFs it is attached to



    """
    params = dict()
    return "CenterOfMassMapping", params
