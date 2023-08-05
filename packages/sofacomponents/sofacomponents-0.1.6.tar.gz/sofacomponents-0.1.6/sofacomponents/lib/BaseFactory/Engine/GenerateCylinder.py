# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component GenerateCylinder

.. autofunction:: GenerateCylinder

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def GenerateCylinder(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, output_TetrahedraPosition=None, output_TrianglesPosition=None, tetrahedra=None, triangles=None, BezierTriangleWeights=None, isBezierTriangleRational=None, BezierTriangleDegree=None, BezierTetrahedronWeights=None, isBezierTetrahedronRational=None, BezierTetrahedronDegree=None, radius=None, height=None, origin=None, openSurface=None, resCircumferential=None, resRadial=None, resHeight=None, **kwargs):
    """
    Generate a Cylindrical Tetrahedral Mesh


    :param name: object name  Default value: GenerateCylinder

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param output_TetrahedraPosition: output array of 3d points of tetrahedra mesh  Default value: []

    :param output_TrianglesPosition: output array of 3d points of triangle mesh  Default value: []

    :param tetrahedra: output mesh tetrahedra  Default value: []

    :param triangles: output triangular mesh  Default value: []

    :param BezierTriangleWeights: weights of rational Bezier triangles  Default value: []

    :param isBezierTriangleRational: booleans indicating if each Bezier triangle is rational or integral  Default value: []

    :param BezierTriangleDegree: order of Bezier triangles  Default value: 0

    :param BezierTetrahedronWeights: weights of rational Bezier tetrahedra  Default value: []

    :param isBezierTetrahedronRational: booleans indicating if each Bezier tetrahedron is rational or integral  Default value: []

    :param BezierTetrahedronDegree: order of Bezier tetrahedra  Default value: 0

    :param radius: input cylinder radius  Default value: 0.2

    :param height: input cylinder height  Default value: 1.0

    :param origin: cylinder origin point  Default value: [[0.0, 0.0, 0.0]]

    :param openSurface: if the cylinder is open at its 2 ends  Default value: 1

    :param resCircumferential: Resolution in the circumferential direction  Default value: 6

    :param resRadial: Resolution in the radial direction  Default value: 3

    :param resHeight: Resolution in the height direction  Default value: 5


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, output_TetrahedraPosition=output_TetrahedraPosition, output_TrianglesPosition=output_TrianglesPosition, tetrahedra=tetrahedra, triangles=triangles, BezierTriangleWeights=BezierTriangleWeights, isBezierTriangleRational=isBezierTriangleRational, BezierTriangleDegree=BezierTriangleDegree, BezierTetrahedronWeights=BezierTetrahedronWeights, isBezierTetrahedronRational=isBezierTetrahedronRational, BezierTetrahedronDegree=BezierTetrahedronDegree, radius=radius, height=height, origin=origin, openSurface=openSurface, resCircumferential=resCircumferential, resRadial=resRadial, resHeight=resHeight)
    return "GenerateCylinder", params
