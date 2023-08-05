# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component FixedRotationConstraint

.. autofunction:: FixedRotationConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def FixedRotationConstraint(self, **kwargs):
    """
    Prevents rotation around x or/and y or/and z axis



    """
    params = dict()
    return "FixedRotationConstraint", params
