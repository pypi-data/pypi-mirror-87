# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component CompositingVisualLoop

.. autofunction:: CompositingVisualLoop

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def CompositingVisualLoop(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, vertFilename=None, fragFilename=None, **kwargs):
    """
    Visual loop enabling multipass rendering. Needs multiple fbo data and a compositing shader


    :param name: object name  Default value: CompositingVisualLoop

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param vertFilename: Set the vertex shader filename to load  Default value: shaders/compositing.vert

    :param fragFilename: Set the fragment shader filename to load  Default value: shaders/compositing.frag


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, vertFilename=vertFilename, fragFilename=fragFilename)
    return "CompositingVisualLoop", params
