# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PenalityContactForceField

.. autofunction:: PenalityContactForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PenalityContactForceField(self, **kwargs):
    """
    Contact using repulsive springs



    """
    params = dict()
    return "PenalityContactForceField", params
