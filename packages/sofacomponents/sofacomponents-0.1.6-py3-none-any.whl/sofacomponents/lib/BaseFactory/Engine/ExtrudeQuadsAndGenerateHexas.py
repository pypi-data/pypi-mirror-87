# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ExtrudeQuadsAndGenerateHexas

.. autofunction:: ExtrudeQuadsAndGenerateHexas

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ExtrudeQuadsAndGenerateHexas(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isVisible=None, scale=None, thicknessIn=None, thicknessOut=None, numberOfSlices=None, surfaceVertices=None, surfaceQuads=None, extrudedVertices=None, extrudedSurfaceQuads=None, extrudedQuads=None, extrudedHexas=None, **kwargs):
    """
    This engine extrudes a quad-based surface into a set of hexahedral elements


    :param name: object name  Default value: ExtrudeQuadsAndGenerateHexas

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isVisible: is Visible ?  Default value: 1

    :param scale: Apply a scaling factor to the extruded mesh  Default value: [[1.0, 1.0, 1.0]]

    :param thicknessIn: Thickness of the extruded volume in the opposite direction of the normals  Default value: 0.0

    :param thicknessOut: Thickness of the extruded volume in the direction of the normals  Default value: 1.0

    :param numberOfSlices: Number of slices / steps in the extrusion  Default value: 1

    :param surfaceVertices: Position coordinates of the surface  Default value: []

    :param surfaceQuads: Indices of the quads of the surface to extrude  Default value: []

    :param extrudedVertices: Coordinates of the extruded vertices  Default value: []

    :param extrudedSurfaceQuads: List of new surface quads generated during the extrusion  Default value: []

    :param extrudedQuads: List of all quads generated during the extrusion  Default value: []

    :param extrudedHexas: List of hexahedra generated during the extrusion  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isVisible=isVisible, scale=scale, thicknessIn=thicknessIn, thicknessOut=thicknessOut, numberOfSlices=numberOfSlices, surfaceVertices=surfaceVertices, surfaceQuads=surfaceQuads, extrudedVertices=extrudedVertices, extrudedSurfaceQuads=extrudedSurfaceQuads, extrudedQuads=extrudedQuads, extrudedHexas=extrudedHexas)
    return "ExtrudeQuadsAndGenerateHexas", params
