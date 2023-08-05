# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PointSetGeometryAlgorithms

.. autofunction:: PointSetGeometryAlgorithms

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PointSetGeometryAlgorithms(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, showIndicesScale=None, showPointIndices=None, tagMechanics=None, **kwargs):
    """
    Point set geometry algorithms


    :param name: object name  Default value: PointSetGeometryAlgorithms

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param showIndicesScale: Debug : scale for view topology indices  Default value: 0.019999999553

    :param showPointIndices: Debug : view Point indices  Default value: 0

    :param tagMechanics: Tag of the Mechanical Object  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, showIndicesScale=showIndicesScale, showPointIndices=showPointIndices, tagMechanics=tagMechanics)
    return "PointSetGeometryAlgorithms", params
