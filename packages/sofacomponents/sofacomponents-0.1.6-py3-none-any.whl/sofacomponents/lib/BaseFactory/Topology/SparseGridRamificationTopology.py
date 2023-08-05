# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SparseGridRamificationTopology

.. autofunction:: SparseGridRamificationTopology

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SparseGridRamificationTopology(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, position=None, edges=None, triangles=None, quads=None, tetrahedra=None, hexahedra=None, uv=None, drawEdges=None, drawTriangles=None, drawQuads=None, drawTetrahedra=None, drawHexahedra=None, fillWeighted=None, onlyInsideCells=None, n=None, min=None, max=None, cellWidth=None, nbVirtualFinerLevels=None, dataResolution=None, voxelSize=None, marchingCubeStep=None, convolutionSize=None, facets=None, finestConnectivity=None, **kwargs):
    """
    Sparse grid in 3D (modified)


    :param name: object name  Default value: SparseGridRamificationTopology

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param filename: Filename of the mesh  Default value: 

    :param position: List of point positions  Default value: []

    :param edges: List of edge indices  Default value: []

    :param triangles: List of triangle indices  Default value: []

    :param quads: List of quad indices  Default value: []

    :param tetrahedra: List of tetrahedron indices  Default value: []

    :param hexahedra: List of hexahedron indices  Default value: []

    :param uv: List of uv coordinates  Default value: []

    :param drawEdges: if true, draw the topology Edges  Default value: 0

    :param drawTriangles: if true, draw the topology Triangles  Default value: 0

    :param drawQuads: if true, draw the topology Quads  Default value: 0

    :param drawTetrahedra: if true, draw the topology Tetrahedra  Default value: 0

    :param drawHexahedra: if true, draw the topology hexahedra  Default value: 0

    :param fillWeighted: Is quantity of matter inside a cell taken into account? (.5 for boundary, 1 for inside)  Default value: 1

    :param onlyInsideCells: Select only inside cells (exclude boundary cells)  Default value: 0

    :param n: grid resolution  Default value: [[2, 2, 2]]

    :param min: Min  Default value: [[0.0, 0.0, 0.0]]

    :param max: Max  Default value: [[0.0, 0.0, 0.0]]

    :param cellWidth: if > 0 : dimension of each cell in the created grid  Default value: 0.0

    :param nbVirtualFinerLevels: create virtual (not in the animation tree) finer sparse grids in order to dispose of finest information (usefull to compute better mechanical properties for example)  Default value: 0

    :param dataResolution: Dimension of the voxel File  Default value: [[0, 0, 0]]

    :param voxelSize: Dimension of one voxel  Default value: [[1.0, 1.0, 1.0]]

    :param marchingCubeStep: Step of the Marching Cube algorithm  Default value: 1

    :param convolutionSize: Dimension of the convolution kernel to smooth the voxels. 0 if no smoothing is required.  Default value: 0

    :param facets: Input mesh facets  Default value: []

    :param finestConnectivity: Test for connectivity at the finest level? (more precise but slower by testing all intersections between the model mesh and the faces between boundary cubes)  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, position=position, edges=edges, triangles=triangles, quads=quads, tetrahedra=tetrahedra, hexahedra=hexahedra, uv=uv, drawEdges=drawEdges, drawTriangles=drawTriangles, drawQuads=drawQuads, drawTetrahedra=drawTetrahedra, drawHexahedra=drawHexahedra, fillWeighted=fillWeighted, onlyInsideCells=onlyInsideCells, n=n, min=min, max=max, cellWidth=cellWidth, nbVirtualFinerLevels=nbVirtualFinerLevels, dataResolution=dataResolution, voxelSize=voxelSize, marchingCubeStep=marchingCubeStep, convolutionSize=convolutionSize, facets=facets, finestConnectivity=finestConnectivity)
    return "SparseGridRamificationTopology", params
