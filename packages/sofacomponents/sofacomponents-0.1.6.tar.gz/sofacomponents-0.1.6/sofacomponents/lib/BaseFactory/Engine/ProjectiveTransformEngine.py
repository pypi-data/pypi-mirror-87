# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ProjectiveTransformEngine

.. autofunction:: ProjectiveTransformEngine

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ProjectiveTransformEngine(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, input_position=None, output_position=None, proj_mat=None, focal_distance=None, **kwargs):
    """
    Project the position of 3d points onto a plane according to a projection matrix


    :param name: object name  Default value: ProjectiveTransformEngine

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param input_position: input array of 3d points  Default value: []

    :param output_position: output array of projected 3d points  Default value: []

    :param proj_mat: projection matrix   Default value: [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

    :param focal_distance: focal distance   Default value: 1.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, input_position=input_position, output_position=output_position, proj_mat=proj_mat, focal_distance=focal_distance)
    return "ProjectiveTransformEngine", params
