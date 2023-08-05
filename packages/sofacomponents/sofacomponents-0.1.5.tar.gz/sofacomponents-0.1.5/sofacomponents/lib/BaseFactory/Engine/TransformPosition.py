# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TransformPosition

.. autofunction:: TransformPosition

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TransformPosition(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, origin=None, input_position=None, output_position=None, normal=None, translation=None, rotation=None, scale=None, matrix=None, method=None, seedValue=None, maxRandomDisplacement=None, fixedIndices=None, filename=None, drawInput=None, drawOutput=None, pointSize=None, **kwargs):
    """
    Transform position of 3d points


    :param name: object name  Default value: TransformPosition

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param origin: A 3d point on the plane/Center of the scale  Default value: [[0.0, 0.0, 0.0]]

    :param input_position: input array of 3d points  Default value: []

    :param output_position: output array of 3d points projected on a plane  Default value: []

    :param normal: plane normal  Default value: [[0.0, 0.0, 0.0]]

    :param translation: translation vector   Default value: [[0.0, 0.0, 0.0]]

    :param rotation: rotation vector   Default value: [[0.0, 0.0, 0.0]]

    :param scale: scale factor  Default value: [[1.0, 1.0, 1.0]]

    :param matrix: 4x4 affine matrix  Default value: [[1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

    :param method: transformation method either translation or scale or rotation or random or projectOnPlane  Default value: projectOnPlane

    :param seedValue: the seed value for the random generator  Default value: 0

    :param maxRandomDisplacement: the maximum displacement around initial position for the random transformation  Default value: 1.0

    :param fixedIndices: Indices of the entries that are not transformed  Default value: []

    :param filename: filename of an affine matrix. Supported extensions are: .trm, .tfm, .xfm and .txt(read as .xfm)  Default value: 

    :param drawInput: Draw input points  Default value: 0

    :param drawOutput: Draw output points  Default value: 0

    :param pointSize: Point size  Default value: 1.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, origin=origin, input_position=input_position, output_position=output_position, normal=normal, translation=translation, rotation=rotation, scale=scale, matrix=matrix, method=method, seedValue=seedValue, maxRandomDisplacement=maxRandomDisplacement, fixedIndices=fixedIndices, filename=filename, drawInput=drawInput, drawOutput=drawOutput, pointSize=pointSize)
    return "TransformPosition", params
