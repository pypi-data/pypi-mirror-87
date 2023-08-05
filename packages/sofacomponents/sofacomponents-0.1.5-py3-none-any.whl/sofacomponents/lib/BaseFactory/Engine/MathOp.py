# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MathOp

.. autofunction:: MathOp

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MathOp(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, nbInputs=None, op=None, output=None, input1=None, input2=None, **kwargs):
    """
    Apply a math operation to combine several inputs


    :param name: object name  Default value: MathOp

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param nbInputs: Number of input values  Default value: 2

    :param op: Selected operation to apply  Default value: +

    :param output: Output values  Default value: []

    :param input1: input values 1  Default value: []

    :param input2: input values 2  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, nbInputs=nbInputs, op=op, output=output, input1=input1, input2=input2)
    return "MathOp", params
