# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component RigidConstraint

.. autofunction:: RigidConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def RigidConstraint(self, **kwargs):
    """
    Rigidify a deformable frame



    """
    params = dict()
    return "RigidConstraint", params
