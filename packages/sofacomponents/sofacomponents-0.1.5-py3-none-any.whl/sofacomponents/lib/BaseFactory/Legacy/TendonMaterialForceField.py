# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TendonMaterialForceField

.. autofunction:: TendonMaterialForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TendonMaterialForceField(self, **kwargs):
    """
    Blember's' Material Law for Tendon materials



    """
    params = dict()
    return "TendonMaterialForceField", params
