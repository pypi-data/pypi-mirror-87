# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component RequiredPlugin

.. autofunction:: RequiredPlugin

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def RequiredPlugin(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, pluginName=None, suffixMap=None, stopAfterFirstNameFound=None, stopAfterFirstSuffixFound=None, requireOne=None, requireAll=None, **kwargs):
    """
    Load the required plugins


    :param name: object name  Default value: RequiredPlugin

    :param printLog: if true, emits extra messages at runtime.  Default value: 1

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param pluginName: plugin name (or several names if you need to load different plugins or a plugin with several alternate names)  Default value: [['RequiredPlugin']]

    :param suffixMap: standard->custom suffixes pairs (to be used if the plugin is compiled outside of Sofa with a non standard way of differenciating versions), using ! to represent empty suffix  Default value: []

    :param stopAfterFirstNameFound: Stop after the first plugin name that is loaded successfully  Default value: 0

    :param stopAfterFirstSuffixFound: For each plugin name, stop after the first suffix that is loaded successfully  Default value: 1

    :param requireOne: Display an error message if no plugin names were successfully loaded  Default value: 0

    :param requireAll: Display an error message if any plugin names failed to be loaded  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, pluginName=pluginName, suffixMap=suffixMap, stopAfterFirstNameFound=stopAfterFirstNameFound, stopAfterFirstSuffixFound=stopAfterFirstSuffixFound, requireOne=requireOne, requireAll=requireAll)
    return "RequiredPlugin", params
