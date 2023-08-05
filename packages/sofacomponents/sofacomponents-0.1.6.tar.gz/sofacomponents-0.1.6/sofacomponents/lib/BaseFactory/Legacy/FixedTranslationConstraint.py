# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component FixedTranslationConstraint

.. autofunction:: FixedTranslationConstraint

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def FixedTranslationConstraint(self, **kwargs):
    """
    Attach given rigids to their initial positions but they still can have rotations



    """
    params = dict()
    return "FixedTranslationConstraint", params
