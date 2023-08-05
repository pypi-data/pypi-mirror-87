# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component OglLineAxis

.. autofunction:: OglLineAxis

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def OglLineAxis(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, axis=None, size=None, thickness=None, draw=None, **kwargs):
    """
    Display scene axis


    :param name: object name  Default value: OglLineAxis

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param axis: Axis to draw  Default value: xyz

    :param size: Size of the squared grid  Default value: 10.0

    :param thickness: Thickness of the lines in the grid  Default value: 1.0

    :param draw: Display the grid or not  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, axis=axis, size=size, thickness=thickness, draw=draw)
    return "OglLineAxis", params
