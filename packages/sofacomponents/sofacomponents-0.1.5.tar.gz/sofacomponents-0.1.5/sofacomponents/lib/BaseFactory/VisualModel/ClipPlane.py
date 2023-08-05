# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ClipPlane

.. autofunction:: ClipPlane

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ClipPlane(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, position=None, normal=None, id=None, active=None, **kwargs):
    """
    OpenGL Clipping Plane


    :param name: object name  Default value: ClipPlane

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param position: Point crossed by the clipping plane  Default value: [[0.0, 0.0, 0.0]]

    :param normal: Normal of the clipping plane, pointing toward the clipped region  Default value: [[1.0, 0.0, 0.0]]

    :param id: Clipping plane OpenGL ID  Default value: 0

    :param active: Control whether the clipping plane should be applied or not  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, position=position, normal=normal, id=id, active=active)
    return "ClipPlane", params
