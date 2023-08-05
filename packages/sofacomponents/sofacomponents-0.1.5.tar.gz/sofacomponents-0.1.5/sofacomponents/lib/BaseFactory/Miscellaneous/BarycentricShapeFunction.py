# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component BarycentricShapeFunction

.. autofunction:: BarycentricShapeFunction

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def BarycentricShapeFunction(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, nbRef=None, position=None, tolerance=None, **kwargs):
    """
    Computes Barycentric shape functions


    :param name: object name  Default value: BarycentricShapeFunction

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param nbRef: maximum number of parents per child  Default value: 4

    :param position: position of parent nodes  Default value: []

    :param tolerance: minimum weight (allows for mapping outside elements)  Default value: -1.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, nbRef=nbRef, position=position, tolerance=tolerance)
    return "BarycentricShapeFunction", params
