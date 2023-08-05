# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component QuadSetGeometryAlgorithms

.. autofunction:: QuadSetGeometryAlgorithms

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def QuadSetGeometryAlgorithms(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, showIndicesScale=None, showPointIndices=None, tagMechanics=None, showEdgeIndices=None, drawEdges=None, drawColorEdges=None, showQuadIndices=None, drawQuads=None, drawColorQuads=None, **kwargs):
    """
    Quad set geometry algorithms


    :param name: object name  Default value: QuadSetGeometryAlgorithms

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param showIndicesScale: Debug : scale for view topology indices  Default value: 0.019999999553

    :param showPointIndices: Debug : view Point indices  Default value: 0

    :param tagMechanics: Tag of the Mechanical Object  Default value: 

    :param showEdgeIndices: Debug : view Edge indices.  Default value: 0

    :param drawEdges: if true, draw the edges in the topology.  Default value: 0

    :param drawColorEdges: RGB code color used to draw edges.  Default value: [[0.4000000059604645, 1.0, 0.30000001192092896, 1.0]]

    :param showQuadIndices: Debug : view Quad indices  Default value: 0

    :param drawQuads: if true, draw the quads in the topology  Default value: 0

    :param drawColorQuads: RGB code color used to draw quads.  Default value: [[0.0, 0.4000000059604645, 0.4000000059604645, 1.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, showIndicesScale=showIndicesScale, showPointIndices=showPointIndices, tagMechanics=tagMechanics, showEdgeIndices=showEdgeIndices, drawEdges=drawEdges, drawColorEdges=drawColorEdges, showQuadIndices=showQuadIndices, drawQuads=drawQuads, drawColorQuads=drawColorQuads)
    return "QuadSetGeometryAlgorithms", params
