# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component StiffSpringForceField

.. autofunction:: StiffSpringForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def StiffSpringForceField(self, **kwargs):
    """
    Stiff springs for implicit integration



    """
    params = dict()
    return "StiffSpringForceField", params
