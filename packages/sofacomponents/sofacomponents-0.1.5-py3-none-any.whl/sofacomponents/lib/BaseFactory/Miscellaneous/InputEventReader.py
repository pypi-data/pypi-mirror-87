# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component InputEventReader

.. autofunction:: InputEventReader

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def InputEventReader(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, inverseSense=None, printEvent=None, key1=None, key2=None, writeEvents=None, outputFilename=None, **kwargs):
    """
    Read events from file


    :param name: object name  Default value: InputEventReader

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param filename: input events file name  Default value: /dev/input/mouse2

    :param inverseSense: inverse the sense of the mouvement  Default value: 0

    :param printEvent: Print event informations  Default value: 0

    :param key1: Key event generated when the left pedal is pressed  Default value: 48

    :param key2: Key event generated when the right pedal is pressed  Default value: 49

    :param writeEvents: If true, write incoming events ; if false, read events from that file (if an output filename is provided)  Default value: 0

    :param outputFilename: Other filename where events will be stored (or read)  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, inverseSense=inverseSense, printEvent=printEvent, key1=key1, key2=key2, writeEvents=writeEvents, outputFilename=outputFilename)
    return "InputEventReader", params
