# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MergeSets

.. autofunction:: MergeSets

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MergeSets(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, in1=None, in2=None, out=None, op=None, **kwargs):
    """
    Merge two sets of indices using specified boolean operation


    :param name: object name  Default value: MergeSets

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param in1: first set of indices  Default value: []

    :param in2: second set of indices  Default value: []

    :param out: merged set of indices  Default value: []

    :param op: name of operation to compute (union, intersection, difference, symmetric_difference)  Default value: union


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, in1=in1, in2=in2, out=out, op=op)
    return "MergeSets", params
