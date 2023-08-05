# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MuscleMaterialForceField

.. autofunction:: MuscleMaterialForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MuscleMaterialForceField(self, **kwargs):
    """
    Blember's' Material Law for muscle materials



    """
    params = dict()
    return "MuscleMaterialForceField", params
