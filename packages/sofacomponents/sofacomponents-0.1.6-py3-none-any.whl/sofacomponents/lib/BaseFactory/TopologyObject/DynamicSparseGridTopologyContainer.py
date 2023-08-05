# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component DynamicSparseGridTopologyContainer

.. autofunction:: DynamicSparseGridTopologyContainer

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def DynamicSparseGridTopologyContainer(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, position=None, checkTopology=None, nbPoints=None, points=None, edges=None, checkConnexity=None, quads=None, createQuadArray=None, hexahedra=None, resolution=None, valuesIndexedInRegularGrid=None, valuesIndexedInTopology=None, idxInRegularGrid=None, idInRegularGrid2IndexInTopo=None, voxelSize=None, **kwargs):
    """
    Hexahedron set topology container


    :param name: object name  Default value: DynamicSparseGridTopologyContainer

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param filename: Filename of the mesh  Default value: 

    :param position: Initial position of points  Default value: []

    :param checkTopology: Parameter to activate internal topology checks (might slow down the simulation)  Default value: 0

    :param nbPoints: Number of points  Default value: 0

    :param points: List of point indices  Default value: []

    :param edges: List of edge indices  Default value: []

    :param checkConnexity: It true, will check the connexity of the mesh.  Default value: 0

    :param quads: List of quad indices  Default value: []

    :param createQuadArray: Force the creation of a set of quads associated with the hexahedra  Default value: 0

    :param hexahedra: List of hexahedron indices  Default value: []

    :param resolution: voxel grid resolution  Default value: [[0, 0, 0]]

    :param valuesIndexedInRegularGrid: values indexed in the Regular Grid  Default value: []

    :param valuesIndexedInTopology: values indexed in the topology  Default value: []

    :param idxInRegularGrid: indices in the Regular Grid  Default value: []

    :param idInRegularGrid2IndexInTopo: map between id in the Regular Grid and index in the topology  Default value: 

    :param voxelSize: Size of the Voxels  Default value: [[1.0, 1.0, 1.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, position=position, checkTopology=checkTopology, nbPoints=nbPoints, points=points, edges=edges, checkConnexity=checkConnexity, quads=quads, createQuadArray=createQuadArray, hexahedra=hexahedra, resolution=resolution, valuesIndexedInRegularGrid=valuesIndexedInRegularGrid, valuesIndexedInTopology=valuesIndexedInTopology, idxInRegularGrid=idxInRegularGrid, idInRegularGrid2IndexInTopo=idInRegularGrid2IndexInTopo, voxelSize=voxelSize)
    return "DynamicSparseGridTopologyContainer", params
