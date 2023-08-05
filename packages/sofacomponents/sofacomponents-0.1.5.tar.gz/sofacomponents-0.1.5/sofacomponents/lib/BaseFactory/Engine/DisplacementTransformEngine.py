# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component DisplacementTransformEngine

.. autofunction:: DisplacementTransformEngine

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def DisplacementTransformEngine(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, x0=None, x=None, displacements=None, **kwargs):
    """
    Converts a vector of Rigid to a vector of displacement transforms.


    :param name: object name  Default value: DisplacementTransformEngine

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param x0: Rest position  Default value: []

    :param x: Current position  Default value: []

    :param displacements: Displacement transforms with respect to original rigid positions  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, x0=x0, x=x, displacements=displacements)
    return "DisplacementTransformEngine", params
