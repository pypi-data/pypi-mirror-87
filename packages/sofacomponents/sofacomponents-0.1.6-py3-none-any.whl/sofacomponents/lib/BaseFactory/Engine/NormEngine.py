# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component NormEngine

.. autofunction:: NormEngine

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def NormEngine(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, input=None, output=None, normType=None, **kwargs):
    """
    Convert Vec in Real


    :param name: object name  Default value: NormEngine

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param input: input array of 3d points  Default value: []

    :param output: output array of scalar norms  Default value: []

    :param normType: The type of norm. Use a negative value for the infinite norm.  Default value: 2


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, input=input, output=output, normType=normType)
    return "NormEngine", params
