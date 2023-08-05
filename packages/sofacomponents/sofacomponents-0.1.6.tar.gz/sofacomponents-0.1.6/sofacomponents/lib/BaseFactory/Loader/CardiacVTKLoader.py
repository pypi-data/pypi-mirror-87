# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component CardiacVTKLoader

.. autofunction:: CardiacVTKLoader

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def CardiacVTKLoader(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, position=None, polylines=None, edges=None, triangles=None, quads=None, polygons=None, highOrderEdgePositions=None, highOrderTrianglePositions=None, highOrderQuadPositions=None, tetrahedra=None, hexahedra=None, pentahedra=None, highOrderTetrahedronPositions=None, highOrderHexahedronPositions=None, pyramids=None, normals=None, edgesGroups=None, trianglesGroups=None, quadsGroups=None, polygonsGroups=None, tetrahedraGroups=None, hexahedraGroups=None, pentahedraGroups=None, pyramidsGroups=None, flipNormals=None, triangulate=None, createSubelements=None, onlyAttachedPoints=None, translation=None, rotation=None, scale3d=None, transformation=None, createFibers=None, outputNodeFibers=None, outputTetraFibers=None, TetraTriangle=None, unitTime=None, TetraZoneName=None, PointZoneName=None, withAHA=None, TriZoneName=None, AHAzoneName=None, startContraction=None, angleEpi=None, angleEndo=None, CellTypes=None, numberOfZone=None, m_zoneNames=None, m_zoneSizes=None, numberOfSurfaceZone=None, m_surfaceZoneNames=None, m_surfaceZoneSizes=None, MSinitSurfaceZoneNames=None, FileNodeFiber=None, nodeFibers=None, FileFacetFiber=None, facetFibers=None, FileFacetBFiber=None, facetBFibers=None, FileTetraTensor=None, tetraTensor=None, FileContractionParameters=None, ContractionParameters=None, InputContractionParameters=None, FileTetraConductivity=None, tetraConductivity=None, FileStiffnessParameters=None, StiffnessParameters=None, InputStiffnessParameters=None, ElectroFile=None, depoTimes=None, APDTimes=None, APDTimesZones=None, APDTimesString=None, APDTimesFile=None, velocityFile=None, velocities=None, **kwargs):
    """
    Specific mesh loader for different tetrahedron files formats.


    :param name: object name  Default value: CardiacVTKLoader

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Invalid

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param filename: Filename of the object  Default value: 

    :param position: Vertices of the mesh loaded  Default value: []

    :param polylines: Polylines of the mesh loaded  Default value: []

    :param edges: Edges of the mesh loaded  Default value: []

    :param triangles: Triangles of the mesh loaded  Default value: []

    :param quads: Quads of the mesh loaded  Default value: []

    :param polygons: Polygons of the mesh loaded  Default value: []

    :param highOrderEdgePositions: High order edge points of the mesh loaded  Default value: []

    :param highOrderTrianglePositions: High order triangle points of the mesh loaded  Default value: []

    :param highOrderQuadPositions: High order quad points of the mesh loaded  Default value: []

    :param tetrahedra: Tetrahedra of the mesh loaded  Default value: []

    :param hexahedra: Hexahedra of the mesh loaded  Default value: []

    :param pentahedra: Pentahedra of the mesh loaded  Default value: []

    :param highOrderTetrahedronPositions: High order tetrahedron points of the mesh loaded  Default value: []

    :param highOrderHexahedronPositions: High order hexahedron points of the mesh loaded  Default value: []

    :param pyramids: Pyramids of the mesh loaded  Default value: []

    :param normals: Normals of the mesh loaded  Default value: []

    :param edgesGroups: Groups of Edges  Default value: 

    :param trianglesGroups: Groups of Triangles  Default value: 

    :param quadsGroups: Groups of Quads  Default value: 

    :param polygonsGroups: Groups of Polygons  Default value: 

    :param tetrahedraGroups: Groups of Tetrahedra  Default value: 

    :param hexahedraGroups: Groups of Hexahedra  Default value: 

    :param pentahedraGroups: Groups of Pentahedra  Default value: 

    :param pyramidsGroups: Groups of Pyramids  Default value: 

    :param flipNormals: Flip Normals  Default value: 0

    :param triangulate: Divide all polygons into triangles  Default value: 0

    :param createSubelements: Divide all n-D elements into their (n-1)-D boundary elements (e.g. tetrahedra to triangles)  Default value: 0

    :param onlyAttachedPoints: Only keep points attached to elements of the mesh  Default value: 0

    :param translation: Translation of the DOFs  Default value: [[0.0, 0.0, 0.0]]

    :param rotation: Rotation of the DOFs  Default value: [[0.0, 0.0, 0.0]]

    :param scale3d: Scale of the DOFs in 3 dimensions  Default value: [[1.0, 1.0, 1.0]]

    :param transformation: 4x4 Homogeneous matrix to transform the DOFs (when present replace any)  Default value: [[1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

    :param createFibers: if the loader must create the Fibers  Default value: 0

    :param outputNodeFibers: output Fibers  Default value: 

    :param outputTetraFibers: output Tetra Fibers  Default value: 

    :param TetraTriangle: Tetra or Triangle mesh  Default value: 

    :param unitTime: unit of the time scale use for electrophysiology (s or ms)  Default value: 

    :param TetraZoneName: name of the tetra data   Default value: LVRVTetrazones

    :param PointZoneName: PointZoneName  Default value: 

    :param withAHA: with AHA zones  Default value: 0

    :param TriZoneName: name of the endo epi data  Default value: 

    :param AHAzoneName: name of the tetra data   Default value: AHATetraZones

    :param startContraction: time at which the contraction starts  Default value: 0.0

    :param angleEpi: if the loader must create the Fibers  Default value: 0.0

    :param angleEndo: if the loader must create the Fibers  Default value: 0.0

    :param CellTypes: Type of each cell element  Default value: []

    :param numberOfZone: Vertices of the mesh loaded  Default value: 0

    :param m_zoneNames: See zones Name.  Default value: []

    :param m_zoneSizes: See zones Size.  Default value: []

    :param numberOfSurfaceZone: Vertices of the mesh loaded  Default value: 0

    :param m_surfaceZoneNames: See surface zones Name.  Default value: []

    :param m_surfaceZoneSizes: See surface zones Size.  Default value: []

    :param MSinitSurfaceZoneNames: Input-names of the surface zones for the init pacing of Mitchell Shaeffer (need for coupling)  Default value: []

    :param FileNodeFiber: Filename of the fiber par node of the mesh loaded (.bb file).  Default value: 

    :param nodeFibers: Fiber par node of the mesh loaded.  Default value: []

    :param FileFacetFiber: Filename of the fiber par facet of the mesh loaded (.tbb file).  Default value: 

    :param facetFibers: Fiber par facet of the mesh loaded.  Default value: []

    :param FileFacetBFiber: Filename of the fiber par facet of the mesh loaded, described in barycentric coordinates (.lbb file).  Default value: 

    :param facetBFibers: Fiber par facet of the mesh loaded, described in barycentric coordinates.  Default value: []

    :param FileTetraTensor: Filename of the tensor for each vertex on a tetra (.ttsr file)  Default value: 

    :param tetraTensor: tensor for each vertex on a tetra  Default value: []

    :param FileContractionParameters: Filename of the .txt containing the contraction parameters per zonename  Default value: 

    :param ContractionParameters: Parameter for linking to ContractionParameters from other components.  Default value: []

    :param InputContractionParameters: contraction parameter at each tetra  Default value: 

    :param FileTetraConductivity: FileTetraConductivity  Default value: 

    :param tetraConductivity:  Conductivity per tetra for MF electrical wave  Default value: []

    :param FileStiffnessParameters: Filename of the .txt containing the stiffness parameters per zonename  Default value: 

    :param StiffnessParameters: Parameter for linking to StiffnessParameters from other components.  Default value: []

    :param InputStiffnessParameters: stiffness parameter at each tetra  Default value: 

    :param ElectroFile: File with precomputed electrophysiology  Default value: 

    :param depoTimes: Times of depolarization per node  Default value: []

    :param APDTimes: Times of APD per node  Default value: []

    :param APDTimesZones: Times of APD per node  Default value: []

    :param APDTimesString: Times of APD per node  Default value: 

    :param APDTimesFile: Times of APD per node  Default value: 

    :param velocityFile: File with intial velocities  Default value: 

    :param velocities: initial velocities  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, position=position, polylines=polylines, edges=edges, triangles=triangles, quads=quads, polygons=polygons, highOrderEdgePositions=highOrderEdgePositions, highOrderTrianglePositions=highOrderTrianglePositions, highOrderQuadPositions=highOrderQuadPositions, tetrahedra=tetrahedra, hexahedra=hexahedra, pentahedra=pentahedra, highOrderTetrahedronPositions=highOrderTetrahedronPositions, highOrderHexahedronPositions=highOrderHexahedronPositions, pyramids=pyramids, normals=normals, edgesGroups=edgesGroups, trianglesGroups=trianglesGroups, quadsGroups=quadsGroups, polygonsGroups=polygonsGroups, tetrahedraGroups=tetrahedraGroups, hexahedraGroups=hexahedraGroups, pentahedraGroups=pentahedraGroups, pyramidsGroups=pyramidsGroups, flipNormals=flipNormals, triangulate=triangulate, createSubelements=createSubelements, onlyAttachedPoints=onlyAttachedPoints, translation=translation, rotation=rotation, scale3d=scale3d, transformation=transformation, createFibers=createFibers, outputNodeFibers=outputNodeFibers, outputTetraFibers=outputTetraFibers, TetraTriangle=TetraTriangle, unitTime=unitTime, TetraZoneName=TetraZoneName, PointZoneName=PointZoneName, withAHA=withAHA, TriZoneName=TriZoneName, AHAzoneName=AHAzoneName, startContraction=startContraction, angleEpi=angleEpi, angleEndo=angleEndo, CellTypes=CellTypes, numberOfZone=numberOfZone, m_zoneNames=m_zoneNames, m_zoneSizes=m_zoneSizes, numberOfSurfaceZone=numberOfSurfaceZone, m_surfaceZoneNames=m_surfaceZoneNames, m_surfaceZoneSizes=m_surfaceZoneSizes, MSinitSurfaceZoneNames=MSinitSurfaceZoneNames, FileNodeFiber=FileNodeFiber, nodeFibers=nodeFibers, FileFacetFiber=FileFacetFiber, facetFibers=facetFibers, FileFacetBFiber=FileFacetBFiber, facetBFibers=facetBFibers, FileTetraTensor=FileTetraTensor, tetraTensor=tetraTensor, FileContractionParameters=FileContractionParameters, ContractionParameters=ContractionParameters, InputContractionParameters=InputContractionParameters, FileTetraConductivity=FileTetraConductivity, tetraConductivity=tetraConductivity, FileStiffnessParameters=FileStiffnessParameters, StiffnessParameters=StiffnessParameters, InputStiffnessParameters=InputStiffnessParameters, ElectroFile=ElectroFile, depoTimes=depoTimes, APDTimes=APDTimes, APDTimesZones=APDTimesZones, APDTimesString=APDTimesString, APDTimesFile=APDTimesFile, velocityFile=velocityFile, velocities=velocities)
    return "CardiacVTKLoader", params
