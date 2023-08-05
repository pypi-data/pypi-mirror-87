# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MeshTetraStuffing

.. autofunction:: MeshTetraStuffing

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MeshTetraStuffing(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, vbbox=None, size=None, inputPoints=None, inputTriangles=None, inputQuads=None, outputPoints=None, outputTetrahedra=None, alphaLong=None, alphaShort=None, snapPoints=None, splitTetrahedra=None, draw=None, **kwargs):
    """
    Create a tetrahedral volume mesh from a surface, using the algorithm from F. Labelle and J.R. Shewchuk, "Isosurface Stuffing: Fast Tetrahedral Meshes with Good Dihedral Angles", SIGGRAPH 2007.


    :param name: object name  Default value: MeshTetraStuffing

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param vbbox: BBox to restrict the volume to  Default value: [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

    :param size: Size of the generate tetrahedra. If negative, number of grid cells in the largest bbox dimension  Default value: -8.0

    :param inputPoints: Input surface mesh points  Default value: []

    :param inputTriangles: Input surface mesh triangles  Default value: []

    :param inputQuads: Input surface mesh quads  Default value: []

    :param outputPoints: Output volume mesh points  Default value: []

    :param outputTetrahedra: Output volume mesh tetrahedra  Default value: []

    :param alphaLong: Minimum alpha values on long edges when snapping points  Default value: 0.24999

    :param alphaShort: Minimum alpha values on short edges when snapping points  Default value: 0.42978

    :param snapPoints: Snap points to the surface if intersections on edges are closed to given alpha values  Default value: 0

    :param splitTetrahedra: Split tetrahedra crossing the surface  Default value: 0

    :param draw: Activate rendering of internal datasets  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, vbbox=vbbox, size=size, inputPoints=inputPoints, inputTriangles=inputTriangles, inputQuads=inputQuads, outputPoints=outputPoints, outputTetrahedra=outputTetrahedra, alphaLong=alphaLong, alphaShort=alphaShort, snapPoints=snapPoints, splitTetrahedra=splitTetrahedra, draw=draw)
    return "MeshTetraStuffing", params
