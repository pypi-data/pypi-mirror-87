# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TransformEngine

.. autofunction:: TransformEngine

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TransformEngine(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, input_position=None, output_position=None, translation=None, rotation=None, quaternion=None, scale=None, inverse=None, **kwargs):
    """
    Transform position of 3d points
Transform position of dofs


    :param name: object name  Default value: TransformEngine

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param input_position: input array of 3d points  Default value: []

    :param output_position: output array of 3d points  Default value: []

    :param translation: translation vector   Default value: [[0.0, 0.0, 0.0]]

    :param rotation: rotation vector   Default value: [[0.0, 0.0, 0.0]]

    :param quaternion: rotation quaternion   Default value: [[0.0, 0.0, 0.0, 1.0]]

    :param scale: scale factor  Default value: [[1.0, 1.0, 1.0]]

    :param inverse: true to apply inverse transformation  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, input_position=input_position, output_position=output_position, translation=translation, rotation=rotation, quaternion=quaternion, scale=scale, inverse=inverse)
    return "TransformEngine", params
