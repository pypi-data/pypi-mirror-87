# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ExtrudeEdgesAndGenerateQuads

.. autofunction:: ExtrudeEdgesAndGenerateQuads

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ExtrudeEdgesAndGenerateQuads(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, extrudeDirection=None, thicknessIn=None, thicknessOut=None, numberOfSections=None, curveVertices=None, curveEdges=None, extrudedVertices=None, extrudedEdges=None, extrudedQuads=None, **kwargs):
    """
    This engine extrudes an edge-based curve into a quad surface patch


    :param name: object name  Default value: ExtrudeEdgesAndGenerateQuads

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param extrudeDirection: Direction along which to extrude the curve  Default value: [[1.0, 0.0, 0.0]]

    :param thicknessIn: Thickness of the extruded volume in the opposite direction of the normals  Default value: 0.0

    :param thicknessOut: Thickness of the extruded volume in the direction of the normals  Default value: 1.0

    :param numberOfSections: Number of sections / steps in the extrusion  Default value: 1

    :param curveVertices: Position coordinates along the initial curve  Default value: []

    :param curveEdges: Indices of the edges of the curve to extrude  Default value: []

    :param extrudedVertices: Coordinates of the extruded vertices  Default value: []

    :param extrudedEdges: List of all edges generated during the extrusion  Default value: []

    :param extrudedQuads: List of all quads generated during the extrusion  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, extrudeDirection=extrudeDirection, thicknessIn=thicknessIn, thicknessOut=thicknessOut, numberOfSections=numberOfSections, curveVertices=curveVertices, curveEdges=curveEdges, extrudedVertices=extrudedVertices, extrudedEdges=extrudedEdges, extrudedQuads=extrudedQuads)
    return "ExtrudeEdgesAndGenerateQuads", params
