# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component CompareState

.. autofunction:: CompareState

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def CompareState(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, interval=None, shift=None, loop=None, scalePos=None, **kwargs):
    """
    Compare State vectors from a reference frame to the associated Mechanical State


    :param name: object name  Default value: CompareState

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param filename: output file name  Default value: 

    :param interval: time duration between inputs  Default value: 0.0

    :param shift: shift between times in the file and times when they will be read  Default value: 0.0

    :param loop: set to 'true' to re-read the file when reaching the end  Default value: 0

    :param scalePos: scale the input mechanical object  Default value: 1.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, interval=interval, shift=shift, loop=loop, scalePos=scalePos)
    return "CompareState", params
