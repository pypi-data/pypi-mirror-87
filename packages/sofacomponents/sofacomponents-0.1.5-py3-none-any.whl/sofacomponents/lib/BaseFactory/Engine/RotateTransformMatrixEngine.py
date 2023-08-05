# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component RotateTransformMatrixEngine

.. autofunction:: RotateTransformMatrixEngine

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def RotateTransformMatrixEngine(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, inT=None, outT=None, rotation=None, **kwargs):
    """
    Compose the input transform (if any) with the given rotation


    :param name: object name  Default value: RotateTransformMatrixEngine

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param inT: input transformation if any  Default value: [[1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

    :param outT: output transformation  Default value: [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

    :param rotation: euler angles  Default value: [[0.0, 0.0, 0.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, inT=inT, outT=outT, rotation=rotation)
    return "RotateTransformMatrixEngine", params
