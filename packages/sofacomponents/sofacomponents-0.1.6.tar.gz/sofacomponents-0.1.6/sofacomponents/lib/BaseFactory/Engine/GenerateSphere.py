# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component GenerateSphere

.. autofunction:: GenerateSphere

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def GenerateSphere(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, output_TetrahedraPosition=None, tetrahedra=None, output_TrianglesPosition=None, triangles=None, BezierTetrahedronDegree=None, BezierTetrahedronWeights=None, isBezierTetrahedronRational=None, BezierTriangleDegree=None, BezierTriangleWeights=None, isBezierTriangleRational=None, radius=None, origin=None, tessellationDegree=None, platonicSolid=None, **kwargs):
    """
    Generate a sphereical (Bezier) Tetrahedral and Triangular Mesh


    :param name: object name  Default value: GenerateSphere

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param output_TetrahedraPosition: output array of 3d points of tetrahedra mesh  Default value: []

    :param tetrahedra: output mesh tetrahedra  Default value: []

    :param output_TrianglesPosition: output array of 3d points of triangle mesh  Default value: []

    :param triangles: output triangular mesh  Default value: []

    :param BezierTetrahedronDegree: order of Bezier tetrahedra  Default value: 0

    :param BezierTetrahedronWeights: weights of rational Bezier tetrahedra  Default value: []

    :param isBezierTetrahedronRational: booleans indicating if each Bezier tetrahedron is rational or integral  Default value: []

    :param BezierTriangleDegree: order of Bezier triangles  Default value: 0

    :param BezierTriangleWeights: weights of rational Bezier triangles  Default value: []

    :param isBezierTriangleRational: booleans indicating if each Bezier triangle is rational or integral  Default value: []

    :param radius: input sphere radius  Default value: 0.2

    :param origin: sphere center point  Default value: [[0.0, 0.0, 0.0]]

    :param tessellationDegree: Degree of tessellation of each Platonic triangulation  Default value: 1

    :param platonicSolid: name of the Platonic triangulation used to create the spherical dome : either "tetrahedron", "octahedron" or "icosahedron"  Default value: icosahedron


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, output_TetrahedraPosition=output_TetrahedraPosition, tetrahedra=tetrahedra, output_TrianglesPosition=output_TrianglesPosition, triangles=triangles, BezierTetrahedronDegree=BezierTetrahedronDegree, BezierTetrahedronWeights=BezierTetrahedronWeights, isBezierTetrahedronRational=isBezierTetrahedronRational, BezierTriangleDegree=BezierTriangleDegree, BezierTriangleWeights=BezierTriangleWeights, isBezierTriangleRational=isBezierTriangleRational, radius=radius, origin=origin, tessellationDegree=tessellationDegree, platonicSolid=platonicSolid)
    return "GenerateSphere", params
