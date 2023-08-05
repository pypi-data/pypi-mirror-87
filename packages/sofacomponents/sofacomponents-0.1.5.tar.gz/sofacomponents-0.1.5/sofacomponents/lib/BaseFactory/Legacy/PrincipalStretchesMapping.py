# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PrincipalStretchesMapping

.. autofunction:: PrincipalStretchesMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PrincipalStretchesMapping(self, **kwargs):
    """
    Map Deformation Gradients to Principal Stretches



    """
    params = dict()
    return "PrincipalStretchesMapping", params
