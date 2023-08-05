# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component AngularSpringForceField

.. autofunction:: AngularSpringForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def AngularSpringForceField(self, **kwargs):
    """
    Angular springs applied to rotational degrees of freedom of a rigid body or frame



    """
    params = dict()
    return "AngularSpringForceField", params
