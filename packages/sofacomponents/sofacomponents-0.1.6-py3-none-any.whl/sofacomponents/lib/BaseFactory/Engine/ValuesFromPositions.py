# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ValuesFromPositions

.. autofunction:: ValuesFromPositions

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ValuesFromPositions(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, inputValues=None, direction=None, position=None, edges=None, triangles=None, tetrahedra=None, values=None, edgeValues=None, triangleValues=None, tetrahedronValues=None, pointVectors=None, edgeVectors=None, triangleVectors=None, tetrahedronVectors=None, fieldType=None, drawVectors=None, drawVectorLength=None, **kwargs):
    """
    Assign values to primitives (vertex/edge/triangle/tetrahedron) based on a linear interpolation of values along a direction


    :param name: object name  Default value: ValuesFromPositions

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param inputValues: Input values  Default value: []

    :param direction: Direction along which the values are interpolated  Default value: [[0.0, 1.0, 0.0]]

    :param position: Rest position coordinates of the degrees of freedom  Default value: []

    :param edges: Edge Topology  Default value: []

    :param triangles: Triangle Topology  Default value: []

    :param tetrahedra: Tetrahedron Topology  Default value: []

    :param values: Values of the points contained in the ROI  Default value: []

    :param edgeValues: Values of the edges contained in the ROI  Default value: []

    :param triangleValues: Values of the triangles contained in the ROI  Default value: []

    :param tetrahedronValues: Values of the tetrahedra contained in the ROI  Default value: []

    :param pointVectors: Vectors of the points contained in the ROI  Default value: []

    :param edgeVectors: Vectors of the edges contained in the ROI  Default value: []

    :param triangleVectors: Vectors of the triangles contained in the ROI  Default value: []

    :param tetrahedronVectors: Vectors of the tetrahedra contained in the ROI  Default value: []

    :param fieldType: field type of output elements  Default value: Scalar

    :param drawVectors: draw vectors line  Default value: 0

    :param drawVectorLength: vector length visualisation.   Default value: 10.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, inputValues=inputValues, direction=direction, position=position, edges=edges, triangles=triangles, tetrahedra=tetrahedra, values=values, edgeValues=edgeValues, triangleValues=triangleValues, tetrahedronValues=tetrahedronValues, pointVectors=pointVectors, edgeVectors=edgeVectors, triangleVectors=triangleVectors, tetrahedronVectors=tetrahedronVectors, fieldType=fieldType, drawVectors=drawVectors, drawVectorLength=drawVectorLength)
    return "ValuesFromPositions", params
