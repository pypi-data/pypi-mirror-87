# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ExtrudeSurface

.. autofunction:: ExtrudeSurface

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ExtrudeSurface(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isVisible=None, heightFactor=None, triangles=None, extrusionVertices=None, surfaceVertices=None, extrusionTriangles=None, surfaceTriangles=None, **kwargs):
    """
    This class truns on spiral any topological model


    :param name: object name  Default value: ExtrudeSurface

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isVisible: is Visible ?  Default value: 1

    :param heightFactor: Factor for the height of the extrusion (based on normal) ?  Default value: 1.0

    :param triangles: List of triangle indices  Default value: []

    :param extrusionVertices: Position coordinates of the extrusion  Default value: []

    :param surfaceVertices: Position coordinates of the surface  Default value: []

    :param extrusionTriangles: Triangles indices of the extrusion  Default value: []

    :param surfaceTriangles: Indices of the triangles of the surface to extrude  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isVisible=isVisible, heightFactor=heightFactor, triangles=triangles, extrusionVertices=extrusionVertices, surfaceVertices=surfaceVertices, extrusionTriangles=extrusionTriangles, surfaceTriangles=surfaceTriangles)
    return "ExtrudeSurface", params
