# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TetrahedronSetGeometryAlgorithms

.. autofunction:: TetrahedronSetGeometryAlgorithms

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TetrahedronSetGeometryAlgorithms(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, showIndicesScale=None, showPointIndices=None, tagMechanics=None, showEdgeIndices=None, drawEdges=None, drawColorEdges=None, showTriangleIndices=None, drawTriangles=None, drawColorTriangles=None, drawNormals=None, drawNormalLength=None, recomputeTrianglesOrientation=None, flipNormals=None, showTetrahedraIndices=None, drawTetrahedra=None, drawScaleTetrahedra=None, drawColorTetrahedra=None, **kwargs):
    """
    Tetrahedron set geometry algorithms


    :param name: object name  Default value: TetrahedronSetGeometryAlgorithms

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

    :param showTriangleIndices: Debug : view Triangle indices  Default value: 0

    :param drawTriangles: if true, draw the triangles in the topology  Default value: 0

    :param drawColorTriangles: RGBA code color used to draw edges.  Default value: [[0.30000001192092896, 0.5, 0.800000011920929, 1.0]]

    :param drawNormals: if true, draw the triangles in the topology  Default value: 0

    :param drawNormalLength: Fiber length visualisation.  Default value: 10.0

    :param recomputeTrianglesOrientation: if true, will recompute triangles orientation according to normals.  Default value: 0

    :param flipNormals: if true, will flip normal of the first triangle used to recompute triangle orientation.  Default value: 0

    :param showTetrahedraIndices: Debug : view Tetrahedrons indices  Default value: 0

    :param drawTetrahedra: if true, draw the tetrahedra in the topology  Default value: 0

    :param drawScaleTetrahedra: Scale of the terahedra (between 0 and 1; if <1.0, it produces gaps between the tetrahedra)  Default value: 1.0

    :param drawColorTetrahedra: RGBA code color used to draw tetrahedra.  Default value: [[1.0, 1.0, 0.0, 1.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, showIndicesScale=showIndicesScale, showPointIndices=showPointIndices, tagMechanics=tagMechanics, showEdgeIndices=showEdgeIndices, drawEdges=drawEdges, drawColorEdges=drawColorEdges, showTriangleIndices=showTriangleIndices, drawTriangles=drawTriangles, drawColorTriangles=drawColorTriangles, drawNormals=drawNormals, drawNormalLength=drawNormalLength, recomputeTrianglesOrientation=recomputeTrianglesOrientation, flipNormals=flipNormals, showTetrahedraIndices=showTetrahedraIndices, drawTetrahedra=drawTetrahedra, drawScaleTetrahedra=drawScaleTetrahedra, drawColorTetrahedra=drawColorTetrahedra)
    return "TetrahedronSetGeometryAlgorithms", params
