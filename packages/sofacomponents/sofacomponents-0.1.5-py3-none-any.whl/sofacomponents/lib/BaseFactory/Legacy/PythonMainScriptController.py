# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PythonMainScriptController

.. autofunction:: PythonMainScriptController

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PythonMainScriptController(self, **kwargs):
    """
    A Sofa controller scripted in python, looking for callbacks directly in the file (not in a class like the more general and powerful PythonScriptController



    """
    params = dict()
    return "PythonMainScriptController", params
