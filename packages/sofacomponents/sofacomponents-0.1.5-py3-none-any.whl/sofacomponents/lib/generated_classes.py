from .base_component import sofa_component


class BaseSofaComponents:
    @sofa_component
    def EulerImplicitSolver(
        self,
        rayleighStiffness=None,
        rayleighMass=None,
        vdamping=None,
        firstOrder=None,
        trapezoidalScheme=None,
        solveConstraint=None,
        threadSafeVisitor=None,
        **kwargs
    ):
        """
        EulerImplicitSolver

        :param rayleighStiffness: Rayleigh damping coefficient related to stiffness, > 0
        :param rayleighMass: Rayleigh damping coefficient related to mass, > 0
        :param vdamping: Velocity decay coefficient (no decay if null)
        :param firstOrder: Use backward Euler scheme for first order ode system.
        :param trapezoidalScheme: Optional: use the trapezoidal scheme instead of the implicit Euler scheme and get second order accuracy in time
        :param solveConstraint: Apply ConstraintSolver (requires a ConstraintSolver in the same node as this solver, disabled by by default for now)
        :param threadSafeVisitor: If true, do not use realloc and free visitors in fwdInteractionForceField.
        """
        params = dict(
            rayleighStiffness=rayleighStiffness,
            rayleighMass=rayleighMass,
            vdamping=vdamping,
            firstOrder=firstOrder,
            trapezoidalScheme=trapezoidalScheme,
            solveConstraint=solveConstraint,
            threadSafeVisitor=threadSafeVisitor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "EulerImplicitSolver", params

    @sofa_component
    def StaticSolver(self, **kwargs):
        """
        StaticSolver
        """
        params = dict()
        return "StaticSolver", params

    @sofa_component
    def BaseVTKReader(self, **kwargs):
        """
        BaseVTKReader
        """
        params = dict()
        return "BaseVTKReader", params

    @sofa_component
    def MeshObjLoader(
        self,
        handleSeams=None,
        loadMaterial=None,
        defaultMaterial=None,
        materials=None,
        faceList=None,
        texcoordsIndex=None,
        positionsDefinition=None,
        texcoordsDefinition=None,
        normalsIndex=None,
        normalsDefinition=None,
        texcoords=None,
        computeMaterialFaces=None,
        vertPosIdx=None,
        vertNormIdx=None,
        **kwargs
    ):
        """
        MeshObjLoader

        :param handleSeams: Preserve UV and normal seams information (vertices with multiple UV and/or normals)
        :param loadMaterial: Load the related MTL file or use a default one?
        :param defaultMaterial: Default material
        :param materials: List of materials
        :param faceList: List of face definitions.
        :param texcoordsIndex: Indices of textures coordinates used in faces definition.
        :param positionsDefinition: Vertex positions definition
        :param texcoordsDefinition: Texture coordinates definition
        :param normalsIndex: List of normals of elements of the mesh loaded.
        :param normalsDefinition: Normals definition
        :param texcoords: Texture coordinates of all faces, to be used as the parent data of a VisualModel texcoords data
        :param computeMaterialFaces: True to activate export of Data instances containing list of face indices for each material
        :param vertPosIdx: If vertices have multiple normals/texcoords stores vertices position indices
        :param vertNormIdx: If vertices have multiple normals/texcoords stores vertices normal indices
        """
        params = dict(
            handleSeams=handleSeams,
            loadMaterial=loadMaterial,
            defaultMaterial=defaultMaterial,
            materials=materials,
            faceList=faceList,
            texcoordsIndex=texcoordsIndex,
            positionsDefinition=positionsDefinition,
            texcoordsDefinition=texcoordsDefinition,
            normalsIndex=normalsIndex,
            normalsDefinition=normalsDefinition,
            texcoords=texcoords,
            computeMaterialFaces=computeMaterialFaces,
            vertPosIdx=vertPosIdx,
            vertNormIdx=vertNormIdx,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshObjLoader", params

    @sofa_component
    def MeshVTKLoader(self, **kwargs):
        """
        MeshVTKLoader
        """
        params = dict()
        return "MeshVTKLoader", params

    @sofa_component
    def PenalityContactForceField(self, contacts=None, **kwargs):
        """
        PenalityContactForceField

        :param contacts: Contacts
        """
        params = dict(contacts=contacts)
        params = {k: v for k, v in params.items() if v is not None}
        return "PenalityContactForceField", params

    @sofa_component
    def BarycentricMapper(self, **kwargs):
        """
        BarycentricMapper
        """
        params = dict()
        return "BarycentricMapper", params

    @sofa_component
    def TopologyBarycentricMapper(self, **kwargs):
        """
        TopologyBarycentricMapper
        """
        params = dict()
        return "TopologyBarycentricMapper", params

    @sofa_component
    def BarycentricMapperMeshTopology(self, **kwargs):
        """
        BarycentricMapperMeshTopology
        """
        params = dict()
        return "BarycentricMapperMeshTopology", params

    @sofa_component
    def BarycentricMapperRegularGridTopology(self, **kwargs):
        """
        BarycentricMapperRegularGridTopology
        """
        params = dict()
        return "BarycentricMapperRegularGridTopology", params

    @sofa_component
    def BarycentricMapperSparseGridTopology(self, **kwargs):
        """
        BarycentricMapperSparseGridTopology
        """
        params = dict()
        return "BarycentricMapperSparseGridTopology", params

    @sofa_component
    def BarycentricMapperTopologyContainer(self, map=None, **kwargs):
        """
        BarycentricMapperTopologyContainer

        :param map: mapper data
        """
        params = dict(map=map)
        params = {k: v for k, v in params.items() if v is not None}
        return "BarycentricMapperTopologyContainer", params

    @sofa_component
    def BarycentricMapperEdgeSetTopology(self, **kwargs):
        """
        BarycentricMapperEdgeSetTopology
        """
        params = dict()
        return "BarycentricMapperEdgeSetTopology", params

    @sofa_component
    def BarycentricMapperTriangleSetTopology(self, **kwargs):
        """
        BarycentricMapperTriangleSetTopology
        """
        params = dict()
        return "BarycentricMapperTriangleSetTopology", params

    @sofa_component
    def BarycentricMapperQuadSetTopology(self, **kwargs):
        """
        BarycentricMapperQuadSetTopology
        """
        params = dict()
        return "BarycentricMapperQuadSetTopology", params

    @sofa_component
    def BarycentricMapperTetrahedronSetTopology(self, **kwargs):
        """
        BarycentricMapperTetrahedronSetTopology
        """
        params = dict()
        return "BarycentricMapperTetrahedronSetTopology", params

    @sofa_component
    def BarycentricMapperHexahedronSetTopology(self, **kwargs):
        """
        BarycentricMapperHexahedronSetTopology
        """
        params = dict()
        return "BarycentricMapperHexahedronSetTopology", params

    @sofa_component
    def BarycentricMapping(self, **kwargs):
        """
        BarycentricMapping
        """
        params = dict()
        return "BarycentricMapping", params

    @sofa_component
    def DiagonalMass(
        self,
        vertexMass=None,
        massDensity=None,
        totalMass=None,
        computeMassOnRest=None,
        showGravityCenter=None,
        showAxisSizeFactor=None,
        filename=None,
        **kwargs
    ):
        """
        DiagonalMass

        :param vertexMass: Specify a vector giving the mass of each vertex. \n
        :param massDensity: Specify one single real and positive value for the mass density. \n
        :param totalMass: Specify the total mass resulting from all particles. \n
        :param computeMassOnRest: If true, the mass of every element is computed based on the rest position rather than the position
        :param showGravityCenter: Display the center of gravity of the system
        :param showAxisSizeFactor: Factor length of the axis displayed (only used for rigids)
        :param filename: Xsp3.0 file to specify the mass parameters
        """
        params = dict(
            vertexMass=vertexMass,
            massDensity=massDensity,
            totalMass=totalMass,
            computeMassOnRest=computeMassOnRest,
            showGravityCenter=showGravityCenter,
            showAxisSizeFactor=showAxisSizeFactor,
            filename=filename,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "DiagonalMass", params

    @sofa_component
    def IdentityMapping(self, **kwargs):
        """
        IdentityMapping
        """
        params = dict()
        return "IdentityMapping", params

    @sofa_component
    def MappedObject(self, position=None, velocity=None, **kwargs):
        """
        MappedObject

        :param position: position vector
        :param velocity: velocity vector
        """
        params = dict(position=position, velocity=velocity)
        params = {k: v for k, v in params.items() if v is not None}
        return "MappedObject", params

    @sofa_component
    def MechanicalObject(
        self,
        position=None,
        velocity=None,
        force=None,
        rest_position=None,
        externalForce=None,
        derivX=None,
        free_position=None,
        free_velocity=None,
        constraint=None,
        mappingJacobian=None,
        reset_position=None,
        reset_velocity=None,
        restScale=None,
        useTopology=None,
        showObject=None,
        showObjectScale=None,
        showIndices=None,
        showIndicesScale=None,
        showVectors=None,
        showVectorsScale=None,
        drawMode=None,
        showColor=None,
        translation=None,
        rotation=None,
        scale3d=None,
        translation2=None,
        rotation2=None,
        size=None,
        reserve=None,
        **kwargs
    ):
        """
        MechanicalObject

        :param position: position coordinates of the degrees of freedom
        :param velocity: velocity coordinates of the degrees of freedom
        :param force: force vector of the degrees of freedom
        :param rest_position: rest position coordinates of the degrees of freedom
        :param externalForce: externalForces vector of the degrees of freedom
        :param derivX: dx vector of the degrees of freedom
        :param free_position: free position coordinates of the degrees of freedom
        :param free_velocity: free velocity coordinates of the degrees of freedom
        :param constraint: constraints applied to the degrees of freedom
        :param mappingJacobian: mappingJacobian applied to the degrees of freedom
        :param reset_position: reset position coordinates of the degrees of freedom
        :param reset_velocity: reset velocity coordinates of the degrees of freedom
        :param restScale: optional scaling of rest position coordinates (to simulated pre-existing internal tension).(default = 1.0)
        :param useTopology: Shall this object rely on any active topology to initialize its size and positions
        :param showObject: Show objects. (default=false)
        :param showObjectScale: Scale for object display. (default=0.1)
        :param showIndices: Show indices. (default=false)
        :param showIndicesScale: Scale for indices display. (default=0.02)
        :param showVectors: Show velocity. (default=false)
        :param showVectorsScale: Scale for vectors display. (default=0.0001)
        :param drawMode: The way vectors will be drawn:\n- 0: Line\n- 1:Cylinder\n- 2: Arrow.\n\nThe DOFS will be drawn:\n- 0: point\n- >1: sphere. (default=0)
        :param showColor: Color for object display. (default=[1 1 1 1])
        :param translation: Translation of the DOFs
        :param rotation: Rotation of the DOFs
        :param scale3d: Scale of the DOFs in 3 dimensions
        :param translation2: Translation of the DOFs, applied after the rest position has been computed
        :param rotation2: Rotation of the DOFs, applied the after the rest position has been computed
        :param size: Size of the vectors
        :param reserve: Size to reserve when creating vectors. (default=0)
        """
        params = dict(
            position=position,
            velocity=velocity,
            force=force,
            rest_position=rest_position,
            externalForce=externalForce,
            derivX=derivX,
            free_position=free_position,
            free_velocity=free_velocity,
            constraint=constraint,
            mappingJacobian=mappingJacobian,
            reset_position=reset_position,
            reset_velocity=reset_velocity,
            restScale=restScale,
            useTopology=useTopology,
            showObject=showObject,
            showObjectScale=showObjectScale,
            showIndices=showIndices,
            showIndicesScale=showIndicesScale,
            showVectors=showVectors,
            showVectorsScale=showVectorsScale,
            drawMode=drawMode,
            showColor=showColor,
            translation=translation,
            rotation=rotation,
            scale3d=scale3d,
            translation2=translation2,
            rotation2=rotation2,
            size=size,
            reserve=reserve,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MechanicalObject", params

    @sofa_component
    def SubsetMapping(
        self,
        indices=None,
        first=None,
        last=None,
        radius=None,
        handleTopologyChange=None,
        ignoreNotFound=None,
        resizeToModel=None,
        **kwargs
    ):
        """
        SubsetMapping

        :param indices: list of input indices
        :param first: first index (use if indices are sequential)
        :param last: last index (use if indices are sequential)
        :param radius: search radius to find corresponding points in case no indices are given
        :param handleTopologyChange: Enable support of topological changes for indices (disable if it is linked from SubsetTopologicalMapping::pointD2S)
        :param ignoreNotFound: True to ignore points that are not found in the input model, they will be treated as fixed points
        :param resizeToModel: True to resize the output MechanicalState to match the size of indices
        """
        params = dict(
            indices=indices,
            first=first,
            last=last,
            radius=radius,
            handleTopologyChange=handleTopologyChange,
            ignoreNotFound=ignoreNotFound,
            resizeToModel=resizeToModel,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SubsetMapping", params

    @sofa_component
    def UniformMass(
        self,
        vertexMass=None,
        totalMass=None,
        filename=None,
        showGravityCenter=None,
        showAxisSizeFactor=None,
        compute_mapping_inertia=None,
        showInitialCenterOfGravity=None,
        showX0=None,
        localRange=None,
        indices=None,
        handleTopologicalChanges=None,
        preserveTotalMass=None,
        **kwargs
    ):
        """
        UniformMass

        :param vertexMass: Specify one single, positive, real value for the mass of each particle. \n
        :param totalMass: Specify the total mass resulting from all particles. \n
        :param filename: rigid file to load the mass parameters
        :param showGravityCenter: display the center of gravity of the system
        :param showAxisSizeFactor: factor length of the axis displayed (only used for rigids)
        :param compute_mapping_inertia: to be used if the mass is placed under a mapping
        :param showInitialCenterOfGravity: display the initial center of gravity of the system
        :param showX0: display the rest positions
        :param localRange: optional range of local DOF indices. \n
        :param indices: optional local DOF indices. Any computation involving only indices outside of this list are discarded
        :param handleTopologicalChanges: The mass and totalMass are recomputed on particles add/remove.
        :param preserveTotalMass: Prevent totalMass from decreasing when removing particles.
        """
        params = dict(
            vertexMass=vertexMass,
            totalMass=totalMass,
            filename=filename,
            showGravityCenter=showGravityCenter,
            showAxisSizeFactor=showAxisSizeFactor,
            compute_mapping_inertia=compute_mapping_inertia,
            showInitialCenterOfGravity=showInitialCenterOfGravity,
            showX0=showX0,
            localRange=localRange,
            indices=indices,
            handleTopologicalChanges=handleTopologicalChanges,
            preserveTotalMass=preserveTotalMass,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "UniformMass", params

    @sofa_component
    def EdgeSetGeometryAlgorithms(
        self, showEdgeIndices=None, drawEdges=None, drawColorEdges=None, **kwargs
    ):
        """
        EdgeSetGeometryAlgorithms

        :param showEdgeIndices: Debug : view Edge indices.
        :param drawEdges: if true, draw the edges in the topology.
        :param drawColorEdges: RGB code color used to draw edges.
        """
        params = dict(
            showEdgeIndices=showEdgeIndices,
            drawEdges=drawEdges,
            drawColorEdges=drawColorEdges,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "EdgeSetGeometryAlgorithms", params

    @sofa_component
    def EdgeSetTopologyAlgorithms(self, **kwargs):
        """
        EdgeSetTopologyAlgorithms
        """
        params = dict()
        return "EdgeSetTopologyAlgorithms", params

    @sofa_component
    def EdgeSetTopologyContainer(self, edges=None, checkConnexity=None, **kwargs):
        """
        EdgeSetTopologyContainer

        :param edges: List of edge indices
        :param checkConnexity: It true, will check the connexity of the mesh.
        """
        params = dict(edges=edges, checkConnexity=checkConnexity)
        params = {k: v for k, v in params.items() if v is not None}
        return "EdgeSetTopologyContainer", params

    @sofa_component
    def EdgeSetTopologyModifier(self, **kwargs):
        """
        EdgeSetTopologyModifier
        """
        params = dict()
        return "EdgeSetTopologyModifier", params

    @sofa_component
    def GridTopology(
        self,
        n=None,
        computeHexaList=None,
        computeQuadList=None,
        computeTriangleList=None,
        computeEdgeList=None,
        computePointList=None,
        createTexCoords=None,
        **kwargs
    ):
        """
        GridTopology

        :param n: grid resolution. (default = 2 2 2)
        :param computeHexaList: put true if the list of Hexahedra is needed during init (default=true)
        :param computeQuadList: put true if the list of Quad is needed during init (default=true)
        :param computeTriangleList: put true if the list of triangle is needed during init (default=true)
        :param computeEdgeList: put true if the list of Lines is needed during init (default=true)
        :param computePointList: put true if the list of Points is needed during init (default=true)
        :param createTexCoords: If set to true, virtual texture coordinates will be generated using 3D interpolation (default=false).
        """
        params = dict(
            n=n,
            computeHexaList=computeHexaList,
            computeQuadList=computeQuadList,
            computeTriangleList=computeTriangleList,
            computeEdgeList=computeEdgeList,
            computePointList=computePointList,
            createTexCoords=createTexCoords,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "GridTopology", params

    @sofa_component
    def HexahedronSetGeometryAlgorithms(
        self,
        showHexaIndices=None,
        drawHexahedra=None,
        drawScaleHexahedra=None,
        drawColorHexahedra=None,
        **kwargs
    ):
        """
        HexahedronSetGeometryAlgorithms

        :param showHexaIndices: Debug : view Hexa indices
        :param drawHexahedra: if true, draw the Hexahedron in the topology
        :param drawScaleHexahedra: Scale of the hexahedra (between 0 and 1; if <1.0, it produces gaps between the hexahedra)
        :param drawColorHexahedra: RGB code color used to draw hexahedra.
        """
        params = dict(
            showHexaIndices=showHexaIndices,
            drawHexahedra=drawHexahedra,
            drawScaleHexahedra=drawScaleHexahedra,
            drawColorHexahedra=drawColorHexahedra,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "HexahedronSetGeometryAlgorithms", params

    @sofa_component
    def HexahedronSetTopologyAlgorithms(self, **kwargs):
        """
        HexahedronSetTopologyAlgorithms
        """
        params = dict()
        return "HexahedronSetTopologyAlgorithms", params

    @sofa_component
    def HexahedronSetTopologyContainer(
        self, createQuadArray=None, hexahedra=None, **kwargs
    ):
        """
        HexahedronSetTopologyContainer

        :param createQuadArray: Force the creation of a set of quads associated with the hexahedra
        :param hexahedra: List of hexahedron indices
        """
        params = dict(createQuadArray=createQuadArray, hexahedra=hexahedra)
        params = {k: v for k, v in params.items() if v is not None}
        return "HexahedronSetTopologyContainer", params

    @sofa_component
    def HexahedronSetTopologyModifier(self, removeIsolated=None, **kwargs):
        """
        HexahedronSetTopologyModifier

        :param removeIsolated: remove Isolated dof
        """
        params = dict(removeIsolated=removeIsolated)
        params = {k: v for k, v in params.items() if v is not None}
        return "HexahedronSetTopologyModifier", params

    @sofa_component
    def MeshTopology(
        self,
        position=None,
        edges=None,
        triangles=None,
        quads=None,
        tetrahedra=None,
        hexahedra=None,
        uv=None,
        drawEdges=None,
        drawTriangles=None,
        drawQuads=None,
        drawTetrahedra=None,
        drawHexahedra=None,
        **kwargs
    ):
        """
        MeshTopology

        :param position: List of point positions
        :param edges: List of edge indices
        :param triangles: List of triangle indices
        :param quads: List of quad indices
        :param tetrahedra: List of tetrahedron indices
        :param hexahedra: List of hexahedron indices
        :param uv: List of uv coordinates
        :param drawEdges: if true, draw the topology Edges
        :param drawTriangles: if true, draw the topology Triangles
        :param drawQuads: if true, draw the topology Quads
        :param drawTetrahedra: if true, draw the topology Tetrahedra
        :param drawHexahedra: if true, draw the topology hexahedra
        """
        params = dict(
            position=position,
            edges=edges,
            triangles=triangles,
            quads=quads,
            tetrahedra=tetrahedra,
            hexahedra=hexahedra,
            uv=uv,
            drawEdges=drawEdges,
            drawTriangles=drawTriangles,
            drawQuads=drawQuads,
            drawTetrahedra=drawTetrahedra,
            drawHexahedra=drawHexahedra,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshTopology", params

    @sofa_component
    def NumericalIntegrationDescriptor(self, **kwargs):
        """
        NumericalIntegrationDescriptor
        """
        params = dict()
        return "NumericalIntegrationDescriptor", params

    @sofa_component
    def PointSetGeometryAlgorithms(
        self, showIndicesScale=None, showPointIndices=None, tagMechanics=None, **kwargs
    ):
        """
        PointSetGeometryAlgorithms

        :param showIndicesScale: Debug : scale for view topology indices
        :param showPointIndices: Debug : view Point indices
        :param tagMechanics: Tag of the Mechanical Object
        """
        params = dict(
            showIndicesScale=showIndicesScale,
            showPointIndices=showPointIndices,
            tagMechanics=tagMechanics,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PointSetGeometryAlgorithms", params

    @sofa_component
    def PointSetTopologyAlgorithms(self, **kwargs):
        """
        PointSetTopologyAlgorithms
        """
        params = dict()
        return "PointSetTopologyAlgorithms", params

    @sofa_component
    def PointSetTopologyContainer(
        self, position=None, checkTopology=None, nbPoints=None, points=None, **kwargs
    ):
        """
        PointSetTopologyContainer

        :param position: Initial position of points
        :param checkTopology: Parameter to activate internal topology checks (might slow down the simulation)
        :param nbPoints: Number of points
        :param points: List of point indices
        """
        params = dict(
            position=position,
            checkTopology=checkTopology,
            nbPoints=nbPoints,
            points=points,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PointSetTopologyContainer", params

    @sofa_component
    def PointSetTopologyModifier(self, propagateToDOF=None, **kwargs):
        """
        PointSetTopologyModifier

        :param propagateToDOF:  propagate changes to MEchanical object DOFs if true
        """
        params = dict(propagateToDOF=propagateToDOF)
        params = {k: v for k, v in params.items() if v is not None}
        return "PointSetTopologyModifier", params

    @sofa_component
    def QuadSetGeometryAlgorithms(
        self, showQuadIndices=None, drawQuads=None, drawColorQuads=None, **kwargs
    ):
        """
        QuadSetGeometryAlgorithms

        :param showQuadIndices: Debug : view Quad indices
        :param drawQuads: if true, draw the quads in the topology
        :param drawColorQuads: RGB code color used to draw quads.
        """
        params = dict(
            showQuadIndices=showQuadIndices,
            drawQuads=drawQuads,
            drawColorQuads=drawColorQuads,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "QuadSetGeometryAlgorithms", params

    @sofa_component
    def QuadSetTopologyAlgorithms(self, **kwargs):
        """
        QuadSetTopologyAlgorithms
        """
        params = dict()
        return "QuadSetTopologyAlgorithms", params

    @sofa_component
    def QuadSetTopologyContainer(self, quads=None, **kwargs):
        """
        QuadSetTopologyContainer

        :param quads: List of quad indices
        """
        params = dict(quads=quads)
        params = {k: v for k, v in params.items() if v is not None}
        return "QuadSetTopologyContainer", params

    @sofa_component
    def QuadSetTopologyModifier(self, **kwargs):
        """
        QuadSetTopologyModifier
        """
        params = dict()
        return "QuadSetTopologyModifier", params

    @sofa_component
    def RegularGridTopology(
        self, min=None, max=None, p0=None, cellWidth=None, **kwargs
    ):
        """
        RegularGridTopology

        :param min: Min end of the diagonal
        :param max: Max end of the diagonal
        :param p0: Offset all the grid points
        :param cellWidth: if > 0 : dimension of each cell in the created grid. Otherwise, the cell size is computed based on min, max, and resolution n.
        """
        params = dict(min=min, max=max, p0=p0, cellWidth=cellWidth)
        params = {k: v for k, v in params.items() if v is not None}
        return "RegularGridTopology", params

    @sofa_component
    def SparseGridTopology(
        self,
        fillWeighted=None,
        onlyInsideCells=None,
        n=None,
        min=None,
        max=None,
        cellWidth=None,
        nbVirtualFinerLevels=None,
        dataResolution=None,
        voxelSize=None,
        marchingCubeStep=None,
        convolutionSize=None,
        facets=None,
        **kwargs
    ):
        """
        SparseGridTopology

        :param fillWeighted: Is quantity of matter inside a cell taken into account? (.5 for boundary, 1 for inside)
        :param onlyInsideCells: Select only inside cells (exclude boundary cells)
        :param n: grid resolution
        :param min: Min
        :param max: Max
        :param cellWidth: if > 0 : dimension of each cell in the created grid
        :param nbVirtualFinerLevels: create virtual (not in the animation tree) finer sparse grids in order to dispose of finest information (usefull to compute better mechanical properties for example)
        :param dataResolution: Dimension of the voxel File
        :param voxelSize: Dimension of one voxel
        :param marchingCubeStep: Step of the Marching Cube algorithm
        :param convolutionSize: Dimension of the convolution kernel to smooth the voxels. 0 if no smoothing is required.
        :param facets: Input mesh facets
        """
        params = dict(
            fillWeighted=fillWeighted,
            onlyInsideCells=onlyInsideCells,
            n=n,
            min=min,
            max=max,
            cellWidth=cellWidth,
            nbVirtualFinerLevels=nbVirtualFinerLevels,
            dataResolution=dataResolution,
            voxelSize=voxelSize,
            marchingCubeStep=marchingCubeStep,
            convolutionSize=convolutionSize,
            facets=facets,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SparseGridTopology", params

    @sofa_component
    def TetrahedronSetGeometryAlgorithms(
        self,
        showTetrahedraIndices=None,
        drawTetrahedra=None,
        drawScaleTetrahedra=None,
        drawColorTetrahedra=None,
        **kwargs
    ):
        """
        TetrahedronSetGeometryAlgorithms

        :param showTetrahedraIndices: Debug : view Tetrahedrons indices
        :param drawTetrahedra: if true, draw the tetrahedra in the topology
        :param drawScaleTetrahedra: Scale of the terahedra (between 0 and 1; if <1.0, it produces gaps between the tetrahedra)
        :param drawColorTetrahedra: RGBA code color used to draw tetrahedra.
        """
        params = dict(
            showTetrahedraIndices=showTetrahedraIndices,
            drawTetrahedra=drawTetrahedra,
            drawScaleTetrahedra=drawScaleTetrahedra,
            drawColorTetrahedra=drawColorTetrahedra,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedronSetGeometryAlgorithms", params

    @sofa_component
    def TetrahedronSetTopologyAlgorithms(self, **kwargs):
        """
        TetrahedronSetTopologyAlgorithms
        """
        params = dict()
        return "TetrahedronSetTopologyAlgorithms", params

    @sofa_component
    def TetrahedronSetTopologyContainer(
        self, createTriangleArray=None, tetrahedra=None, **kwargs
    ):
        """
        TetrahedronSetTopologyContainer

        :param createTriangleArray: Force the creation of a set of triangles associated with each tetrahedron
        :param tetrahedra: List of tetrahedron indices
        """
        params = dict(createTriangleArray=createTriangleArray, tetrahedra=tetrahedra)
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedronSetTopologyContainer", params

    @sofa_component
    def TetrahedronSetTopologyModifier(self, removeIsolated=None, **kwargs):
        """
        TetrahedronSetTopologyModifier

        :param removeIsolated: remove Isolated dof
        """
        params = dict(removeIsolated=removeIsolated)
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedronSetTopologyModifier", params

    @sofa_component
    def TopologyData(self, **kwargs):
        """
        TopologyData
        """
        params = dict()
        return "TopologyData", params

    @sofa_component
    def TopologyDataHandler(self, **kwargs):
        """
        TopologyDataHandler
        """
        params = dict()
        return "TopologyDataHandler", params

    @sofa_component
    def TopologyEngine(self, **kwargs):
        """
        TopologyEngine
        """
        params = dict()
        return "TopologyEngine", params

    @sofa_component
    def TopologySparseData(self, **kwargs):
        """
        TopologySparseData
        """
        params = dict()
        return "TopologySparseData", params

    @sofa_component
    def TopologySparseDataHandler(self, **kwargs):
        """
        TopologySparseDataHandler
        """
        params = dict()
        return "TopologySparseDataHandler", params

    @sofa_component
    def TopologySubsetData(self, **kwargs):
        """
        TopologySubsetData
        """
        params = dict()
        return "TopologySubsetData", params

    @sofa_component
    def TopologySubsetDataHandler(self, **kwargs):
        """
        TopologySubsetDataHandler
        """
        params = dict()
        return "TopologySubsetDataHandler", params

    @sofa_component
    def TriangleSetGeometryAlgorithms(
        self,
        showTriangleIndices=None,
        drawTriangles=None,
        drawColorTriangles=None,
        drawNormals=None,
        drawNormalLength=None,
        recomputeTrianglesOrientation=None,
        flipNormals=None,
        **kwargs
    ):
        """
        TriangleSetGeometryAlgorithms

        :param showTriangleIndices: Debug : view Triangle indices
        :param drawTriangles: if true, draw the triangles in the topology
        :param drawColorTriangles: RGBA code color used to draw edges.
        :param drawNormals: if true, draw the triangles in the topology
        :param drawNormalLength: Fiber length visualisation.
        :param recomputeTrianglesOrientation: if true, will recompute triangles orientation according to normals.
        :param flipNormals: if true, will flip normal of the first triangle used to recompute triangle orientation.
        """
        params = dict(
            showTriangleIndices=showTriangleIndices,
            drawTriangles=drawTriangles,
            drawColorTriangles=drawColorTriangles,
            drawNormals=drawNormals,
            drawNormalLength=drawNormalLength,
            recomputeTrianglesOrientation=recomputeTrianglesOrientation,
            flipNormals=flipNormals,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangleSetGeometryAlgorithms", params

    @sofa_component
    def TriangleSetTopologyAlgorithms(
        self, RemoveTrianglesByIndex=None, addTrianglesByIndex=None, **kwargs
    ):
        """
        TriangleSetTopologyAlgorithms

        :param RemoveTrianglesByIndex: Debug : Remove a triangle or a list of triangles by using their indices (only while animate).
        :param addTrianglesByIndex: Debug : Add a triangle or a list of triangles by using their indices (only while animate).
        """
        params = dict(
            RemoveTrianglesByIndex=RemoveTrianglesByIndex,
            addTrianglesByIndex=addTrianglesByIndex,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangleSetTopologyAlgorithms", params

    @sofa_component
    def TriangleSetTopologyContainer(self, triangles=None, **kwargs):
        """
        TriangleSetTopologyContainer

        :param triangles: List of triangle indices
        """
        params = dict(triangles=triangles)
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangleSetTopologyContainer", params

    @sofa_component
    def TriangleSetTopologyModifier(self, list_Out=None, **kwargs):
        """
        TriangleSetTopologyModifier

        :param list_Out: triangles with at least one null values.
        """
        params = dict(list_Out=list_Out)
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangleSetTopologyModifier", params

    @sofa_component
    def fake_TopologyScene(self, **kwargs):
        """
        fake_TopologyScene
        """
        params = dict()
        return "fake_TopologyScene", params

    @sofa_component
    def EigenMatrixManipulator(self, **kwargs):
        """
        EigenMatrixManipulator
        """
        params = dict()
        return "EigenMatrixManipulator", params

    @sofa_component
    def EigenVector(self, **kwargs):
        """
        EigenVector
        """
        params = dict()
        return "EigenVector", params

    @sofa_component
    def SVDLinearSolver(
        self, verbose=None, minSingularValue=None, conditionNumber=None, **kwargs
    ):
        """
        SVDLinearSolver

        :param verbose: Dump system state at each iteration
        :param minSingularValue: Thershold under which a singular value is set to 0, for the stabilization of ill-conditioned system.
        :param conditionNumber: Condition number of the matrix: ratio between the largest and smallest singular values. Computed in method solve.
        """
        params = dict(
            verbose=verbose,
            minSingularValue=minSingularValue,
            conditionNumber=conditionNumber,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SVDLinearSolver", params

    @sofa_component
    def EulerSolver(
        self,
        symplectic=None,
        optimizedForDiagonalMatrix=None,
        threadSafeVisitor=None,
        **kwargs
    ):
        """
        EulerSolver

        :param symplectic: If true, the velocities are updated before the positions and the method is symplectic (more robust). If false, the positions are updated before the velocities (standard Euler, less robust).
        :param optimizedForDiagonalMatrix: If true, solution to the system Ax=b can be directly found by computing x = f/m. Must be set to false if M is sparse.
        :param threadSafeVisitor: If true, do not use realloc and free visitors in fwdInteractionForceField.
        """
        params = dict(
            symplectic=symplectic,
            optimizedForDiagonalMatrix=optimizedForDiagonalMatrix,
            threadSafeVisitor=threadSafeVisitor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "EulerSolver", params

    @sofa_component
    def BarycentricContactMapper(self, **kwargs):
        """
        BarycentricContactMapper
        """
        params = dict()
        return "BarycentricContactMapper", params

    @sofa_component
    def BarycentricPenalityContact(self, **kwargs):
        """
        BarycentricPenalityContact
        """
        params = dict()
        return "BarycentricPenalityContact", params

    @sofa_component
    def IdentityContactMapper(self, **kwargs):
        """
        IdentityContactMapper
        """
        params = dict()
        return "IdentityContactMapper", params

    @sofa_component
    def IntrMeshUtility(self, **kwargs):
        """
        IntrMeshUtility
        """
        params = dict()
        return "IntrMeshUtility", params

    @sofa_component
    def IntrTriangleOBB(self, **kwargs):
        """
        IntrTriangleOBB
        """
        params = dict()
        return "IntrTriangleOBB", params

    @sofa_component
    def LineLocalMinDistanceFilter(self, pointInfo=None, lineInfo=None, **kwargs):
        """
        LineLocalMinDistanceFilter

        :param pointInfo: point filter data
        :param lineInfo: line filter data
        """
        params = dict(pointInfo=pointInfo, lineInfo=lineInfo)
        params = {k: v for k, v in params.items() if v is not None}
        return "LineLocalMinDistanceFilter", params

    @sofa_component
    def LineModel(self, bothSide=None, displayFreePosition=None, **kwargs):
        """
        LineModel

        :param bothSide: activate collision on both side of the line model (when surface normals are defined on these lines)
        :param displayFreePosition: Display Collision Model Points free position(in green)
        """
        params = dict(bothSide=bothSide, displayFreePosition=displayFreePosition)
        params = {k: v for k, v in params.items() if v is not None}
        return "LineModel", params

    @sofa_component
    def LocalMinDistanceFilter(
        self, coneExtension=None, coneMinAngle=None, isRigid=None, **kwargs
    ):
        """
        LocalMinDistanceFilter

        :param coneExtension: Filtering cone extension angle.
        :param coneMinAngle: Minimal filtering cone angle value, independent from geometry.
        :param isRigid: filters optimization for rigid case.
        """
        params = dict(
            coneExtension=coneExtension, coneMinAngle=coneMinAngle, isRigid=isRigid
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "LocalMinDistanceFilter", params

    @sofa_component
    def MeshIntTool(self, **kwargs):
        """
        MeshIntTool
        """
        params = dict()
        return "MeshIntTool", params

    @sofa_component
    def MeshNewProximityIntersection(self, **kwargs):
        """
        MeshNewProximityIntersection
        """
        params = dict()
        return "MeshNewProximityIntersection", params

    @sofa_component
    def PointLocalMinDistanceFilter(self, pointInfo=None, **kwargs):
        """
        PointLocalMinDistanceFilter

        :param pointInfo: point filter data
        """
        params = dict(pointInfo=pointInfo)
        params = {k: v for k, v in params.items() if v is not None}
        return "PointLocalMinDistanceFilter", params

    @sofa_component
    def PointModel(
        self, bothSide=None, computeNormals=None, displayFreePosition=None, **kwargs
    ):
        """
        PointModel

        :param bothSide: activate collision on both side of the point model (when surface normals are defined on these points)
        :param computeNormals: activate computation of normal vectors (required for some collision detection algorithms)
        :param displayFreePosition: Display Collision Model Points free position(in green)
        """
        params = dict(
            bothSide=bothSide,
            computeNormals=computeNormals,
            displayFreePosition=displayFreePosition,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PointModel", params

    @sofa_component
    def RayTriangleIntersection(self, **kwargs):
        """
        RayTriangleIntersection
        """
        params = dict()
        return "RayTriangleIntersection", params

    @sofa_component
    def RigidContactMapper(self, **kwargs):
        """
        RigidContactMapper
        """
        params = dict()
        return "RigidContactMapper", params

    @sofa_component
    def SubsetContactMapper(self, **kwargs):
        """
        SubsetContactMapper
        """
        params = dict()
        return "SubsetContactMapper", params

    @sofa_component
    def TriangleLocalMinDistanceFilter(
        self, pointInfo=None, lineInfo=None, triangleInfo=None, **kwargs
    ):
        """
        TriangleLocalMinDistanceFilter

        :param pointInfo: point filter data
        :param lineInfo: line filter data
        :param triangleInfo: triangle filter data
        """
        params = dict(pointInfo=pointInfo, lineInfo=lineInfo, triangleInfo=triangleInfo)
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangleLocalMinDistanceFilter", params

    @sofa_component
    def TriangleModel(self, bothSide=None, computeNormals=None, **kwargs):
        """
        TriangleModel

        :param bothSide: activate collision on both side of the triangle model
        :param computeNormals: set to false to disable computation of triangles normal
        """
        params = dict(bothSide=bothSide, computeNormals=computeNormals)
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangleModel", params

    @sofa_component
    def TaskSchedulerTestTasks(self, **kwargs):
        """
        TaskSchedulerTestTasks
        """
        params = dict()
        return "TaskSchedulerTestTasks", params

    @sofa_component
    def BaseContactMapper(self, **kwargs):
        """
        BaseContactMapper
        """
        params = dict()
        return "BaseContactMapper", params

    @sofa_component
    def BaseIntTool(self, **kwargs):
        """
        BaseIntTool
        """
        params = dict()
        return "BaseIntTool", params

    @sofa_component
    def BaseProximityIntersection(
        self, alarmDistance=None, contactDistance=None, **kwargs
    ):
        """
        BaseProximityIntersection

        :param alarmDistance: Proximity detection distance
        :param contactDistance: Distance below which a contact is created
        """
        params = dict(alarmDistance=alarmDistance, contactDistance=contactDistance)
        params = {k: v for k, v in params.items() if v is not None}
        return "BaseProximityIntersection", params

    @sofa_component
    def BruteForceDetection(self, box=None, **kwargs):
        """
        BruteForceDetection

        :param box: if not empty, objects that do not intersect this bounding-box will be ignored
        """
        params = dict(box=box)
        params = {k: v for k, v in params.items() if v is not None}
        return "BruteForceDetection", params

    @sofa_component
    def CapsuleIntTool(self, **kwargs):
        """
        CapsuleIntTool
        """
        params = dict()
        return "CapsuleIntTool", params

    @sofa_component
    def CapsuleModel(self, listCapsuleRadii=None, defaultRadius=None, **kwargs):
        """
        CapsuleModel

        :param listCapsuleRadii: Radius of each capsule
        :param defaultRadius: The default radius
        """
        params = dict(listCapsuleRadii=listCapsuleRadii, defaultRadius=defaultRadius)
        params = {k: v for k, v in params.items() if v is not None}
        return "CapsuleModel", params

    @sofa_component
    def ContactListener(self, **kwargs):
        """
        ContactListener
        """
        params = dict()
        return "ContactListener", params

    @sofa_component
    def CubeModel(self, **kwargs):
        """
        CubeModel
        """
        params = dict()
        return "CubeModel", params

    @sofa_component
    def CylinderModel(
        self,
        radii=None,
        heights=None,
        defaultRadius=None,
        defaultHeight=None,
        defaultLocalAxis=None,
        **kwargs
    ):
        """
        CylinderModel

        :param radii: Radius of each cylinder
        :param heights: The cylinder heights
        :param defaultRadius: The default radius
        :param defaultHeight: The default height
        :param defaultLocalAxis: The default local axis cylinder is modeled around
        """
        params = dict(
            radii=radii,
            heights=heights,
            defaultRadius=defaultRadius,
            defaultHeight=defaultHeight,
            defaultLocalAxis=defaultLocalAxis,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CylinderModel", params

    @sofa_component
    def DefaultContactManager(self, response=None, responseParams=None, **kwargs):
        """
        DefaultContactManager

        :param response: contact response class
        :param responseParams: contact response parameters (syntax: name1=value1&name2=value2&...)
        """
        params = dict(response=response, responseParams=responseParams)
        params = {k: v for k, v in params.items() if v is not None}
        return "DefaultContactManager", params

    @sofa_component
    def DefaultPipeline(self, **kwargs):
        """
        DefaultPipeline
        """
        params = dict()
        return "DefaultPipeline", params

    @sofa_component
    def DiscreteIntersection(self, **kwargs):
        """
        DiscreteIntersection
        """
        params = dict()
        return "DiscreteIntersection", params

    @sofa_component
    def IntrCapsuleOBB(self, **kwargs):
        """
        IntrCapsuleOBB
        """
        params = dict()
        return "IntrCapsuleOBB", params

    @sofa_component
    def IntrOBBOBB(self, **kwargs):
        """
        IntrOBBOBB
        """
        params = dict()
        return "IntrOBBOBB", params

    @sofa_component
    def IntrSphereOBB(self, **kwargs):
        """
        IntrSphereOBB
        """
        params = dict()
        return "IntrSphereOBB", params

    @sofa_component
    def IntrUtility3(self, **kwargs):
        """
        IntrUtility3
        """
        params = dict()
        return "IntrUtility3", params

    @sofa_component
    def MinProximityIntersection(
        self,
        useSphereTriangle=None,
        usePointPoint=None,
        useSurfaceNormals=None,
        useLinePoint=None,
        useLineLine=None,
        **kwargs
    ):
        """
        MinProximityIntersection

        :param useSphereTriangle: activate Sphere-Triangle intersection tests
        :param usePointPoint: activate Point-Point intersection tests
        :param useSurfaceNormals: Compute the norms of the Detection Outputs by considering the normals of the surfaces involved.
        :param useLinePoint: activate Line-Point intersection tests
        :param useLineLine: activate Line-Line  intersection tests
        """
        params = dict(
            useSphereTriangle=useSphereTriangle,
            usePointPoint=usePointPoint,
            useSurfaceNormals=useSurfaceNormals,
            useLinePoint=useLinePoint,
            useLineLine=useLineLine,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MinProximityIntersection", params

    @sofa_component
    def NewProximityIntersection(self, useLineLine=None, **kwargs):
        """
        NewProximityIntersection

        :param useLineLine: Line-line collision detection enabled
        """
        params = dict(useLineLine=useLineLine)
        params = {k: v for k, v in params.items() if v is not None}
        return "NewProximityIntersection", params

    @sofa_component
    def OBBIntTool(self, **kwargs):
        """
        OBBIntTool
        """
        params = dict()
        return "OBBIntTool", params

    @sofa_component
    def OBBModel(self, extents=None, defaultExtent=None, **kwargs):
        """
        OBBModel

        :param extents: Extents in x,y and z directions
        :param defaultExtent: Default extent
        """
        params = dict(extents=extents, defaultExtent=defaultExtent)
        params = {k: v for k, v in params.items() if v is not None}
        return "OBBModel", params

    @sofa_component
    def RigidCapsuleModel(
        self, radii=None, heights=None, defaultRadius=None, dafaultHeight=None, **kwargs
    ):
        """
        RigidCapsuleModel

        :param radii: Radius of each capsule
        :param heights: The capsule heights
        :param defaultRadius: The default radius
        :param dafaultHeight: The default height
        """
        params = dict(
            radii=radii,
            heights=heights,
            defaultRadius=defaultRadius,
            dafaultHeight=dafaultHeight,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "RigidCapsuleModel", params

    @sofa_component
    def SphereModel(self, listRadius=None, radius=None, showImpostors=None, **kwargs):
        """
        SphereModel

        :param listRadius: Radius of each sphere
        :param radius: Default Radius. (default=1.0)
        :param showImpostors: Draw spheres as impostors instead of real spheres
        """
        params = dict(listRadius=listRadius, radius=radius, showImpostors=showImpostors)
        params = {k: v for k, v in params.items() if v is not None}
        return "SphereModel", params

    @sofa_component
    def BoxROI(
        self,
        box=None,
        orientedBox=None,
        position=None,
        edges=None,
        triangles=None,
        tetrahedra=None,
        hexahedra=None,
        quad=None,
        computeEdges=None,
        computeTriangles=None,
        computeTetrahedra=None,
        computeHexahedra=None,
        computeQuad=None,
        strict=None,
        indices=None,
        edgeIndices=None,
        triangleIndices=None,
        tetrahedronIndices=None,
        hexahedronIndices=None,
        quadIndices=None,
        pointsInROI=None,
        edgesInROI=None,
        trianglesInROI=None,
        tetrahedraInROI=None,
        hexahedraInROI=None,
        quadInROI=None,
        nbIndices=None,
        drawBoxes=None,
        drawPoints=None,
        drawEdges=None,
        drawTriangles=None,
        drawTetrahedra=None,
        drawHexahedra=None,
        drawQuads=None,
        drawSize=None,
        doUpdate=None,
        rest_position=None,
        isVisible=None,
        **kwargs
    ):
        """
        BoxROI

        :param box: List of boxes defined by xmin,ymin,zmin, xmax,ymax,zmax
        :param orientedBox: List of boxes defined by 3 points (p0, p1, p2) and a depth distance \n
        :param position: Rest position coordinates of the degrees of freedom. \n
        :param edges: Edge Topology
        :param triangles: Triangle Topology
        :param tetrahedra: Tetrahedron Topology
        :param hexahedra: Hexahedron Topology
        :param quad: Quad Topology
        :param computeEdges: If true, will compute edge list and index list inside the ROI. (default = true)
        :param computeTriangles: If true, will compute triangle list and index list inside the ROI. (default = true)
        :param computeTetrahedra: If true, will compute tetrahedra list and index list inside the ROI. (default = true)
        :param computeHexahedra: If true, will compute hexahedra list and index list inside the ROI. (default = true)
        :param computeQuad: If true, will compute quad list and index list inside the ROI. (default = true)
        :param strict: If true, an element is inside the box iif all of its nodes are inside. If False, only the center point of the element is checked. (default = true)
        :param indices: Indices of the points contained in the ROI
        :param edgeIndices: Indices of the edges contained in the ROI
        :param triangleIndices: Indices of the triangles contained in the ROI
        :param tetrahedronIndices: Indices of the tetrahedra contained in the ROI
        :param hexahedronIndices: Indices of the hexahedra contained in the ROI
        :param quadIndices: Indices of the quad contained in the ROI
        :param pointsInROI: Points contained in the ROI
        :param edgesInROI: Edges contained in the ROI
        :param trianglesInROI: Triangles contained in the ROI
        :param tetrahedraInROI: Tetrahedra contained in the ROI
        :param hexahedraInROI: Hexahedra contained in the ROI
        :param quadInROI: Quad contained in the ROI
        :param nbIndices: Number of selected indices
        :param drawBoxes: Draw Boxes. (default = false)
        :param drawPoints: Draw Points. (default = false)
        :param drawEdges: Draw Edges. (default = false)
        :param drawTriangles: Draw Triangles. (default = false)
        :param drawTetrahedra: Draw Tetrahedra. (default = false)
        :param drawHexahedra: Draw Tetrahedra. (default = false)
        :param drawQuads: Draw Quads. (default = false)
        :param drawSize: rendering size for box and topological elements
        :param doUpdate: If true, updates the selection at the beginning of simulation steps. (default = true)
        :param rest_position: (deprecated) Replaced with the attribute 'position'
        :param isVisible: (deprecated)Replaced with the attribute 'drawBoxes'
        """
        params = dict(
            box=box,
            orientedBox=orientedBox,
            position=position,
            edges=edges,
            triangles=triangles,
            tetrahedra=tetrahedra,
            hexahedra=hexahedra,
            quad=quad,
            computeEdges=computeEdges,
            computeTriangles=computeTriangles,
            computeTetrahedra=computeTetrahedra,
            computeHexahedra=computeHexahedra,
            computeQuad=computeQuad,
            strict=strict,
            indices=indices,
            edgeIndices=edgeIndices,
            triangleIndices=triangleIndices,
            tetrahedronIndices=tetrahedronIndices,
            hexahedronIndices=hexahedronIndices,
            quadIndices=quadIndices,
            pointsInROI=pointsInROI,
            edgesInROI=edgesInROI,
            trianglesInROI=trianglesInROI,
            tetrahedraInROI=tetrahedraInROI,
            hexahedraInROI=hexahedraInROI,
            quadInROI=quadInROI,
            nbIndices=nbIndices,
            drawBoxes=drawBoxes,
            drawPoints=drawPoints,
            drawEdges=drawEdges,
            drawTriangles=drawTriangles,
            drawTetrahedra=drawTetrahedra,
            drawHexahedra=drawHexahedra,
            drawQuads=drawQuads,
            drawSize=drawSize,
            doUpdate=doUpdate,
            rest_position=rest_position,
            isVisible=isVisible,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "BoxROI", params

    @sofa_component
    def TestEngine(self, number=None, factor=None, result=None, **kwargs):
        """
        TestEngine

        :param number: number that will be multiplied by the factor
        :param factor: multiplication factor
        :param result: result of the multiplication of numberToMultiply by factor
        """
        params = dict(number=number, factor=factor, result=result)
        params = {k: v for k, v in params.items() if v is not None}
        return "TestEngine", params

    @sofa_component
    def BaseCamera(
        self,
        position=None,
        orientation=None,
        lookAt=None,
        distance=None,
        fieldOfView=None,
        zNear=None,
        zFar=None,
        computeZClip=None,
        minBBox=None,
        maxBBox=None,
        widthViewport=None,
        heightViewport=None,
        projectionType=None,
        activated=None,
        fixedLookAt=None,
        modelViewMatrix=None,
        projectionMatrix=None,
        **kwargs
    ):
        """
        BaseCamera

        :param position: Camera's position
        :param orientation: Camera's orientation
        :param lookAt: Camera's look at
        :param distance: Distance between camera and look at
        :param fieldOfView: Camera's FOV
        :param zNear: Camera's zNear
        :param zFar: Camera's zFar
        :param computeZClip: Compute Z clip planes (Near and Far) according to the bounding box
        :param minBBox: minBBox
        :param maxBBox: maxBBox
        :param widthViewport: widthViewport
        :param heightViewport: heightViewport
        :param projectionType: Camera Type (0 = Perspective, 1 = Orthographic)
        :param activated: Camera activated ?
        :param fixedLookAt: keep the lookAt point always fixed
        :param modelViewMatrix: ModelView Matrix
        :param projectionMatrix: Projection Matrix
        """
        params = dict(
            position=position,
            orientation=orientation,
            lookAt=lookAt,
            distance=distance,
            fieldOfView=fieldOfView,
            zNear=zNear,
            zFar=zFar,
            computeZClip=computeZClip,
            minBBox=minBBox,
            maxBBox=maxBBox,
            widthViewport=widthViewport,
            heightViewport=heightViewport,
            projectionType=projectionType,
            activated=activated,
            fixedLookAt=fixedLookAt,
            modelViewMatrix=modelViewMatrix,
            projectionMatrix=projectionMatrix,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "BaseCamera", params

    @sofa_component
    def BackgroundSetting(self, color=None, image=None, **kwargs):
        """
        BackgroundSetting

        :param color: Color of the background
        :param image: Image to be used as background
        """
        params = dict(color=color, image=image)
        params = {k: v for k, v in params.items() if v is not None}
        return "BackgroundSetting", params

    @sofa_component
    def Camera(self, **kwargs):
        """
        Camera
        """
        params = dict()
        return "Camera", params

    @sofa_component
    def InteractiveCamera(self, zoomSpeed=None, panSpeed=None, pivot=None, **kwargs):
        """
        InteractiveCamera

        :param zoomSpeed: Zoom Speed
        :param panSpeed: Pan Speed
        :param pivot: Pivot (0 => Camera lookAt, 1 => Camera position, 2 => Scene center, 3 => World center
        """
        params = dict(zoomSpeed=zoomSpeed, panSpeed=panSpeed, pivot=pivot)
        params = {k: v for k, v in params.items() if v is not None}
        return "InteractiveCamera", params

    @sofa_component
    def VisualModelImpl(
        self,
        position=None,
        restPosition=None,
        normal=None,
        initRestPositions=None,
        useNormals=None,
        updateNormals=None,
        computeTangents=None,
        updateTangents=None,
        handleDynamicTopology=None,
        fixMergedUVSeams=None,
        keepLines=None,
        vertices=None,
        texcoords=None,
        tangents=None,
        bitangents=None,
        edges=None,
        triangles=None,
        quads=None,
        vertPosIdx=None,
        vertNormIdx=None,
        filename=None,
        texturename=None,
        translation=None,
        rotation=None,
        scale3d=None,
        scaleTex=None,
        translationTex=None,
        material=None,
        putOnlyTexCoords=None,
        srgbTexturing=None,
        materials=None,
        groups=None,
        **kwargs
    ):
        """
        VisualModelImpl

        :param position: Vertices coordinates
        :param restPosition: Vertices rest coordinates
        :param normal: Normals of the model
        :param initRestPositions: True if rest positions must be initialized with initial positions
        :param useNormals: True if normal smoothing groups should be read from file
        :param updateNormals: True if normals should be updated at each iteration
        :param computeTangents: True if tangents should be computed at startup
        :param updateTangents: True if tangents should be updated at each iteration
        :param handleDynamicTopology: True if topological changes should be handled
        :param fixMergedUVSeams: True if UV seams should be handled even when duplicate UVs are merged
        :param keepLines: keep and draw lines (false by default)
        :param vertices: vertices of the model (only if vertices have multiple normals/texcoords, otherwise positions are used)
        :param texcoords: coordinates of the texture
        :param tangents: tangents for normal mapping
        :param bitangents: tangents for normal mapping
        :param edges: edges of the model
        :param triangles: triangles of the model
        :param quads: quads of the model
        :param vertPosIdx: If vertices have multiple normals/texcoords stores vertices position indices
        :param vertNormIdx: If vertices have multiple normals/texcoords stores vertices normal indices
        :param filename:  Path to an ogl model
        :param texturename: Name of the Texture
        :param translation: Initial Translation of the object
        :param rotation: Initial Rotation of the object
        :param scale3d: Initial Scale of the object
        :param scaleTex: Scale of the texture
        :param translationTex: Translation of the texture
        :param material: Material
        :param putOnlyTexCoords: Give Texture Coordinates without the texture binding
        :param srgbTexturing: When sRGB rendering is enabled, is the texture in sRGB colorspace?
        :param materials: List of materials
        :param groups: Groups of triangles and quads using a given material
        """
        params = dict(
            position=position,
            restPosition=restPosition,
            normal=normal,
            initRestPositions=initRestPositions,
            useNormals=useNormals,
            updateNormals=updateNormals,
            computeTangents=computeTangents,
            updateTangents=updateTangents,
            handleDynamicTopology=handleDynamicTopology,
            fixMergedUVSeams=fixMergedUVSeams,
            keepLines=keepLines,
            vertices=vertices,
            texcoords=texcoords,
            tangents=tangents,
            bitangents=bitangents,
            edges=edges,
            triangles=triangles,
            quads=quads,
            vertPosIdx=vertPosIdx,
            vertNormIdx=vertNormIdx,
            filename=filename,
            texturename=texturename,
            translation=translation,
            rotation=rotation,
            scale3d=scale3d,
            scaleTex=scaleTex,
            translationTex=translationTex,
            material=material,
            putOnlyTexCoords=putOnlyTexCoords,
            srgbTexturing=srgbTexturing,
            materials=materials,
            groups=groups,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "VisualModelImpl", params

    @sofa_component
    def VisualStyle(self, displayFlags=None, **kwargs):
        """
        VisualStyle

        :param displayFlags: Display Flags
        """
        params = dict(displayFlags=displayFlags)
        params = {k: v for k, v in params.items() if v is not None}
        return "VisualStyle", params

    @sofa_component
    def HexahedronFEMForceField(
        self,
        method=None,
        poissonRatio=None,
        youngModulus=None,
        updateStiffnessMatrix=None,
        assembling=None,
        gatherPt=None,
        gatherBsize=None,
        drawing=None,
        drawPercentageOffset=None,
        stiffnessMatrices=None,
        initialPoints=None,
        **kwargs
    ):
        """
        HexahedronFEMForceField

        :param method: large or polar or small displacements
        :param poissonRatio:
        :param youngModulus:
        :param updateStiffnessMatrix:
        :param assembling:
        :param gatherPt: number of dof accumulated per threads during the gather operation (Only use in GPU version)
        :param gatherBsize: number of dof accumulated per threads during the gather operation (Only use in GPU version)
        :param drawing:  draw the forcefield if true
        :param drawPercentageOffset: size of the hexa
        :param stiffnessMatrices: Stiffness matrices per element (K_i)
        :param initialPoints: Initial Position
        """
        params = dict(
            method=method,
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            updateStiffnessMatrix=updateStiffnessMatrix,
            assembling=assembling,
            gatherPt=gatherPt,
            gatherBsize=gatherBsize,
            drawing=drawing,
            drawPercentageOffset=drawPercentageOffset,
            stiffnessMatrices=stiffnessMatrices,
            initialPoints=initialPoints,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "HexahedronFEMForceField", params

    @sofa_component
    def TetrahedronFEMForceField(
        self,
        initialPoints=None,
        method=None,
        poissonRatio=None,
        youngModulus=None,
        localStiffnessFactor=None,
        updateStiffnessMatrix=None,
        computeGlobalMatrix=None,
        plasticMaxThreshold=None,
        plasticYieldThreshold=None,
        plasticCreep=None,
        gatherPt=None,
        gatherBsize=None,
        drawHeterogeneousTetra=None,
        drawAsEdges=None,
        computeVonMisesStress=None,
        vonMisesPerElement=None,
        vonMisesPerNode=None,
        vonMisesStressColors=None,
        showStressColorMap=None,
        showStressAlpha=None,
        showVonMisesStressPerNode=None,
        updateStiffness=None,
        **kwargs
    ):
        """
        TetrahedronFEMForceField

        :param initialPoints: Initial Position
        :param method: small, large (by QR), polar or svd displacements
        :param poissonRatio: FEM Poisson Ratio [0,0.5[
        :param youngModulus: FEM Young Modulus
        :param localStiffnessFactor: Allow specification of different stiffness per element. If there are N element and M values are specified, the youngModulus factor for element i would be localStiffnessFactor[i*M/N]
        :param updateStiffnessMatrix:
        :param computeGlobalMatrix:
        :param plasticMaxThreshold: Plastic Max Threshold (2-norm of the strain)
        :param plasticYieldThreshold: Plastic Yield Threshold (2-norm of the strain)
        :param plasticCreep: Plastic Creep Factor * dt [0,1]. Warning this factor depends on dt.
        :param gatherPt: number of dof accumulated per threads during the gather operation (Only use in GPU version)
        :param gatherBsize: number of dof accumulated per threads during the gather operation (Only use in GPU version)
        :param drawHeterogeneousTetra: Draw Heterogeneous Tetra in different color
        :param drawAsEdges: Draw as edges instead of tetrahedra
        :param computeVonMisesStress: compute and display von Mises stress: 0: no computations, 1: using corotational strain, 2: using full Green strain
        :param vonMisesPerElement: von Mises Stress per element
        :param vonMisesPerNode: von Mises Stress per node
        :param vonMisesStressColors: Vector of colors describing the VonMises stress
        :param showStressColorMap: Color map used to show stress values
        :param showStressAlpha: Alpha for vonMises visualisation
        :param showVonMisesStressPerNode: draw points  showing vonMises stress interpolated in nodes
        :param updateStiffness: udpate structures (precomputed in init) using stiffness parameters in each iteration (set listening=1)
        """
        params = dict(
            initialPoints=initialPoints,
            method=method,
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            localStiffnessFactor=localStiffnessFactor,
            updateStiffnessMatrix=updateStiffnessMatrix,
            computeGlobalMatrix=computeGlobalMatrix,
            plasticMaxThreshold=plasticMaxThreshold,
            plasticYieldThreshold=plasticYieldThreshold,
            plasticCreep=plasticCreep,
            gatherPt=gatherPt,
            gatherBsize=gatherBsize,
            drawHeterogeneousTetra=drawHeterogeneousTetra,
            drawAsEdges=drawAsEdges,
            computeVonMisesStress=computeVonMisesStress,
            vonMisesPerElement=vonMisesPerElement,
            vonMisesPerNode=vonMisesPerNode,
            vonMisesStressColors=vonMisesStressColors,
            showStressColorMap=showStressColorMap,
            showStressAlpha=showStressAlpha,
            showVonMisesStressPerNode=showVonMisesStressPerNode,
            updateStiffness=updateStiffness,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedronFEMForceField", params

    @sofa_component
    def TetrahedronDiffusionFEMForceField(
        self,
        constantDiffusionCoefficient=None,
        tetraDiffusionCoefficient=None,
        scalarDiffusion=None,
        anisotropyRatio=None,
        transverseAnisotropyArray=None,
        tagMechanics=None,
        drawConduc=None,
        **kwargs
    ):
        """
        TetrahedronDiffusionFEMForceField

        :param constantDiffusionCoefficient: Constant diffusion coefficient
        :param tetraDiffusionCoefficient: Diffusion coefficient for each tetrahedron, by default equal to constantDiffusionCoefficient.
        :param scalarDiffusion: if true, diffuse only on the first dimension.
        :param anisotropyRatio: Anisotropy ratio (r²>1).\n Default is 1.0 = isotropy.
        :param transverseAnisotropyArray: Data to handle topology on tetrahedra
        :param tagMechanics: Tag of the Mechanical Object.
        :param drawConduc: To display conductivity map.
        """
        params = dict(
            constantDiffusionCoefficient=constantDiffusionCoefficient,
            tetraDiffusionCoefficient=tetraDiffusionCoefficient,
            scalarDiffusion=scalarDiffusion,
            anisotropyRatio=anisotropyRatio,
            transverseAnisotropyArray=transverseAnisotropyArray,
            tagMechanics=tagMechanics,
            drawConduc=drawConduc,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedronDiffusionFEMForceField", params

    @sofa_component
    def CGLinearSolver(
        self,
        iterations=None,
        tolerance=None,
        threshold=None,
        warmStart=None,
        verbose=None,
        graph=None,
        **kwargs
    ):
        """
        CGLinearSolver

        :param iterations: Maximum number of iterations of the Conjugate Gradient solution
        :param tolerance: Desired accuracy of the Conjugate Gradient solution (ratio of current residual norm over initial residual norm)
        :param threshold: Minimum value of the denominator in the conjugate Gradient solution
        :param warmStart: Use previous solution as initial solution
        :param verbose: Dump system state at each iteration
        :param graph: Graph of residuals at each iteration
        """
        params = dict(
            iterations=iterations,
            tolerance=tolerance,
            threshold=threshold,
            warmStart=warmStart,
            verbose=verbose,
            graph=graph,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CGLinearSolver", params

    @sofa_component
    def CompressedRowSparseMatrix(self, **kwargs):
        """
        CompressedRowSparseMatrix
        """
        params = dict()
        return "CompressedRowSparseMatrix", params

    @sofa_component
    def DefaultMultiMatrixAccessor(self, **kwargs):
        """
        DefaultMultiMatrixAccessor
        """
        params = dict()
        return "DefaultMultiMatrixAccessor", params

    @sofa_component
    def FullVector(self, **kwargs):
        """
        FullVector
        """
        params = dict()
        return "FullVector", params

    @sofa_component
    def GraphScatteredTypes(self, **kwargs):
        """
        GraphScatteredTypes
        """
        params = dict()
        return "GraphScatteredTypes", params

    @sofa_component
    def MatrixLinearSolver(self, **kwargs):
        """
        MatrixLinearSolver
        """
        params = dict()
        return "MatrixLinearSolver", params

    @sofa_component
    def SingleMatrixAccessor(self, **kwargs):
        """
        SingleMatrixAccessor
        """
        params = dict()
        return "SingleMatrixAccessor", params

    @sofa_component
    def AngularSpringForceField(
        self,
        indices=None,
        angularStiffness=None,
        limit=None,
        drawSpring=None,
        springColor=None,
        **kwargs
    ):
        """
        AngularSpringForceField

        :param indices: index of nodes controlled by the angular springs
        :param angularStiffness: angular stiffness for the controlled nodes
        :param limit: angular limit (max; min) values where the force applies
        :param drawSpring: draw Spring
        :param springColor: spring color
        """
        params = dict(
            indices=indices,
            angularStiffness=angularStiffness,
            limit=limit,
            drawSpring=drawSpring,
            springColor=springColor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "AngularSpringForceField", params

    @sofa_component
    def MeshSpringForceField(
        self,
        linesStiffness=None,
        linesDamping=None,
        trianglesStiffness=None,
        trianglesDamping=None,
        quadsStiffness=None,
        quadsDamping=None,
        tetrahedraStiffness=None,
        tetrahedraDamping=None,
        cubesStiffness=None,
        cubesDamping=None,
        noCompression=None,
        drawMinElongationRange=None,
        drawMaxElongationRange=None,
        drawSpringSize=None,
        localRange=None,
        **kwargs
    ):
        """
        MeshSpringForceField

        :param linesStiffness: Stiffness for the Lines
        :param linesDamping: Damping for the Lines
        :param trianglesStiffness: Stiffness for the Triangles
        :param trianglesDamping: Damping for the Triangles
        :param quadsStiffness: Stiffness for the Quads
        :param quadsDamping: Damping for the Quads
        :param tetrahedraStiffness: Stiffness for the Tetrahedra
        :param tetrahedraDamping: Damping for the Tetrahedra
        :param cubesStiffness: Stiffness for the Cubes
        :param cubesDamping: Damping for the Cubes
        :param noCompression: Only consider elongation
        :param drawMinElongationRange: Min range of elongation (red eongation - blue neutral - green compression)
        :param drawMaxElongationRange: Max range of elongation (red eongation - blue neutral - green compression)
        :param drawSpringSize: Size of drawed lines
        :param localRange: optional range of local DOF indices. Any computation involving only indices outside of this range are discarded (useful for parallelization using mesh partitionning)
        """
        params = dict(
            linesStiffness=linesStiffness,
            linesDamping=linesDamping,
            trianglesStiffness=trianglesStiffness,
            trianglesDamping=trianglesDamping,
            quadsStiffness=quadsStiffness,
            quadsDamping=quadsDamping,
            tetrahedraStiffness=tetrahedraStiffness,
            tetrahedraDamping=tetrahedraDamping,
            cubesStiffness=cubesStiffness,
            cubesDamping=cubesDamping,
            noCompression=noCompression,
            drawMinElongationRange=drawMinElongationRange,
            drawMaxElongationRange=drawMaxElongationRange,
            drawSpringSize=drawSpringSize,
            localRange=localRange,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshSpringForceField", params

    @sofa_component
    def RestShapeSpringsForceField(
        self,
        points=None,
        stiffness=None,
        angularStiffness=None,
        pivot_points=None,
        external_points=None,
        recompute_indices=None,
        drawSpring=None,
        springColor=None,
        **kwargs
    ):
        """
        RestShapeSpringsForceField

        :param points: points controlled by the rest shape springs
        :param stiffness: stiffness values between the actual position and the rest shape position
        :param angularStiffness: angularStiffness assigned when controlling the rotation of the points
        :param pivot_points: global pivot points used when translations instead of the rigid mass centers
        :param external_points: points from the external Mechancial State that define the rest shape springs
        :param recompute_indices: Recompute indices (should be false for BBOX)
        :param drawSpring: draw Spring
        :param springColor: spring color. (default=[0.0,1.0,0.0,1.0])
        """
        params = dict(
            points=points,
            stiffness=stiffness,
            angularStiffness=angularStiffness,
            pivot_points=pivot_points,
            external_points=external_points,
            recompute_indices=recompute_indices,
            drawSpring=drawSpring,
            springColor=springColor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "RestShapeSpringsForceField", params

    @sofa_component
    def SpringForceField(
        self,
        stiffness=None,
        damping=None,
        showArrowSize=None,
        drawMode=None,
        spring=None,
        **kwargs
    ):
        """
        SpringForceField

        :param stiffness: uniform stiffness for the all springs
        :param damping: uniform damping for the all springs
        :param showArrowSize: size of the axis
        :param drawMode: The way springs will be drawn:\n- 0: Line\n- 1:Cylinder\n- 2: Arrow
        :param spring: pairs of indices, stiffness, damping, rest length
        """
        params = dict(
            stiffness=stiffness,
            damping=damping,
            showArrowSize=showArrowSize,
            drawMode=drawMode,
            spring=spring,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SpringForceField", params

    @sofa_component
    def StiffSpringForceField(
        self, indices1=None, indices2=None, length=None, **kwargs
    ):
        """
        StiffSpringForceField

        :param indices1: Indices of the source points on the first model
        :param indices2: Indices of the fixed points on the second model
        :param length: uniform length of all springs
        """
        params = dict(indices1=indices1, indices2=indices2, length=length)
        params = {k: v for k, v in params.items() if v is not None}
        return "StiffSpringForceField", params

    @sofa_component
    def ExportDotVisitor(self, **kwargs):
        """
        ExportDotVisitor
        """
        params = dict()
        return "ExportDotVisitor", params

    @sofa_component
    def GNode(self, **kwargs):
        """
        GNode
        """
        params = dict()
        return "GNode", params

    @sofa_component
    def GNodeMultiMappingElement(self, **kwargs):
        """
        GNodeMultiMappingElement
        """
        params = dict()
        return "GNodeMultiMappingElement", params

    @sofa_component
    def GNodeVisitor(self, **kwargs):
        """
        GNodeVisitor
        """
        params = dict()
        return "GNodeVisitor", params

    @sofa_component
    def TreeSimulation(self, **kwargs):
        """
        TreeSimulation
        """
        params = dict()
        return "TreeSimulation", params

    @sofa_component
    def DAGNode(self, **kwargs):
        """
        DAGNode
        """
        params = dict()
        return "DAGNode", params

    @sofa_component
    def DAGNodeMultiMappingElement(self, **kwargs):
        """
        DAGNodeMultiMappingElement
        """
        params = dict()
        return "DAGNodeMultiMappingElement", params

    @sofa_component
    def DAGSimulation(self, **kwargs):
        """
        DAGSimulation
        """
        params = dict()
        return "DAGSimulation", params

    @sofa_component
    def SimpleApi(self, **kwargs):
        """
        SimpleApi
        """
        params = dict()
        return "SimpleApi", params

    @sofa_component
    def JointSpring(self, **kwargs):
        """
        JointSpring
        """
        params = dict()
        return "JointSpring", params

    @sofa_component
    def JointSpringForceField(
        self,
        outfile=None,
        infile=None,
        period=None,
        reinit=None,
        spring=None,
        showLawfulTorsion=None,
        showExtraTorsion=None,
        showFactorSize=None,
        **kwargs
    ):
        """
        JointSpringForceField

        :param outfile: output file name
        :param infile: input file containing constant joint force
        :param period: period between outputs
        :param reinit: flag enabling reinitialization of the output file at each timestep
        :param spring: pairs of indices, stiffness, damping, rest length
        :param showLawfulTorsion: display the lawful part of the joint rotation
        :param showExtraTorsion: display the illicit part of the joint rotation
        :param showFactorSize: modify the size of the debug information of a given factor
        """
        params = dict(
            outfile=outfile,
            infile=infile,
            period=period,
            reinit=reinit,
            spring=spring,
            showLawfulTorsion=showLawfulTorsion,
            showExtraTorsion=showExtraTorsion,
            showFactorSize=showFactorSize,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "JointSpringForceField", params

    @sofa_component
    def RigidMapping(
        self,
        initialPoints=None,
        index=None,
        filename=None,
        useX0=None,
        indexFromEnd=None,
        rigidIndexPerPoint=None,
        globalToLocalCoords=None,
        geometricStiffness=None,
        **kwargs
    ):
        """
        RigidMapping

        :param initialPoints: Local Coordinates of the points
        :param index: input DOF index
        :param filename: Xsp file where rigid mapping information can be loaded from.
        :param useX0: Use x0 instead of local copy of initial positions (to support topo changes)
        :param indexFromEnd: input DOF index starts from the end of input DOFs vector
        :param rigidIndexPerPoint: For each mapped point, the index of the Rigid it is mapped from
        :param globalToLocalCoords: are the output DOFs initially expressed in global coordinates
        :param geometricStiffness: assemble (and use) geometric stiffness (0=no GS, 1=non symmetric, 2=symmetrized)
        """
        params = dict(
            initialPoints=initialPoints,
            index=index,
            filename=filename,
            useX0=useX0,
            indexFromEnd=indexFromEnd,
            rigidIndexPerPoint=rigidIndexPerPoint,
            globalToLocalCoords=globalToLocalCoords,
            geometricStiffness=geometricStiffness,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "RigidMapping", params

    @sofa_component
    def RigidRigidMapping(
        self,
        initialPoints=None,
        repartition=None,
        index=None,
        filename=None,
        axisLength=None,
        indexFromEnd=None,
        globalToLocalCoords=None,
        **kwargs
    ):
        """
        RigidRigidMapping

        :param initialPoints: Initial position of the points
        :param repartition: number of child frames per parent frame. \n
        :param index: input frame index
        :param filename: Xsp file where to load rigidrigid mapping description
        :param axisLength: axis length for display
        :param indexFromEnd: input DOF index starts from the end of input DOFs vector
        :param globalToLocalCoords: are the output DOFs initially expressed in global coordinates
        """
        params = dict(
            initialPoints=initialPoints,
            repartition=repartition,
            index=index,
            filename=filename,
            axisLength=axisLength,
            indexFromEnd=indexFromEnd,
            globalToLocalCoords=globalToLocalCoords,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "RigidRigidMapping", params

    @sofa_component
    def ComponentA(self, **kwargs):
        """
        ComponentA
        """
        params = dict()
        return "ComponentA", params

    @sofa_component
    def ComponentB(self, **kwargs):
        """
        ComponentB
        """
        params = dict()
        return "ComponentB", params

    @sofa_component
    def SceneLoaderPHP(self, **kwargs):
        """
        SceneLoaderPHP
        """
        params = dict()
        return "SceneLoaderPHP", params

    @sofa_component
    def SceneLoaderXML(self, **kwargs):
        """
        SceneLoaderXML
        """
        params = dict()
        return "SceneLoaderXML", params

    @sofa_component
    def TransformationVisitor(self, **kwargs):
        """
        TransformationVisitor
        """
        params = dict()
        return "TransformationVisitor", params

    @sofa_component
    def AttributeElement(self, **kwargs):
        """
        AttributeElement
        """
        params = dict()
        return "AttributeElement", params

    @sofa_component
    def BaseElement(self, **kwargs):
        """
        BaseElement
        """
        params = dict()
        return "BaseElement", params

    @sofa_component
    def BaseMultiMappingElement(self, **kwargs):
        """
        BaseMultiMappingElement
        """
        params = dict()
        return "BaseMultiMappingElement", params

    @sofa_component
    def DataElement(self, **kwargs):
        """
        DataElement
        """
        params = dict()
        return "DataElement", params

    @sofa_component
    def ElementNameHelper(self, **kwargs):
        """
        ElementNameHelper
        """
        params = dict()
        return "ElementNameHelper", params

    @sofa_component
    def NodeElement(self, **kwargs):
        """
        NodeElement
        """
        params = dict()
        return "NodeElement", params

    @sofa_component
    def ObjectElement(self, **kwargs):
        """
        ObjectElement
        """
        params = dict()
        return "ObjectElement", params

    @sofa_component
    def XML(self, **kwargs):
        """
        XML
        """
        params = dict()
        return "XML", params

    @sofa_component
    def myexcept(self, **kwargs):
        """
        myexcept
        """
        params = dict()
        return "myexcept", params

    @sofa_component
    def newmatrm(self, **kwargs):
        """
        newmatrm
        """
        params = dict()
        return "newmatrm", params

    @sofa_component
    def tinystr(self, **kwargs):
        """
        tinystr
        """
        params = dict()
        return "tinystr", params

    @sofa_component
    def tinyxml(self, **kwargs):
        """
        tinyxml
        """
        params = dict()
        return "tinyxml", params

    @sofa_component
    def CentralDifferenceSolver(
        self, rayleighMass=None, threadSafeVisitor=None, **kwargs
    ):
        """
        CentralDifferenceSolver

        :param rayleighMass: Rayleigh damping coefficient related to mass
        :param threadSafeVisitor: If true, do not use realloc and free visitors in fwdInteractionForceField.
        """
        params = dict(rayleighMass=rayleighMass, threadSafeVisitor=threadSafeVisitor)
        params = {k: v for k, v in params.items() if v is not None}
        return "CentralDifferenceSolver", params

    @sofa_component
    def RungeKutta2Solver(self, **kwargs):
        """
        RungeKutta2Solver
        """
        params = dict()
        return "RungeKutta2Solver", params

    @sofa_component
    def RungeKutta4Solver(self, **kwargs):
        """
        RungeKutta4Solver
        """
        params = dict()
        return "RungeKutta4Solver", params

    @sofa_component
    def ReadState(
        self,
        filename=None,
        interval=None,
        shift=None,
        loop=None,
        scalePos=None,
        **kwargs
    ):
        """
        ReadState

        :param filename: output file name
        :param interval: time duration between inputs
        :param shift: shift between times in the file and times when they will be read
        :param loop: set to 'true' to re-read the file when reaching the end
        :param scalePos: scale the input mechanical object
        """
        params = dict(
            filename=filename,
            interval=interval,
            shift=shift,
            loop=loop,
            scalePos=scalePos,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ReadState", params

    @sofa_component
    def ReadTopology(
        self, filename=None, interval=None, shift=None, loop=None, **kwargs
    ):
        """
        ReadTopology

        :param filename: input file name
        :param interval: time duration between inputs
        :param shift: shift between times in the file and times when they will be read
        :param loop: set to 'true' to re-read the file when reaching the end
        """
        params = dict(filename=filename, interval=interval, shift=shift, loop=loop)
        params = {k: v for k, v in params.items() if v is not None}
        return "ReadTopology", params

    @sofa_component
    def GIDMeshLoader(self, **kwargs):
        """
        GIDMeshLoader
        """
        params = dict()
        return "GIDMeshLoader", params

    @sofa_component
    def GridMeshCreator(self, resolution=None, trianglePattern=None, **kwargs):
        """
        GridMeshCreator

        :param resolution: Number of vertices in each direction
        :param trianglePattern: 0: no triangles, 1: alternate triangles, 2: upward triangles, 3: downward triangles
        """
        params = dict(resolution=resolution, trianglePattern=trianglePattern)
        params = {k: v for k, v in params.items() if v is not None}
        return "GridMeshCreator", params

    @sofa_component
    def InputEventReader(
        self,
        filename=None,
        inverseSense=None,
        printEvent=None,
        timeout=None,
        key1=None,
        key2=None,
        writeEvents=None,
        outputFilename=None,
        **kwargs
    ):
        """
        InputEventReader

        :param filename: input events file name
        :param inverseSense: inverse the sense of the mouvement
        :param printEvent: Print event informations
        :param timeout: time out to get an event from file
        :param key1: Key event generated when the left pedal is pressed
        :param key2: Key event generated when the right pedal is pressed
        :param writeEvents: If true, write incoming events ; if false, read events from that file (if an output filename is provided)
        :param outputFilename: Other filename where events will be stored (or read)
        """
        params = dict(
            filename=filename,
            inverseSense=inverseSense,
            printEvent=printEvent,
            timeout=timeout,
            key1=key1,
            key2=key2,
            writeEvents=writeEvents,
            outputFilename=outputFilename,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "InputEventReader", params

    @sofa_component
    def MeshGmshLoader(self, **kwargs):
        """
        MeshGmshLoader
        """
        params = dict()
        return "MeshGmshLoader", params

    @sofa_component
    def MeshOffLoader(self, **kwargs):
        """
        MeshOffLoader
        """
        params = dict()
        return "MeshOffLoader", params

    @sofa_component
    def MeshSTLLoader(
        self, headerSize=None, forceBinary=None, mergePositionUsingMap=None, **kwargs
    ):
        """
        MeshSTLLoader

        :param headerSize: Size of the header binary file (just before the number of facet).
        :param forceBinary: Force reading in binary mode. Even in first keyword of the file is solid.
        :param mergePositionUsingMap: Since positions are duplicated in a STL, they have to be merged. Using a map to do so will temporarily duplicate memory but should be more efficient. Disable it if memory is really an issue.
        """
        params = dict(
            headerSize=headerSize,
            forceBinary=forceBinary,
            mergePositionUsingMap=mergePositionUsingMap,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshSTLLoader", params

    @sofa_component
    def MeshTrianLoader(
        self,
        trian2=None,
        neighborTable=None,
        edgesOnBorder=None,
        trianglesOnBorderList=None,
        **kwargs
    ):
        """
        MeshTrianLoader

        :param trian2: Set to true if the mesh is a trian2 format.
        :param neighborTable: Table of neighborhood triangle indices for each triangle.
        :param edgesOnBorder: List of edges which are on the border of the mesh loaded.
        :param trianglesOnBorderList: List of triangle indices which are on the border of the mesh loaded.
        """
        params = dict(
            trian2=trian2,
            neighborTable=neighborTable,
            edgesOnBorder=edgesOnBorder,
            trianglesOnBorderList=trianglesOnBorderList,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshTrianLoader", params

    @sofa_component
    def MeshXspLoader(self, **kwargs):
        """
        MeshXspLoader
        """
        params = dict()
        return "MeshXspLoader", params

    @sofa_component
    def OffSequenceLoader(self, nbOfFiles=None, stepDuration=None, **kwargs):
        """
        OffSequenceLoader

        :param nbOfFiles: number of files in the sequence
        :param stepDuration: how long each file is loaded
        """
        params = dict(nbOfFiles=nbOfFiles, stepDuration=stepDuration)
        params = {k: v for k, v in params.items() if v is not None}
        return "OffSequenceLoader", params

    @sofa_component
    def SphereLoader(
        self, position=None, listRadius=None, scale=None, translation=None, **kwargs
    ):
        """
        SphereLoader

        :param position: Sphere centers
        :param listRadius: Radius of each sphere
        :param scale: Scale applied to sphere positions & radius
        :param translation: Translation applied to sphere positions
        """
        params = dict(
            position=position,
            listRadius=listRadius,
            scale=scale,
            translation=translation,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SphereLoader", params

    @sofa_component
    def StringMeshCreator(self, resolution=None, **kwargs):
        """
        StringMeshCreator

        :param resolution: Number of vertices
        """
        params = dict(resolution=resolution)
        params = {k: v for k, v in params.items() if v is not None}
        return "StringMeshCreator", params

    @sofa_component
    def VoxelGridLoader(
        self,
        voxelSize=None,
        resolution=None,
        ROI=None,
        header=None,
        segmentationHeader=None,
        idxInRegularGrid=None,
        bgValue=None,
        dataValue=None,
        generateHexa=None,
        **kwargs
    ):
        """
        VoxelGridLoader

        :param voxelSize: Dimension of one voxel
        :param resolution: Resolution of the voxel file
        :param ROI: Region of interest (xmin, ymin, zmin, xmax, ymax, zmax)
        :param header: Header size in bytes
        :param segmentationHeader: Header size in bytes
        :param idxInRegularGrid: indices of the hexa in the grid.
        :param bgValue: Background values (to be ignored)
        :param dataValue: Active data values
        :param generateHexa: Interpret voxel as either hexa or points
        """
        params = dict(
            voxelSize=voxelSize,
            resolution=resolution,
            ROI=ROI,
            header=header,
            segmentationHeader=segmentationHeader,
            idxInRegularGrid=idxInRegularGrid,
            bgValue=bgValue,
            dataValue=dataValue,
            generateHexa=generateHexa,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "VoxelGridLoader", params

    @sofa_component
    def DirectSAP(self, draw=None, box=None, **kwargs):
        """
        DirectSAP

        :param draw: enable/disable display of results
        :param box: if not empty, objects that do not intersect this bounding-box will be ignored
        """
        params = dict(draw=draw, box=box)
        params = {k: v for k, v in params.items() if v is not None}
        return "DirectSAP", params

    @sofa_component
    def IncrSAP(self, draw=None, box=None, **kwargs):
        """
        IncrSAP

        :param draw: enable/disable display of results
        :param box: if not empty, objects that do not intersect this bounding-box will be ignored
        """
        params = dict(draw=draw, box=box)
        params = {k: v for k, v in params.items() if v is not None}
        return "IncrSAP", params

    @sofa_component
    def MeshDiscreteIntersection(self, **kwargs):
        """
        MeshDiscreteIntersection
        """
        params = dict()
        return "MeshDiscreteIntersection", params

    @sofa_component
    def MeshMinProximityIntersection(self, **kwargs):
        """
        MeshMinProximityIntersection
        """
        params = dict()
        return "MeshMinProximityIntersection", params

    @sofa_component
    def TriangleOctree(self, **kwargs):
        """
        TriangleOctree
        """
        params = dict()
        return "TriangleOctree", params

    @sofa_component
    def TriangleOctreeModel(self, **kwargs):
        """
        TriangleOctreeModel
        """
        params = dict()
        return "TriangleOctreeModel", params

    @sofa_component
    def TopologicalChangeProcessor(
        self,
        filename=None,
        listChanges=None,
        interval=None,
        shift=None,
        loop=None,
        useDataInputs=None,
        timeToRemove=None,
        edgesToRemove=None,
        trianglesToRemove=None,
        quadsToRemove=None,
        tetrahedraToRemove=None,
        hexahedraToRemove=None,
        saveIndicesAtInit=None,
        epsilonSnapPath=None,
        epsilonSnapBorder=None,
        draw=None,
        **kwargs
    ):
        """
        TopologicalChangeProcessor

        :param filename: input file name for topological changes.
        :param listChanges: 0 for adding, 1 for removing, 2 for cutting and associated indices.
        :param interval: time duration between 2 actions
        :param shift: shift between times in the file and times when they will be read
        :param loop: set to 'true' to re-read the file when reaching the end
        :param useDataInputs: If true, will perform operation using Data input lists rather than text file.
        :param timeToRemove: If using option useDataInputs, time at which will be done the operations. Possibility to use the interval Data also.
        :param edgesToRemove: List of edge IDs to be removed.
        :param trianglesToRemove: List of triangle IDs to be removed.
        :param quadsToRemove: List of quad IDs to be removed.
        :param tetrahedraToRemove: List of tetrahedron IDs to be removed.
        :param hexahedraToRemove: List of hexahedron IDs to be removed.
        :param saveIndicesAtInit: set to 'true' to save the incision to do in the init to incise even after a movement
        :param epsilonSnapPath: epsilon snap path
        :param epsilonSnapBorder: epsilon snap path
        :param draw: draw information
        """
        params = dict(
            filename=filename,
            listChanges=listChanges,
            interval=interval,
            shift=shift,
            loop=loop,
            useDataInputs=useDataInputs,
            timeToRemove=timeToRemove,
            edgesToRemove=edgesToRemove,
            trianglesToRemove=trianglesToRemove,
            quadsToRemove=quadsToRemove,
            tetrahedraToRemove=tetrahedraToRemove,
            hexahedraToRemove=hexahedraToRemove,
            saveIndicesAtInit=saveIndicesAtInit,
            epsilonSnapPath=epsilonSnapPath,
            epsilonSnapBorder=epsilonSnapBorder,
            draw=draw,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TopologicalChangeProcessor", params

    @sofa_component
    def BilateralInteractionConstraint(
        self,
        first_point=None,
        second_point=None,
        rest_vector=None,
        activateAtIteration=None,
        merge=None,
        derivative=None,
        keepOrientationDifference=None,
        **kwargs
    ):
        """
        BilateralInteractionConstraint

        :param first_point: index of the constraint on the first model
        :param second_point: index of the constraint on the second model
        :param rest_vector: Relative position to maintain between attached points (optional)
        :param activateAtIteration: activate constraint at specified interation (0 = always enabled, -1=disabled)
        :param merge: TEST: merge the bilateral constraints in a unique constraint
        :param derivative: TEST: derivative
        :param keepOrientationDifference: keep the initial difference in orientation (only for rigids)
        """
        params = dict(
            first_point=first_point,
            second_point=second_point,
            rest_vector=rest_vector,
            activateAtIteration=activateAtIteration,
            merge=merge,
            derivative=derivative,
            keepOrientationDifference=keepOrientationDifference,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "BilateralInteractionConstraint", params

    @sofa_component
    def ConstraintAnimationLoop(
        self,
        displayTime=None,
        tolerance=None,
        maxIterations=None,
        doCollisionsFirst=None,
        doubleBuffer=None,
        scaleTolerance=None,
        allVerified=None,
        sor=None,
        schemeCorrection=None,
        realTimeCompensation=None,
        graphErrors=None,
        graphConstraints=None,
        graphForces=None,
        **kwargs
    ):
        """
        ConstraintAnimationLoop

        :param displayTime: Display time for each important step of ConstraintAnimationLoop.
        :param tolerance: Tolerance of the Gauss-Seidel
        :param maxIterations: Maximum number of iterations of the Gauss-Seidel
        :param doCollisionsFirst: Compute the collisions first (to support penality-based contacts)
        :param doubleBuffer: Buffer the constraint problem in a double buffer to be accessible with an other thread
        :param scaleTolerance: Scale the error tolerance with the number of constraints
        :param allVerified: All contraints must be verified (each constraint's error < tolerance)
        :param sor: Successive Over Relaxation parameter (0-2)
        :param schemeCorrection: Apply new scheme where compliance is progressively corrected
        :param realTimeCompensation: If the total computational time T < dt, sleep(dt-T)
        :param graphErrors: Sum of the constraints' errors at each iteration
        :param graphConstraints: Graph of each constraint's error at the end of the resolution
        :param graphForces: Graph of each constraint's force at each step of the resolution
        """
        params = dict(
            displayTime=displayTime,
            tolerance=tolerance,
            maxIterations=maxIterations,
            doCollisionsFirst=doCollisionsFirst,
            doubleBuffer=doubleBuffer,
            scaleTolerance=scaleTolerance,
            allVerified=allVerified,
            sor=sor,
            schemeCorrection=schemeCorrection,
            realTimeCompensation=realTimeCompensation,
            graphErrors=graphErrors,
            graphConstraints=graphConstraints,
            graphForces=graphForces,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ConstraintAnimationLoop", params

    @sofa_component
    def ConstraintAttachBodyPerformer(self, **kwargs):
        """
        ConstraintAttachBodyPerformer
        """
        params = dict()
        return "ConstraintAttachBodyPerformer", params

    @sofa_component
    def ConstraintSolverImpl(self, **kwargs):
        """
        ConstraintSolverImpl
        """
        params = dict()
        return "ConstraintSolverImpl", params

    @sofa_component
    def ConstraintStoreLambdaVisitor(self, **kwargs):
        """
        ConstraintStoreLambdaVisitor
        """
        params = dict()
        return "ConstraintStoreLambdaVisitor", params

    @sofa_component
    def ContactIdentifier(self, **kwargs):
        """
        ContactIdentifier
        """
        params = dict()
        return "ContactIdentifier", params

    @sofa_component
    def FreeMotionAnimationLoop(
        self, solveVelocityConstraintFirst=None, threadSafeVisitor=None, **kwargs
    ):
        """
        FreeMotionAnimationLoop

        :param solveVelocityConstraintFirst: solve separately velocity constraint violations before position constraint violations
        :param threadSafeVisitor: If true, do not use realloc and free visitors in fwdInteractionForceField.
        """
        params = dict(
            solveVelocityConstraintFirst=solveVelocityConstraintFirst,
            threadSafeVisitor=threadSafeVisitor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "FreeMotionAnimationLoop", params

    @sofa_component
    def FrictionContact(self, mu=None, tol=None, **kwargs):
        """
        FrictionContact

        :param mu: friction coefficient (0 for frictionless contacts)
        :param tol: tolerance for the constraints resolution (0 for default tolerance)
        """
        params = dict(mu=mu, tol=tol)
        params = {k: v for k, v in params.items() if v is not None}
        return "FrictionContact", params

    @sofa_component
    def GenericConstraintCorrection(
        self, solverName=None, ODESolverName=None, complianceFactor=None, **kwargs
    ):
        """
        GenericConstraintCorrection

        :param solverName: name of the constraint solver
        :param ODESolverName: name of the ode solver
        :param complianceFactor: Factor applied to the position factor and velocity factor used to calculate compliance matrix
        """
        params = dict(
            solverName=solverName,
            ODESolverName=ODESolverName,
            complianceFactor=complianceFactor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "GenericConstraintCorrection", params

    @sofa_component
    def GenericConstraintSolver(
        self,
        displayTime=None,
        maxIterations=None,
        tolerance=None,
        sor=None,
        scaleTolerance=None,
        allVerified=None,
        schemeCorrection=None,
        unbuilt=None,
        computeGraphs=None,
        graphErrors=None,
        graphConstraints=None,
        graphForces=None,
        graphViolations=None,
        currentNumConstraints=None,
        currentNumConstraintGroups=None,
        currentIterations=None,
        currentError=None,
        reverseAccumulateOrder=None,
        constraintForces=None,
        **kwargs
    ):
        """
        GenericConstraintSolver

        :param displayTime: Display time for each important step of GenericConstraintSolver.
        :param maxIterations: maximal number of iterations of the Gauss-Seidel algorithm
        :param tolerance: residual error threshold for termination of the Gauss-Seidel algorithm
        :param sor: Successive Over Relaxation parameter (0-2)
        :param scaleTolerance: Scale the error tolerance with the number of constraints
        :param allVerified: All contraints must be verified (each constraint's error < tolerance)
        :param schemeCorrection: Apply new scheme where compliance is progressively corrected
        :param unbuilt: Compliance is not fully built
        :param computeGraphs: Compute graphs of errors and forces during resolution
        :param graphErrors: Sum of the constraints' errors at each iteration
        :param graphConstraints: Graph of each constraint's error at the end of the resolution
        :param graphForces: Graph of each constraint's force at each step of the resolution
        :param graphViolations: Graph of each constraint's violation at each step of the resolution
        :param currentNumConstraints: OUTPUT: current number of constraints
        :param currentNumConstraintGroups: OUTPUT: current number of constraints
        :param currentIterations: OUTPUT: current number of constraint groups
        :param currentError: OUTPUT: current error
        :param reverseAccumulateOrder: True to accumulate constraints from nodes in reversed order (can be necessary when using multi-mappings or interaction constraints not following the node hierarchy)
        :param constraintForces: OUTPUT: constraint forces (stored only if computeConstraintForces=True)
        """
        params = dict(
            displayTime=displayTime,
            maxIterations=maxIterations,
            tolerance=tolerance,
            sor=sor,
            scaleTolerance=scaleTolerance,
            allVerified=allVerified,
            schemeCorrection=schemeCorrection,
            unbuilt=unbuilt,
            computeGraphs=computeGraphs,
            graphErrors=graphErrors,
            graphConstraints=graphConstraints,
            graphForces=graphForces,
            graphViolations=graphViolations,
            currentNumConstraints=currentNumConstraints,
            currentNumConstraintGroups=currentNumConstraintGroups,
            currentIterations=currentIterations,
            currentError=currentError,
            reverseAccumulateOrder=reverseAccumulateOrder,
            constraintForces=constraintForces,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "GenericConstraintSolver", params

    @sofa_component
    def LCPConstraintSolver(
        self,
        displayDebug=None,
        displayTime=None,
        initial_guess=None,
        build_lcp=None,
        tolerance=None,
        maxIt=None,
        mu=None,
        minW=None,
        maxF=None,
        multi_grid=None,
        multi_grid_levels=None,
        merge_method=None,
        merge_spatial_step=None,
        merge_local_levels=None,
        group=None,
        graph=None,
        showLevels=None,
        showCellWidth=None,
        showTranslation=None,
        showLevelTranslation=None,
        **kwargs
    ):
        """
        LCPConstraintSolver

        :param displayDebug: Display debug information.
        :param displayTime: Display time for each important step of LCPConstraintSolver.
        :param initial_guess: activate LCP results history to improve its resolution performances.
        :param build_lcp: LCP is not fully built to increase performance in some case.
        :param tolerance: residual error threshold for termination of the Gauss-Seidel algorithm
        :param maxIt: maximal number of iterations of the Gauss-Seidel algorithm
        :param mu: Friction coefficient
        :param minW: If not zero, constraints whose self-compliance (i.e. the corresponding value on the diagonal of W) is smaller than this threshold will be ignored
        :param maxF: If not zero, constraints whose response force becomes larger than this threshold will be ignored
        :param multi_grid: activate multi_grid resolution (NOT STABLE YET)
        :param multi_grid_levels: if multi_grid is active: how many levels to create (>=2)
        :param merge_method: if multi_grid is active: which method to use to merge constraints (0 = compliance-based, 1 = spatial coordinates)
        :param merge_spatial_step: if merge_method is 1: grid size reduction between multigrid levels
        :param merge_local_levels: if merge_method is 1: up to the specified level of the multigrid, constraints are grouped locally, i.e. separately within each contact pairs, while on upper levels they are grouped globally independently of contact pairs.
        :param group: list of ID of groups of constraints to be handled by this solver.
        :param graph: Graph of residuals at each iteration
        :param showLevels: Number of constraint levels to display
        :param showCellWidth: Distance between each constraint cells
        :param showTranslation: Position of the first cell
        :param showLevelTranslation: Translation between levels
        """
        params = dict(
            displayDebug=displayDebug,
            displayTime=displayTime,
            initial_guess=initial_guess,
            build_lcp=build_lcp,
            tolerance=tolerance,
            maxIt=maxIt,
            mu=mu,
            minW=minW,
            maxF=maxF,
            multi_grid=multi_grid,
            multi_grid_levels=multi_grid_levels,
            merge_method=merge_method,
            merge_spatial_step=merge_spatial_step,
            merge_local_levels=merge_local_levels,
            group=group,
            graph=graph,
            showLevels=showLevels,
            showCellWidth=showCellWidth,
            showTranslation=showTranslation,
            showLevelTranslation=showLevelTranslation,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "LCPConstraintSolver", params

    @sofa_component
    def LMDNewProximityIntersection(self, useLineLine=None, **kwargs):
        """
        LMDNewProximityIntersection

        :param useLineLine: Line-line collision detection enabled
        """
        params = dict(useLineLine=useLineLine)
        params = {k: v for k, v in params.items() if v is not None}
        return "LMDNewProximityIntersection", params

    @sofa_component
    def LinearSolverConstraintCorrection(
        self, wire_optimization=None, solverName=None, **kwargs
    ):
        """
        LinearSolverConstraintCorrection

        :param wire_optimization: constraints are reordered along a wire-like topology (from tip to base)
        :param solverName: search for the following names upward the scene graph
        """
        params = dict(wire_optimization=wire_optimization, solverName=solverName)
        params = {k: v for k, v in params.items() if v is not None}
        return "LinearSolverConstraintCorrection", params

    @sofa_component
    def LocalMinDistance(
        self,
        filterIntersection=None,
        angleCone=None,
        coneFactor=None,
        useLMDFilters=None,
        **kwargs
    ):
        """
        LocalMinDistance

        :param filterIntersection: Activate LMD filter
        :param angleCone: Filtering cone extension angle
        :param coneFactor: Factor for filtering cone angle computation
        :param useLMDFilters: Use external cone computation (Work in Progress)
        """
        params = dict(
            filterIntersection=filterIntersection,
            angleCone=angleCone,
            coneFactor=coneFactor,
            useLMDFilters=useLMDFilters,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "LocalMinDistance", params

    @sofa_component
    def MappingGeometricStiffnessForceField(self, **kwargs):
        """
        MappingGeometricStiffnessForceField
        """
        params = dict()
        return "MappingGeometricStiffnessForceField", params

    @sofa_component
    def PrecomputedConstraintCorrection(
        self,
        rotations=None,
        restDeformations=None,
        recompute=None,
        debugViewFrameScale=None,
        fileCompliance=None,
        fileDir=None,
        **kwargs
    ):
        """
        PrecomputedConstraintCorrection

        :param rotations:
        :param restDeformations:
        :param recompute: if true, always recompute the compliance
        :param debugViewFrameScale: Scale on computed node's frame
        :param fileCompliance: Precomputed compliance matrix data file
        :param fileDir: If not empty, the compliance will be saved in this repertory
        """
        params = dict(
            rotations=rotations,
            restDeformations=restDeformations,
            recompute=recompute,
            debugViewFrameScale=debugViewFrameScale,
            fileCompliance=fileCompliance,
            fileDir=fileDir,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PrecomputedConstraintCorrection", params

    @sofa_component
    def SlidingConstraint(
        self, sliding_point=None, axis_1=None, axis_2=None, force=None, **kwargs
    ):
        """
        SlidingConstraint

        :param sliding_point: index of the spliding point on the first model
        :param axis_1: index of one end of the sliding axis
        :param axis_2: index of the other end of the sliding axis
        :param force: force (impulse) used to solve the constraint
        """
        params = dict(
            sliding_point=sliding_point, axis_1=axis_1, axis_2=axis_2, force=force
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SlidingConstraint", params

    @sofa_component
    def StickContactConstraint(self, keepAlive=None, **kwargs):
        """
        StickContactConstraint

        :param keepAlive: set to true to keep this contact alive even after collisions are no longer detected
        """
        params = dict(keepAlive=keepAlive)
        params = {k: v for k, v in params.items() if v is not None}
        return "StickContactConstraint", params

    @sofa_component
    def StopperConstraint(self, index=None, min=None, max=None, **kwargs):
        """
        StopperConstraint

        :param index: index of the stop constraint
        :param min: minimum value accepted
        :param max: maximum value accepted
        """
        params = dict(index=index, min=min, max=max)
        params = {k: v for k, v in params.items() if v is not None}
        return "StopperConstraint", params

    @sofa_component
    def UncoupledConstraintCorrection(
        self,
        compliance=None,
        defaultCompliance=None,
        verbose=None,
        correctionVelocityFactor=None,
        correctionPositionFactor=None,
        useOdeSolverIntegrationFactors=None,
        **kwargs
    ):
        """
        UncoupledConstraintCorrection

        :param compliance: compliance value on each dof. If Rigid compliance (7 values): 1st value for translations, 6 others for upper-triangular part of symmetric 3x3 rotation compliance matrix
        :param defaultCompliance: Default compliance value for new dof or if all should have the same (in which case compliance vector should be empty)
        :param verbose: Dump the constraint matrix at each iteration
        :param correctionVelocityFactor: Factor applied to the constraint forces when correcting the velocities
        :param correctionPositionFactor: Factor applied to the constraint forces when correcting the positions
        :param useOdeSolverIntegrationFactors: Use odeSolver integration factors instead of correctionVelocityFactor and correctionPositionFactor
        """
        params = dict(
            compliance=compliance,
            defaultCompliance=defaultCompliance,
            verbose=verbose,
            correctionVelocityFactor=correctionVelocityFactor,
            correctionPositionFactor=correctionPositionFactor,
            useOdeSolverIntegrationFactors=useOdeSolverIntegrationFactors,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "UncoupledConstraintCorrection", params

    @sofa_component
    def UniformConstraint(self, iterative=None, constrainToRestPos=None, **kwargs):
        """
        UniformConstraint

        :param iterative: Iterate over the bilateral constraints, otherwise a block factorisation is computed.
        :param constrainToRestPos: if false, constrains the pos to be zero / if true constraint the current position to stay at rest position
        """
        params = dict(iterative=iterative, constrainToRestPos=constrainToRestPos)
        params = {k: v for k, v in params.items() if v is not None}
        return "UniformConstraint", params

    @sofa_component
    def UnilateralInteractionConstraint(self, **kwargs):
        """
        UnilateralInteractionConstraint
        """
        params = dict()
        return "UnilateralInteractionConstraint", params

    @sofa_component
    def BarycentricDistanceLMConstraintContact(self, **kwargs):
        """
        BarycentricDistanceLMConstraintContact
        """
        params = dict()
        return "BarycentricDistanceLMConstraintContact", params

    @sofa_component
    def DOFBlockerLMConstraint(
        self,
        rotationAxis=None,
        factorAxis=None,
        indices=None,
        showSizeAxis=None,
        **kwargs
    ):
        """
        DOFBlockerLMConstraint

        :param rotationAxis: List of rotation axis to constrain
        :param factorAxis: Factor to apply in order to block only a certain amount of rotation along the axis
        :param indices: List of the index of particles to be fixed
        :param showSizeAxis: size of the vector used to display the constrained axis
        """
        params = dict(
            rotationAxis=rotationAxis,
            factorAxis=factorAxis,
            indices=indices,
            showSizeAxis=showSizeAxis,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "DOFBlockerLMConstraint", params

    @sofa_component
    def FixedLMConstraint(self, indices=None, drawSize=None, **kwargs):
        """
        FixedLMConstraint

        :param indices: List of the index of particles to be fixed
        :param drawSize: 0 -> point based rendering, >0 -> radius of spheres
        """
        params = dict(indices=indices, drawSize=drawSize)
        params = {k: v for k, v in params.items() if v is not None}
        return "FixedLMConstraint", params

    @sofa_component
    def DistanceLMContactConstraint(
        self, pointPairs=None, contactFriction=None, **kwargs
    ):
        """
        DistanceLMContactConstraint

        :param pointPairs: List of the edges to constrain
        :param contactFriction: Coulomb friction coefficient (same for all)
        """
        params = dict(pointPairs=pointPairs, contactFriction=contactFriction)
        params = {k: v for k, v in params.items() if v is not None}
        return "DistanceLMContactConstraint", params

    @sofa_component
    def DistanceLMConstraint(self, vecConstraint=None, **kwargs):
        """
        DistanceLMConstraint

        :param vecConstraint: List of the edges to constrain
        """
        params = dict(vecConstraint=vecConstraint)
        params = {k: v for k, v in params.items() if v is not None}
        return "DistanceLMConstraint", params

    @sofa_component
    def LMConstraintSolver(
        self,
        constraintAcc=None,
        constraintVel=None,
        constraintPos=None,
        numIterations=None,
        maxError=None,
        graphGSError=None,
        traceKineticEnergy=None,
        graphKineticEnergy=None,
        **kwargs
    ):
        """
        LMConstraintSolver

        :param constraintAcc: Constraint the acceleration
        :param constraintVel: Constraint the velocity
        :param constraintPos: Constraint the position
        :param numIterations: Number of iterations for Gauss-Seidel when solving the Constraints
        :param maxError: threshold for the residue of the Gauss-Seidel algorithm
        :param graphGSError: Graph of residuals at each iteration
        :param traceKineticEnergy: Trace the evolution of the Kinetic Energy throughout the solution of the system
        :param graphKineticEnergy: Graph of the kinetic energy of the system
        """
        params = dict(
            constraintAcc=constraintAcc,
            constraintVel=constraintVel,
            constraintPos=constraintPos,
            numIterations=numIterations,
            maxError=maxError,
            graphGSError=graphGSError,
            traceKineticEnergy=traceKineticEnergy,
            graphKineticEnergy=graphKineticEnergy,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "LMConstraintSolver", params

    @sofa_component
    def LMConstraintDirectSolver(self, solverAlgorithm=None, **kwargs):
        """
        LMConstraintDirectSolver

        :param solverAlgorithm: Algorithm used to solve the system W.Lambda=c
        """
        params = dict(solverAlgorithm=solverAlgorithm)
        params = {k: v for k, v in params.items() if v is not None}
        return "LMConstraintDirectSolver", params

    @sofa_component
    def BeamFEMForceField(
        self,
        beamsData=None,
        poissonRatio=None,
        youngModulus=None,
        radius=None,
        radiusInner=None,
        listSegment=None,
        useSymmetricAssembly=None,
        **kwargs
    ):
        """
        BeamFEMForceField

        :param beamsData: Internal element data
        :param poissonRatio: Potion Ratio
        :param youngModulus: Young Modulus
        :param radius: radius of the section
        :param radiusInner: inner radius of the section for hollow beams
        :param listSegment: apply the forcefield to a subset list of beam segments. If no segment defined, forcefield applies to the whole topology
        :param useSymmetricAssembly: use symmetric assembly of the matrix K
        """
        params = dict(
            beamsData=beamsData,
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            radius=radius,
            radiusInner=radiusInner,
            listSegment=listSegment,
            useSymmetricAssembly=useSymmetricAssembly,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "BeamFEMForceField", params

    @sofa_component
    def HexahedralFEMForceField(
        self,
        method=None,
        poissonRatio=None,
        youngModulus=None,
        hexahedronInfo=None,
        **kwargs
    ):
        """
        HexahedralFEMForceField

        :param method: large or polar displacements
        :param poissonRatio:
        :param youngModulus:
        :param hexahedronInfo: Internal hexahedron data
        """
        params = dict(
            method=method,
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            hexahedronInfo=hexahedronInfo,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "HexahedralFEMForceField", params

    @sofa_component
    def HexahedralFEMForceFieldAndMass(
        self,
        density=None,
        lumpedMass=None,
        massMatrices=None,
        totalMass=None,
        particleMasses=None,
        lumpedMasses=None,
        **kwargs
    ):
        """
        HexahedralFEMForceFieldAndMass

        :param density: density == volumetric mass in english (kg.m-3)
        :param lumpedMass: Does it use lumped masses?
        :param massMatrices: Mass matrices per element (M_i)
        :param totalMass: Total mass per element
        :param particleMasses: Mass per particle
        :param lumpedMasses: Lumped masses
        """
        params = dict(
            density=density,
            lumpedMass=lumpedMass,
            massMatrices=massMatrices,
            totalMass=totalMass,
            particleMasses=particleMasses,
            lumpedMasses=lumpedMasses,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "HexahedralFEMForceFieldAndMass", params

    @sofa_component
    def HexahedronFEMForceFieldAndMass(
        self, massMatrices=None, density=None, lumpedMass=None, **kwargs
    ):
        """
        HexahedronFEMForceFieldAndMass

        :param massMatrices: Mass matrices per element (M_i)
        :param density: density == volumetric mass in english (kg.m-3)
        :param lumpedMass: Does it use lumped masses?
        """
        params = dict(massMatrices=massMatrices, density=density, lumpedMass=lumpedMass)
        params = {k: v for k, v in params.items() if v is not None}
        return "HexahedronFEMForceFieldAndMass", params

    @sofa_component
    def TetrahedralCorotationalFEMForceField(
        self,
        tetrahedronInfo=None,
        method=None,
        poissonRatio=None,
        youngModulus=None,
        localStiffnessFactor=None,
        updateStiffnessMatrix=None,
        computeGlobalMatrix=None,
        drawing=None,
        drawColor1=None,
        drawColor2=None,
        drawColor3=None,
        drawColor4=None,
        **kwargs
    ):
        """
        TetrahedralCorotationalFEMForceField

        :param tetrahedronInfo: Internal tetrahedron data
        :param method: small, large (by QR) or polar displacements
        :param poissonRatio: FEM Poisson Ratio
        :param youngModulus: FEM Young Modulus
        :param localStiffnessFactor: Allow specification of different stiffness per element. If there are N element and M values are specified, the youngModulus factor for element i would be localStiffnessFactor[i*M/N]
        :param updateStiffnessMatrix:
        :param computeGlobalMatrix:
        :param drawing:  draw the forcefield if true
        :param drawColor1:  draw color for faces 1
        :param drawColor2:  draw color for faces 2
        :param drawColor3:  draw color for faces 3
        :param drawColor4:  draw color for faces 4
        """
        params = dict(
            tetrahedronInfo=tetrahedronInfo,
            method=method,
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            localStiffnessFactor=localStiffnessFactor,
            updateStiffnessMatrix=updateStiffnessMatrix,
            computeGlobalMatrix=computeGlobalMatrix,
            drawing=drawing,
            drawColor1=drawColor1,
            drawColor2=drawColor2,
            drawColor3=drawColor3,
            drawColor4=drawColor4,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralCorotationalFEMForceField", params

    @sofa_component
    def TriangularFEMForceFieldOptim(
        self,
        triangleInfo=None,
        triangleState=None,
        vertexInfo=None,
        edgeInfo=None,
        poissonRatio=None,
        youngModulus=None,
        damping=None,
        restScale=None,
        showStressVector=None,
        showStressMaxValue=None,
        **kwargs
    ):
        """
        TriangularFEMForceFieldOptim

        :param triangleInfo: Internal triangle data (persistent)
        :param triangleState: Internal triangle data (time-dependent)
        :param vertexInfo: Internal point data
        :param edgeInfo: Internal edge data
        :param poissonRatio: Poisson ratio in Hooke's law
        :param youngModulus: Young modulus in Hooke's law
        :param damping: Ratio damping/stiffness
        :param restScale: Scale factor applied to rest positions (to simulate pre-stretched materials)
        :param showStressVector: Flag activating rendering of stress directions within each triangle
        :param showStressMaxValue: Max value for rendering of stress values
        """
        params = dict(
            triangleInfo=triangleInfo,
            triangleState=triangleState,
            vertexInfo=vertexInfo,
            edgeInfo=edgeInfo,
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            damping=damping,
            restScale=restScale,
            showStressVector=showStressVector,
            showStressMaxValue=showStressMaxValue,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangularFEMForceFieldOptim", params

    @sofa_component
    def DampVelocitySolver(self, rate=None, threshold=None, **kwargs):
        """
        DampVelocitySolver

        :param rate: Factor used to reduce the velocities. Typically between 0 and 1.
        :param threshold: Threshold under which the velocities are canceled.
        """
        params = dict(rate=rate, threshold=threshold)
        params = {k: v for k, v in params.items() if v is not None}
        return "DampVelocitySolver", params

    @sofa_component
    def NewmarkImplicitSolver(
        self,
        rayleighStiffness=None,
        rayleighMass=None,
        vdamping=None,
        gamma=None,
        beta=None,
        threadSafeVisitor=None,
        **kwargs
    ):
        """
        NewmarkImplicitSolver

        :param rayleighStiffness: Rayleigh damping coefficient related to stiffness
        :param rayleighMass: Rayleigh damping coefficient related to mass
        :param vdamping: Velocity decay coefficient (no decay if null)
        :param gamma: Newmark scheme gamma coefficient
        :param beta: Newmark scheme beta coefficient
        :param threadSafeVisitor: If true, do not use realloc and free visitors in fwdInteractionForceField.
        """
        params = dict(
            rayleighStiffness=rayleighStiffness,
            rayleighMass=rayleighMass,
            vdamping=vdamping,
            gamma=gamma,
            beta=beta,
            threadSafeVisitor=threadSafeVisitor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "NewmarkImplicitSolver", params

    @sofa_component
    def GearSpringForceField(
        self,
        spring=None,
        filename=None,
        period=None,
        reinit=None,
        showFactorSize=None,
        **kwargs
    ):
        """
        GearSpringForceField

        :param spring: pairs of indices, stiffness, damping
        :param filename: output file name
        :param period: period between outputs
        :param reinit: flag enabling reinitialization of the output file at each timestep
        :param showFactorSize: modify the size of the debug information of a given factor
        """
        params = dict(
            spring=spring,
            filename=filename,
            period=period,
            reinit=reinit,
            showFactorSize=showFactorSize,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "GearSpringForceField", params

    @sofa_component
    def MeshMatrixMass(
        self,
        vertexMass=None,
        massDensity=None,
        totalMass=None,
        vertexMassInfo=None,
        edgeMassInfo=None,
        edgeMass=None,
        computeMassOnRest=None,
        showGravityCenter=None,
        showAxisSizeFactor=None,
        lumping=None,
        printMass=None,
        graph=None,
        **kwargs
    ):
        """
        MeshMatrixMass

        :param vertexMass: Specify a vector giving the mass of each vertex. \n
        :param massDensity: Specify real and strictly positive value(s) for the mass density. \n
        :param totalMass: Specify the total mass resulting from all particles. \n
        :param vertexMassInfo: internal values of the particles masses on vertices, supporting topological changes
        :param edgeMassInfo: internal values of the particles masses on edges, supporting topological changes
        :param edgeMass: values of the particles masses on edges
        :param computeMassOnRest: If true, the mass of every element is computed based on the rest position rather than the position
        :param showGravityCenter: display the center of gravity of the system
        :param showAxisSizeFactor: factor length of the axis displayed (only used for rigids)
        :param lumping: boolean if you need to use a lumped mass matrix
        :param printMass: boolean if you want to check the mass conservation
        :param graph: Graph of the controlled potential
        """
        params = dict(
            vertexMass=vertexMass,
            massDensity=massDensity,
            totalMass=totalMass,
            vertexMassInfo=vertexMassInfo,
            edgeMassInfo=edgeMassInfo,
            edgeMass=edgeMass,
            computeMassOnRest=computeMassOnRest,
            showGravityCenter=showGravityCenter,
            showAxisSizeFactor=showAxisSizeFactor,
            lumping=lumping,
            printMass=printMass,
            graph=graph,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshMatrixMass", params

    @sofa_component
    def LennardJonesForceField(
        self,
        aInit=None,
        alpha=None,
        beta=None,
        dmax=None,
        fmax=None,
        d0=None,
        p0=None,
        damping=None,
        **kwargs
    ):
        """
        LennardJonesForceField

        :param aInit: a for Gravitational FF which corresponds to G*m1*m2 alpha should be equal to 1 and beta to 0.
        :param alpha: Alpha
        :param beta: Beta
        :param dmax: DMax
        :param fmax: FMax
        :param d0: d0
        :param p0: p0
        :param damping: Damping
        """
        params = dict(
            aInit=aInit,
            alpha=alpha,
            beta=beta,
            dmax=dmax,
            fmax=fmax,
            d0=d0,
            p0=p0,
            damping=damping,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "LennardJonesForceField", params

    @sofa_component
    def csparse(self, **kwargs):
        """
        csparse
        """
        params = dict()
        return "csparse", params

    @sofa_component
    def FastTetrahedralCorotationalForceField(
        self,
        pointInfo=None,
        edgeInfo=None,
        tetrahedronInfo=None,
        method=None,
        poissonRatio=None,
        youngModulus=None,
        drawing=None,
        drawColor1=None,
        drawColor2=None,
        drawColor3=None,
        drawColor4=None,
        **kwargs
    ):
        """
        FastTetrahedralCorotationalForceField

        :param pointInfo: Internal point data
        :param edgeInfo: Internal edge data
        :param tetrahedronInfo: Internal tetrahedron data
        :param method:  method for rotation computation :qr (by QR) or polar or polar2 or none (Linear elastic)
        :param poissonRatio: Poisson ratio in Hooke's law
        :param youngModulus: Young modulus in Hooke's law
        :param drawing:  draw the forcefield if true
        :param drawColor1:  draw color for faces 1
        :param drawColor2:  draw color for faces 2
        :param drawColor3:  draw color for faces 3
        :param drawColor4:  draw color for faces 4
        """
        params = dict(
            pointInfo=pointInfo,
            edgeInfo=edgeInfo,
            tetrahedronInfo=tetrahedronInfo,
            method=method,
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            drawing=drawing,
            drawColor1=drawColor1,
            drawColor2=drawColor2,
            drawColor3=drawColor3,
            drawColor4=drawColor4,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "FastTetrahedralCorotationalForceField", params

    @sofa_component
    def StandardTetrahedralFEMForceField(
        self,
        materialName=None,
        ParameterSet=None,
        AnisotropyDirections=None,
        ParameterFile=None,
        tetrahedronInfo=None,
        edgeInfo=None,
        **kwargs
    ):
        """
        StandardTetrahedralFEMForceField

        :param materialName: the name of the material to be used
        :param ParameterSet: The global parameters specifying the material
        :param AnisotropyDirections: The global directions of anisotropy of the material
        :param ParameterFile: the name of the file describing the material parameters for all tetrahedra
        :param tetrahedronInfo: Internal tetrahedron data
        :param edgeInfo: Internal edge data
        """
        params = dict(
            materialName=materialName,
            ParameterSet=ParameterSet,
            AnisotropyDirections=AnisotropyDirections,
            ParameterFile=ParameterFile,
            tetrahedronInfo=tetrahedronInfo,
            edgeInfo=edgeInfo,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "StandardTetrahedralFEMForceField", params

    @sofa_component
    def TetrahedralTensorMassForceField(
        self, poissonRatio=None, youngModulus=None, edgeInfo=None, **kwargs
    ):
        """
        TetrahedralTensorMassForceField

        :param poissonRatio: Poisson ratio in Hooke's law
        :param youngModulus: Young modulus in Hooke's law
        :param edgeInfo: Internal edge data
        """
        params = dict(
            poissonRatio=poissonRatio, youngModulus=youngModulus, edgeInfo=edgeInfo
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralTensorMassForceField", params

    @sofa_component
    def TetrahedronHyperelasticityFEMForceField(
        self,
        matrixRegularization=None,
        materialName=None,
        ParameterSet=None,
        AnisotropyDirections=None,
        tetrahedronInfo=None,
        edgeInfo=None,
        **kwargs
    ):
        """
        TetrahedronHyperelasticityFEMForceField

        :param matrixRegularization: Regularization of the Stiffness Matrix (between true or false)
        :param materialName: the name of the material to be used
        :param ParameterSet: The global parameters specifying the material
        :param AnisotropyDirections: The global directions of anisotropy of the material
        :param tetrahedronInfo: Internal tetrahedron data
        :param edgeInfo: Internal edge data
        """
        params = dict(
            matrixRegularization=matrixRegularization,
            materialName=materialName,
            ParameterSet=ParameterSet,
            AnisotropyDirections=AnisotropyDirections,
            tetrahedronInfo=tetrahedronInfo,
            edgeInfo=edgeInfo,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedronHyperelasticityFEMForceField", params

    @sofa_component
    def TriangleFEMForceField(
        self,
        initialPoints=None,
        method=None,
        poissonRatio=None,
        youngModulus=None,
        thickness=None,
        damping=None,
        planeStrain=None,
        **kwargs
    ):
        """
        TriangleFEMForceField

        :param initialPoints: Initial Position
        :param method: large: large displacements, small: small displacements
        :param poissonRatio: Poisson ratio in Hooke's law
        :param youngModulus: Young modulus in Hooke's law
        :param thickness: Thickness of the elements
        :param damping: Ratio damping/stiffness
        :param planeStrain: Plane strain or plane stress assumption
        """
        params = dict(
            initialPoints=initialPoints,
            method=method,
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            thickness=thickness,
            damping=damping,
            planeStrain=planeStrain,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangleFEMForceField", params

    @sofa_component
    def PlasticMaterial(self, poissonRatio=None, youngModulus=None, **kwargs):
        """
        PlasticMaterial

        :param poissonRatio: Poisson ratio in Hooke's law
        :param youngModulus: Young modulus in Hooke's law
        """
        params = dict(poissonRatio=poissonRatio, youngModulus=youngModulus)
        params = {k: v for k, v in params.items() if v is not None}
        return "PlasticMaterial", params

    @sofa_component
    def TriangularAnisotropicFEMForceField(
        self,
        transverseYoungModulus=None,
        fiberAngle=None,
        fiberCenter=None,
        showFiber=None,
        localFiberDirection=None,
        **kwargs
    ):
        """
        TriangularAnisotropicFEMForceField

        :param transverseYoungModulus: Young modulus along transverse direction
        :param fiberAngle: Fiber angle in global reference frame (in degrees)
        :param fiberCenter: Concentric fiber center in global reference frame
        :param showFiber: Flag activating rendering of fiber directions within each triangle
        :param localFiberDirection: Computed fibers direction within each triangle
        """
        params = dict(
            transverseYoungModulus=transverseYoungModulus,
            fiberAngle=fiberAngle,
            fiberCenter=fiberCenter,
            showFiber=showFiber,
            localFiberDirection=localFiberDirection,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangularAnisotropicFEMForceField", params

    @sofa_component
    def TriangularFEMForceField(
        self,
        triangleInfo=None,
        vertexInfo=None,
        edgeInfo=None,
        method=None,
        poissonRatio=None,
        youngModulus=None,
        damping=None,
        rotatedInitialElements=None,
        initialTransformation=None,
        fracturable=None,
        hosfordExponant=None,
        criteriaValue=None,
        showStressValue=None,
        showStressVector=None,
        showFracturableTriangles=None,
        computePrincipalStress=None,
        id=None,
        graphMaxStress=None,
        graphCriteria=None,
        graphOrientation=None,
        **kwargs
    ):
        """
        TriangularFEMForceField

        :param triangleInfo: Internal triangle data
        :param vertexInfo: Internal point data
        :param edgeInfo: Internal edge data
        :param method: large: large displacements, small: small displacements
        :param poissonRatio: Poisson ratio in Hooke's law (vector)
        :param youngModulus: Young modulus in Hooke's law (vector)
        :param damping: Ratio damping/stiffness
        :param rotatedInitialElements: Flag activating rendering of stress directions within each triangle
        :param initialTransformation: Flag activating rendering of stress directions within each triangle
        :param fracturable: the forcefield computes the next fracturable Edge
        :param hosfordExponant: Exponant in the Hosford yield criteria
        :param criteriaValue: Fracturable threshold used to draw fracturable triangles
        :param showStressValue: Flag activating rendering of stress values as a color in each triangle
        :param showStressVector: Flag activating rendering of stress directions within each triangle
        :param showFracturableTriangles: Flag activating rendering of triangles to fracture
        :param computePrincipalStress: Compute principal stress for each triangle
        :param id: element id to follow for fracture criteria
        :param graphMaxStress: Graph of max stress corresponding to the element id
        :param graphCriteria: Graph of the fracture criteria corresponding to the element id
        :param graphOrientation: Graph of the orientation of the principal stress direction corresponding to the element id
        """
        params = dict(
            triangleInfo=triangleInfo,
            vertexInfo=vertexInfo,
            edgeInfo=edgeInfo,
            method=method,
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            damping=damping,
            rotatedInitialElements=rotatedInitialElements,
            initialTransformation=initialTransformation,
            fracturable=fracturable,
            hosfordExponant=hosfordExponant,
            criteriaValue=criteriaValue,
            showStressValue=showStressValue,
            showStressVector=showStressVector,
            showFracturableTriangles=showFracturableTriangles,
            computePrincipalStress=computePrincipalStress,
            id=id,
            graphMaxStress=graphMaxStress,
            graphCriteria=graphCriteria,
            graphOrientation=graphOrientation,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangularFEMForceField", params

    @sofa_component
    def ArticulatedHierarchyContainer(
        self,
        axis=None,
        rotation=None,
        translation=None,
        articulationIndex=None,
        parentIndex=None,
        childIndex=None,
        globalPosition=None,
        posOnParent=None,
        posOnChild=None,
        articulationProcess=None,
        filename=None,
        **kwargs
    ):
        """
        ArticulatedHierarchyContainer

        :param axis: Set the rotation axis for the articulation
        :param rotation: Rotation
        :param translation: Translation
        :param articulationIndex: Articulation index
        :param parentIndex: Parent of the center articulation
        :param childIndex: Child of the center articulation
        :param globalPosition: Global position of the articulation center
        :param posOnParent: Parent position of the articulation center
        :param posOnChild: Child position of the articulation center
        :param articulationProcess:  0 - (default) hierarchy between articulations (euler angles)\n 1- ( on Parent) no hierarchy - axis are attached to the parent\n 2- (attached on Child) no hierarchy - axis are attached to the child
        :param filename: BVH File to load the articulation
        """
        params = dict(
            axis=axis,
            rotation=rotation,
            translation=translation,
            articulationIndex=articulationIndex,
            parentIndex=parentIndex,
            childIndex=childIndex,
            globalPosition=globalPosition,
            posOnParent=posOnParent,
            posOnChild=posOnChild,
            articulationProcess=articulationProcess,
            filename=filename,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ArticulatedHierarchyContainer", params

    @sofa_component
    def ArticulatedSystemMapping(self, **kwargs):
        """
        ArticulatedSystemMapping
        """
        params = dict()
        return "ArticulatedSystemMapping", params

    @sofa_component
    def LineSetSkinningMapping(
        self,
        neighborhoodLevel=None,
        numberInfluencedLines=None,
        weightCoef=None,
        **kwargs
    ):
        """
        LineSetSkinningMapping

        :param neighborhoodLevel: Set the neighborhood line level
        :param numberInfluencedLines: Set the number of most influenced lines by each vertice
        :param weightCoef: Set the coefficient used to compute the weight of lines
        """
        params = dict(
            neighborhoodLevel=neighborhoodLevel,
            numberInfluencedLines=numberInfluencedLines,
            weightCoef=weightCoef,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "LineSetSkinningMapping", params

    @sofa_component
    def SkinningMapping(
        self,
        initPos=None,
        nbRef=None,
        indices=None,
        weight=None,
        showFromIndex=None,
        showWeights=None,
        **kwargs
    ):
        """
        SkinningMapping

        :param initPos: initial child coordinates in the world reference frame.
        :param nbRef: Number of primitives influencing each point.
        :param indices: parent indices for each child.
        :param weight: influence weights of the Dofs.
        :param showFromIndex: Displayed From Index.
        :param showWeights: Show influence.
        """
        params = dict(
            initPos=initPos,
            nbRef=nbRef,
            indices=indices,
            weight=weight,
            showFromIndex=showFromIndex,
            showWeights=showWeights,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SkinningMapping", params

    @sofa_component
    def ForceFeedback(self, activate=None, indice=None, **kwargs):
        """
        ForceFeedback

        :param activate: boolean to activate or deactivate the forcefeedback
        :param indice: Tool indice in the OmniDriver
        """
        params = dict(activate=activate, indice=indice)
        params = {k: v for k, v in params.items() if v is not None}
        return "ForceFeedback", params

    @sofa_component
    def LCPForceFeedback(
        self,
        forceCoef=None,
        solverTimeout=None,
        derivRotations=None,
        localHapticConstraintAllFrames=None,
        **kwargs
    ):
        """
        LCPForceFeedback

        :param forceCoef: multiply haptic force by this coef.
        :param solverTimeout: max time to spend solving constraints.
        :param derivRotations: if true, deriv the rotations when updating the violations
        :param localHapticConstraintAllFrames: Flag to enable/disable constraint haptic influence from all frames
        """
        params = dict(
            forceCoef=forceCoef,
            solverTimeout=solverTimeout,
            derivRotations=derivRotations,
            localHapticConstraintAllFrames=localHapticConstraintAllFrames,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "LCPForceFeedback", params

    @sofa_component
    def NullForceFeedback(self, **kwargs):
        """
        NullForceFeedback
        """
        params = dict()
        return "NullForceFeedback", params

    @sofa_component
    def NullForceFeedbackT(self, **kwargs):
        """
        NullForceFeedbackT
        """
        params = dict()
        return "NullForceFeedbackT", params

    @sofa_component
    def MeshTetraStuffing(
        self,
        vbbox=None,
        size=None,
        inputPoints=None,
        inputTriangles=None,
        inputQuads=None,
        outputPoints=None,
        outputTetrahedra=None,
        alphaLong=None,
        alphaShort=None,
        snapPoints=None,
        splitTetrahedra=None,
        draw=None,
        **kwargs
    ):
        """
        MeshTetraStuffing

        :param vbbox: BBox to restrict the volume to
        :param size: Size of the generate tetrahedra. If negative, number of grid cells in the largest bbox dimension
        :param inputPoints: Input surface mesh points
        :param inputTriangles: Input surface mesh triangles
        :param inputQuads: Input surface mesh quads
        :param outputPoints: Output volume mesh points
        :param outputTetrahedra: Output volume mesh tetrahedra
        :param alphaLong: Minimum alpha values on long edges when snapping points
        :param alphaShort: Minimum alpha values on short edges when snapping points
        :param snapPoints: Snap points to the surface if intersections on edges are closed to given alpha values
        :param splitTetrahedra: Split tetrahedra crossing the surface
        :param draw: Activate rendering of internal datasets
        """
        params = dict(
            vbbox=vbbox,
            size=size,
            inputPoints=inputPoints,
            inputTriangles=inputTriangles,
            inputQuads=inputQuads,
            outputPoints=outputPoints,
            outputTetrahedra=outputTetrahedra,
            alphaLong=alphaLong,
            alphaShort=alphaShort,
            snapPoints=snapPoints,
            splitTetrahedra=splitTetrahedra,
            draw=draw,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshTetraStuffing", params

    @sofa_component
    def MultiStepAnimationLoop(
        self, collisionSteps=None, integrationSteps=None, **kwargs
    ):
        """
        MultiStepAnimationLoop

        :param collisionSteps: number of collision steps between each frame rendering
        :param integrationSteps: number of integration steps between each collision detection
        """
        params = dict(collisionSteps=collisionSteps, integrationSteps=integrationSteps)
        params = {k: v for k, v in params.items() if v is not None}
        return "MultiStepAnimationLoop", params

    @sofa_component
    def MultiTagAnimationLoop(self, **kwargs):
        """
        MultiTagAnimationLoop
        """
        params = dict()
        return "MultiTagAnimationLoop", params

    @sofa_component
    def AddFrameButtonSetting(self, **kwargs):
        """
        AddFrameButtonSetting
        """
        params = dict()
        return "AddFrameButtonSetting", params

    @sofa_component
    def AddRecordedCameraButtonSetting(self, **kwargs):
        """
        AddRecordedCameraButtonSetting
        """
        params = dict()
        return "AddRecordedCameraButtonSetting", params

    @sofa_component
    def AttachBodyButtonSetting(
        self, stiffness=None, arrowSize=None, showFactorSize=None, **kwargs
    ):
        """
        AttachBodyButtonSetting

        :param stiffness: Stiffness of the spring to attach a particule
        :param arrowSize: Size of the drawn spring: if >0 an arrow will be drawn
        :param showFactorSize: Show factor size of the JointSpringForcefield  when interacting with rigids
        """
        params = dict(
            stiffness=stiffness, arrowSize=arrowSize, showFactorSize=showFactorSize
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "AttachBodyButtonSetting", params

    @sofa_component
    def FixPickedParticleButtonSetting(self, stiffness=None, **kwargs):
        """
        FixPickedParticleButtonSetting

        :param stiffness: Stiffness of the spring to fix a particule
        """
        params = dict(stiffness=stiffness)
        params = {k: v for k, v in params.items() if v is not None}
        return "FixPickedParticleButtonSetting", params

    @sofa_component
    def Gravity(self, gravity=None, **kwargs):
        """
        Gravity

        :param gravity: Gravity in the world coordinate system
        """
        params = dict(gravity=gravity)
        params = {k: v for k, v in params.items() if v is not None}
        return "Gravity", params

    @sofa_component
    def MouseButtonSetting(self, button=None, **kwargs):
        """
        MouseButtonSetting

        :param button: Mouse button used
        """
        params = dict(button=button)
        params = {k: v for k, v in params.items() if v is not None}
        return "MouseButtonSetting", params

    @sofa_component
    def PauseAnimation(self, **kwargs):
        """
        PauseAnimation
        """
        params = dict()
        return "PauseAnimation", params

    @sofa_component
    def PauseAnimationOnEvent(self, **kwargs):
        """
        PauseAnimationOnEvent
        """
        params = dict()
        return "PauseAnimationOnEvent", params

    @sofa_component
    def SofaDefaultPathSetting(self, recordPath=None, gnuplotPath=None, **kwargs):
        """
        SofaDefaultPathSetting

        :param recordPath: Path where will be saved the data of the recorded simulation
        :param gnuplotPath: Path where will be saved the gnuplot files
        """
        params = dict(recordPath=recordPath, gnuplotPath=gnuplotPath)
        params = {k: v for k, v in params.items() if v is not None}
        return "SofaDefaultPathSetting", params

    @sofa_component
    def StatsSetting(
        self,
        dumpState=None,
        logTime=None,
        exportState=None,
        traceVisitors=None,
        **kwargs
    ):
        """
        StatsSetting

        :param dumpState: Dump state vectors at each time step of the simulation
        :param logTime: Output in the console an average of the time spent during different stages of the simulation
        :param exportState: Create GNUPLOT files with the positions, velocities and forces of all the simulated objects of the scene
        :param traceVisitors: Trace the time spent by each visitor, and allows to profile precisely one step of a simulation
        """
        params = dict(
            dumpState=dumpState,
            logTime=logTime,
            exportState=exportState,
            traceVisitors=traceVisitors,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "StatsSetting", params

    @sofa_component
    def ViewerSetting(
        self,
        resolution=None,
        fullscreen=None,
        cameraMode=None,
        objectPickingMethod=None,
        **kwargs
    ):
        """
        ViewerSetting

        :param resolution: resolution of the Viewer
        :param fullscreen: Fullscreen mode
        :param cameraMode: Camera mode
        :param objectPickingMethod: The method used to pick objects
        """
        params = dict(
            resolution=resolution,
            fullscreen=fullscreen,
            cameraMode=cameraMode,
            objectPickingMethod=objectPickingMethod,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ViewerSetting", params

    @sofa_component
    def SceneCheckDuplicatedName(self, **kwargs):
        """
        SceneCheckDuplicatedName
        """
        params = dict()
        return "SceneCheckDuplicatedName", params

    @sofa_component
    def SceneCheckMissingRequiredPlugin(self, **kwargs):
        """
        SceneCheckMissingRequiredPlugin
        """
        params = dict()
        return "SceneCheckMissingRequiredPlugin", params

    @sofa_component
    def SceneCheckAPIChange(self, **kwargs):
        """
        SceneCheckAPIChange
        """
        params = dict()
        return "SceneCheckAPIChange", params

    @sofa_component
    def SceneCheckUsingAlias(self, **kwargs):
        """
        SceneCheckUsingAlias
        """
        params = dict()
        return "SceneCheckUsingAlias", params

    @sofa_component
    def SceneCheckerVisitor(self, **kwargs):
        """
        SceneCheckerVisitor
        """
        params = dict()
        return "SceneCheckerVisitor", params

    @sofa_component
    def SceneCheckerListener(self, **kwargs):
        """
        SceneCheckerListener
        """
        params = dict()
        return "SceneCheckerListener", params

    @sofa_component
    def APIVersion(self, level=None, **kwargs):
        """
        APIVersion

        :param level: The API Level of the scene ('17.06', '17.12', '18.06', ...)
        """
        params = dict(level=level)
        params = {k: v for k, v in params.items() if v is not None}
        return "APIVersion", params

    @sofa_component
    def FastTriangularBendingSprings(
        self, bendingStiffness=None, minDistValidity=None, edgeInfo=None, **kwargs
    ):
        """
        FastTriangularBendingSprings

        :param bendingStiffness: bending stiffness of the material
        :param minDistValidity: Distance under which a spring is not valid
        :param edgeInfo: Internal edge data
        """
        params = dict(
            bendingStiffness=bendingStiffness,
            minDistValidity=minDistValidity,
            edgeInfo=edgeInfo,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "FastTriangularBendingSprings", params

    @sofa_component
    def FrameSpringForceField(self, spring=None, **kwargs):
        """
        FrameSpringForceField

        :param spring: pairs of indices, stiffness, damping, rest length
        """
        params = dict(spring=spring)
        params = {k: v for k, v in params.items() if v is not None}
        return "FrameSpringForceField", params

    @sofa_component
    def QuadBendingSprings(self, localRange=None, **kwargs):
        """
        QuadBendingSprings

        :param localRange: optional range of local DOF indices. Any computation involving only indices outside of this range are discarded (useful for parallelization using mesh partitionning)
        """
        params = dict(localRange=localRange)
        params = {k: v for k, v in params.items() if v is not None}
        return "QuadBendingSprings", params

    @sofa_component
    def QuadularBendingSprings(
        self, stiffness=None, damping=None, edgeInfo=None, **kwargs
    ):
        """
        QuadularBendingSprings

        :param stiffness: uniform stiffness for the all springs
        :param damping: uniform damping for the all springs
        :param edgeInfo: Internal edge data
        """
        params = dict(stiffness=stiffness, damping=damping, edgeInfo=edgeInfo)
        params = {k: v for k, v in params.items() if v is not None}
        return "QuadularBendingSprings", params

    @sofa_component
    def RegularGridSpringForceField(
        self,
        linesStiffness=None,
        linesDamping=None,
        quadsStiffness=None,
        quadsDamping=None,
        cubesStiffness=None,
        cubesDamping=None,
        **kwargs
    ):
        """
        RegularGridSpringForceField

        :param linesStiffness: Lines Stiffness
        :param linesDamping: Lines Damping
        :param quadsStiffness: Quads Stiffness
        :param quadsDamping: Quads Damping
        :param cubesStiffness: Cubes Stiffness
        :param cubesDamping: Cubes Damping
        """
        params = dict(
            linesStiffness=linesStiffness,
            linesDamping=linesDamping,
            quadsStiffness=quadsStiffness,
            quadsDamping=quadsDamping,
            cubesStiffness=cubesStiffness,
            cubesDamping=cubesDamping,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "RegularGridSpringForceField", params

    @sofa_component
    def TriangleBendingSprings(self, **kwargs):
        """
        TriangleBendingSprings
        """
        params = dict()
        return "TriangleBendingSprings", params

    @sofa_component
    def TriangularBendingSprings(
        self, stiffness=None, damping=None, edgeInfo=None, **kwargs
    ):
        """
        TriangularBendingSprings

        :param stiffness: uniform stiffness for the all springs
        :param damping: uniform damping for the all springs
        :param edgeInfo: Internal edge data
        """
        params = dict(stiffness=stiffness, damping=damping, edgeInfo=edgeInfo)
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangularBendingSprings", params

    @sofa_component
    def TriangularBiquadraticSpringsForceField(
        self,
        triangleInfo=None,
        edgeInfo=None,
        initialPoints=None,
        poissonRatio=None,
        youngModulus=None,
        dampingRatio=None,
        useAngularSprings=None,
        compressible=None,
        matrixRegularization=None,
        **kwargs
    ):
        """
        TriangularBiquadraticSpringsForceField

        :param triangleInfo: Internal triangle data
        :param edgeInfo: Internal edge data
        :param initialPoints: Initial Position
        :param poissonRatio: Poisson ratio in Hooke's law
        :param youngModulus: Young modulus in Hooke's law
        :param dampingRatio: Ratio damping/stiffness
        :param useAngularSprings: If Angular Springs should be used or not
        :param compressible: If additional energy penalizing compressibility should be used
        :param matrixRegularization: Regularization of the Stiffnes Matrix (between 0 and 1)
        """
        params = dict(
            triangleInfo=triangleInfo,
            edgeInfo=edgeInfo,
            initialPoints=initialPoints,
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            dampingRatio=dampingRatio,
            useAngularSprings=useAngularSprings,
            compressible=compressible,
            matrixRegularization=matrixRegularization,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangularBiquadraticSpringsForceField", params

    @sofa_component
    def TriangularQuadraticSpringsForceField(
        self,
        initialPoints=None,
        poissonRatio=None,
        youngModulus=None,
        dampingRatio=None,
        useAngularSprings=None,
        triangleInfo=None,
        edgeInfo=None,
        **kwargs
    ):
        """
        TriangularQuadraticSpringsForceField

        :param initialPoints: Initial Position
        :param poissonRatio: Poisson ratio in Hooke's law
        :param youngModulus: Young modulus in Hooke's law
        :param dampingRatio: Ratio damping/stiffness
        :param useAngularSprings: If Angular Springs should be used or not
        :param triangleInfo: Internal triangle data
        :param edgeInfo: Internal edge data
        """
        params = dict(
            initialPoints=initialPoints,
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            dampingRatio=dampingRatio,
            useAngularSprings=useAngularSprings,
            triangleInfo=triangleInfo,
            edgeInfo=edgeInfo,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangularQuadraticSpringsForceField", params

    @sofa_component
    def TriangularTensorMassForceField(
        self, edgeInfo=None, poissonRatio=None, youngModulus=None, **kwargs
    ):
        """
        TriangularTensorMassForceField

        :param edgeInfo: Internal edge data
        :param poissonRatio: Poisson ratio in Hooke's law
        :param youngModulus: Young modulus in Hooke's law
        """
        params = dict(
            edgeInfo=edgeInfo, poissonRatio=poissonRatio, youngModulus=youngModulus
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangularTensorMassForceField", params

    @sofa_component
    def VectorSpringForceField(
        self,
        springs=None,
        filename=None,
        stiffness=None,
        viscosity=None,
        useTopology=None,
        **kwargs
    ):
        """
        VectorSpringForceField

        :param springs: springs data
        :param filename: File name from which the spring informations are loaded
        :param stiffness: Default edge stiffness used in absence of file information
        :param viscosity: Default edge viscosity used in absence of file information
        :param useTopology: Activate/Desactivate topology mode of the component (springs on each edge)
        """
        params = dict(
            springs=springs,
            filename=filename,
            stiffness=stiffness,
            viscosity=viscosity,
            useTopology=useTopology,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "VectorSpringForceField", params

    @sofa_component
    def RecordedCamera(
        self,
        zoomSpeed=None,
        panSpeed=None,
        pivot=None,
        startTime=None,
        endTime=None,
        rotationMode=None,
        translationMode=None,
        navigationMode=None,
        rotationSpeed=None,
        rotationCenter=None,
        rotationStartPoint=None,
        rotationLookAt=None,
        rotationAxis=None,
        cameraUp=None,
        drawRotation=None,
        drawTranslation=None,
        cameraPositions=None,
        cameraOrientations=None,
        **kwargs
    ):
        """
        RecordedCamera

        :param zoomSpeed: Zoom Speed
        :param panSpeed: Pan Speed
        :param pivot: Pivot (0 => Scene center, 1 => World Center
        :param startTime: Time when the camera moves will start
        :param endTime: Time when the camera moves will end (or loop)
        :param rotationMode: If true, rotation will be performed
        :param translationMode: If true, translation will be performed
        :param navigationMode: If true, navigation will be performed
        :param rotationSpeed: rotation Speed
        :param rotationCenter: Rotation center coordinates
        :param rotationStartPoint: Rotation start position coordinates
        :param rotationLookAt: Position to be focused during rotation
        :param rotationAxis: Rotation axis
        :param cameraUp: Camera Up axis
        :param drawRotation: If true, will draw the rotation path
        :param drawTranslation: If true, will draw the translation path
        :param cameraPositions: Intermediate camera's positions
        :param cameraOrientations: Intermediate camera's orientations
        """
        params = dict(
            zoomSpeed=zoomSpeed,
            panSpeed=panSpeed,
            pivot=pivot,
            startTime=startTime,
            endTime=endTime,
            rotationMode=rotationMode,
            translationMode=translationMode,
            navigationMode=navigationMode,
            rotationSpeed=rotationSpeed,
            rotationCenter=rotationCenter,
            rotationStartPoint=rotationStartPoint,
            rotationLookAt=rotationLookAt,
            rotationAxis=rotationAxis,
            cameraUp=cameraUp,
            drawRotation=drawRotation,
            drawTranslation=drawTranslation,
            cameraPositions=cameraPositions,
            cameraOrientations=cameraOrientations,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "RecordedCamera", params

    @sofa_component
    def VisualTransform(self, transform=None, recursive=None, **kwargs):
        """
        VisualTransform

        :param transform: Transformation to apply
        :param recursive: True to apply transform to all nodes below
        """
        params = dict(transform=transform, recursive=recursive)
        params = {k: v for k, v in params.items() if v is not None}
        return "VisualTransform", params

    @sofa_component
    def Visual3DText(
        self, text=None, position=None, scale=None, color=None, depthTest=None, **kwargs
    ):
        """
        Visual3DText

        :param text: Test to display
        :param position: 3d position
        :param scale: text scale
        :param color: text color. (default=[1.0,1.0,1.0,1.0])
        :param depthTest: perform depth test
        """
        params = dict(
            text=text, position=position, scale=scale, color=color, depthTest=depthTest
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "Visual3DText", params

    @sofa_component
    def DisplacementMatrixEngine(
        self, x0=None, x=None, displacements=None, scales=None, **kwargs
    ):
        """
        DisplacementMatrixEngine

        :param x0: Rest position
        :param x: Current position
        :param displacements: Displacement transforms with respect to original rigid positions
        :param scales: Scale transformation added to the rigid transformation
        """
        params = dict(x0=x0, x=x, displacements=displacements, scales=scales)
        params = {k: v for k, v in params.items() if v is not None}
        return "DisplacementMatrixEngine", params

    @sofa_component
    def Distances(
        self,
        showMapIndex=None,
        showDistancesMap=None,
        showGoalDistancesMap=None,
        showTextScaleFactor=None,
        showGradients=None,
        showGradientsScaleFactor=None,
        offset=None,
        distanceType=None,
        initTarget=None,
        initTargetStep=None,
        zonesFramePair=None,
        harmonicMaxValue=None,
        filename=None,
        targetPath=None,
        hexaContainerPath=None,
        **kwargs
    ):
        """
        Distances

        :param showMapIndex: Frame DOF index on which display values.
        :param showDistancesMap: show the dsitance for each point of the target point set.
        :param showGoalDistancesMap: show the dsitance for each point of the target point set.
        :param showTextScaleFactor: Scale to apply on the text.
        :param showGradients: show gradients for each point of the target point set.
        :param showGradientsScaleFactor: scale for the gradients displayed.
        :param offset: translation offset between the topology and the point set.
        :param distanceType: type of distance to compute for inserted frames.
        :param initTarget: initialize the target MechanicalObject from the grid.
        :param initTargetStep: initialize the target MechanicalObject from the grid using this step.
        :param zonesFramePair: Correspondance between the segmented value and the frames.
        :param harmonicMaxValue: Max value used to initialize the harmonic distance grid.
        :param filename: file containing the result of the computation of the distances
        :param targetPath: path to the goal point set topology
        :param hexaContainerPath: path to the grid used to compute the distances
        """
        params = dict(
            showMapIndex=showMapIndex,
            showDistancesMap=showDistancesMap,
            showGoalDistancesMap=showGoalDistancesMap,
            showTextScaleFactor=showTextScaleFactor,
            showGradients=showGradients,
            showGradientsScaleFactor=showGradientsScaleFactor,
            offset=offset,
            distanceType=distanceType,
            initTarget=initTarget,
            initTargetStep=initTargetStep,
            zonesFramePair=zonesFramePair,
            harmonicMaxValue=harmonicMaxValue,
            filename=filename,
            targetPath=targetPath,
            hexaContainerPath=hexaContainerPath,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "Distances", params

    @sofa_component
    def ProjectiveTransformEngine(
        self,
        input_position=None,
        output_position=None,
        proj_mat=None,
        focal_distance=None,
        **kwargs
    ):
        """
        ProjectiveTransformEngine

        :param input_position: input array of 3d points
        :param output_position: output array of projected 3d points
        :param proj_mat: projection matrix
        :param focal_distance: focal distance
        """
        params = dict(
            input_position=input_position,
            output_position=output_position,
            proj_mat=proj_mat,
            focal_distance=focal_distance,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ProjectiveTransformEngine", params

    @sofa_component
    def BTDLinearSolver(
        self,
        verbose=None,
        showProblem=None,
        subpartSolve=None,
        verification=None,
        test_perf=None,
        blockSize=None,
        **kwargs
    ):
        """
        BTDLinearSolver

        :param verbose: Dump system state at each iteration
        :param showProblem: display debug informations about subpartSolve computation
        :param subpartSolve: Allows for the computation of a subpart of the system
        :param verification: verification of the subpartSolve
        :param test_perf: verification of performance
        :param blockSize: dimension of the blocks in the matrix
        """
        params = dict(
            verbose=verbose,
            showProblem=showProblem,
            subpartSolve=subpartSolve,
            verification=verification,
            test_perf=test_perf,
            blockSize=blockSize,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "BTDLinearSolver", params

    @sofa_component
    def CholeskySolver(self, verbose=None, **kwargs):
        """
        CholeskySolver

        :param verbose: Dump system state at each iteration
        """
        params = dict(verbose=verbose)
        params = {k: v for k, v in params.items() if v is not None}
        return "CholeskySolver", params

    @sofa_component
    def MinResLinearSolver(
        self, iterations=None, tolerance=None, verbose=None, graph=None, **kwargs
    ):
        """
        MinResLinearSolver

        :param iterations: maximum number of iterations of the Conjugate Gradient solution
        :param tolerance: desired precision of the Conjugate Gradient Solution (ratio of current residual norm over initial residual norm)
        :param verbose: Dump system state at each iteration
        :param graph: Graph of residuals at each iteration
        """
        params = dict(
            iterations=iterations, tolerance=tolerance, verbose=verbose, graph=graph
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MinResLinearSolver", params

    @sofa_component
    def InteractionPerformer(self, **kwargs):
        """
        InteractionPerformer
        """
        params = dict()
        return "InteractionPerformer", params

    @sofa_component
    def MouseInteractor(self, **kwargs):
        """
        MouseInteractor
        """
        params = dict()
        return "MouseInteractor", params

    @sofa_component
    def AddRecordedCameraPerformer(self, **kwargs):
        """
        AddRecordedCameraPerformer
        """
        params = dict()
        return "AddRecordedCameraPerformer", params

    @sofa_component
    def AttachBodyPerformer(self, **kwargs):
        """
        AttachBodyPerformer
        """
        params = dict()
        return "AttachBodyPerformer", params

    @sofa_component
    def ComponentMouseInteraction(self, **kwargs):
        """
        ComponentMouseInteraction
        """
        params = dict()
        return "ComponentMouseInteraction", params

    @sofa_component
    def Controller(self, handleEventTriggersUpdate=None, **kwargs):
        """
        Controller

        :param handleEventTriggersUpdate: Event handling frequency controls the controller update frequency
        """
        params = dict(handleEventTriggersUpdate=handleEventTriggersUpdate)
        params = {k: v for k, v in params.items() if v is not None}
        return "Controller", params

    @sofa_component
    def FixParticlePerformer(self, **kwargs):
        """
        FixParticlePerformer
        """
        params = dict()
        return "FixParticlePerformer", params

    @sofa_component
    def InciseAlongPathPerformer(self, **kwargs):
        """
        InciseAlongPathPerformer
        """
        params = dict()
        return "InciseAlongPathPerformer", params

    @sofa_component
    def MechanicalStateController(
        self,
        index=None,
        onlyTranslation=None,
        buttonDeviceState=None,
        mainDirection=None,
        **kwargs
    ):
        """
        MechanicalStateController

        :param index: Index of the controlled DOF
        :param onlyTranslation: Controlling the DOF only in translation
        :param buttonDeviceState: state of ths device button
        :param mainDirection: Main direction and orientation of the controlled DOF
        """
        params = dict(
            index=index,
            onlyTranslation=onlyTranslation,
            buttonDeviceState=buttonDeviceState,
            mainDirection=mainDirection,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MechanicalStateController", params

    @sofa_component
    def RayContact(self, **kwargs):
        """
        RayContact
        """
        params = dict()
        return "RayContact", params

    @sofa_component
    def RayDiscreteIntersection(self, **kwargs):
        """
        RayDiscreteIntersection
        """
        params = dict()
        return "RayDiscreteIntersection", params

    @sofa_component
    def RayModel(self, **kwargs):
        """
        RayModel
        """
        params = dict()
        return "RayModel", params

    @sofa_component
    def RayNewProximityIntersection(self, **kwargs):
        """
        RayNewProximityIntersection
        """
        params = dict()
        return "RayNewProximityIntersection", params

    @sofa_component
    def RayTraceDetection(self, **kwargs):
        """
        RayTraceDetection
        """
        params = dict()
        return "RayTraceDetection", params

    @sofa_component
    def SleepController(
        self,
        minTimeSinceWakeUp=None,
        immobileThreshold=None,
        rotationThreshold=None,
        **kwargs
    ):
        """
        SleepController

        :param minTimeSinceWakeUp: Do not do anything before objects have been moving for this duration
        :param immobileThreshold: Speed value under which we consider a particule to be immobile
        :param rotationThreshold: If non null, this is the rotation speed value under which we consider a particule to be immobile
        """
        params = dict(
            minTimeSinceWakeUp=minTimeSinceWakeUp,
            immobileThreshold=immobileThreshold,
            rotationThreshold=rotationThreshold,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SleepController", params

    @sofa_component
    def TopologicalChangeManager(self, **kwargs):
        """
        TopologicalChangeManager
        """
        params = dict()
        return "TopologicalChangeManager", params

    @sofa_component
    def RemovePrimitivePerformer(self, **kwargs):
        """
        RemovePrimitivePerformer
        """
        params = dict()
        return "RemovePrimitivePerformer", params

    @sofa_component
    def StartNavigationPerformer(self, **kwargs):
        """
        StartNavigationPerformer
        """
        params = dict()
        return "StartNavigationPerformer", params

    @sofa_component
    def SuturePointPerformer(self, **kwargs):
        """
        SuturePointPerformer
        """
        params = dict()
        return "SuturePointPerformer", params

    @sofa_component
    def Main(self, **kwargs):
        """
        Main
        """
        params = dict()
        return "Main", params

    @sofa_component
    def CenterPointTopologicalMapping(self, **kwargs):
        """
        CenterPointTopologicalMapping
        """
        params = dict()
        return "CenterPointTopologicalMapping", params

    @sofa_component
    def Edge2QuadTopologicalMapping(
        self,
        nbPointsOnEachCircle=None,
        radius=None,
        edgeList=None,
        flipNormals=None,
        **kwargs
    ):
        """
        Edge2QuadTopologicalMapping

        :param nbPointsOnEachCircle: Discretization of created circles
        :param radius: Radius of created circles
        :param edgeList: list of input edges for the topological mapping: by default, all considered
        :param flipNormals: Flip Normal ? (Inverse point order when creating quad)
        """
        params = dict(
            nbPointsOnEachCircle=nbPointsOnEachCircle,
            radius=radius,
            edgeList=edgeList,
            flipNormals=flipNormals,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "Edge2QuadTopologicalMapping", params

    @sofa_component
    def Hexa2QuadTopologicalMapping(self, flipNormals=None, **kwargs):
        """
        Hexa2QuadTopologicalMapping

        :param flipNormals: Flip Normal ? (Inverse point order when creating triangle)
        """
        params = dict(flipNormals=flipNormals)
        params = {k: v for k, v in params.items() if v is not None}
        return "Hexa2QuadTopologicalMapping", params

    @sofa_component
    def Hexa2TetraTopologicalMapping(self, swapping=None, **kwargs):
        """
        Hexa2TetraTopologicalMapping

        :param swapping: Boolean enabling to swapp hexa-edges\n in order to avoid bias effect
        """
        params = dict(swapping=swapping)
        params = {k: v for k, v in params.items() if v is not None}
        return "Hexa2TetraTopologicalMapping", params

    @sofa_component
    def IdentityTopologicalMapping(self, **kwargs):
        """
        IdentityTopologicalMapping
        """
        params = dict()
        return "IdentityTopologicalMapping", params

    @sofa_component
    def Mesh2PointMechanicalMapping(self, **kwargs):
        """
        Mesh2PointMechanicalMapping
        """
        params = dict()
        return "Mesh2PointMechanicalMapping", params

    @sofa_component
    def Mesh2PointTopologicalMapping(
        self,
        pointBaryCoords=None,
        edgeBaryCoords=None,
        triangleBaryCoords=None,
        quadBaryCoords=None,
        tetraBaryCoords=None,
        hexaBaryCoords=None,
        copyEdges=None,
        copyTriangles=None,
        copyTetrahedra=None,
        **kwargs
    ):
        """
        Mesh2PointTopologicalMapping

        :param pointBaryCoords: Coordinates for the points of the output topology created from the points of the input topology
        :param edgeBaryCoords: Coordinates for the points of the output topology created from the edges of the input topology
        :param triangleBaryCoords: Coordinates for the points of the output topology created from the triangles of the input topology
        :param quadBaryCoords: Coordinates for the points of the output topology created from the quads of the input topology
        :param tetraBaryCoords: Coordinates for the points of the output topology created from the tetra of the input topology
        :param hexaBaryCoords: Coordinates for the points of the output topology created from the hexa of the input topology
        :param copyEdges: Activate mapping of input edges into the output topology (requires at least one item in pointBaryCoords)
        :param copyTriangles: Activate mapping of input triangles into the output topology (requires at least one item in pointBaryCoords)
        :param copyTetrahedra: Activate mapping of input tetrahedra into the output topology (requires at least one item in pointBaryCoords)
        """
        params = dict(
            pointBaryCoords=pointBaryCoords,
            edgeBaryCoords=edgeBaryCoords,
            triangleBaryCoords=triangleBaryCoords,
            quadBaryCoords=quadBaryCoords,
            tetraBaryCoords=tetraBaryCoords,
            hexaBaryCoords=hexaBaryCoords,
            copyEdges=copyEdges,
            copyTriangles=copyTriangles,
            copyTetrahedra=copyTetrahedra,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "Mesh2PointTopologicalMapping", params

    @sofa_component
    def Quad2TriangleTopologicalMapping(self, **kwargs):
        """
        Quad2TriangleTopologicalMapping
        """
        params = dict()
        return "Quad2TriangleTopologicalMapping", params

    @sofa_component
    def SimpleTesselatedHexaTopologicalMapping(self, **kwargs):
        """
        SimpleTesselatedHexaTopologicalMapping
        """
        params = dict()
        return "SimpleTesselatedHexaTopologicalMapping", params

    @sofa_component
    def SimpleTesselatedTetraMechanicalMapping(self, **kwargs):
        """
        SimpleTesselatedTetraMechanicalMapping
        """
        params = dict()
        return "SimpleTesselatedTetraMechanicalMapping", params

    @sofa_component
    def SimpleTesselatedTetraTopologicalMapping(
        self,
        tetrahedraMappedFromTetra=None,
        tetraSource=None,
        pointMappedFromPoint=None,
        pointMappedFromEdge=None,
        pointSource=None,
        **kwargs
    ):
        """
        SimpleTesselatedTetraTopologicalMapping

        :param tetrahedraMappedFromTetra: Each Tetrahedron of the input topology is mapped to the 8 tetrahedrons in which it can be divided
        :param tetraSource: Which tetra from the input topology map to a given tetra in the output topology (-1 if none)
        :param pointMappedFromPoint: Each point of the input topology is mapped to the same point
        :param pointMappedFromEdge: Each edge of the input topology is mapped to his midpoint
        :param pointSource: Which input topology element map to a given point in the output topology : 0 -> none, > 0 -> point index + 1, < 0 , - edge index -1
        """
        params = dict(
            tetrahedraMappedFromTetra=tetrahedraMappedFromTetra,
            tetraSource=tetraSource,
            pointMappedFromPoint=pointMappedFromPoint,
            pointMappedFromEdge=pointMappedFromEdge,
            pointSource=pointSource,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SimpleTesselatedTetraTopologicalMapping", params

    @sofa_component
    def SubsetTopologicalMapping(
        self,
        samePoints=None,
        handleEdges=None,
        handleTriangles=None,
        handleQuads=None,
        handleTetrahedra=None,
        handleHexahedra=None,
        pointS2D=None,
        pointD2S=None,
        edgeS2D=None,
        edgeD2S=None,
        triangleS2D=None,
        triangleD2S=None,
        quadS2D=None,
        quadD2S=None,
        tetrahedronS2D=None,
        tetrahedronD2S=None,
        hexahedronS2D=None,
        hexahedronD2S=None,
        **kwargs
    ):
        """
        SubsetTopologicalMapping

        :param samePoints: True if the same set of points is used in both topologies
        :param handleEdges: True if edges events and mapping should be handled
        :param handleTriangles: True if triangles events and mapping should be handled
        :param handleQuads: True if quads events and mapping should be handled
        :param handleTetrahedra: True if tetrahedra events and mapping should be handled
        :param handleHexahedra: True if hexahedra events and mapping should be handled
        :param pointS2D: Internal source -> destination topology points map
        :param pointD2S: Internal destination -> source topology points map (link to SubsetMapping::indices to handle the mechanical-side of the mapping
        :param edgeS2D: Internal source -> destination topology edges map
        :param edgeD2S: Internal destination -> source topology edges map
        :param triangleS2D: Internal source -> destination topology triangles map
        :param triangleD2S: Internal destination -> source topology triangles map
        :param quadS2D: Internal source -> destination topology quads map
        :param quadD2S: Internal destination -> source topology quads map
        :param tetrahedronS2D: Internal source -> destination topology tetrahedra map
        :param tetrahedronD2S: Internal destination -> source topology tetrahedra map
        :param hexahedronS2D: Internal source -> destination topology hexahedra map
        :param hexahedronD2S: Internal destination -> source topology hexahedra map
        """
        params = dict(
            samePoints=samePoints,
            handleEdges=handleEdges,
            handleTriangles=handleTriangles,
            handleQuads=handleQuads,
            handleTetrahedra=handleTetrahedra,
            handleHexahedra=handleHexahedra,
            pointS2D=pointS2D,
            pointD2S=pointD2S,
            edgeS2D=edgeS2D,
            edgeD2S=edgeD2S,
            triangleS2D=triangleS2D,
            triangleD2S=triangleD2S,
            quadS2D=quadS2D,
            quadD2S=quadD2S,
            tetrahedronS2D=tetrahedronS2D,
            tetrahedronD2S=tetrahedronD2S,
            hexahedronS2D=hexahedronS2D,
            hexahedronD2S=hexahedronD2S,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SubsetTopologicalMapping", params

    @sofa_component
    def Tetra2TriangleTopologicalMapping(
        self, flipNormals=None, noNewTriangles=None, noInitialTriangles=None, **kwargs
    ):
        """
        Tetra2TriangleTopologicalMapping

        :param flipNormals: Flip Normal ? (Inverse point order when creating triangle)
        :param noNewTriangles: If true no new triangles are being created
        :param noInitialTriangles: If true the list of initial triangles is initially empty. Only additional triangles will be added in the list
        """
        params = dict(
            flipNormals=flipNormals,
            noNewTriangles=noNewTriangles,
            noInitialTriangles=noInitialTriangles,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "Tetra2TriangleTopologicalMapping", params

    @sofa_component
    def Triangle2EdgeTopologicalMapping(self, **kwargs):
        """
        Triangle2EdgeTopologicalMapping
        """
        params = dict()
        return "Triangle2EdgeTopologicalMapping", params

    @sofa_component
    def VariationalSymplecticSolver(
        self,
        newtonError=None,
        steps=None,
        rayleighStiffness=None,
        rayleighMass=None,
        verbose=None,
        saveEnergyInFile=None,
        explicitIntegration=None,
        file=None,
        computeHamiltonian=None,
        hamiltonianEnergy=None,
        useIncrementalPotentialEnergy=None,
        threadSafeVisitor=None,
        **kwargs
    ):
        """
        VariationalSymplecticSolver

        :param newtonError: Error tolerance for Newton iterations
        :param steps: Maximum number of Newton steps
        :param rayleighStiffness: Rayleigh damping coefficient related to stiffness, > 0
        :param rayleighMass: Rayleigh damping coefficient related to mass, > 0
        :param verbose: Dump information on the residual errors and number of Newton iterations
        :param saveEnergyInFile: If kinetic and potential energies should be dumped in a CSV file at each iteration
        :param explicitIntegration: Use explicit integration scheme
        :param file: File name where kinetic and potential energies are saved in a CSV file
        :param computeHamiltonian: Compute hamiltonian
        :param hamiltonianEnergy: hamiltonian energy
        :param useIncrementalPotentialEnergy: use real potential energy, if false use approximate potential energy
        :param threadSafeVisitor: If true, do not use realloc and free visitors in fwdInteractionForceField.
        """
        params = dict(
            newtonError=newtonError,
            steps=steps,
            rayleighStiffness=rayleighStiffness,
            rayleighMass=rayleighMass,
            verbose=verbose,
            saveEnergyInFile=saveEnergyInFile,
            explicitIntegration=explicitIntegration,
            file=file,
            computeHamiltonian=computeHamiltonian,
            hamiltonianEnergy=hamiltonianEnergy,
            useIncrementalPotentialEnergy=useIncrementalPotentialEnergy,
            threadSafeVisitor=threadSafeVisitor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "VariationalSymplecticSolver", params

    @sofa_component
    def AffineMovementConstraint(
        self,
        meshIndices=None,
        indices=None,
        beginConstraintTime=None,
        endConstraintTime=None,
        rotation=None,
        quaternion=None,
        translation=None,
        drawConstrainedPoints=None,
        **kwargs
    ):
        """
        AffineMovementConstraint

        :param meshIndices: Indices of the mesh
        :param indices: Indices of the constrained points
        :param beginConstraintTime: Begin time of the bilinear constraint
        :param endConstraintTime: End time of the bilinear constraint
        :param rotation: rotation applied to border points
        :param quaternion: quaternion applied to border points
        :param translation: translation applied to border points
        :param drawConstrainedPoints: draw constrained points
        """
        params = dict(
            meshIndices=meshIndices,
            indices=indices,
            beginConstraintTime=beginConstraintTime,
            endConstraintTime=endConstraintTime,
            rotation=rotation,
            quaternion=quaternion,
            translation=translation,
            drawConstrainedPoints=drawConstrainedPoints,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "AffineMovementConstraint", params

    @sofa_component
    def ConicalForceField(
        self,
        coneCenter=None,
        coneHeight=None,
        coneAngle=None,
        stiffness=None,
        damping=None,
        color=None,
        **kwargs
    ):
        """
        ConicalForceField

        :param coneCenter: cone center
        :param coneHeight: cone height
        :param coneAngle: cone angle
        :param stiffness: force stiffness
        :param damping: force damping
        :param color: cone color. (default=0.0,0.0,0.0,1.0,1.0)
        """
        params = dict(
            coneCenter=coneCenter,
            coneHeight=coneHeight,
            coneAngle=coneAngle,
            stiffness=stiffness,
            damping=damping,
            color=color,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ConicalForceField", params

    @sofa_component
    def ConstantForceField(
        self,
        indices=None,
        indexFromEnd=None,
        forces=None,
        force=None,
        totalForce=None,
        showArrowSize=None,
        showColor=None,
        **kwargs
    ):
        """
        ConstantForceField

        :param indices: indices where the forces are applied
        :param indexFromEnd: Concerned DOFs indices are numbered from the end of the MState DOFs vector. (default=false)
        :param forces: applied forces at each point
        :param force: applied force to all points if forces attribute is not specified
        :param totalForce: total force for all points, will be distributed uniformly over points
        :param showArrowSize: Size of the drawn arrows (0->no arrows, sign->direction of drawing. (default=0)
        :param showColor: Color for object display (default: [0.2,0.9,0.3,1.0])
        """
        params = dict(
            indices=indices,
            indexFromEnd=indexFromEnd,
            forces=forces,
            force=force,
            totalForce=totalForce,
            showArrowSize=showArrowSize,
            showColor=showColor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ConstantForceField", params

    @sofa_component
    def DiagonalVelocityDampingForceField(self, dampingCoefficient=None, **kwargs):
        """
        DiagonalVelocityDampingForceField

        :param dampingCoefficient: velocity damping coefficients (by cinematic dof)
        """
        params = dict(dampingCoefficient=dampingCoefficient)
        params = {k: v for k, v in params.items() if v is not None}
        return "DiagonalVelocityDampingForceField", params

    @sofa_component
    def EdgePressureForceField(
        self,
        edgePressureMap=None,
        pressure=None,
        edgeIndices=None,
        edges=None,
        normal=None,
        dmin=None,
        dmax=None,
        arrowSizeCoef=None,
        p_intensity=None,
        binormal=None,
        showForces=None,
        **kwargs
    ):
        """
        EdgePressureForceField

        :param edgePressureMap: map between edge indices and their pressure
        :param pressure: Pressure force per unit area
        :param edgeIndices: Indices of edges separated with commas where a pressure is applied
        :param edges: List of edges where a pressure is applied
        :param normal: Normal direction for the plane selection of edges
        :param dmin: Minimum distance from the origin along the normal direction
        :param dmax: Maximum distance from the origin along the normal direction
        :param arrowSizeCoef: Size of the drawn arrows (0->no arrows, sign->direction of drawing
        :param p_intensity: pressure intensity on edge normal
        :param binormal: Binormal of the 2D plane
        :param showForces: draw arrows of edge pressures
        """
        params = dict(
            edgePressureMap=edgePressureMap,
            pressure=pressure,
            edgeIndices=edgeIndices,
            edges=edges,
            normal=normal,
            dmin=dmin,
            dmax=dmax,
            arrowSizeCoef=arrowSizeCoef,
            p_intensity=p_intensity,
            binormal=binormal,
            showForces=showForces,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "EdgePressureForceField", params

    @sofa_component
    def EllipsoidForceField(
        self,
        contacts=None,
        center=None,
        vradius=None,
        stiffness=None,
        damping=None,
        color=None,
        **kwargs
    ):
        """
        EllipsoidForceField

        :param contacts: Contacts
        :param center: ellipsoid center
        :param vradius: ellipsoid radius
        :param stiffness: force stiffness (positive to repulse outward, negative inward)
        :param damping: force damping
        :param color: ellipsoid color. (default=0,0.5,1.0,1.0)
        """
        params = dict(
            contacts=contacts,
            center=center,
            vradius=vradius,
            stiffness=stiffness,
            damping=damping,
            color=color,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "EllipsoidForceField", params

    @sofa_component
    def FixedConstraint(
        self,
        indices=None,
        fixAll=None,
        showObject=None,
        drawSize=None,
        activate_projectVelocity=None,
        **kwargs
    ):
        """
        FixedConstraint

        :param indices: Indices of the fixed points
        :param fixAll: filter all the DOF to implement a fixed object
        :param showObject: draw or not the fixed constraints
        :param drawSize: 0 -> point based rendering, >0 -> radius of spheres
        :param activate_projectVelocity: activate project velocity to set velocity
        """
        params = dict(
            indices=indices,
            fixAll=fixAll,
            showObject=showObject,
            drawSize=drawSize,
            activate_projectVelocity=activate_projectVelocity,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "FixedConstraint", params

    @sofa_component
    def FixedPlaneConstraint(
        self, direction=None, dmin=None, dmax=None, indices=None, **kwargs
    ):
        """
        FixedPlaneConstraint

        :param direction: normal direction of the plane
        :param dmin: Minimum plane distance from the origin
        :param dmax: Maximum plane distance from the origin
        :param indices: Indices of the fixed points
        """
        params = dict(direction=direction, dmin=dmin, dmax=dmax, indices=indices)
        params = {k: v for k, v in params.items() if v is not None}
        return "FixedPlaneConstraint", params

    @sofa_component
    def FixedRotationConstraint(
        self, FixedXRotation=None, FixedYRotation=None, FixedZRotation=None, **kwargs
    ):
        """
        FixedRotationConstraint

        :param FixedXRotation: Prevent Rotation around X axis
        :param FixedYRotation: Prevent Rotation around Y axis
        :param FixedZRotation: Prevent Rotation around Z axis
        """
        params = dict(
            FixedXRotation=FixedXRotation,
            FixedYRotation=FixedYRotation,
            FixedZRotation=FixedZRotation,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "FixedRotationConstraint", params

    @sofa_component
    def FixedTranslationConstraint(
        self, indices=None, fixAll=None, drawSize=None, coordinates=None, **kwargs
    ):
        """
        FixedTranslationConstraint

        :param indices: Indices of the fixed points
        :param fixAll: filter all the DOF to implement a fixed object
        :param drawSize: 0 -> point based rendering, >0 -> radius of spheres
        :param coordinates: Coordinates of the fixed points
        """
        params = dict(
            indices=indices, fixAll=fixAll, drawSize=drawSize, coordinates=coordinates
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "FixedTranslationConstraint", params

    @sofa_component
    def HermiteSplineConstraint(
        self,
        indices=None,
        BeginTime=None,
        EndTime=None,
        X0=None,
        dX0=None,
        X1=None,
        dX1=None,
        SX0=None,
        SX1=None,
        **kwargs
    ):
        """
        HermiteSplineConstraint

        :param indices: Indices of the constrained points
        :param BeginTime: Begin Time of the motion
        :param EndTime: End Time of the motion
        :param X0: first control point
        :param dX0: first control tangente
        :param X1: second control point
        :param dX1: sceond control tangente
        :param SX0: first interpolation vector
        :param SX1: second interpolation vector
        """
        params = dict(
            indices=indices,
            BeginTime=BeginTime,
            EndTime=EndTime,
            X0=X0,
            dX0=dX0,
            X1=X1,
            dX1=dX1,
            SX0=SX0,
            SX1=SX1,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "HermiteSplineConstraint", params

    @sofa_component
    def LinearForceField(
        self,
        points=None,
        force=None,
        times=None,
        forces=None,
        arrowSizeCoef=None,
        **kwargs
    ):
        """
        LinearForceField

        :param points: points where the force is applied
        :param force: applied force to all points
        :param times: key times for the interpolation
        :param forces: forces corresponding to the key times
        :param arrowSizeCoef: Size of the drawn arrows (0->no arrows, sign->direction of drawing
        """
        params = dict(
            points=points,
            force=force,
            times=times,
            forces=forces,
            arrowSizeCoef=arrowSizeCoef,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "LinearForceField", params

    @sofa_component
    def LinearMovementConstraint(
        self,
        indices=None,
        keyTimes=None,
        movements=None,
        relativeMovements=None,
        showMovement=None,
        **kwargs
    ):
        """
        LinearMovementConstraint

        :param indices: Indices of the constrained points
        :param keyTimes: key times for the movements
        :param movements: movements corresponding to the key times
        :param relativeMovements: If true, movements are relative to first position, absolute otherwise
        :param showMovement: Visualization of the movement to be applied to constrained dofs.
        """
        params = dict(
            indices=indices,
            keyTimes=keyTimes,
            movements=movements,
            relativeMovements=relativeMovements,
            showMovement=showMovement,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "LinearMovementConstraint", params

    @sofa_component
    def LinearVelocityConstraint(
        self, indices=None, keyTimes=None, velocities=None, coordinates=None, **kwargs
    ):
        """
        LinearVelocityConstraint

        :param indices: Indices of the constrained points
        :param keyTimes: key times for the movements
        :param velocities: velocities corresponding to the key times
        :param coordinates: coordinates on which to apply velocities
        """
        params = dict(
            indices=indices,
            keyTimes=keyTimes,
            velocities=velocities,
            coordinates=coordinates,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "LinearVelocityConstraint", params

    @sofa_component
    def OscillatingTorsionPressureForceField(
        self,
        trianglePressureMap=None,
        moment=None,
        triangleList=None,
        axis=None,
        center=None,
        penalty=None,
        frequency=None,
        dmin=None,
        dmax=None,
        showForces=None,
        **kwargs
    ):
        """
        OscillatingTorsionPressureForceField

        :param trianglePressureMap: map between edge indices and their pressure
        :param moment: Moment force applied on the entire surface
        :param triangleList: Indices of triangles separated with commas where a pressure is applied
        :param axis: Axis of rotation and normal direction for the plane selection of triangles
        :param center: Center of rotation
        :param penalty: Strength of the penalty force
        :param frequency: frequency of oscillation
        :param dmin: Minimum distance from the origin along the normal direction
        :param dmax: Maximum distance from the origin along the normal direction
        :param showForces: draw triangles which have a given pressure
        """
        params = dict(
            trianglePressureMap=trianglePressureMap,
            moment=moment,
            triangleList=triangleList,
            axis=axis,
            center=center,
            penalty=penalty,
            frequency=frequency,
            dmin=dmin,
            dmax=dmax,
            showForces=showForces,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "OscillatingTorsionPressureForceField", params

    @sofa_component
    def OscillatorConstraint(self, oscillators=None, **kwargs):
        """
        OscillatorConstraint

        :param oscillators: Define a sequence of oscillating particules: \n[index, Mean(x,y,z), amplitude(x,y,z), pulsation, phase]
        """
        params = dict(oscillators=oscillators)
        params = {k: v for k, v in params.items() if v is not None}
        return "OscillatorConstraint", params

    @sofa_component
    def ParabolicConstraint(
        self,
        indices=None,
        P1=None,
        P2=None,
        P3=None,
        BeginTime=None,
        EndTime=None,
        **kwargs
    ):
        """
        ParabolicConstraint

        :param indices: Indices of the constrained points
        :param P1: first point of the parabol
        :param P2: second point of the parabol
        :param P3: third point of the parabol
        :param BeginTime: Begin Time of the motion
        :param EndTime: End Time of the motion
        """
        params = dict(
            indices=indices, P1=P1, P2=P2, P3=P3, BeginTime=BeginTime, EndTime=EndTime
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ParabolicConstraint", params

    @sofa_component
    def PartialFixedConstraint(self, fixedDirections=None, **kwargs):
        """
        PartialFixedConstraint

        :param fixedDirections: for each direction, 1 if fixed, 0 if free
        """
        params = dict(fixedDirections=fixedDirections)
        params = {k: v for k, v in params.items() if v is not None}
        return "PartialFixedConstraint", params

    @sofa_component
    def PartialLinearMovementConstraint(
        self,
        indices=None,
        keyTimes=None,
        movements=None,
        showMovement=None,
        linearMovementBetweenNodesInIndices=None,
        mainIndice=None,
        minDepIndice=None,
        maxDepIndice=None,
        imposedDisplacmentOnMacroNodes=None,
        X0=None,
        Y0=None,
        Z0=None,
        movedDirections=None,
        **kwargs
    ):
        """
        PartialLinearMovementConstraint

        :param indices: Indices of the constrained points
        :param keyTimes: key times for the movements
        :param movements: movements corresponding to the key times
        :param showMovement: Visualization of the movement to be applied to constrained dofs.
        :param linearMovementBetweenNodesInIndices: Take into account the linear movement between the constrained points
        :param mainIndice: The main indice node in the list of constrained nodes, it defines how to apply the linear movement between this constrained nodes
        :param minDepIndice: The indice node in the list of constrained nodes, which is imposed the minimum displacment
        :param maxDepIndice: The indice node in the list of constrained nodes, which is imposed the maximum displacment
        :param imposedDisplacmentOnMacroNodes: The imposed displacment on macro nodes
        :param X0: Size of specimen in X-direction
        :param Y0: Size of specimen in Y-direction
        :param Z0: Size of specimen in Z-direction
        :param movedDirections: for each direction, 1 if moved, 0 if free
        """
        params = dict(
            indices=indices,
            keyTimes=keyTimes,
            movements=movements,
            showMovement=showMovement,
            linearMovementBetweenNodesInIndices=linearMovementBetweenNodesInIndices,
            mainIndice=mainIndice,
            minDepIndice=minDepIndice,
            maxDepIndice=maxDepIndice,
            imposedDisplacmentOnMacroNodes=imposedDisplacmentOnMacroNodes,
            X0=X0,
            Y0=Y0,
            Z0=Z0,
            movedDirections=movedDirections,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PartialLinearMovementConstraint", params

    @sofa_component
    def PatchTestMovementConstraint(
        self,
        meshIndices=None,
        indices=None,
        beginConstraintTime=None,
        endConstraintTime=None,
        constrainedPoints=None,
        cornerMovements=None,
        cornerPoints=None,
        drawConstrainedPoints=None,
        **kwargs
    ):
        """
        PatchTestMovementConstraint

        :param meshIndices: Indices of the mesh
        :param indices: Indices of the constrained points
        :param beginConstraintTime: Begin time of the bilinear constraint
        :param endConstraintTime: End time of the bilinear constraint
        :param constrainedPoints: Coordinates of the constrained points
        :param cornerMovements: movements of the corners of the grid
        :param cornerPoints: corner points for computing constraint
        :param drawConstrainedPoints: draw constrained points
        """
        params = dict(
            meshIndices=meshIndices,
            indices=indices,
            beginConstraintTime=beginConstraintTime,
            endConstraintTime=endConstraintTime,
            constrainedPoints=constrainedPoints,
            cornerMovements=cornerMovements,
            cornerPoints=cornerPoints,
            drawConstrainedPoints=drawConstrainedPoints,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PatchTestMovementConstraint", params

    @sofa_component
    def PlaneForceField(
        self,
        normal=None,
        d=None,
        stiffness=None,
        damping=None,
        maxForce=None,
        bilateral=None,
        localRange=None,
        showPlane=None,
        planeColor=None,
        showPlaneSize=None,
        **kwargs
    ):
        """
        PlaneForceField

        :param normal: plane normal. (default=[0,1,0])
        :param d: plane d coef. (default=0)
        :param stiffness: force stiffness. (default=500)
        :param damping: force damping. (default=5)
        :param maxForce: if non-null , the max force that can be applied to the object. (default=0)
        :param bilateral: if true the plane force field is applied on both sides. (default=false)
        :param localRange: optional range of local DOF indices. Any computation involving indices outside of this range are discarded (useful for parallelization using mesh partitionning)
        :param showPlane: enable/disable drawing of plane. (default=false)
        :param planeColor: plane color. (default=[0.0,0.5,0.2,1.0])
        :param showPlaneSize: plane display size if draw is enabled. (default=10)
        """
        params = dict(
            normal=normal,
            d=d,
            stiffness=stiffness,
            damping=damping,
            maxForce=maxForce,
            bilateral=bilateral,
            localRange=localRange,
            showPlane=showPlane,
            planeColor=planeColor,
            showPlaneSize=showPlaneSize,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PlaneForceField", params

    @sofa_component
    def PointConstraint(self, indices=None, drawSize=None, **kwargs):
        """
        PointConstraint

        :param indices: Indices of the fixed points
        :param drawSize: 0 -> point based rendering, >0 -> radius of spheres
        """
        params = dict(indices=indices, drawSize=drawSize)
        params = {k: v for k, v in params.items() if v is not None}
        return "PointConstraint", params

    @sofa_component
    def PositionBasedDynamicsConstraint(
        self, stiffness=None, position=None, velocity=None, old_position=None, **kwargs
    ):
        """
        PositionBasedDynamicsConstraint

        :param stiffness: Blending between current pos and target pos.
        :param position: Target positions.
        :param velocity: Velocities.
        :param old_position: Old positions.
        """
        params = dict(
            stiffness=stiffness,
            position=position,
            velocity=velocity,
            old_position=old_position,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PositionBasedDynamicsConstraint", params

    @sofa_component
    def QuadPressureForceField(
        self,
        pressure=None,
        quadList=None,
        normal=None,
        dmin=None,
        dmax=None,
        showForces=None,
        quadPressureMap=None,
        **kwargs
    ):
        """
        QuadPressureForceField

        :param pressure: Pressure force per unit area
        :param quadList: Indices of quads separated with commas where a pressure is applied
        :param normal: Normal direction for the plane selection of quads
        :param dmin: Minimum distance from the origin along the normal direction
        :param dmax: Maximum distance from the origin along the normal direction
        :param showForces: draw quads which have a given pressure
        :param quadPressureMap: map between edge indices and their pressure
        """
        params = dict(
            pressure=pressure,
            quadList=quadList,
            normal=normal,
            dmin=dmin,
            dmax=dmax,
            showForces=showForces,
            quadPressureMap=quadPressureMap,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "QuadPressureForceField", params

    @sofa_component
    def SkeletalMotionConstraint(
        self, joints=None, bones=None, animationSpeed=None, active=None, **kwargs
    ):
        """
        SkeletalMotionConstraint

        :param joints: skeleton joints
        :param bones: skeleton bones
        :param animationSpeed: animation speed
        :param active: is the constraint active?
        """
        params = dict(
            joints=joints, bones=bones, animationSpeed=animationSpeed, active=active
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SkeletalMotionConstraint", params

    @sofa_component
    def SphereForceField(
        self,
        contacts=None,
        center=None,
        radius=None,
        stiffness=None,
        damping=None,
        color=None,
        localRange=None,
        bilateral=None,
        **kwargs
    ):
        """
        SphereForceField

        :param contacts: Contacts
        :param center: sphere center
        :param radius: sphere radius
        :param stiffness: force stiffness
        :param damping: force damping
        :param color: sphere color. (default=[0,0,1,1])
        :param localRange: optional range of local DOF indices. Any computation involving only indices outside of this range are discarded (useful for parallelization using mesh partitionning)
        :param bilateral: if true the sphere force field is applied on both sides
        """
        params = dict(
            contacts=contacts,
            center=center,
            radius=radius,
            stiffness=stiffness,
            damping=damping,
            color=color,
            localRange=localRange,
            bilateral=bilateral,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SphereForceField", params

    @sofa_component
    def SurfacePressureForceField(
        self,
        pressure=None,
        min=None,
        max=None,
        triangleIndices=None,
        quadIndices=None,
        pulseMode=None,
        pressureLowerBound=None,
        pressureSpeed=None,
        volumeConservationMode=None,
        useTangentStiffness=None,
        defaultVolume=None,
        mainDirection=None,
        drawForceScale=None,
        **kwargs
    ):
        """
        SurfacePressureForceField

        :param pressure: Pressure force per unit area
        :param min: Lower bond of the selection box
        :param max: Upper bond of the selection box
        :param triangleIndices: Indices of affected triangles
        :param quadIndices: Indices of affected quads
        :param pulseMode: Cyclic pressure application
        :param pressureLowerBound: Pressure lower bound force per unit area (active in pulse mode)
        :param pressureSpeed: Continuous pressure application in Pascal per second. Only active in pulse mode
        :param volumeConservationMode: Pressure variation follow the inverse of the volume variation
        :param useTangentStiffness: Whether (non-symmetric) stiffness matrix should be used
        :param defaultVolume: Default Volume
        :param mainDirection: Main direction for pressure application
        :param drawForceScale: DEBUG: scale used to render force vectors
        """
        params = dict(
            pressure=pressure,
            min=min,
            max=max,
            triangleIndices=triangleIndices,
            quadIndices=quadIndices,
            pulseMode=pulseMode,
            pressureLowerBound=pressureLowerBound,
            pressureSpeed=pressureSpeed,
            volumeConservationMode=volumeConservationMode,
            useTangentStiffness=useTangentStiffness,
            defaultVolume=defaultVolume,
            mainDirection=mainDirection,
            drawForceScale=drawForceScale,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SurfacePressureForceField", params

    @sofa_component
    def TaitSurfacePressureForceField(
        self,
        p0=None,
        B=None,
        gamma=None,
        injectedVolume=None,
        maxInjectionRate=None,
        initialVolume=None,
        currentInjectedVolume=None,
        v0=None,
        currentVolume=None,
        currentPressure=None,
        currentStiffness=None,
        pressureTriangles=None,
        initialSurfaceArea=None,
        currentSurfaceArea=None,
        drawForceScale=None,
        drawForceColor=None,
        volumeAfterTC=None,
        surfaceAreaAfterTC=None,
        **kwargs
    ):
        """
        TaitSurfacePressureForceField

        :param p0: IN: Rest pressure when V = V0
        :param B: IN: Bulk modulus (resistance to uniform compression)
        :param gamma: IN: Bulk modulus (resistance to uniform compression)
        :param injectedVolume: IN: Injected (or extracted) volume since the start of the simulation
        :param maxInjectionRate: IN: Maximum injection rate (volume per second)
        :param initialVolume: OUT: Initial volume, as computed from the surface rest position
        :param currentInjectedVolume: OUT: Current injected (or extracted) volume (taking into account maxInjectionRate)
        :param v0: OUT: Rest volume (as computed from initialVolume + injectedVolume)
        :param currentVolume: OUT: Current volume, as computed from the last surface position
        :param currentPressure: OUT: Current pressure, as computed from the last surface position
        :param currentStiffness: OUT: dP/dV at current volume and pressure
        :param pressureTriangles: OUT: list of triangles where a pressure is applied (mesh triangles + tesselated quads)
        :param initialSurfaceArea: OUT: Initial surface area, as computed from the surface rest position
        :param currentSurfaceArea: OUT: Current surface area, as computed from the last surface position
        :param drawForceScale: DEBUG: scale used to render force vectors
        :param drawForceColor: DEBUG: color used to render force vectors
        :param volumeAfterTC: OUT: Volume after a topology change
        :param surfaceAreaAfterTC: OUT: Surface area after a topology change
        """
        params = dict(
            p0=p0,
            B=B,
            gamma=gamma,
            injectedVolume=injectedVolume,
            maxInjectionRate=maxInjectionRate,
            initialVolume=initialVolume,
            currentInjectedVolume=currentInjectedVolume,
            v0=v0,
            currentVolume=currentVolume,
            currentPressure=currentPressure,
            currentStiffness=currentStiffness,
            pressureTriangles=pressureTriangles,
            initialSurfaceArea=initialSurfaceArea,
            currentSurfaceArea=currentSurfaceArea,
            drawForceScale=drawForceScale,
            drawForceColor=drawForceColor,
            volumeAfterTC=volumeAfterTC,
            surfaceAreaAfterTC=surfaceAreaAfterTC,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TaitSurfacePressureForceField", params

    @sofa_component
    def TorsionForceField(
        self, indices=None, torque=None, axis=None, origin=None, **kwargs
    ):
        """
        TorsionForceField

        :param indices: indices of the selected points
        :param torque: torque to apply
        :param axis: direction of the axis (will be normalized)
        :param origin: origin of the axis
        """
        params = dict(indices=indices, torque=torque, axis=axis, origin=origin)
        params = {k: v for k, v in params.items() if v is not None}
        return "TorsionForceField", params

    @sofa_component
    def TrianglePressureForceField(
        self,
        pressure=None,
        cauchyStress=None,
        triangleList=None,
        normal=None,
        dmin=None,
        dmax=None,
        showForces=None,
        useConstantForce=None,
        trianglePressureMap=None,
        **kwargs
    ):
        """
        TrianglePressureForceField

        :param pressure: Pressure force per unit area
        :param cauchyStress: Cauchy Stress applied on the normal of each triangle
        :param triangleList: Indices of triangles separated with commas where a pressure is applied
        :param normal: Normal direction for the plane selection of triangles
        :param dmin: Minimum distance from the origin along the normal direction
        :param dmax: Maximum distance from the origin along the normal direction
        :param showForces: draw triangles which have a given pressure
        :param useConstantForce: applied force is computed as the the pressure vector times the area at rest
        :param trianglePressureMap: map between edge indices and their pressure
        """
        params = dict(
            pressure=pressure,
            cauchyStress=cauchyStress,
            triangleList=triangleList,
            normal=normal,
            dmin=dmin,
            dmax=dmax,
            showForces=showForces,
            useConstantForce=useConstantForce,
            trianglePressureMap=trianglePressureMap,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TrianglePressureForceField", params

    @sofa_component
    def UniformVelocityDampingForceField(
        self, dampingCoefficient=None, implicit=None, **kwargs
    ):
        """
        UniformVelocityDampingForceField

        :param dampingCoefficient: velocity damping coefficient
        :param implicit: should it generate damping matrix df/dv? (explicit otherwise, i.e. only generating a force)
        """
        params = dict(dampingCoefficient=dampingCoefficient, implicit=implicit)
        params = {k: v for k, v in params.items() if v is not None}
        return "UniformVelocityDampingForceField", params

    @sofa_component
    def ProjectToLineConstraint(
        self, indices=None, drawSize=None, origin=None, direction=None, **kwargs
    ):
        """
        ProjectToLineConstraint

        :param indices: Indices of the fixed points
        :param drawSize: 0 -> point based rendering, >0 -> radius of spheres
        :param origin: A point in the line
        :param direction: Direction of the line
        """
        params = dict(
            indices=indices, drawSize=drawSize, origin=origin, direction=direction
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ProjectToLineConstraint", params

    @sofa_component
    def ProjectToPlaneConstraint(
        self, indices=None, origin=None, normal=None, drawSize=None, **kwargs
    ):
        """
        ProjectToPlaneConstraint

        :param indices: Indices of the fixed points
        :param origin: A point in the plane
        :param normal: Normal vector to the plane
        :param drawSize: 0 -> point based rendering, >0 -> radius of spheres
        """
        params = dict(indices=indices, origin=origin, normal=normal, drawSize=drawSize)
        params = {k: v for k, v in params.items() if v is not None}
        return "ProjectToPlaneConstraint", params

    @sofa_component
    def ProjectToPointConstraint(
        self, indices=None, point=None, fixAll=None, drawSize=None, **kwargs
    ):
        """
        ProjectToPointConstraint

        :param indices: Indices of the points to project
        :param point: Target of the projection
        :param fixAll: filter all the DOF to implement a fixed object
        :param drawSize: 0 -> point based rendering, >0 -> radius of spheres
        """
        params = dict(indices=indices, point=point, fixAll=fixAll, drawSize=drawSize)
        params = {k: v for k, v in params.items() if v is not None}
        return "ProjectToPointConstraint", params

    @sofa_component
    def ProjectDirectionConstraint(
        self, indices=None, drawSize=None, direction=None, **kwargs
    ):
        """
        ProjectDirectionConstraint

        :param indices: Indices of the fixed points
        :param drawSize: 0 -> point based rendering, >0 -> radius of spheres
        :param direction: Direction of the line
        """
        params = dict(indices=indices, drawSize=drawSize, direction=direction)
        params = {k: v for k, v in params.items() if v is not None}
        return "ProjectDirectionConstraint", params

    @sofa_component
    def BarycentricMappingRigid(self, map=None, mapOrient=None, **kwargs):
        """
        BarycentricMappingRigid

        :param map: mapper data
        :param mapOrient: mapper data for mapped frames
        """
        params = dict(map=map, mapOrient=mapOrient)
        params = {k: v for k, v in params.items() if v is not None}
        return "BarycentricMappingRigid", params

    @sofa_component
    def BeamLinearMapping(self, index=None, localCoord=None, **kwargs):
        """
        BeamLinearMapping

        :param index: input DOF index
        :param localCoord: true if initial coordinates are in the beam local coordinate system (i.e. a point at (10,0,0) is on the DOF number 10, whereas if this is false it is at whatever position on the beam where the distance from the initial DOF is 10)
        """
        params = dict(index=index, localCoord=localCoord)
        params = {k: v for k, v in params.items() if v is not None}
        return "BeamLinearMapping", params

    @sofa_component
    def CenterOfMassMapping(self, **kwargs):
        """
        CenterOfMassMapping
        """
        params = dict()
        return "CenterOfMassMapping", params

    @sofa_component
    def CenterOfMassMulti2Mapping(self, **kwargs):
        """
        CenterOfMassMulti2Mapping
        """
        params = dict()
        return "CenterOfMassMulti2Mapping", params

    @sofa_component
    def CenterOfMassMultiMapping(self, **kwargs):
        """
        CenterOfMassMultiMapping
        """
        params = dict()
        return "CenterOfMassMultiMapping", params

    @sofa_component
    def DeformableOnRigidFrameMapping(
        self,
        index=None,
        indexFromEnd=None,
        repartition=None,
        globalToLocalCoords=None,
        rootAngularForceScaleFactor=None,
        rootLinearForceScaleFactor=None,
        **kwargs
    ):
        """
        DeformableOnRigidFrameMapping

        :param index: input DOF index
        :param indexFromEnd: input DOF index starts from the end of input DOFs vector
        :param repartition: number of dest dofs per entry dof
        :param globalToLocalCoords: are the output DOFs initially expressed in global coordinates
        :param rootAngularForceScaleFactor: Scale factor applied on the angular force accumulated on the rigid model
        :param rootLinearForceScaleFactor: Scale factor applied on the linear force accumulated on the rigid model
        """
        params = dict(
            index=index,
            indexFromEnd=indexFromEnd,
            repartition=repartition,
            globalToLocalCoords=globalToLocalCoords,
            rootAngularForceScaleFactor=rootAngularForceScaleFactor,
            rootLinearForceScaleFactor=rootLinearForceScaleFactor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "DeformableOnRigidFrameMapping", params

    @sofa_component
    def DistanceFromTargetMapping(
        self,
        indices=None,
        targetPositions=None,
        restLengths=None,
        geometricStiffness=None,
        showObjectScale=None,
        showColor=None,
        **kwargs
    ):
        """
        DistanceFromTargetMapping

        :param indices: Indices of the parent points
        :param targetPositions: Positions to compute the distances from
        :param restLengths: Rest lengths of the connections.
        :param geometricStiffness: 0 -> no GS, 1 -> exact GS, 2 -> stabilized GS (default)
        :param showObjectScale: Scale for object display
        :param showColor: Color for object display. (default=[1.0,1.0,0.0,1.0])
        """
        params = dict(
            indices=indices,
            targetPositions=targetPositions,
            restLengths=restLengths,
            geometricStiffness=geometricStiffness,
            showObjectScale=showObjectScale,
            showColor=showColor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "DistanceFromTargetMapping", params

    @sofa_component
    def DistanceMapping(
        self,
        computeDistance=None,
        restLengths=None,
        showObjectScale=None,
        showColor=None,
        geometricStiffness=None,
        indexPairs=None,
        **kwargs
    ):
        """
        DistanceMapping

        :param computeDistance: if 'computeDistance = true', then rest length of each element equal 0, otherwise rest length is the initial lenght of each of them
        :param restLengths: Rest lengths of the connections
        :param showObjectScale: Scale for object display
        :param showColor: Color for object display. (default=[1.0,1.0,0.0,1.0])
        :param geometricStiffness: 0 -> no GS, 1 -> exact GS, 2 -> stabilized GS (default)
        :param indexPairs: list of couples (parent index + index in the parent)
        """
        params = dict(
            computeDistance=computeDistance,
            restLengths=restLengths,
            showObjectScale=showObjectScale,
            showColor=showColor,
            geometricStiffness=geometricStiffness,
            indexPairs=indexPairs,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "DistanceMapping", params

    @sofa_component
    def IdentityMultiMapping(self, **kwargs):
        """
        IdentityMultiMapping
        """
        params = dict()
        return "IdentityMultiMapping", params

    @sofa_component
    def SquareDistanceMapping(
        self,
        computeDistance=None,
        restLengths=None,
        showObjectScale=None,
        showColor=None,
        geometricStiffness=None,
        **kwargs
    ):
        """
        SquareDistanceMapping

        :param computeDistance: if no restLengths are given and if 'computeDistance = true', then rest length of each element equal 0, otherwise rest length is the initial lenght of each of them
        :param restLengths: Rest lengths of the connections
        :param showObjectScale: Scale for object display
        :param showColor: Color for object display. (default=[1.0,1.0,0.0,1.0])
        :param geometricStiffness: 0 -> no GS, 1 -> exact GS, 2 -> stabilized GS (default)
        """
        params = dict(
            computeDistance=computeDistance,
            restLengths=restLengths,
            showObjectScale=showObjectScale,
            showColor=showColor,
            geometricStiffness=geometricStiffness,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SquareDistanceMapping", params

    @sofa_component
    def SquareMapping(self, geometricStiffness=None, **kwargs):
        """
        SquareMapping

        :param geometricStiffness: 0 -> no GS, 1 -> exact GS (default)
        """
        params = dict(geometricStiffness=geometricStiffness)
        params = {k: v for k, v in params.items() if v is not None}
        return "SquareMapping", params

    @sofa_component
    def SubsetMultiMapping(self, indexPairs=None, **kwargs):
        """
        SubsetMultiMapping

        :param indexPairs: list of couples (parent index + index in the parent)
        """
        params = dict(indexPairs=indexPairs)
        params = {k: v for k, v in params.items() if v is not None}
        return "SubsetMultiMapping", params

    @sofa_component
    def TubularMapping(
        self, nbPointsOnEachCircle=None, radius=None, peak=None, **kwargs
    ):
        """
        TubularMapping

        :param nbPointsOnEachCircle: Discretization of created circles
        :param radius: Radius of created circles
        :param peak: =0 no peak, =1 peak on the first segment =2 peak on the two first segment, =-1 peak on the last segment
        """
        params = dict(
            nbPointsOnEachCircle=nbPointsOnEachCircle, radius=radius, peak=peak
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TubularMapping", params

    @sofa_component
    def VoidMapping(self, **kwargs):
        """
        VoidMapping
        """
        params = dict()
        return "VoidMapping", params

    @sofa_component
    def ClipPlane(self, position=None, normal=None, id=None, active=None, **kwargs):
        """
        ClipPlane

        :param position: Point crossed by the clipping plane
        :param normal: Normal of the clipping plane, pointing toward the clipped region
        :param id: Clipping plane OpenGL ID
        :param active: Control whether the clipping plane should be applied or not
        """
        params = dict(position=position, normal=normal, id=id, active=active)
        params = {k: v for k, v in params.items() if v is not None}
        return "ClipPlane", params

    @sofa_component
    def OglColorMap(
        self,
        paletteSize=None,
        colorScheme=None,
        showLegend=None,
        legendOffset=None,
        legendTitle=None,
        min=None,
        max=None,
        legendRangeScale=None,
        **kwargs
    ):
        """
        OglColorMap

        :param paletteSize: How many colors to use
        :param colorScheme: Color scheme to use
        :param showLegend: Activate rendering of color scale legend on the side
        :param legendOffset: Draw the legend on screen with an x,y offset
        :param legendTitle: Add a title to the legend
        :param min: min value for drawing the legend without the need to actually use the range with getEvaluator method wich sets the min
        :param max: max value for drawing the legend without the need to actually use the range with getEvaluator method wich sets the max
        :param legendRangeScale: to change the unit of the min/max value of the legend
        """
        params = dict(
            paletteSize=paletteSize,
            colorScheme=colorScheme,
            showLegend=showLegend,
            legendOffset=legendOffset,
            legendTitle=legendTitle,
            min=min,
            max=max,
            legendRangeScale=legendRangeScale,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "OglColorMap", params

    @sofa_component
    def CompositingVisualLoop(self, vertFilename=None, fragFilename=None, **kwargs):
        """
        CompositingVisualLoop

        :param vertFilename: Set the vertex shader filename to load
        :param fragFilename: Set the fragment shader filename to load
        """
        params = dict(vertFilename=vertFilename, fragFilename=fragFilename)
        params = {k: v for k, v in params.items() if v is not None}
        return "CompositingVisualLoop", params

    @sofa_component
    def DataDisplay(
        self,
        maximalRange=None,
        pointData=None,
        triangleData=None,
        quadData=None,
        pointTriangleData=None,
        pointQuadData=None,
        colorNaN=None,
        userRange=None,
        currentMin=None,
        currentMax=None,
        shininess=None,
        **kwargs
    ):
        """
        DataDisplay

        :param maximalRange: Keep the maximal range through all timesteps
        :param pointData: Data associated with nodes
        :param triangleData: Data associated with triangles
        :param quadData: Data associated with quads
        :param pointTriangleData: Data associated with nodes per triangle
        :param pointQuadData: Data associated with nodes per quad
        :param colorNaN: Color used for NaN values.(default=[0.0,0.0,0.0,1.0])
        :param userRange: Clamp to this values (if max>min)
        :param currentMin: Current min range
        :param currentMax: Current max range
        :param shininess: Shininess for rendering point-based data [0,128].  <0 means no specularity
        """
        params = dict(
            maximalRange=maximalRange,
            pointData=pointData,
            triangleData=triangleData,
            quadData=quadData,
            pointTriangleData=pointTriangleData,
            pointQuadData=pointQuadData,
            colorNaN=colorNaN,
            userRange=userRange,
            currentMin=currentMin,
            currentMax=currentMax,
            shininess=shininess,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "DataDisplay", params

    @sofa_component
    def OglLabel(
        self,
        prefix=None,
        label=None,
        suffix=None,
        x=None,
        y=None,
        fontsize=None,
        color=None,
        selectContrastingColor=None,
        updateLabelEveryNbSteps=None,
        visible=None,
        **kwargs
    ):
        """
        OglLabel

        :param prefix: The prefix of the text to display
        :param label: The text to display
        :param suffix: The suffix of the text to display
        :param x: The x position of the text on the screen
        :param y: The y position of the text on the screen
        :param fontsize: The size of the font used to display the text on the screen
        :param color: The color of the text to display. (default='gray')
        :param selectContrastingColor: Overide the color value but one that contrast with the background color
        :param updateLabelEveryNbSteps: Update the display of the label every nb of time steps
        :param visible: Is label displayed
        """
        params = dict(
            prefix=prefix,
            label=label,
            suffix=suffix,
            x=x,
            y=y,
            fontsize=fontsize,
            color=color,
            selectContrastingColor=selectContrastingColor,
            updateLabelEveryNbSteps=updateLabelEveryNbSteps,
            visible=visible,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "OglLabel", params

    @sofa_component
    def OglModel(
        self,
        blendTranslucency=None,
        premultipliedAlpha=None,
        writeZTransparent=None,
        alphaBlend=None,
        depthTest=None,
        cullFace=None,
        lineWidth=None,
        pointSize=None,
        lineSmooth=None,
        pointSmooth=None,
        isEnabled=None,
        primitiveType=None,
        blendEquation=None,
        sfactor=None,
        dfactor=None,
        **kwargs
    ):
        """
        OglModel

        :param blendTranslucency: Blend transparent parts
        :param premultipliedAlpha: is alpha premultiplied ?
        :param writeZTransparent: Write into Z Buffer for Transparent Object
        :param alphaBlend: Enable alpha blending
        :param depthTest: Enable depth testing
        :param cullFace: Face culling (0 = no culling, 1 = cull back faces, 2 = cull front faces)
        :param lineWidth: Line width (set if != 1, only for lines rendering)
        :param pointSize: Point size (set if != 1, only for points rendering)
        :param lineSmooth: Enable smooth line rendering
        :param pointSmooth: Enable smooth point rendering
        :param isEnabled: Activate/deactive the component.
        :param primitiveType: Select types of primitives to send (necessary for some shader types such as geometry or tesselation)
        :param blendEquation: if alpha blending is enabled this specifies how source and destination colors are combined
        :param sfactor: if alpha blending is enabled this specifies how the red, green, blue, and alpha source blending factors are computed
        :param dfactor: if alpha blending is enabled this specifies how the red, green, blue, and alpha destination blending factors are computed
        """
        params = dict(
            blendTranslucency=blendTranslucency,
            premultipliedAlpha=premultipliedAlpha,
            writeZTransparent=writeZTransparent,
            alphaBlend=alphaBlend,
            depthTest=depthTest,
            cullFace=cullFace,
            lineWidth=lineWidth,
            pointSize=pointSize,
            lineSmooth=lineSmooth,
            pointSmooth=pointSmooth,
            isEnabled=isEnabled,
            primitiveType=primitiveType,
            blendEquation=blendEquation,
            sfactor=sfactor,
            dfactor=dfactor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "OglModel", params

    @sofa_component
    def PointSplatModel(
        self,
        radius=None,
        textureSize=None,
        alpha=None,
        color=None,
        pointData=None,
        **kwargs
    ):
        """
        PointSplatModel

        :param radius: Radius of the spheres.
        :param textureSize: Size of the billboard texture.
        :param alpha: Opacity of the billboards. 1.0 is 100% opaque.
        :param color: Billboard color.(default=[1.0,1.0,1.0,1.0])
        :param pointData: scalar field modulating point colors
        """
        params = dict(
            radius=radius,
            textureSize=textureSize,
            alpha=alpha,
            color=color,
            pointData=pointData,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PointSplatModel", params

    @sofa_component
    def MergeVisualModels(self, nb=None, **kwargs):
        """
        MergeVisualModels

        :param nb: number of input visual models to merge
        """
        params = dict(nb=nb)
        params = {k: v for k, v in params.items() if v is not None}
        return "MergeVisualModels", params

    @sofa_component
    def LightManager(
        self, shadows=None, softShadows=None, ambient=None, debugDraw=None, **kwargs
    ):
        """
        LightManager

        :param shadows: Enable Shadow in the scene. (default=0)
        :param softShadows: If Shadows enabled, Enable Variance Soft Shadow in the scene. (default=0)
        :param ambient: Ambient lights contribution (Vec4f)(default=[0.0f,0.0f,0.0f,0.0f])
        :param debugDraw: enable/disable drawing of lights shadow textures. (default=false)
        """
        params = dict(
            shadows=shadows,
            softShadows=softShadows,
            ambient=ambient,
            debugDraw=debugDraw,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "LightManager", params

    @sofa_component
    def Light(
        self,
        color=None,
        shadowTextureSize=None,
        drawSource=None,
        zNear=None,
        zFar=None,
        shadowsEnabled=None,
        softShadows=None,
        shadowFactor=None,
        VSMLightBleeding=None,
        VSMMinVariance=None,
        textureUnit=None,
        modelViewMatrix=None,
        projectionMatrix=None,
        direction=None,
        fixed=None,
        position=None,
        attenuation=None,
        cutoff=None,
        exponent=None,
        lookat=None,
        **kwargs
    ):
        """
        Light

        :param color: Set the color of the light. (default=[1.0,1.0,1.0,1.0])
        :param shadowTextureSize: [Shadowing] Set size for shadow texture
        :param drawSource: Draw Light Source
        :param zNear: [Shadowing] Light's ZNear
        :param zFar: [Shadowing] Light's ZFar
        :param shadowsEnabled: [Shadowing] Enable Shadow from this light
        :param softShadows: [Shadowing] Turn on Soft Shadow from this light
        :param shadowFactor: [Shadowing] Shadow Factor (decrease/increase darkness)
        :param VSMLightBleeding: [Shadowing] (VSM only) Light bleeding paramter
        :param VSMMinVariance: [Shadowing] (VSM only) Minimum variance parameter
        :param textureUnit: [Shadowing] Texture unit for the genereated shadow texture
        :param modelViewMatrix: [Shadowing] ModelView Matrix
        :param projectionMatrix: [Shadowing] Projection Matrix
        :param direction: Set the direction of the light
        :param fixed: Fix light position from the camera
        :param position: Set the position of the light
        :param attenuation: Set the attenuation of the light
        :param cutoff: Set the angle (cutoff) of the spot
        :param exponent: Set the exponent of the spot
        :param lookat: If true, direction specify the point at which the spotlight should be pointed to
        """
        params = dict(
            color=color,
            shadowTextureSize=shadowTextureSize,
            drawSource=drawSource,
            zNear=zNear,
            zFar=zFar,
            shadowsEnabled=shadowsEnabled,
            softShadows=softShadows,
            shadowFactor=shadowFactor,
            VSMLightBleeding=VSMLightBleeding,
            VSMMinVariance=VSMMinVariance,
            textureUnit=textureUnit,
            modelViewMatrix=modelViewMatrix,
            projectionMatrix=projectionMatrix,
            direction=direction,
            fixed=fixed,
            position=position,
            attenuation=attenuation,
            cutoff=cutoff,
            exponent=exponent,
            lookat=lookat,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "Light", params

    @sofa_component
    def OrderIndependentTransparencyManager(self, depthScale=None, **kwargs):
        """
        OrderIndependentTransparencyManager

        :param depthScale: Depth scale
        """
        params = dict(depthScale=depthScale)
        params = {k: v for k, v in params.items() if v is not None}
        return "OrderIndependentTransparencyManager", params

    @sofa_component
    def OglOITShader(self, **kwargs):
        """
        OglOITShader
        """
        params = dict()
        return "OglOITShader", params

    @sofa_component
    def OglAttribute(self, value=None, **kwargs):
        """
        OglAttribute

        :param value: internal Data
        """
        params = dict(value=value)
        params = {k: v for k, v in params.items() if v is not None}
        return "OglAttribute", params

    @sofa_component
    def OglShader(
        self,
        turnOn=None,
        passive=None,
        fileVertexShaders=None,
        fileFragmentShaders=None,
        fileGeometryShaders=None,
        fileTessellationControlShaders=None,
        fileTessellationEvaluationShaders=None,
        geometryInputType=None,
        geometryOutputType=None,
        geometryVerticesOut=None,
        tessellationOuterLevel=None,
        tessellationInnerLevel=None,
        indexActiveShader=None,
        backfaceWriting=None,
        clampVertexColor=None,
        id=None,
        indexShader=None,
        **kwargs
    ):
        """
        OglShader

        :param turnOn: Turn On the shader?
        :param passive: Will this shader be activated manually or automatically?
        :param fileVertexShaders: Set the vertex shader filename to load
        :param fileFragmentShaders: Set the fragment shader filename to load
        :param fileGeometryShaders: Set the geometry shader filename to load
        :param fileTessellationControlShaders: Set the tessellation control filename to load
        :param fileTessellationEvaluationShaders: Set the tessellation evaluation filename to load
        :param geometryInputType: Set input types for the geometry shader
        :param geometryOutputType: Set output types for the geometry shader
        :param geometryVerticesOut: Set max number of vertices in output for the geometry shader
        :param tessellationOuterLevel: For tessellation without control shader: default outer level (edge subdivisions)
        :param tessellationInnerLevel: For tessellation without control shader: default inner level (face subdivisions)
        :param indexActiveShader: Set current active shader
        :param backfaceWriting: it enables writing to gl_BackColor inside a GLSL vertex shader
        :param clampVertexColor: clamp the vertex color between 0 and 1
        :param id: Set an ID name
        :param indexShader: Set the index of the desired shader you want to apply this parameter
        """
        params = dict(
            turnOn=turnOn,
            passive=passive,
            fileVertexShaders=fileVertexShaders,
            fileFragmentShaders=fileFragmentShaders,
            fileGeometryShaders=fileGeometryShaders,
            fileTessellationControlShaders=fileTessellationControlShaders,
            fileTessellationEvaluationShaders=fileTessellationEvaluationShaders,
            geometryInputType=geometryInputType,
            geometryOutputType=geometryOutputType,
            geometryVerticesOut=geometryVerticesOut,
            tessellationOuterLevel=tessellationOuterLevel,
            tessellationInnerLevel=tessellationInnerLevel,
            indexActiveShader=indexActiveShader,
            backfaceWriting=backfaceWriting,
            clampVertexColor=clampVertexColor,
            id=id,
            indexShader=indexShader,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "OglShader", params

    @sofa_component
    def OglShaderMacro(self, value=None, **kwargs):
        """
        OglShaderMacro

        :param value: Set a value for define macro
        """
        params = dict(value=value)
        params = {k: v for k, v in params.items() if v is not None}
        return "OglShaderMacro", params

    @sofa_component
    def OglShaderVisualModel(self, **kwargs):
        """
        OglShaderVisualModel
        """
        params = dict()
        return "OglShaderVisualModel", params

    @sofa_component
    def OglShadowShader(self, **kwargs):
        """
        OglShadowShader
        """
        params = dict()
        return "OglShadowShader", params

    @sofa_component
    def OglTexture(
        self,
        filename=None,
        textureUnit=None,
        enabled=None,
        repeat=None,
        linearInterpolation=None,
        generateMipmaps=None,
        srgbColorspace=None,
        minLod=None,
        maxLod=None,
        proceduralTextureWidth=None,
        proceduralTextureHeight=None,
        proceduralTextureNbBits=None,
        proceduralTextureData=None,
        cubemapFilenamePosX=None,
        cubemapFilenamePosY=None,
        cubemapFilenamePosZ=None,
        cubemapFilenameNegX=None,
        cubemapFilenameNegY=None,
        cubemapFilenameNegZ=None,
        texture2DFilename=None,
        **kwargs
    ):
        """
        OglTexture

        :param filename: Texture Filename
        :param textureUnit: Set the texture unit
        :param enabled: enabled ?
        :param repeat: Repeat Texture ?
        :param linearInterpolation: Interpolate Texture ?
        :param generateMipmaps: Generate mipmaps ?
        :param srgbColorspace: SRGB colorspace ?
        :param minLod: Minimum mipmap lod ?
        :param maxLod: Maximum mipmap lod ?
        :param proceduralTextureWidth: Width of procedural Texture
        :param proceduralTextureHeight: Height of procedural Texture
        :param proceduralTextureNbBits: Nb bits per color
        :param proceduralTextureData: Data of procedural Texture
        :param cubemapFilenamePosX: Texture filename of positive-X cubemap face
        :param cubemapFilenamePosY: Texture filename of positive-Y cubemap face
        :param cubemapFilenamePosZ: Texture filename of positive-Z cubemap face
        :param cubemapFilenameNegX: Texture filename of negative-X cubemap face
        :param cubemapFilenameNegY: Texture filename of negative-Y cubemap face
        :param cubemapFilenameNegZ: Texture filename of negative-Z cubemap face
        :param texture2DFilename: Texture2D Filename
        """
        params = dict(
            filename=filename,
            textureUnit=textureUnit,
            enabled=enabled,
            repeat=repeat,
            linearInterpolation=linearInterpolation,
            generateMipmaps=generateMipmaps,
            srgbColorspace=srgbColorspace,
            minLod=minLod,
            maxLod=maxLod,
            proceduralTextureWidth=proceduralTextureWidth,
            proceduralTextureHeight=proceduralTextureHeight,
            proceduralTextureNbBits=proceduralTextureNbBits,
            proceduralTextureData=proceduralTextureData,
            cubemapFilenamePosX=cubemapFilenamePosX,
            cubemapFilenamePosY=cubemapFilenamePosY,
            cubemapFilenamePosZ=cubemapFilenamePosZ,
            cubemapFilenameNegX=cubemapFilenameNegX,
            cubemapFilenameNegY=cubemapFilenameNegY,
            cubemapFilenameNegZ=cubemapFilenameNegZ,
            texture2DFilename=texture2DFilename,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "OglTexture", params

    @sofa_component
    def OglTexturePointer(self, textureUnit=None, enabled=None, **kwargs):
        """
        OglTexturePointer

        :param textureUnit: Set the texture unit
        :param enabled: enabled ?
        """
        params = dict(textureUnit=textureUnit, enabled=enabled)
        params = {k: v for k, v in params.items() if v is not None}
        return "OglTexturePointer", params

    @sofa_component
    def OglVariable(self, value=None, transpose=None, **kwargs):
        """
        OglVariable

        :param value: Set Uniform Value
        :param transpose: Transpose the matrix (e.g. to use row-dominant matrices in OpenGL
        """
        params = dict(value=value, transpose=transpose)
        params = {k: v for k, v in params.items() if v is not None}
        return "OglVariable", params

    @sofa_component
    def OglViewport(
        self,
        screenPosition=None,
        screenSize=None,
        cameraPosition=None,
        cameraOrientation=None,
        cameraRigid=None,
        zNear=None,
        zFar=None,
        fovy=None,
        enabled=None,
        advancedRendering=None,
        useFBO=None,
        swapMainView=None,
        drawCamera=None,
        **kwargs
    ):
        """
        OglViewport

        :param screenPosition: Viewport position
        :param screenSize: Viewport size
        :param cameraPosition: Camera's position in eye's space
        :param cameraOrientation: Camera's orientation
        :param cameraRigid: Camera's rigid coord
        :param zNear: Camera's ZNear
        :param zFar: Camera's ZFar
        :param fovy: Field of View (Y axis)
        :param enabled: Enable visibility of the viewport
        :param advancedRendering: If true, viewport will be hidden if advancedRendering visual flag is not enabled
        :param useFBO: Use a FBO to render the viewport
        :param swapMainView: Swap this viewport with the main view
        :param drawCamera: Draw a frame representing the camera (see it in main viewport)
        """
        params = dict(
            screenPosition=screenPosition,
            screenSize=screenSize,
            cameraPosition=cameraPosition,
            cameraOrientation=cameraOrientation,
            cameraRigid=cameraRigid,
            zNear=zNear,
            zFar=zFar,
            fovy=fovy,
            enabled=enabled,
            advancedRendering=advancedRendering,
            useFBO=useFBO,
            swapMainView=swapMainView,
            drawCamera=drawCamera,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "OglViewport", params

    @sofa_component
    def OglCylinderModel(
        self, radius=None, color=None, edges=None, pointData=None, **kwargs
    ):
        """
        OglCylinderModel

        :param radius: Radius of the cylinder.
        :param color: Color of the cylinders.
        :param edges: List of edge indices
        :param pointData: scalar field modulating point colors
        """
        params = dict(radius=radius, color=color, edges=edges, pointData=pointData)
        params = {k: v for k, v in params.items() if v is not None}
        return "OglCylinderModel", params

    @sofa_component
    def OglGrid(
        self,
        plane=None,
        size=None,
        nbSubdiv=None,
        color=None,
        thickness=None,
        draw=None,
        **kwargs
    ):
        """
        OglGrid

        :param plane: Plane of the grid
        :param size: Size of the squared grid
        :param nbSubdiv: Number of subdivisions
        :param color: Color of the lines in the grid. default=(0.34,0.34,0.34,1.0)
        :param thickness: Thickness of the lines in the grid
        :param draw: Display the grid or not
        """
        params = dict(
            plane=plane,
            size=size,
            nbSubdiv=nbSubdiv,
            color=color,
            thickness=thickness,
            draw=draw,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "OglGrid", params

    @sofa_component
    def OglRenderingSRGB(self, **kwargs):
        """
        OglRenderingSRGB
        """
        params = dict()
        return "OglRenderingSRGB", params

    @sofa_component
    def OglLineAxis(self, axis=None, size=None, thickness=None, draw=None, **kwargs):
        """
        OglLineAxis

        :param axis: Axis to draw
        :param size: Size of the squared grid
        :param thickness: Thickness of the lines in the grid
        :param draw: Display the grid or not
        """
        params = dict(axis=axis, size=size, thickness=thickness, draw=draw)
        params = {k: v for k, v in params.items() if v is not None}
        return "OglLineAxis", params

    @sofa_component
    def OglSceneFrame(self, draw=None, style=None, alignment=None, **kwargs):
        """
        OglSceneFrame

        :param draw: Display the frame or not
        :param style: Style of the frame
        :param alignment: Alignment of the frame in the view
        """
        params = dict(draw=draw, style=style, alignment=alignment)
        params = {k: v for k, v in params.items() if v is not None}
        return "OglSceneFrame", params

    @sofa_component
    def PostProcessManager(self, zNear=None, zFar=None, **kwargs):
        """
        PostProcessManager

        :param zNear: Set zNear distance (for Depth Buffer)
        :param zFar: Set zFar distance (for Depth Buffer)
        """
        params = dict(zNear=zNear, zFar=zFar)
        params = {k: v for k, v in params.items() if v is not None}
        return "PostProcessManager", params

    @sofa_component
    def SlicedVolumetricModel(self, alpha=None, color=None, nbSlices=None, **kwargs):
        """
        SlicedVolumetricModel

        :param alpha: Opacity of the billboards. 1.0 is 100% opaque.
        :param color: Billboard color.(default=1.0,1.0,1.0,1.0)
        :param nbSlices: Number of billboards.
        """
        params = dict(alpha=alpha, color=color, nbSlices=nbSlices)
        params = {k: v for k, v in params.items() if v is not None}
        return "SlicedVolumetricModel", params

    @sofa_component
    def VisualManagerPass(
        self, factor=None, renderToScreen=None, outputName=None, **kwargs
    ):
        """
        VisualManagerPass

        :param factor: set the resolution factor for the output pass. default value:1.0
        :param renderToScreen: if true, this pass will be displayed on screen (only one renderPass in the scene must be defined as renderToScreen)
        :param outputName: name the output texture
        """
        params = dict(
            factor=factor, renderToScreen=renderToScreen, outputName=outputName
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "VisualManagerPass", params

    @sofa_component
    def VisualManagerSecondaryPass(
        self, input_tags=None, output_tags=None, fragFilename=None, **kwargs
    ):
        """
        VisualManagerSecondaryPass

        :param input_tags: list of input passes used as source textures
        :param output_tags: output reference tag (use it if the resulting fbo is used as a source for another secondary pass)
        :param fragFilename: Set the fragment shader filename to load
        """
        params = dict(
            input_tags=input_tags, output_tags=output_tags, fragFilename=fragFilename
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "VisualManagerSecondaryPass", params

    @sofa_component
    def AttachConstraint(
        self,
        indices1=None,
        indices2=None,
        twoWay=None,
        freeRotations=None,
        lastFreeRotation=None,
        restRotations=None,
        lastPos=None,
        lastDir=None,
        clamp=None,
        minDistance=None,
        positionFactor=None,
        velocityFactor=None,
        responseFactor=None,
        constraintFactor=None,
        **kwargs
    ):
        """
        AttachConstraint

        :param indices1: Indices of the source points on the first model
        :param indices2: Indices of the fixed points on the second model
        :param twoWay: true if forces should be projected back from model2 to model1
        :param freeRotations: true to keep rotations free (only used for Rigid DOFs)
        :param lastFreeRotation: true to keep rotation of the last attached point free (only used for Rigid DOFs)
        :param restRotations: true to use rest rotations local offsets (only used for Rigid DOFs)
        :param lastPos: position at which the attach constraint should become inactive
        :param lastDir: direction from lastPos at which the attach coustraint should become inactive
        :param clamp: true to clamp particles at lastPos instead of freeing them.
        :param minDistance: the constraint become inactive if the distance between the points attached is bigger than minDistance.
        :param positionFactor: IN: Factor applied to projection of position
        :param velocityFactor: IN: Factor applied to projection of velocity
        :param responseFactor: IN: Factor applied to projection of force/acceleration
        :param constraintFactor: Constraint factor per pair of points constrained. 0 -> the constraint is released. 1 -> the constraint is fully constrained
        """
        params = dict(
            indices1=indices1,
            indices2=indices2,
            twoWay=twoWay,
            freeRotations=freeRotations,
            lastFreeRotation=lastFreeRotation,
            restRotations=restRotations,
            lastPos=lastPos,
            lastDir=lastDir,
            clamp=clamp,
            minDistance=minDistance,
            positionFactor=positionFactor,
            velocityFactor=velocityFactor,
            responseFactor=responseFactor,
            constraintFactor=constraintFactor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "AttachConstraint", params

    @sofa_component
    def BoxStiffSpringForceField(
        self,
        box_object1=None,
        box_object2=None,
        factorRestLength=None,
        forceOldBehavior=None,
        **kwargs
    ):
        """
        BoxStiffSpringForceField

        :param box_object1: Box for the object1 where springs will be attached
        :param box_object2: Box for the object2 where springs will be attached
        :param factorRestLength: Factor used to compute the rest length of the springs generated
        :param forceOldBehavior: Keep using the old behavior
        """
        params = dict(
            box_object1=box_object1,
            box_object2=box_object2,
            factorRestLength=factorRestLength,
            forceOldBehavior=forceOldBehavior,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "BoxStiffSpringForceField", params

    @sofa_component
    def InteractionEllipsoidForceField(
        self,
        contacts=None,
        center=None,
        vradius=None,
        stiffness=None,
        damping=None,
        color=None,
        draw=None,
        object2_dof_index=None,
        object2_forces=None,
        object2_invert=None,
        **kwargs
    ):
        """
        InteractionEllipsoidForceField

        :param contacts: Contacts
        :param center: ellipsoid center
        :param vradius: ellipsoid radius
        :param stiffness: force stiffness (positive to repulse outward, negative inward)
        :param damping: force damping
        :param color: ellipsoid color. (default=[0.0,0.5,1.0,1.0])
        :param draw: enable/disable drawing of the ellipsoid
        :param object2_dof_index: Dof index of object 2 where the forcefield is attached
        :param object2_forces: enable/disable propagation of forces to object 2
        :param object2_invert: inverse transform from object 2 (use when object 1 is in local coordinates within a frame defined by object 2)
        """
        params = dict(
            contacts=contacts,
            center=center,
            vradius=vradius,
            stiffness=stiffness,
            damping=damping,
            color=color,
            draw=draw,
            object2_dof_index=object2_dof_index,
            object2_forces=object2_forces,
            object2_invert=object2_invert,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "InteractionEllipsoidForceField", params

    @sofa_component
    def RepulsiveSpringForceField(self, **kwargs):
        """
        RepulsiveSpringForceField
        """
        params = dict()
        return "RepulsiveSpringForceField", params

    @sofa_component
    def AverageCoord(self, indices=None, vecId=None, average=None, **kwargs):
        """
        AverageCoord

        :param indices: indices of the coordinates to average
        :param vecId: index of the vector (default value corresponds to core::VecCoordId::position() )
        :param average: average of the values with the given indices in the given coordinate vector \n
        """
        params = dict(indices=indices, vecId=vecId, average=average)
        params = {k: v for k, v in params.items() if v is not None}
        return "AverageCoord", params

    @sofa_component
    def ClusteringEngine(
        self,
        useTopo=None,
        radius=None,
        fixedRadius=None,
        number=None,
        fixedPosition=None,
        position=None,
        cluster=None,
        inFile=None,
        outFile=None,
        **kwargs
    ):
        """
        ClusteringEngine

        :param useTopo: Use avalaible topology to compute neighborhood.
        :param radius: Neighborhood range.
        :param fixedRadius: Neighborhood range (for non mechanical particles).
        :param number: Number of clusters (-1 means that all input points are selected).
        :param fixedPosition: Input positions of fixed (non mechanical) particles.
        :param position: Input rest positions.
        :param cluster: Computed clusters.
        :param inFile: import precomputed clusters
        :param outFile: export clusters
        """
        params = dict(
            useTopo=useTopo,
            radius=radius,
            fixedRadius=fixedRadius,
            number=number,
            fixedPosition=fixedPosition,
            position=position,
            cluster=cluster,
            inFile=inFile,
            outFile=outFile,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ClusteringEngine", params

    @sofa_component
    def ComplementaryROI(
        self, position=None, nbSet=None, indices=None, pointsInROI=None, **kwargs
    ):
        """
        ComplementaryROI

        :param position: input positions
        :param nbSet: number of sets to complement
        :param indices: indices of the point in the ROI
        :param pointsInROI: points in the ROI
        """
        params = dict(
            position=position, nbSet=nbSet, indices=indices, pointsInROI=pointsInROI
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ComplementaryROI", params

    @sofa_component
    def DilateEngine(
        self,
        input_position=None,
        output_position=None,
        triangles=None,
        quads=None,
        normal=None,
        thickness=None,
        distance=None,
        minThickness=None,
        **kwargs
    ):
        """
        DilateEngine

        :param input_position: input array of 3d points
        :param output_position: output array of 3d points
        :param triangles: input mesh triangles
        :param quads: input mesh quads
        :param normal: point normals
        :param thickness: point thickness
        :param distance: distance to move the points (positive for dilatation, negative for erosion)
        :param minThickness: minimal thickness to enforce
        """
        params = dict(
            input_position=input_position,
            output_position=output_position,
            triangles=triangles,
            quads=quads,
            normal=normal,
            thickness=thickness,
            distance=distance,
            minThickness=minThickness,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "DilateEngine", params

    @sofa_component
    def DifferenceEngine(self, input=None, substractor=None, output=None, **kwargs):
        """
        DifferenceEngine

        :param input: input vector
        :param substractor: vector to substract to input
        :param output: output vector = input-substractor
        """
        params = dict(input=input, substractor=substractor, output=output)
        params = {k: v for k, v in params.items() if v is not None}
        return "DifferenceEngine", params

    @sofa_component
    def ExtrudeEdgesAndGenerateQuads(
        self,
        extrudeDirection=None,
        thicknessIn=None,
        thicknessOut=None,
        numberOfSections=None,
        curveVertices=None,
        curveEdges=None,
        extrudedVertices=None,
        extrudedEdges=None,
        extrudedQuads=None,
        **kwargs
    ):
        """
        ExtrudeEdgesAndGenerateQuads

        :param extrudeDirection: Direction along which to extrude the curve
        :param thicknessIn: Thickness of the extruded volume in the opposite direction of the normals
        :param thicknessOut: Thickness of the extruded volume in the direction of the normals
        :param numberOfSections: Number of sections / steps in the extrusion
        :param curveVertices: Position coordinates along the initial curve
        :param curveEdges: Indices of the edges of the curve to extrude
        :param extrudedVertices: Coordinates of the extruded vertices
        :param extrudedEdges: List of all edges generated during the extrusion
        :param extrudedQuads: List of all quads generated during the extrusion
        """
        params = dict(
            extrudeDirection=extrudeDirection,
            thicknessIn=thicknessIn,
            thicknessOut=thicknessOut,
            numberOfSections=numberOfSections,
            curveVertices=curveVertices,
            curveEdges=curveEdges,
            extrudedVertices=extrudedVertices,
            extrudedEdges=extrudedEdges,
            extrudedQuads=extrudedQuads,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ExtrudeEdgesAndGenerateQuads", params

    @sofa_component
    def ExtrudeQuadsAndGenerateHexas(
        self,
        isVisible=None,
        scale=None,
        thicknessIn=None,
        thicknessOut=None,
        numberOfSlices=None,
        surfaceVertices=None,
        surfaceQuads=None,
        extrudedVertices=None,
        extrudedSurfaceQuads=None,
        extrudedQuads=None,
        extrudedHexas=None,
        **kwargs
    ):
        """
        ExtrudeQuadsAndGenerateHexas

        :param isVisible: is Visible ?
        :param scale: Apply a scaling factor to the extruded mesh
        :param thicknessIn: Thickness of the extruded volume in the opposite direction of the normals
        :param thicknessOut: Thickness of the extruded volume in the direction of the normals
        :param numberOfSlices: Number of slices / steps in the extrusion
        :param surfaceVertices: Position coordinates of the surface
        :param surfaceQuads: Indices of the quads of the surface to extrude
        :param extrudedVertices: Coordinates of the extruded vertices
        :param extrudedSurfaceQuads: List of new surface quads generated during the extrusion
        :param extrudedQuads: List of all quads generated during the extrusion
        :param extrudedHexas: List of hexahedra generated during the extrusion
        """
        params = dict(
            isVisible=isVisible,
            scale=scale,
            thicknessIn=thicknessIn,
            thicknessOut=thicknessOut,
            numberOfSlices=numberOfSlices,
            surfaceVertices=surfaceVertices,
            surfaceQuads=surfaceQuads,
            extrudedVertices=extrudedVertices,
            extrudedSurfaceQuads=extrudedSurfaceQuads,
            extrudedQuads=extrudedQuads,
            extrudedHexas=extrudedHexas,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ExtrudeQuadsAndGenerateHexas", params

    @sofa_component
    def ExtrudeSurface(
        self,
        isVisible=None,
        heightFactor=None,
        triangles=None,
        extrusionVertices=None,
        surfaceVertices=None,
        extrusionTriangles=None,
        surfaceTriangles=None,
        **kwargs
    ):
        """
        ExtrudeSurface

        :param isVisible: is Visible ?
        :param heightFactor: Factor for the height of the extrusion (based on normal) ?
        :param triangles: List of triangle indices
        :param extrusionVertices: Position coordinates of the extrusion
        :param surfaceVertices: Position coordinates of the surface
        :param extrusionTriangles: Triangles indices of the extrusion
        :param surfaceTriangles: Indices of the triangles of the surface to extrude
        """
        params = dict(
            isVisible=isVisible,
            heightFactor=heightFactor,
            triangles=triangles,
            extrusionVertices=extrusionVertices,
            surfaceVertices=surfaceVertices,
            extrusionTriangles=extrusionTriangles,
            surfaceTriangles=surfaceTriangles,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ExtrudeSurface", params

    @sofa_component
    def GenerateCylinder(
        self,
        output_TetrahedraPosition=None,
        output_TrianglesPosition=None,
        tetrahedra=None,
        triangles=None,
        BezierTriangleWeights=None,
        isBezierTriangleRational=None,
        BezierTriangleDegree=None,
        BezierTetrahedronWeights=None,
        isBezierTetrahedronRational=None,
        BezierTetrahedronDegree=None,
        radius=None,
        height=None,
        origin=None,
        openSurface=None,
        resCircumferential=None,
        resRadial=None,
        resHeight=None,
        **kwargs
    ):
        """
        GenerateCylinder

        :param output_TetrahedraPosition: output array of 3d points of tetrahedra mesh
        :param output_TrianglesPosition: output array of 3d points of triangle mesh
        :param tetrahedra: output mesh tetrahedra
        :param triangles: output triangular mesh
        :param BezierTriangleWeights: weights of rational Bezier triangles
        :param isBezierTriangleRational: booleans indicating if each Bezier triangle is rational or integral
        :param BezierTriangleDegree: order of Bezier triangles
        :param BezierTetrahedronWeights: weights of rational Bezier tetrahedra
        :param isBezierTetrahedronRational: booleans indicating if each Bezier tetrahedron is rational or integral
        :param BezierTetrahedronDegree: order of Bezier tetrahedra
        :param radius: input cylinder radius
        :param height: input cylinder height
        :param origin: cylinder origin point
        :param openSurface: if the cylinder is open at its 2 ends
        :param resCircumferential: Resolution in the circumferential direction
        :param resRadial: Resolution in the radial direction
        :param resHeight: Resolution in the height direction
        """
        params = dict(
            output_TetrahedraPosition=output_TetrahedraPosition,
            output_TrianglesPosition=output_TrianglesPosition,
            tetrahedra=tetrahedra,
            triangles=triangles,
            BezierTriangleWeights=BezierTriangleWeights,
            isBezierTriangleRational=isBezierTriangleRational,
            BezierTriangleDegree=BezierTriangleDegree,
            BezierTetrahedronWeights=BezierTetrahedronWeights,
            isBezierTetrahedronRational=isBezierTetrahedronRational,
            BezierTetrahedronDegree=BezierTetrahedronDegree,
            radius=radius,
            height=height,
            origin=origin,
            openSurface=openSurface,
            resCircumferential=resCircumferential,
            resRadial=resRadial,
            resHeight=resHeight,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "GenerateCylinder", params

    @sofa_component
    def GenerateGrid(
        self,
        output_position=None,
        tetrahedra=None,
        quads=None,
        triangles=None,
        hexahedra=None,
        min=None,
        max=None,
        resolution=None,
        **kwargs
    ):
        """
        GenerateGrid

        :param output_position: output array of 3d points
        :param tetrahedra: output mesh tetrahedra
        :param quads: output mesh quads
        :param triangles: output mesh triangles
        :param hexahedra: output mesh hexahedra
        :param min: the 3 coordinates of the minimum corner
        :param max: the 3 coordinates of the maximum corner
        :param resolution: the number of cubes in the x,y,z directions. If resolution in the z direction is  0 then a 2D grid is generated
        """
        params = dict(
            output_position=output_position,
            tetrahedra=tetrahedra,
            quads=quads,
            triangles=triangles,
            hexahedra=hexahedra,
            min=min,
            max=max,
            resolution=resolution,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "GenerateGrid", params

    @sofa_component
    def GenerateRigidMass(
        self,
        density=None,
        position=None,
        triangles=None,
        quads=None,
        polygons=None,
        rigidMass=None,
        mass=None,
        volume=None,
        inertiaMatrix=None,
        massCenter=None,
        centerToOrigin=None,
        **kwargs
    ):
        """
        GenerateRigidMass

        :param density: input: Density of the object
        :param position: input: positions of the vertices
        :param triangles: input: triangles of the mesh
        :param quads: input: quads of the mesh
        :param polygons: input: polygons of the mesh
        :param rigidMass: output: rigid mass computed
        :param mass: output: mass of the mesh
        :param volume: output: volume of the mesh
        :param inertiaMatrix: output: the inertia matrix of the mesh
        :param massCenter: output: the gravity center of the mesh
        :param centerToOrigin: output: vector going from the mass center to the space origin
        """
        params = dict(
            density=density,
            position=position,
            triangles=triangles,
            quads=quads,
            polygons=polygons,
            rigidMass=rigidMass,
            mass=mass,
            volume=volume,
            inertiaMatrix=inertiaMatrix,
            massCenter=massCenter,
            centerToOrigin=centerToOrigin,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "GenerateRigidMass", params

    @sofa_component
    def GenerateSphere(
        self,
        output_TetrahedraPosition=None,
        tetrahedra=None,
        output_TrianglesPosition=None,
        triangles=None,
        BezierTetrahedronDegree=None,
        BezierTetrahedronWeights=None,
        isBezierTetrahedronRational=None,
        BezierTriangleDegree=None,
        BezierTriangleWeights=None,
        isBezierTriangleRational=None,
        radius=None,
        origin=None,
        tessellationDegree=None,
        platonicSolid=None,
        **kwargs
    ):
        """
        GenerateSphere

        :param output_TetrahedraPosition: output array of 3d points of tetrahedra mesh
        :param tetrahedra: output mesh tetrahedra
        :param output_TrianglesPosition: output array of 3d points of triangle mesh
        :param triangles: output triangular mesh
        :param BezierTetrahedronDegree: order of Bezier tetrahedra
        :param BezierTetrahedronWeights: weights of rational Bezier tetrahedra
        :param isBezierTetrahedronRational: booleans indicating if each Bezier tetrahedron is rational or integral
        :param BezierTriangleDegree: order of Bezier triangles
        :param BezierTriangleWeights: weights of rational Bezier triangles
        :param isBezierTriangleRational: booleans indicating if each Bezier triangle is rational or integral
        :param radius: input sphere radius
        :param origin: sphere center point
        :param tessellationDegree: Degree of tessellation of each Platonic triangulation
        :param platonicSolid: name of the Platonic triangulation used to create the spherical dome : either tetrahedron, octahedron or icosahedron
        """
        params = dict(
            output_TetrahedraPosition=output_TetrahedraPosition,
            tetrahedra=tetrahedra,
            output_TrianglesPosition=output_TrianglesPosition,
            triangles=triangles,
            BezierTetrahedronDegree=BezierTetrahedronDegree,
            BezierTetrahedronWeights=BezierTetrahedronWeights,
            isBezierTetrahedronRational=isBezierTetrahedronRational,
            BezierTriangleDegree=BezierTriangleDegree,
            BezierTriangleWeights=BezierTriangleWeights,
            isBezierTriangleRational=isBezierTriangleRational,
            radius=radius,
            origin=origin,
            tessellationDegree=tessellationDegree,
            platonicSolid=platonicSolid,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "GenerateSphere", params

    @sofa_component
    def GroupFilterYoungModulus(
        self,
        groups=None,
        primitives=None,
        elementsGroup=None,
        youngModulus=None,
        mapGroupModulus=None,
        defaultYoungModulus=None,
        groupModulus=None,
        **kwargs
    ):
        """
        GroupFilterYoungModulus

        :param groups: Groups
        :param primitives: Vector of primitives (indices)
        :param elementsGroup: Vector of groups (each element gives its group
        :param youngModulus: Vector of young modulus for each primitive
        :param mapGroupModulus: Mapping between groups and modulus
        :param defaultYoungModulus: Default value if the primitive is not in a group
        :param groupModulus: list of young modulus for each group
        """
        params = dict(
            groups=groups,
            primitives=primitives,
            elementsGroup=elementsGroup,
            youngModulus=youngModulus,
            mapGroupModulus=mapGroupModulus,
            defaultYoungModulus=defaultYoungModulus,
            groupModulus=groupModulus,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "GroupFilterYoungModulus", params

    @sofa_component
    def HausdorffDistance(
        self,
        points1=None,
        points2=None,
        d12=None,
        d21=None,
        max=None,
        update=None,
        **kwargs
    ):
        """
        HausdorffDistance

        :param points1: Points belonging to the first point cloud
        :param points2: Points belonging to the second point cloud
        :param d12: Distance from point cloud 1 to 2
        :param d21: Distance from point cloud 2 to 1
        :param max: Symmetrical Hausdorff distance
        :param update: Recompute every time step
        """
        params = dict(
            points1=points1, points2=points2, d12=d12, d21=d21, max=max, update=update
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "HausdorffDistance", params

    @sofa_component
    def IndexValueMapper(
        self,
        inputValues=None,
        indices=None,
        value=None,
        outputValues=None,
        defaultValue=None,
        **kwargs
    ):
        """
        IndexValueMapper

        :param inputValues: Already existing values (can be empty)
        :param indices: Indices to map value on
        :param value: Value to map indices on
        :param outputValues: New map between indices and values
        :param defaultValue: Default value for indices without any value
        """
        params = dict(
            inputValues=inputValues,
            indices=indices,
            value=value,
            outputValues=outputValues,
            defaultValue=defaultValue,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "IndexValueMapper", params

    @sofa_component
    def Indices2ValuesMapper(
        self,
        inputValues=None,
        indices=None,
        values=None,
        outputValues=None,
        defaultValue=None,
        **kwargs
    ):
        """
        Indices2ValuesMapper

        :param inputValues: Already existing values (can be empty)
        :param indices: Indices to map value on
        :param values: Values to map indices on
        :param outputValues: New map between indices and values
        :param defaultValue: Default value for indices without any value
        """
        params = dict(
            inputValues=inputValues,
            indices=indices,
            values=values,
            outputValues=outputValues,
            defaultValue=defaultValue,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "Indices2ValuesMapper", params

    @sofa_component
    def IndicesFromValues(
        self,
        values=None,
        indices=None,
        otherIndices=None,
        recursiveSearch=None,
        **kwargs
    ):
        """
        IndicesFromValues

        :param values: input values
        :param indices: Output indices of the given values, searched in global
        :param otherIndices: Output indices of the other values, (NOT the given ones) searched in global
        :param recursiveSearch: if set to true, output are indices of the global data matching with one of the values
        """
        params = dict(
            values=values,
            indices=indices,
            otherIndices=otherIndices,
            recursiveSearch=recursiveSearch,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "IndicesFromValues", params

    @sofa_component
    def JoinPoints(self, points=None, distance=None, mergedPoints=None, **kwargs):
        """
        JoinPoints

        :param points: Points
        :param distance: Distance to merge points
        :param mergedPoints: Merged Points
        """
        params = dict(points=points, distance=distance, mergedPoints=mergedPoints)
        params = {k: v for k, v in params.items() if v is not None}
        return "JoinPoints", params

    @sofa_component
    def MapIndices(self, indices=None, out=None, outStr=None, transpose=None, **kwargs):
        """
        MapIndices

        :param indices: array containing in ith cell the input index corresponding to the output index i (or reversively if transpose=true)
        :param out: Output indices
        :param outStr: Output indices, converted as a string
        :param transpose: Should the transposed mapping be used ?
        """
        params = dict(indices=indices, out=out, outStr=outStr, transpose=transpose)
        params = {k: v for k, v in params.items() if v is not None}
        return "MapIndices", params

    @sofa_component
    def MathOp(self, nbInputs=None, op=None, output=None, **kwargs):
        """
        MathOp

        :param nbInputs: Number of input values
        :param op: Selected operation to apply
        :param output: Output values
        """
        params = dict(nbInputs=nbInputs, op=op, output=output)
        params = {k: v for k, v in params.items() if v is not None}
        return "MathOp", params

    @sofa_component
    def MergeMeshes(
        self,
        nbMeshes=None,
        npoints=None,
        position=None,
        edges=None,
        triangles=None,
        quads=None,
        polygons=None,
        tetrahedra=None,
        hexahedra=None,
        **kwargs
    ):
        """
        MergeMeshes

        :param nbMeshes: number of meshes to merge
        :param npoints: Number Of out points
        :param position: Output Vertices of the merged mesh
        :param edges: Output Edges of the merged mesh
        :param triangles: Output Triangles of the merged mesh
        :param quads: Output Quads of the merged mesh
        :param polygons: Output Polygons of the merged mesh
        :param tetrahedra: Output Tetrahedra of the merged mesh
        :param hexahedra: Output Hexahedra of the merged mesh
        """
        params = dict(
            nbMeshes=nbMeshes,
            npoints=npoints,
            position=position,
            edges=edges,
            triangles=triangles,
            quads=quads,
            polygons=polygons,
            tetrahedra=tetrahedra,
            hexahedra=hexahedra,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MergeMeshes", params

    @sofa_component
    def MergePoints(
        self,
        position1=None,
        position2=None,
        mappingX2=None,
        indices1=None,
        indices2=None,
        points=None,
        noUpdate=None,
        **kwargs
    ):
        """
        MergePoints

        :param position1: position coordinates of the degrees of freedom of the first object
        :param position2: Rest position coordinates of the degrees of freedom of the second object
        :param mappingX2: Mapping of indices to inject position2 inside position1 vertex buffer
        :param indices1: Indices of the points of the first object
        :param indices2: Indices of the points of the second object
        :param points: position coordinates of the merge
        :param noUpdate: do not update the output at eacth time step (false)
        """
        params = dict(
            position1=position1,
            position2=position2,
            mappingX2=mappingX2,
            indices1=indices1,
            indices2=indices2,
            points=points,
            noUpdate=noUpdate,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MergePoints", params

    @sofa_component
    def MergeROIs(self, nbROIs=None, roiIndices=None, **kwargs):
        """
        MergeROIs

        :param nbROIs: size of indices/value vector
        :param roiIndices: Vector of ROIs
        """
        params = dict(nbROIs=nbROIs, roiIndices=roiIndices)
        params = {k: v for k, v in params.items() if v is not None}
        return "MergeROIs", params

    @sofa_component
    def MergeSets(self, in1=None, in2=None, out=None, op=None, **kwargs):
        """
        MergeSets

        :param in1: first set of indices
        :param in2: second set of indices
        :param out: merged set of indices
        :param op: name of operation to compute (union, intersection, difference, symmetric_difference)
        """
        params = dict(in1=in1, in2=in2, out=out, op=op)
        params = {k: v for k, v in params.items() if v is not None}
        return "MergeSets", params

    @sofa_component
    def MergeVectors(self, nbInputs=None, output=None, **kwargs):
        """
        MergeVectors

        :param nbInputs: Number of input vectors
        :param output: Output vector
        """
        params = dict(nbInputs=nbInputs, output=output)
        params = {k: v for k, v in params.items() if v is not None}
        return "MergeVectors", params

    @sofa_component
    def MeshBarycentricMapperEngine(
        self,
        inputPositions=None,
        mappedPointPositions=None,
        barycentricPositions=None,
        tableElements=None,
        computeLinearInterpolation=None,
        linearInterpolationIndices=None,
        linearInterpolationValues=None,
        **kwargs
    ):
        """
        MeshBarycentricMapperEngine

        :param inputPositions: Initial positions of the master points
        :param mappedPointPositions: Initial positions of the mapped points
        :param barycentricPositions: Output : Barycentric positions of the mapped points
        :param tableElements: Output : Table that provides the element index to which each input point belongs
        :param computeLinearInterpolation: if true, computes a linear interpolation (debug)
        :param linearInterpolationIndices: Indices of a linear interpolation
        :param linearInterpolationValues: Values of a linear interpolation
        """
        params = dict(
            inputPositions=inputPositions,
            mappedPointPositions=mappedPointPositions,
            barycentricPositions=barycentricPositions,
            tableElements=tableElements,
            computeLinearInterpolation=computeLinearInterpolation,
            linearInterpolationIndices=linearInterpolationIndices,
            linearInterpolationValues=linearInterpolationValues,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshBarycentricMapperEngine", params

    @sofa_component
    def MeshClosingEngine(
        self,
        inputPosition=None,
        inputTriangles=None,
        inputQuads=None,
        position=None,
        triangles=None,
        quads=None,
        indices=None,
        closingPosition=None,
        closingTriangles=None,
        **kwargs
    ):
        """
        MeshClosingEngine

        :param inputPosition: input vertices
        :param inputTriangles: input triangles
        :param inputQuads: input quads
        :param position: Vertices of closed mesh
        :param triangles: Triangles of closed mesh
        :param quads: Quads of closed mesh (=input quads with current method)
        :param indices: Index lists of the closing parts
        :param closingPosition: Vertices of the closing parts
        :param closingTriangles: Triangles of the closing parts
        """
        params = dict(
            inputPosition=inputPosition,
            inputTriangles=inputTriangles,
            inputQuads=inputQuads,
            position=position,
            triangles=triangles,
            quads=quads,
            indices=indices,
            closingPosition=closingPosition,
            closingTriangles=closingTriangles,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshClosingEngine", params

    @sofa_component
    def MeshBoundaryROI(
        self, triangles=None, quads=None, inputROI=None, indices=None, **kwargs
    ):
        """
        MeshBoundaryROI

        :param triangles: input triangles
        :param quads: input quads
        :param inputROI: optional subset of the input mesh
        :param indices: Index lists of the closing vertices
        """
        params = dict(
            triangles=triangles, quads=quads, inputROI=inputROI, indices=indices
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshBoundaryROI", params

    @sofa_component
    def MeshROI(
        self,
        position=None,
        edges=None,
        triangles=None,
        tetrahedra=None,
        ROIposition=None,
        ROIedges=None,
        ROItriangles=None,
        computeEdges=None,
        computeTriangles=None,
        computeTetrahedra=None,
        computeMeshROI=None,
        box=None,
        indices=None,
        edgeIndices=None,
        triangleIndices=None,
        tetrahedronIndices=None,
        pointsInROI=None,
        edgesInROI=None,
        trianglesInROI=None,
        tetrahedraInROI=None,
        pointsOutROI=None,
        edgesOutROI=None,
        trianglesOutROI=None,
        tetrahedraOutROI=None,
        indicesOut=None,
        edgeOutIndices=None,
        triangleOutIndices=None,
        tetrahedronOutIndices=None,
        drawOut=None,
        drawMesh=None,
        drawBox=None,
        drawPoints=None,
        drawEdges=None,
        drawTriangles=None,
        drawTetrahedra=None,
        drawSize=None,
        doUpdate=None,
        **kwargs
    ):
        """
        MeshROI

        :param position: Rest position coordinates of the degrees of freedom
        :param edges: Edge Topology
        :param triangles: Triangle Topology
        :param tetrahedra: Tetrahedron Topology
        :param ROIposition: ROI position coordinates of the degrees of freedom
        :param ROIedges: ROI Edge Topology
        :param ROItriangles: ROI Triangle Topology
        :param computeEdges: If true, will compute edge list and index list inside the ROI.
        :param computeTriangles: If true, will compute triangle list and index list inside the ROI.
        :param computeTetrahedra: If true, will compute tetrahedra list and index list inside the ROI.
        :param computeMeshROI: Compute with the mesh (not only bounding box)
        :param box: Bounding box defined by xmin,ymin,zmin, xmax,ymax,zmax
        :param indices: Indices of the points contained in the ROI
        :param edgeIndices: Indices of the edges contained in the ROI
        :param triangleIndices: Indices of the triangles contained in the ROI
        :param tetrahedronIndices: Indices of the tetrahedra contained in the ROI
        :param pointsInROI: Points contained in the ROI
        :param edgesInROI: Edges contained in the ROI
        :param trianglesInROI: Triangles contained in the ROI
        :param tetrahedraInROI: Tetrahedra contained in the ROI
        :param pointsOutROI: Points not contained in the ROI
        :param edgesOutROI: Edges not contained in the ROI
        :param trianglesOutROI: Triangles not contained in the ROI
        :param tetrahedraOutROI: Tetrahedra not contained in the ROI
        :param indicesOut: Indices of the points not contained in the ROI
        :param edgeOutIndices: Indices of the edges not contained in the ROI
        :param triangleOutIndices: Indices of the triangles not contained in the ROI
        :param tetrahedronOutIndices: Indices of the tetrahedra not contained in the ROI
        :param drawOut: Draw the data not contained in the ROI
        :param drawMesh: Draw Mesh used for the ROI
        :param drawBox: Draw the Bounding box around the mesh used for the ROI
        :param drawPoints: Draw Points
        :param drawEdges: Draw Edges
        :param drawTriangles: Draw Triangles
        :param drawTetrahedra: Draw Tetrahedra
        :param drawSize: rendering size for mesh and topological elements
        :param doUpdate: Update the computation (not only at the init)
        """
        params = dict(
            position=position,
            edges=edges,
            triangles=triangles,
            tetrahedra=tetrahedra,
            ROIposition=ROIposition,
            ROIedges=ROIedges,
            ROItriangles=ROItriangles,
            computeEdges=computeEdges,
            computeTriangles=computeTriangles,
            computeTetrahedra=computeTetrahedra,
            computeMeshROI=computeMeshROI,
            box=box,
            indices=indices,
            edgeIndices=edgeIndices,
            triangleIndices=triangleIndices,
            tetrahedronIndices=tetrahedronIndices,
            pointsInROI=pointsInROI,
            edgesInROI=edgesInROI,
            trianglesInROI=trianglesInROI,
            tetrahedraInROI=tetrahedraInROI,
            pointsOutROI=pointsOutROI,
            edgesOutROI=edgesOutROI,
            trianglesOutROI=trianglesOutROI,
            tetrahedraOutROI=tetrahedraOutROI,
            indicesOut=indicesOut,
            edgeOutIndices=edgeOutIndices,
            triangleOutIndices=triangleOutIndices,
            tetrahedronOutIndices=tetrahedronOutIndices,
            drawOut=drawOut,
            drawMesh=drawMesh,
            drawBox=drawBox,
            drawPoints=drawPoints,
            drawEdges=drawEdges,
            drawTriangles=drawTriangles,
            drawTetrahedra=drawTetrahedra,
            drawSize=drawSize,
            doUpdate=doUpdate,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshROI", params

    @sofa_component
    def MeshSampler(
        self,
        number=None,
        position=None,
        edges=None,
        maxIter=None,
        outputIndices=None,
        outputPosition=None,
        **kwargs
    ):
        """
        MeshSampler

        :param number: Sample number
        :param position: Input positions.
        :param edges: Input edges for geodesic sampling (Euclidean distances are used if not specified).
        :param maxIter: Max number of Lloyd iterations.
        :param outputIndices: Computed sample indices.
        :param outputPosition: Computed sample coordinates.
        """
        params = dict(
            number=number,
            position=position,
            edges=edges,
            maxIter=maxIter,
            outputIndices=outputIndices,
            outputPosition=outputPosition,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshSampler", params

    @sofa_component
    def MeshSplittingEngine(
        self,
        position=None,
        edges=None,
        triangles=None,
        quads=None,
        tetrahedra=None,
        hexahedra=None,
        nbInputs=None,
        indexPairs=None,
        **kwargs
    ):
        """
        MeshSplittingEngine

        :param position: input vertices
        :param edges: input edges
        :param triangles: input triangles
        :param quads: input quads
        :param tetrahedra: input tetrahedra
        :param hexahedra: input hexahedra
        :param nbInputs: Number of input vectors
        :param indexPairs: couples for input vertices: ROI index + index in the ROI
        """
        params = dict(
            position=position,
            edges=edges,
            triangles=triangles,
            quads=quads,
            tetrahedra=tetrahedra,
            hexahedra=hexahedra,
            nbInputs=nbInputs,
            indexPairs=indexPairs,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshSplittingEngine", params

    @sofa_component
    def MeshSubsetEngine(
        self,
        inputPosition=None,
        inputEdges=None,
        inputTriangles=None,
        inputQuads=None,
        indices=None,
        position=None,
        edges=None,
        triangles=None,
        quads=None,
        **kwargs
    ):
        """
        MeshSubsetEngine

        :param inputPosition: input vertices
        :param inputEdges: input edges
        :param inputTriangles: input triangles
        :param inputQuads: input quads
        :param indices: Index lists of the selected vertices
        :param position: Vertices of mesh subset
        :param edges: edges of mesh subset
        :param triangles: Triangles of mesh subset
        :param quads: Quads of mesh subset
        """
        params = dict(
            inputPosition=inputPosition,
            inputEdges=inputEdges,
            inputTriangles=inputTriangles,
            inputQuads=inputQuads,
            indices=indices,
            position=position,
            edges=edges,
            triangles=triangles,
            quads=quads,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshSubsetEngine", params

    @sofa_component
    def NearestPointROI(self, indices1=None, indices2=None, radius=None, **kwargs):
        """
        NearestPointROI

        :param indices1: Indices of the points on the first model
        :param indices2: Indices of the points on the second model
        :param radius: Radius to search corresponding fixed point
        """
        params = dict(indices1=indices1, indices2=indices2, radius=radius)
        params = {k: v for k, v in params.items() if v is not None}
        return "NearestPointROI", params

    @sofa_component
    def NormEngine(self, input=None, output=None, normType=None, **kwargs):
        """
        NormEngine

        :param input: input array of 3d points
        :param output: output array of scalar norms
        :param normType: The type of norm. Use a negative value for the infinite norm.
        """
        params = dict(input=input, output=output, normType=normType)
        params = {k: v for k, v in params.items() if v is not None}
        return "NormEngine", params

    @sofa_component
    def NormalsFromPoints(
        self,
        position=None,
        triangles=None,
        quads=None,
        normals=None,
        invertNormals=None,
        useAngles=None,
        **kwargs
    ):
        """
        NormalsFromPoints

        :param position: Vertices of the mesh
        :param triangles: Triangles of the mesh
        :param quads: Quads of the mesh
        :param normals: Computed vertex normals of the mesh
        :param invertNormals: Swap normals
        :param useAngles: Use incident angles to weight faces normal contributions at each vertex
        """
        params = dict(
            position=position,
            triangles=triangles,
            quads=quads,
            normals=normals,
            invertNormals=invertNormals,
            useAngles=useAngles,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "NormalsFromPoints", params

    @sofa_component
    def PairBoxRoi(
        self,
        inclusiveBox=None,
        includedBox=None,
        position=None,
        meshPosition=None,
        indices=None,
        pointsInROI=None,
        drawInclusiveBox=None,
        drawInclusdedBx=None,
        drawPoints=None,
        drawSize=None,
        **kwargs
    ):
        """
        PairBoxRoi

        :param inclusiveBox: Inclusive box defined by xmin,ymin,zmin, xmax,ymax,zmax
        :param includedBox: Included box defined by xmin,ymin,zmin, xmax,ymax,zmax
        :param position: Rest position coordinates of the degrees of freedom
        :param meshPosition: Vertices of the mesh loaded
        :param indices: Indices of the points contained in the ROI
        :param pointsInROI: Points contained in the ROI
        :param drawInclusiveBox: Draw Inclusive Box
        :param drawInclusdedBx: Draw Included Box
        :param drawPoints: Draw Points
        :param drawSize: Draw Size
        """
        params = dict(
            inclusiveBox=inclusiveBox,
            includedBox=includedBox,
            position=position,
            meshPosition=meshPosition,
            indices=indices,
            pointsInROI=pointsInROI,
            drawInclusiveBox=drawInclusiveBox,
            drawInclusdedBx=drawInclusdedBx,
            drawPoints=drawPoints,
            drawSize=drawSize,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PairBoxRoi", params

    @sofa_component
    def PlaneROI(
        self,
        plane=None,
        position=None,
        edges=None,
        triangles=None,
        tetrahedra=None,
        computeEdges=None,
        computeTriangles=None,
        computeTetrahedra=None,
        indices=None,
        edgeIndices=None,
        triangleIndices=None,
        tetrahedronIndices=None,
        pointsInROI=None,
        edgesInROI=None,
        trianglesInROI=None,
        tetrahedraInROI=None,
        drawBoxes=None,
        drawPoints=None,
        drawEdges=None,
        drawTriangles=None,
        drawTetrahedra=None,
        drawSize=None,
        **kwargs
    ):
        """
        PlaneROI

        :param plane: Plane defined by 3 points and a depth distance
        :param position: Rest position coordinates of the degrees of freedom
        :param edges: Edge Topology
        :param triangles: Triangle Topology
        :param tetrahedra: Tetrahedron Topology
        :param computeEdges: If true, will compute edge list and index list inside the ROI.
        :param computeTriangles: If true, will compute triangle list and index list inside the ROI.
        :param computeTetrahedra: If true, will compute tetrahedra list and index list inside the ROI.
        :param indices: Indices of the points contained in the ROI
        :param edgeIndices: Indices of the edges contained in the ROI
        :param triangleIndices: Indices of the triangles contained in the ROI
        :param tetrahedronIndices: Indices of the tetrahedra contained in the ROI
        :param pointsInROI: Points contained in the ROI
        :param edgesInROI: Edges contained in the ROI
        :param trianglesInROI: Triangles contained in the ROI
        :param tetrahedraInROI: Tetrahedra contained in the ROI
        :param drawBoxes: Draw Box(es)
        :param drawPoints: Draw Points
        :param drawEdges: Draw Edges
        :param drawTriangles: Draw Triangles
        :param drawTetrahedra: Draw Tetrahedra
        :param drawSize: rendering size for box and topological elements
        """
        params = dict(
            plane=plane,
            position=position,
            edges=edges,
            triangles=triangles,
            tetrahedra=tetrahedra,
            computeEdges=computeEdges,
            computeTriangles=computeTriangles,
            computeTetrahedra=computeTetrahedra,
            indices=indices,
            edgeIndices=edgeIndices,
            triangleIndices=triangleIndices,
            tetrahedronIndices=tetrahedronIndices,
            pointsInROI=pointsInROI,
            edgesInROI=edgesInROI,
            trianglesInROI=trianglesInROI,
            tetrahedraInROI=tetrahedraInROI,
            drawBoxes=drawBoxes,
            drawPoints=drawPoints,
            drawEdges=drawEdges,
            drawTriangles=drawTriangles,
            drawTetrahedra=drawTetrahedra,
            drawSize=drawSize,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PlaneROI", params

    @sofa_component
    def PointsFromIndices(
        self, position=None, indices=None, indices_position=None, **kwargs
    ):
        """
        PointsFromIndices

        :param position: Position coordinates of the degrees of freedom
        :param indices: Indices of the points
        :param indices_position: Coordinates of the points contained in indices
        """
        params = dict(
            position=position, indices=indices, indices_position=indices_position
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PointsFromIndices", params

    @sofa_component
    def ProximityROI(
        self,
        centers=None,
        radii=None,
        N=None,
        position=None,
        indices=None,
        pointsInROI=None,
        distance=None,
        indicesOut=None,
        drawSphere=None,
        drawPoints=None,
        drawSize=None,
        **kwargs
    ):
        """
        ProximityROI

        :param centers: Center(s) of the sphere(s)
        :param radii: Radius(i) of the sphere(s)
        :param N: Maximum number of points to select
        :param position: Rest position coordinates of the degrees of freedom
        :param indices: Indices of the points contained in the ROI
        :param pointsInROI: Points contained in the ROI
        :param distance: distance between the points contained in the ROI and the closest center.
        :param indicesOut: Indices of the points not contained in the ROI
        :param drawSphere: Draw shpere(s)
        :param drawPoints: Draw Points
        :param drawSize: rendering size for box and topological elements
        """
        params = dict(
            centers=centers,
            radii=radii,
            N=N,
            position=position,
            indices=indices,
            pointsInROI=pointsInROI,
            distance=distance,
            indicesOut=indicesOut,
            drawSphere=drawSphere,
            drawPoints=drawPoints,
            drawSize=drawSize,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ProximityROI", params

    @sofa_component
    def QuatToRigidEngine(
        self,
        positions=None,
        orientations=None,
        colinearPositions=None,
        rigids=None,
        **kwargs
    ):
        """
        QuatToRigidEngine

        :param positions: Positions (Vector of 3)
        :param orientations: Orientations (Quaternion)
        :param colinearPositions: Optional positions to restrict output to be colinear in the quaternion Z direction
        :param rigids: Rigid (Position + Orientation)
        """
        params = dict(
            positions=positions,
            orientations=orientations,
            colinearPositions=colinearPositions,
            rigids=rigids,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "QuatToRigidEngine", params

    @sofa_component
    def ROIValueMapper(
        self, nbROIs=None, outputValues=None, defaultValue=None, **kwargs
    ):
        """
        ROIValueMapper

        :param nbROIs: size of indices/value vector
        :param outputValues: New vector of values
        :param defaultValue: Default value for indices out of ROIs
        """
        params = dict(
            nbROIs=nbROIs, outputValues=outputValues, defaultValue=defaultValue
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ROIValueMapper", params

    @sofa_component
    def RandomPointDistributionInSurface(
        self,
        randomSeed=None,
        isVisible=None,
        drawOutputPoints=None,
        minDistanceBetweenPoints=None,
        numberOfInPoints=None,
        numberOfTests=None,
        vertices=None,
        triangles=None,
        inPoints=None,
        outPoints=None,
        **kwargs
    ):
        """
        RandomPointDistributionInSurface

        :param randomSeed: Set a specified seed for random generation (0 for true pseudo-randomness
        :param isVisible: is Visible ?
        :param drawOutputPoints: Output points visible ?
        :param minDistanceBetweenPoints: Min Distance between 2 points (-1 for true randomness)
        :param numberOfInPoints: Number of points inside
        :param numberOfTests: Number of tests to find if the point is inside or not (odd number)
        :param vertices: Vertices
        :param triangles: Triangles indices
        :param inPoints: Points inside the surface
        :param outPoints: Points outside the surface
        """
        params = dict(
            randomSeed=randomSeed,
            isVisible=isVisible,
            drawOutputPoints=drawOutputPoints,
            minDistanceBetweenPoints=minDistanceBetweenPoints,
            numberOfInPoints=numberOfInPoints,
            numberOfTests=numberOfTests,
            vertices=vertices,
            triangles=triangles,
            inPoints=inPoints,
            outPoints=outPoints,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "RandomPointDistributionInSurface", params

    @sofa_component
    def RigidToQuatEngine(
        self,
        positions=None,
        orientations=None,
        orientationsEuler=None,
        rigids=None,
        **kwargs
    ):
        """
        RigidToQuatEngine

        :param positions: Positions (Vector of 3)
        :param orientations: Orientations (Quaternion)
        :param orientationsEuler: Orientations (Euler angle)
        :param rigids: Rigid (Position + Orientation)
        """
        params = dict(
            positions=positions,
            orientations=orientations,
            orientationsEuler=orientationsEuler,
            rigids=rigids,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "RigidToQuatEngine", params

    @sofa_component
    def SelectLabelROI(self, labels=None, selectLabels=None, indices=None, **kwargs):
        """
        SelectLabelROI

        :param labels: lists of labels associated to each point/cell
        :param selectLabels: list of selected labels
        :param indices: selected point/cell indices
        """
        params = dict(labels=labels, selectLabels=selectLabels, indices=indices)
        params = {k: v for k, v in params.items() if v is not None}
        return "SelectLabelROI", params

    @sofa_component
    def SelectConnectedLabelsROI(self, **kwargs):
        """
        SelectConnectedLabelsROI
        """
        params = dict()
        return "SelectConnectedLabelsROI", params

    @sofa_component
    def ShapeMatching(
        self,
        iterations=None,
        affineRatio=None,
        fixedweight=None,
        fixedPosition0=None,
        fixedPosition=None,
        position=None,
        cluster=None,
        targetPosition=None,
        **kwargs
    ):
        """
        ShapeMatching

        :param iterations: Number of iterations.
        :param affineRatio: Blending between affine and rigid.
        :param fixedweight: weight of fixed particles.
        :param fixedPosition0: rest positions of non mechanical particles.
        :param fixedPosition: current (fixed) positions of non mechanical particles.
        :param position: Input positions.
        :param cluster: Input clusters.
        :param targetPosition: Computed target positions.
        """
        params = dict(
            iterations=iterations,
            affineRatio=affineRatio,
            fixedweight=fixedweight,
            fixedPosition0=fixedPosition0,
            fixedPosition=fixedPosition,
            position=position,
            cluster=cluster,
            targetPosition=targetPosition,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ShapeMatching", params

    @sofa_component
    def SmoothMeshEngine(
        self,
        input_position=None,
        input_indices=None,
        output_position=None,
        nb_iterations=None,
        showInput=None,
        showOutput=None,
        **kwargs
    ):
        """
        SmoothMeshEngine

        :param input_position: Input position
        :param input_indices: Position indices that need to be smoothed, leave empty for all positions
        :param output_position: Output position
        :param nb_iterations: Number of iterations of laplacian smoothing
        :param showInput: showInput
        :param showOutput: showOutput
        """
        params = dict(
            input_position=input_position,
            input_indices=input_indices,
            output_position=output_position,
            nb_iterations=nb_iterations,
            showInput=showInput,
            showOutput=showOutput,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SmoothMeshEngine", params

    @sofa_component
    def SphereROI(
        self,
        centers=None,
        radii=None,
        direction=None,
        normal=None,
        edgeAngle=None,
        triAngle=None,
        position=None,
        edges=None,
        triangles=None,
        quads=None,
        tetrahedra=None,
        computeEdges=None,
        computeTriangles=None,
        computeQuads=None,
        computeTetrahedra=None,
        indices=None,
        edgeIndices=None,
        triangleIndices=None,
        quadIndices=None,
        tetrahedronIndices=None,
        pointsInROI=None,
        edgesInROI=None,
        trianglesInROI=None,
        quadsInROI=None,
        tetrahedraInROI=None,
        indicesOut=None,
        drawSphere=None,
        drawPoints=None,
        drawEdges=None,
        drawTriangles=None,
        drawQuads=None,
        drawTetrahedra=None,
        drawSize=None,
        **kwargs
    ):
        """
        SphereROI

        :param centers: Center(s) of the sphere(s)
        :param radii: Radius(i) of the sphere(s)
        :param direction: Edge direction(if edgeAngle > 0)
        :param normal: Normal direction of the triangles (if triAngle > 0)
        :param edgeAngle: Max angle between the direction of the selected edges and the specified direction
        :param triAngle: Max angle between the normal of the selected triangle and the specified normal direction
        :param position: Rest position coordinates of the degrees of freedom
        :param edges: Edge Topology
        :param triangles: Triangle Topology
        :param quads: Quads Topology
        :param tetrahedra: Tetrahedron Topology
        :param computeEdges: If true, will compute edge list and index list inside the ROI.
        :param computeTriangles: If true, will compute triangle list and index list inside the ROI.
        :param computeQuads: If true, will compute quad list and index list inside the ROI.
        :param computeTetrahedra: If true, will compute tetrahedra list and index list inside the ROI.
        :param indices: Indices of the points contained in the ROI
        :param edgeIndices: Indices of the edges contained in the ROI
        :param triangleIndices: Indices of the triangles contained in the ROI
        :param quadIndices: Indices of the quads contained in the ROI
        :param tetrahedronIndices: Indices of the tetrahedra contained in the ROI
        :param pointsInROI: Points contained in the ROI
        :param edgesInROI: Edges contained in the ROI
        :param trianglesInROI: Triangles contained in the ROI
        :param quadsInROI: Quads contained in the ROI
        :param tetrahedraInROI: Tetrahedra contained in the ROI
        :param indicesOut: Indices of the points not contained in the ROI
        :param drawSphere: Draw shpere(s)
        :param drawPoints: Draw Points
        :param drawEdges: Draw Edges
        :param drawTriangles: Draw Triangles
        :param drawQuads: Draw Quads
        :param drawTetrahedra: Draw Tetrahedra
        :param drawSize: rendering size for box and topological elements
        """
        params = dict(
            centers=centers,
            radii=radii,
            direction=direction,
            normal=normal,
            edgeAngle=edgeAngle,
            triAngle=triAngle,
            position=position,
            edges=edges,
            triangles=triangles,
            quads=quads,
            tetrahedra=tetrahedra,
            computeEdges=computeEdges,
            computeTriangles=computeTriangles,
            computeQuads=computeQuads,
            computeTetrahedra=computeTetrahedra,
            indices=indices,
            edgeIndices=edgeIndices,
            triangleIndices=triangleIndices,
            quadIndices=quadIndices,
            tetrahedronIndices=tetrahedronIndices,
            pointsInROI=pointsInROI,
            edgesInROI=edgesInROI,
            trianglesInROI=trianglesInROI,
            quadsInROI=quadsInROI,
            tetrahedraInROI=tetrahedraInROI,
            indicesOut=indicesOut,
            drawSphere=drawSphere,
            drawPoints=drawPoints,
            drawEdges=drawEdges,
            drawTriangles=drawTriangles,
            drawQuads=drawQuads,
            drawTetrahedra=drawTetrahedra,
            drawSize=drawSize,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SphereROI", params

    @sofa_component
    def Spiral(self, rest_position=None, position=None, curvature=None, **kwargs):
        """
        Spiral

        :param rest_position: Rest position coordinates of the degrees of freedom
        :param position: Position coordinates of the degrees of freedom
        :param curvature: Spiral curvature factor
        """
        params = dict(
            rest_position=rest_position, position=position, curvature=curvature
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "Spiral", params

    @sofa_component
    def SubsetTopology(
        self,
        box=None,
        centers=None,
        radii=None,
        direction=None,
        normal=None,
        edgeAngle=None,
        triAngle=None,
        rest_position=None,
        edges=None,
        triangles=None,
        quads=None,
        tetrahedra=None,
        hexahedra=None,
        tetrahedraInput=None,
        indices=None,
        edgeIndices=None,
        triangleIndices=None,
        quadIndices=None,
        tetrahedronIndices=None,
        hexahedronIndices=None,
        pointsInROI=None,
        pointsOutROI=None,
        edgesInROI=None,
        edgesOutROI=None,
        trianglesInROI=None,
        trianglesOutROI=None,
        quadsInROI=None,
        quadsOutROI=None,
        tetrahedraInROI=None,
        tetrahedraOutROI=None,
        hexahedraInROI=None,
        hexahedraOutROI=None,
        nbrborder=None,
        localIndices=None,
        drawROI=None,
        drawPoints=None,
        drawEdges=None,
        drawTriangle=None,
        drawTetrahedra=None,
        drawSize=None,
        **kwargs
    ):
        """
        SubsetTopology

        :param box: Box defined by xmin,ymin,zmin, xmax,ymax,zmax
        :param centers: Center(s) of the sphere(s)
        :param radii: Radius(i) of the sphere(s)
        :param direction: Edge direction(if edgeAngle > 0)
        :param normal: Normal direction of the triangles (if triAngle > 0)
        :param edgeAngle: Max angle between the direction of the selected edges and the specified direction
        :param triAngle: Max angle between the normal of the selected triangle and the specified normal direction
        :param rest_position: Rest position coordinates of the degrees of freedom
        :param edges: Edge Topology
        :param triangles: Triangle Topology
        :param quads: Quad Topology
        :param tetrahedra: Tetrahedron Topology
        :param hexahedra: Hexahedron Topology
        :param tetrahedraInput: Indices of the tetrahedra to keep
        :param indices: Indices of the points contained in the ROI
        :param edgeIndices: Indices of the edges contained in the ROI
        :param triangleIndices: Indices of the triangles contained in the ROI
        :param quadIndices: Indices of the quads contained in the ROI
        :param tetrahedronIndices: Indices of the tetrahedra contained in the ROI
        :param hexahedronIndices: Indices of the hexahedra contained in the ROI
        :param pointsInROI: Points contained in the ROI
        :param pointsOutROI: Points out of the ROI
        :param edgesInROI: Edges contained in the ROI
        :param edgesOutROI: Edges out of the ROI
        :param trianglesInROI: Triangles contained in the ROI
        :param trianglesOutROI: Triangles out of the ROI
        :param quadsInROI: Quads contained in the ROI
        :param quadsOutROI: Quads out of the ROI
        :param tetrahedraInROI: Tetrahedra contained in the ROI
        :param tetrahedraOutROI: Tetrahedra out of the ROI
        :param hexahedraInROI: Hexahedra contained in the ROI
        :param hexahedraOutROI: Hexahedra out of the ROI
        :param nbrborder: If localIndices option is activated, will give the number of vertices on the border of the ROI (being the n first points of each output Topology).
        :param localIndices: If true, will compute local dof indices in topological elements
        :param drawROI: Draw ROI
        :param drawPoints: Draw Points
        :param drawEdges: Draw Edges
        :param drawTriangle: Draw Triangles
        :param drawTetrahedra: Draw Tetrahedra
        :param drawSize: rendering size for box and topological elements
        """
        params = dict(
            box=box,
            centers=centers,
            radii=radii,
            direction=direction,
            normal=normal,
            edgeAngle=edgeAngle,
            triAngle=triAngle,
            rest_position=rest_position,
            edges=edges,
            triangles=triangles,
            quads=quads,
            tetrahedra=tetrahedra,
            hexahedra=hexahedra,
            tetrahedraInput=tetrahedraInput,
            indices=indices,
            edgeIndices=edgeIndices,
            triangleIndices=triangleIndices,
            quadIndices=quadIndices,
            tetrahedronIndices=tetrahedronIndices,
            hexahedronIndices=hexahedronIndices,
            pointsInROI=pointsInROI,
            pointsOutROI=pointsOutROI,
            edgesInROI=edgesInROI,
            edgesOutROI=edgesOutROI,
            trianglesInROI=trianglesInROI,
            trianglesOutROI=trianglesOutROI,
            quadsInROI=quadsInROI,
            quadsOutROI=quadsOutROI,
            tetrahedraInROI=tetrahedraInROI,
            tetrahedraOutROI=tetrahedraOutROI,
            hexahedraInROI=hexahedraInROI,
            hexahedraOutROI=hexahedraOutROI,
            nbrborder=nbrborder,
            localIndices=localIndices,
            drawROI=drawROI,
            drawPoints=drawPoints,
            drawEdges=drawEdges,
            drawTriangle=drawTriangle,
            drawTetrahedra=drawTetrahedra,
            drawSize=drawSize,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SubsetTopology", params

    @sofa_component
    def SumEngine(self, input=None, output=None, **kwargs):
        """
        SumEngine

        :param input: input vector
        :param output: output sum
        """
        params = dict(input=input, output=output)
        params = {k: v for k, v in params.items() if v is not None}
        return "SumEngine", params

    @sofa_component
    def TextureInterpolation(
        self,
        input_states=None,
        input_coordinates=None,
        output_coordinates=None,
        scalarField=None,
        min_value=None,
        max_value=None,
        manual_scale=None,
        drawPotentiels=None,
        showIndicesScale=None,
        vertexPloted=None,
        graph=None,
        **kwargs
    ):
        """
        TextureInterpolation

        :param input_states: input array of state values.
        :param input_coordinates: input array of coordinates values.
        :param output_coordinates: output array of texture coordinates.
        :param scalarField: To interpolate only the first dimension of input field (useful if this component need to be templated in higher dimension).
        :param min_value: minimum value of state value for interpolation.
        :param max_value: maximum value of state value for interpolation.
        :param manual_scale: compute texture interpolation on manually scale defined above.
        :param drawPotentiels: Debug: view state values.
        :param showIndicesScale: Debug : scale of state values displayed.
        :param vertexPloted: Vertex index of values display in graph for each iteration.
        :param graph: Vertex state value per iteration
        """
        params = dict(
            input_states=input_states,
            input_coordinates=input_coordinates,
            output_coordinates=output_coordinates,
            scalarField=scalarField,
            min_value=min_value,
            max_value=max_value,
            manual_scale=manual_scale,
            drawPotentiels=drawPotentiels,
            showIndicesScale=showIndicesScale,
            vertexPloted=vertexPloted,
            graph=graph,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TextureInterpolation", params

    @sofa_component
    def TransformEngine(
        self,
        input_position=None,
        output_position=None,
        translation=None,
        rotation=None,
        quaternion=None,
        scale=None,
        inverse=None,
        **kwargs
    ):
        """
        TransformEngine

        :param input_position: input array of 3d points
        :param output_position: output array of 3d points
        :param translation: translation vector
        :param rotation: rotation vector
        :param quaternion: rotation quaternion
        :param scale: scale factor
        :param inverse: true to apply inverse transformation
        """
        params = dict(
            input_position=input_position,
            output_position=output_position,
            translation=translation,
            rotation=rotation,
            quaternion=quaternion,
            scale=scale,
            inverse=inverse,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TransformEngine", params

    @sofa_component
    def TransformMatrixEngine(
        self, inT=None, outT=None, translation=None, rotation=None, scale=None, **kwargs
    ):
        """
        TransformMatrixEngine

        :param inT: input transformation if any
        :param outT: output transformation
        :param translation: translation vector
        :param rotation: euler angles
        :param scale: scaling values
        """
        params = dict(
            inT=inT, outT=outT, translation=translation, rotation=rotation, scale=scale
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TransformMatrixEngine", params

    @sofa_component
    def TransformPosition(
        self,
        origin=None,
        input_position=None,
        output_position=None,
        normal=None,
        translation=None,
        rotation=None,
        scale=None,
        matrix=None,
        method=None,
        seedValue=None,
        maxRandomDisplacement=None,
        fixedIndices=None,
        filename=None,
        drawInput=None,
        drawOutput=None,
        pointSize=None,
        **kwargs
    ):
        """
        TransformPosition

        :param origin: A 3d point on the plane/Center of the scale
        :param input_position: input array of 3d points
        :param output_position: output array of 3d points projected on a plane
        :param normal: plane normal
        :param translation: translation vector
        :param rotation: rotation vector
        :param scale: scale factor
        :param matrix: 4x4 affine matrix
        :param method: transformation method either translation or scale or rotation or random or projectOnPlane
        :param seedValue: the seed value for the random generator
        :param maxRandomDisplacement: the maximum displacement around initial position for the random transformation
        :param fixedIndices: Indices of the entries that are not transformed
        :param filename: filename of an affine matrix. Supported extensions are: .trm, .tfm, .xfm and .txt(read as .xfm)
        :param drawInput: Draw input points
        :param drawOutput: Draw output points
        :param pointSize: Point size
        """
        params = dict(
            origin=origin,
            input_position=input_position,
            output_position=output_position,
            normal=normal,
            translation=translation,
            rotation=rotation,
            scale=scale,
            matrix=matrix,
            method=method,
            seedValue=seedValue,
            maxRandomDisplacement=maxRandomDisplacement,
            fixedIndices=fixedIndices,
            filename=filename,
            drawInput=drawInput,
            drawOutput=drawOutput,
            pointSize=pointSize,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TransformPosition", params

    @sofa_component
    def ValuesFromIndices(self, indices=None, out=None, outStr=None, **kwargs):
        """
        ValuesFromIndices

        :param indices: Indices of the values
        :param out: Output values corresponding to the indices
        :param outStr: Output values corresponding to the indices, converted as a string
        """
        params = dict(indices=indices, out=out, outStr=outStr)
        params = {k: v for k, v in params.items() if v is not None}
        return "ValuesFromIndices", params

    @sofa_component
    def ValuesFromPositions(
        self,
        inputValues=None,
        direction=None,
        position=None,
        edges=None,
        triangles=None,
        tetrahedra=None,
        values=None,
        edgeValues=None,
        triangleValues=None,
        tetrahedronValues=None,
        pointVectors=None,
        edgeVectors=None,
        triangleVectors=None,
        tetrahedronVectors=None,
        fieldType=None,
        drawVectors=None,
        drawVectorLength=None,
        **kwargs
    ):
        """
        ValuesFromPositions

        :param inputValues: Input values
        :param direction: Direction along which the values are interpolated
        :param position: Rest position coordinates of the degrees of freedom
        :param edges: Edge Topology
        :param triangles: Triangle Topology
        :param tetrahedra: Tetrahedron Topology
        :param values: Values of the points contained in the ROI
        :param edgeValues: Values of the edges contained in the ROI
        :param triangleValues: Values of the triangles contained in the ROI
        :param tetrahedronValues: Values of the tetrahedra contained in the ROI
        :param pointVectors: Vectors of the points contained in the ROI
        :param edgeVectors: Vectors of the edges contained in the ROI
        :param triangleVectors: Vectors of the triangles contained in the ROI
        :param tetrahedronVectors: Vectors of the tetrahedra contained in the ROI
        :param fieldType: field type of output elements
        :param drawVectors: draw vectors line
        :param drawVectorLength: vector length visualisation.
        """
        params = dict(
            inputValues=inputValues,
            direction=direction,
            position=position,
            edges=edges,
            triangles=triangles,
            tetrahedra=tetrahedra,
            values=values,
            edgeValues=edgeValues,
            triangleValues=triangleValues,
            tetrahedronValues=tetrahedronValues,
            pointVectors=pointVectors,
            edgeVectors=edgeVectors,
            triangleVectors=triangleVectors,
            tetrahedronVectors=tetrahedronVectors,
            fieldType=fieldType,
            drawVectors=drawVectors,
            drawVectorLength=drawVectorLength,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ValuesFromPositions", params

    @sofa_component
    def Vertex2Frame(
        self,
        position=None,
        texCoords=None,
        normals=None,
        frames=None,
        useNormals=None,
        invertNormals=None,
        rotation=None,
        rotationAngle=None,
        **kwargs
    ):
        """
        Vertex2Frame

        :param position: Vertices of the mesh loaded
        :param texCoords: TexCoords of the mesh loaded
        :param normals: Normals of the mesh loaded
        :param frames: Frames at output
        :param useNormals: Use normals to compute the orientations; if disabled the direction of the x axisof a vertice is the one from this vertice to the next one
        :param invertNormals: Swap normals
        :param rotation: Apply a local rotation on the frames. If 0 a x-axis rotation is applied. If 1 a y-axis rotation is applied, If 2 a z-axis rotation is applied.
        :param rotationAngle: Angle rotation
        """
        params = dict(
            position=position,
            texCoords=texCoords,
            normals=normals,
            frames=frames,
            useNormals=useNormals,
            invertNormals=invertNormals,
            rotation=rotation,
            rotationAngle=rotationAngle,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "Vertex2Frame", params

    @sofa_component
    def CubeTopology(
        self,
        nz=None,
        internalPoints=None,
        splitNormals=None,
        min=None,
        max=None,
        **kwargs
    ):
        """
        CubeTopology

        :param nz: z grid resolution
        :param internalPoints: include internal points (allow a one-to-one mapping between points from RegularGridTopology and CubeTopology)
        :param splitNormals: split corner points to have planar normals
        :param min: Min
        :param max: Max
        """
        params = dict(
            nz=nz,
            internalPoints=internalPoints,
            splitNormals=splitNormals,
            min=min,
            max=max,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CubeTopology", params

    @sofa_component
    def CylinderGridTopology(
        self, center=None, axis=None, radius=None, length=None, **kwargs
    ):
        """
        CylinderGridTopology

        :param center: Center of the cylinder
        :param axis: Main direction of the cylinder
        :param radius: Radius of the cylinder
        :param length: Length of the cylinder along its axis
        """
        params = dict(center=center, axis=axis, radius=radius, length=length)
        params = {k: v for k, v in params.items() if v is not None}
        return "CylinderGridTopology", params

    @sofa_component
    def SphereGridTopology(self, center=None, axis=None, radius=None, **kwargs):
        """
        SphereGridTopology

        :param center: Center of the cylinder
        :param axis: Main direction of the cylinder
        :param radius: Radius of the cylinder
        """
        params = dict(center=center, axis=axis, radius=radius)
        params = {k: v for k, v in params.items() if v is not None}
        return "SphereGridTopology", params

    @sofa_component
    def SphereQuadTopology(self, center=None, radius=None, **kwargs):
        """
        SphereQuadTopology

        :param center: Center of the sphere
        :param radius: Radius of the sphere
        """
        params = dict(center=center, radius=radius)
        params = {k: v for k, v in params.items() if v is not None}
        return "SphereQuadTopology", params

    @sofa_component
    def qwt_abstract_legend(self, **kwargs):
        """
        qwt_abstract_legend
        """
        params = dict()
        return "qwt_abstract_legend", params

    @sofa_component
    def qwt_abstract_scale(self, **kwargs):
        """
        qwt_abstract_scale
        """
        params = dict()
        return "qwt_abstract_scale", params

    @sofa_component
    def qwt_abstract_slider(self, **kwargs):
        """
        qwt_abstract_slider
        """
        params = dict()
        return "qwt_abstract_slider", params

    @sofa_component
    def qwt_analog_clock(self, **kwargs):
        """
        qwt_analog_clock
        """
        params = dict()
        return "qwt_analog_clock", params

    @sofa_component
    def qwt_compass(self, **kwargs):
        """
        qwt_compass
        """
        params = dict()
        return "qwt_compass", params

    @sofa_component
    def qwt_counter(self, **kwargs):
        """
        qwt_counter
        """
        params = dict()
        return "qwt_counter", params

    @sofa_component
    def qwt_dial(self, **kwargs):
        """
        qwt_dial
        """
        params = dict()
        return "qwt_dial", params

    @sofa_component
    def qwt_dyngrid_layout(self, **kwargs):
        """
        qwt_dyngrid_layout
        """
        params = dict()
        return "qwt_dyngrid_layout", params

    @sofa_component
    def qwt_knob(self, **kwargs):
        """
        qwt_knob
        """
        params = dict()
        return "qwt_knob", params

    @sofa_component
    def qwt_legend(self, **kwargs):
        """
        qwt_legend
        """
        params = dict()
        return "qwt_legend", params

    @sofa_component
    def qwt_legend_label(self, **kwargs):
        """
        qwt_legend_label
        """
        params = dict()
        return "qwt_legend_label", params

    @sofa_component
    def qwt_magnifier(self, **kwargs):
        """
        qwt_magnifier
        """
        params = dict()
        return "qwt_magnifier", params

    @sofa_component
    def qwt_panner(self, **kwargs):
        """
        qwt_panner
        """
        params = dict()
        return "qwt_panner", params

    @sofa_component
    def qwt_picker(self, **kwargs):
        """
        qwt_picker
        """
        params = dict()
        return "qwt_picker", params

    @sofa_component
    def qwt_plot_canvas(self, **kwargs):
        """
        qwt_plot_canvas
        """
        params = dict()
        return "qwt_plot_canvas", params

    @sofa_component
    def qwt_plot(self, **kwargs):
        """
        qwt_plot
        """
        params = dict()
        return "qwt_plot", params

    @sofa_component
    def qwt_plot_glcanvas(self, **kwargs):
        """
        qwt_plot_glcanvas
        """
        params = dict()
        return "qwt_plot_glcanvas", params

    @sofa_component
    def qwt_plot_magnifier(self, **kwargs):
        """
        qwt_plot_magnifier
        """
        params = dict()
        return "qwt_plot_magnifier", params

    @sofa_component
    def qwt_plot_panner(self, **kwargs):
        """
        qwt_plot_panner
        """
        params = dict()
        return "qwt_plot_panner", params

    @sofa_component
    def qwt_plot_picker(self, **kwargs):
        """
        qwt_plot_picker
        """
        params = dict()
        return "qwt_plot_picker", params

    @sofa_component
    def qwt_plot_renderer(self, **kwargs):
        """
        qwt_plot_renderer
        """
        params = dict()
        return "qwt_plot_renderer", params

    @sofa_component
    def qwt_plot_zoomer(self, **kwargs):
        """
        qwt_plot_zoomer
        """
        params = dict()
        return "qwt_plot_zoomer", params

    @sofa_component
    def qwt_sampling_thread(self, **kwargs):
        """
        qwt_sampling_thread
        """
        params = dict()
        return "qwt_sampling_thread", params

    @sofa_component
    def qwt_scale_widget(self, **kwargs):
        """
        qwt_scale_widget
        """
        params = dict()
        return "qwt_scale_widget", params

    @sofa_component
    def qwt_slider(self, **kwargs):
        """
        qwt_slider
        """
        params = dict()
        return "qwt_slider", params

    @sofa_component
    def qwt_text_label(self, **kwargs):
        """
        qwt_text_label
        """
        params = dict()
        return "qwt_text_label", params

    @sofa_component
    def qwt_thermo(self, **kwargs):
        """
        qwt_thermo
        """
        params = dict()
        return "qwt_thermo", params

    @sofa_component
    def camera(self, **kwargs):
        """
        camera
        """
        params = dict()
        return "camera", params

    @sofa_component
    def frame(self, **kwargs):
        """
        frame
        """
        params = dict()
        return "frame", params

    @sofa_component
    def keyFrameInterpolator(self, **kwargs):
        """
        keyFrameInterpolator
        """
        params = dict()
        return "keyFrameInterpolator", params

    @sofa_component
    def manipulatedCameraFrame(self, **kwargs):
        """
        manipulatedCameraFrame
        """
        params = dict()
        return "manipulatedCameraFrame", params

    @sofa_component
    def manipulatedFrame(self, **kwargs):
        """
        manipulatedFrame
        """
        params = dict()
        return "manipulatedFrame", params

    @sofa_component
    def qglviewer(self, **kwargs):
        """
        qglviewer
        """
        params = dict()
        return "qglviewer", params

    @sofa_component
    def Exporter(self, **kwargs):
        """
        Exporter
        """
        params = dict()
        return "Exporter", params

    @sofa_component
    def NVector3(self, **kwargs):
        """
        NVector3
        """
        params = dict()
        return "NVector3", params

    @sofa_component
    def ParserGL(self, **kwargs):
        """
        ParserGL
        """
        params = dict()
        return "ParserGL", params

    @sofa_component
    def Primitive(self, **kwargs):
        """
        Primitive
        """
        params = dict()
        return "Primitive", params

    @sofa_component
    def PrimitivePositioning(self, **kwargs):
        """
        PrimitivePositioning
        """
        params = dict()
        return "PrimitivePositioning", params

    @sofa_component
    def VRender(self, **kwargs):
        """
        VRender
        """
        params = dict()
        return "VRender", params

    @sofa_component
    def Vector2(self, **kwargs):
        """
        Vector2
        """
        params = dict()
        return "Vector2", params

    @sofa_component
    def Vector3(self, **kwargs):
        """
        Vector3
        """
        params = dict()
        return "Vector3", params

    @sofa_component
    def gpc(self, **kwargs):
        """
        gpc
        """
        params = dict()
        return "gpc", params

    @sofa_component
    def constraint(self, **kwargs):
        """
        constraint
        """
        params = dict()
        return "constraint", params

    @sofa_component
    def mouseGrabber(self, **kwargs):
        """
        mouseGrabber
        """
        params = dict()
        return "mouseGrabber", params

    @sofa_component
    def quaternion(self, **kwargs):
        """
        quaternion
        """
        params = dict()
        return "quaternion", params

    @sofa_component
    def vec(self, **kwargs):
        """
        vec
        """
        params = dict()
        return "vec", params

    @sofa_component
    def mesh(self, **kwargs):
        """
        mesh
        """
        params = dict()
        return "mesh", params

    @sofa_component
    def SofaPhysicsSimulation(self, **kwargs):
        """
        SofaPhysicsSimulation
        """
        params = dict()
        return "SofaPhysicsSimulation", params

    @sofa_component
    def fakegui(self, **kwargs):
        """
        fakegui
        """
        params = dict()
        return "fakegui", params

    @sofa_component
    def AddPreset(self, **kwargs):
        """
        AddPreset
        """
        params = dict()
        return "AddPreset", params

    @sofa_component
    def FilterLibrary(self, **kwargs):
        """
        FilterLibrary
        """
        params = dict()
        return "FilterLibrary", params

    @sofa_component
    def GlobalModification(self, **kwargs):
        """
        GlobalModification
        """
        params = dict()
        return "GlobalModification", params

    @sofa_component
    def GraphHistoryManager(self, **kwargs):
        """
        GraphHistoryManager
        """
        params = dict()
        return "GraphHistoryManager", params

    @sofa_component
    def GraphModeler(self, **kwargs):
        """
        GraphModeler
        """
        params = dict()
        return "GraphModeler", params

    @sofa_component
    def LinkComponent(self, **kwargs):
        """
        LinkComponent
        """
        params = dict()
        return "LinkComponent", params

    @sofa_component
    def ModifierCondition(self, **kwargs):
        """
        ModifierCondition
        """
        params = dict()
        return "ModifierCondition", params

    @sofa_component
    def QCategoryTreeLibrary(self, **kwargs):
        """
        QCategoryTreeLibrary
        """
        params = dict()
        return "QCategoryTreeLibrary", params

    @sofa_component
    def QComponentTreeLibrary(self, **kwargs):
        """
        QComponentTreeLibrary
        """
        params = dict()
        return "QComponentTreeLibrary", params

    @sofa_component
    def QSofaTreeLibrary(self, **kwargs):
        """
        QSofaTreeLibrary
        """
        params = dict()
        return "QSofaTreeLibrary", params

    @sofa_component
    def SofaModeler(self, **kwargs):
        """
        SofaModeler
        """
        params = dict()
        return "SofaModeler", params

    @sofa_component
    def SofaTutorialManager(self, **kwargs):
        """
        SofaTutorialManager
        """
        params = dict()
        return "SofaTutorialManager", params

    @sofa_component
    def TutorialSelector(self, **kwargs):
        """
        TutorialSelector
        """
        params = dict()
        return "TutorialSelector", params

    @sofa_component
    def QSofaMainWindow(self, **kwargs):
        """
        QSofaMainWindow
        """
        params = dict()
        return "QSofaMainWindow", params

    @sofa_component
    def QSofaScene(self, **kwargs):
        """
        QSofaScene
        """
        params = dict()
        return "QSofaScene", params

    @sofa_component
    def QSofaViewer(self, **kwargs):
        """
        QSofaViewer
        """
        params = dict()
        return "QSofaViewer", params

    @sofa_component
    def BulletCapsuleModel(self, margin=None, **kwargs):
        """
        BulletCapsuleModel

        :param margin: Margin used for collision detection within bullet
        """
        params = dict(margin=margin)
        params = {k: v for k, v in params.items() if v is not None}
        return "BulletCapsuleModel", params

    @sofa_component
    def BulletCollisionDetection(
        self, contactDistance=None, useSimpleBroadPhase=None, useSAP=None, **kwargs
    ):
        """
        BulletCollisionDetection

        :param contactDistance: Maximum distance between points when contact is created
        :param useSimpleBroadPhase: enable/disable simple broad phase
        :param useSAP: enable/disable sweep and prune
        """
        params = dict(
            contactDistance=contactDistance,
            useSimpleBroadPhase=useSimpleBroadPhase,
            useSAP=useSAP,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "BulletCollisionDetection", params

    @sofa_component
    def BulletConvexHullContactMapper(self, **kwargs):
        """
        BulletConvexHullContactMapper
        """
        params = dict()
        return "BulletConvexHullContactMapper", params

    @sofa_component
    def BulletConvexHullModel(
        self,
        margin=None,
        computeConvexHullDecomposition=None,
        drawConvexHullDecomposition=None,
        CHPoints=None,
        computeNormals=None,
        positionDefined=None,
        concavityThreeshold=None,
        **kwargs
    ):
        """
        BulletConvexHullModel

        :param margin: Margin used for collision detection within bullet
        :param computeConvexHullDecomposition: compute convex hull decomposition using HACD
        :param drawConvexHullDecomposition: draw convex hull decomposition using
        :param CHPoints: points defining the convex hull
        :param computeNormals: set to false to disable computation of triangles normal
        :param positionDefined: set to true if the collision model position is defined in the mechanical object
        :param concavityThreeshold: Threeshold used in the decomposition
        """
        params = dict(
            margin=margin,
            computeConvexHullDecomposition=computeConvexHullDecomposition,
            drawConvexHullDecomposition=drawConvexHullDecomposition,
            CHPoints=CHPoints,
            computeNormals=computeNormals,
            positionDefined=positionDefined,
            concavityThreeshold=concavityThreeshold,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "BulletConvexHullModel", params

    @sofa_component
    def BulletCylinderModel(self, margin=None, **kwargs):
        """
        BulletCylinderModel

        :param margin: Margin used for collision detection within bullet
        """
        params = dict(margin=margin)
        params = {k: v for k, v in params.items() if v is not None}
        return "BulletCylinderModel", params

    @sofa_component
    def BulletOBBModel(self, margin=None, **kwargs):
        """
        BulletOBBModel

        :param margin: Margin used for collision detection within bullet
        """
        params = dict(margin=margin)
        params = {k: v for k, v in params.items() if v is not None}
        return "BulletOBBModel", params

    @sofa_component
    def BulletSphereModel(self, margin=None, **kwargs):
        """
        BulletSphereModel

        :param margin: Margin used for collision detection within bullet
        """
        params = dict(margin=margin)
        params = {k: v for k, v in params.items() if v is not None}
        return "BulletSphereModel", params

    @sofa_component
    def BulletTriangleModel(self, margin=None, **kwargs):
        """
        BulletTriangleModel

        :param margin: Margin used for collision detection within bullet
        """
        params = dict(margin=margin)
        params = {k: v for k, v in params.items() if v is not None}
        return "BulletTriangleModel", params

    @sofa_component
    def PrimitiveCreation(self, **kwargs):
        """
        PrimitiveCreation
        """
        params = dict()
        return "PrimitiveCreation", params

    @sofa_component
    def FEMGridBehaviorModel(
        self,
        youngModulus=None,
        poissonRatio=None,
        totalMass=None,
        subdivisions=None,
        **kwargs
    ):
        """
        FEMGridBehaviorModel

        :param youngModulus: Uniform Young modulus
        :param poissonRatio: Uniform Poisson ratio
        :param totalMass: Total Mass (lumped and uniformly distributed on particles
        :param subdivisions: nb grid subdivisions
        """
        params = dict(
            youngModulus=youngModulus,
            poissonRatio=poissonRatio,
            totalMass=totalMass,
            subdivisions=subdivisions,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "FEMGridBehaviorModel", params

    @sofa_component
    def PreassembledMass(self, massMatrix=None, **kwargs):
        """
        PreassembledMass

        :param massMatrix: AssembledMassMatrix
        """
        params = dict(massMatrix=massMatrix)
        params = {k: v for k, v in params.items() if v is not None}
        return "PreassembledMass", params

    @sofa_component
    def CPUSPHFluidForceField(self, **kwargs):
        """
        CPUSPHFluidForceField
        """
        params = dict()
        return "CPUSPHFluidForceField", params

    @sofa_component
    def CPUSPHFluidForceFieldWithOpenCL(self, **kwargs):
        """
        CPUSPHFluidForceFieldWithOpenCL
        """
        params = dict()
        return "CPUSPHFluidForceFieldWithOpenCL", params

    @sofa_component
    def OpenCLCommon(self, **kwargs):
        """
        OpenCLCommon
        """
        params = dict()
        return "OpenCLCommon", params

    @sofa_component
    def OpenCLFixedConstraint(self, **kwargs):
        """
        OpenCLFixedConstraint
        """
        params = dict()
        return "OpenCLFixedConstraint", params

    @sofa_component
    def OpenCLIdentityMapping(self, **kwargs):
        """
        OpenCLIdentityMapping
        """
        params = dict()
        return "OpenCLIdentityMapping", params

    @sofa_component
    def OpenCLMechanicalObject(self, **kwargs):
        """
        OpenCLMechanicalObject
        """
        params = dict()
        return "OpenCLMechanicalObject", params

    @sofa_component
    def OpenCLMemoryManager(self, **kwargs):
        """
        OpenCLMemoryManager
        """
        params = dict()
        return "OpenCLMemoryManager", params

    @sofa_component
    def OpenCLPlaneForceField(self, **kwargs):
        """
        OpenCLPlaneForceField
        """
        params = dict()
        return "OpenCLPlaneForceField", params

    @sofa_component
    def OpenCLProgram(self, **kwargs):
        """
        OpenCLProgram
        """
        params = dict()
        return "OpenCLProgram", params

    @sofa_component
    def OpenCLSphereForceField(self, **kwargs):
        """
        OpenCLSphereForceField
        """
        params = dict()
        return "OpenCLSphereForceField", params

    @sofa_component
    def OpenCLSpringForceField(self, **kwargs):
        """
        OpenCLSpringForceField
        """
        params = dict()
        return "OpenCLSpringForceField", params

    @sofa_component
    def OpenCLUniformMass(self, **kwargs):
        """
        OpenCLUniformMass
        """
        params = dict()
        return "OpenCLUniformMass", params

    @sofa_component
    def myopencl(self, **kwargs):
        """
        myopencl
        """
        params = dict()
        return "myopencl", params

    @sofa_component
    def RadixSort(self, **kwargs):
        """
        RadixSort
        """
        params = dict()
        return "RadixSort", params

    @sofa_component
    def Scan(self, **kwargs):
        """
        Scan
        """
        params = dict()
        return "Scan", params

    @sofa_component
    def showvector(self, **kwargs):
        """
        showvector
        """
        params = dict()
        return "showvector", params

    @sofa_component
    def top(self, **kwargs):
        """
        top
        """
        params = dict()
        return "top", params

    @sofa_component
    def OpenCLSPHFluidForceField(self, **kwargs):
        """
        OpenCLSPHFluidForceField
        """
        params = dict()
        return "OpenCLSPHFluidForceField", params

    @sofa_component
    def OglTetrahedralModel(
        self, position=None, depthTest=None, blending=None, **kwargs
    ):
        """
        OglTetrahedralModel

        :param position: Vertices coordinates
        :param depthTest: Set Depth Test
        :param blending: Set Blending
        """
        params = dict(position=position, depthTest=depthTest, blending=blending)
        params = {k: v for k, v in params.items() if v is not None}
        return "OglTetrahedralModel", params

    @sofa_component
    def OglVolumetricModel(
        self,
        tetrahedra=None,
        hexahedra=None,
        volumeScale=None,
        depthTest=None,
        blending=None,
        defaultColor=None,
        **kwargs
    ):
        """
        OglVolumetricModel

        :param tetrahedra: Tetrahedra to draw
        :param hexahedra: Hexahedra to draw
        :param volumeScale: Scale for each volumetric primitive
        :param depthTest: Set Depth Test
        :param blending: Set Blending
        :param defaultColor: Color for each volume (if the attribute a_vertexColor is not detected)
        """
        params = dict(
            tetrahedra=tetrahedra,
            hexahedra=hexahedra,
            volumeScale=volumeScale,
            depthTest=depthTest,
            blending=blending,
            defaultColor=defaultColor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "OglVolumetricModel", params

    @sofa_component
    def LeapMotionDriver(
        self,
        scale=None,
        translation=None,
        rotation=None,
        handPalmCoordinate=None,
        sphereCenter=None,
        sphereRadius=None,
        fingersCoordinates=None,
        gestureType=None,
        gesturePosition=None,
        gestureDirection=None,
        scrollDirection=None,
        displayHand=None,
        **kwargs
    ):
        """
        LeapMotionDriver

        :param scale: Default scale applied to the Leap Motion Coordinates.
        :param translation: Position of the tool/hand in the Leap Motion reference frame
        :param rotation: Rotation of the DOFs of the hand
        :param handPalmCoordinate: Coordinate of the hand detected by the Leap Motion
        :param sphereCenter: Center of the sphere of the hand detected by the Leap Motion
        :param sphereRadius: Radius of the sphere of the hand detected by the Leap Motion
        :param fingersCoordinates: Coordinate of the fingers detected by the Leap Motion
        :param gestureType: Type of the current gesture detected by the Leap Motion
        :param gesturePosition: Position of the current gesture detected by the Leap Motion
        :param gestureDirection: Direction of the current gesture detected by the Leap Motion
        :param scrollDirection: Enter 0 if no scrolling (1 if scoll increases the value, 2 if scroll decreases it)
        :param displayHand: display the hand detected by the Leap Motion
        """
        params = dict(
            scale=scale,
            translation=translation,
            rotation=rotation,
            handPalmCoordinate=handPalmCoordinate,
            sphereCenter=sphereCenter,
            sphereRadius=sphereRadius,
            fingersCoordinates=fingersCoordinates,
            gestureType=gestureType,
            gesturePosition=gesturePosition,
            gestureDirection=gestureDirection,
            scrollDirection=scrollDirection,
            displayHand=displayHand,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "LeapMotionDriver", params

    @sofa_component
    def MyListener(self, **kwargs):
        """
        MyListener
        """
        params = dict()
        return "MyListener", params

    @sofa_component
    def RazerHydraDriver(
        self,
        scale=None,
        positionBase=None,
        orientationBase=None,
        positionFirstTool=None,
        positionSecondTool=None,
        orientationFirstTool=None,
        orientationSecondTool=None,
        triggerJustPressedFirstTool=None,
        triggerJustPressedSecondTool=None,
        triggerValueFirstTool=None,
        triggerValueSecondTool=None,
        useBothTools=None,
        displayTools=None,
        **kwargs
    ):
        """
        RazerHydraDriver

        :param scale: Default scale applied to the Leap Motion Coordinates.
        :param positionBase: Position of the interface base in the scene world coordinates
        :param orientationBase: Orientation of the interface base in the scene world coordinates
        :param positionFirstTool: Position of the first tool
        :param positionSecondTool: Position of the second tool
        :param orientationFirstTool: Orientation of the first tool
        :param orientationSecondTool: Orientation of the second tool
        :param triggerJustPressedFirstTool: Boolean passing to true when the trigger of the first tool is pressed
        :param triggerJustPressedSecondTool: Boolean passing to true when the trigger of the second tool is pressed
        :param triggerValueFirstTool: Trigger value of the first tool (between 0 and 1.0)
        :param triggerValueSecondTool: Trigger value of the second tool (between 0 and 1.0)
        :param useBothTools: If true, the two controllers are used, otherwise only one controller is used
        :param displayTools: display the Razer Hydra Controller joysticks as tools
        """
        params = dict(
            scale=scale,
            positionBase=positionBase,
            orientationBase=orientationBase,
            positionFirstTool=positionFirstTool,
            positionSecondTool=positionSecondTool,
            orientationFirstTool=orientationFirstTool,
            orientationSecondTool=orientationSecondTool,
            triggerJustPressedFirstTool=triggerJustPressedFirstTool,
            triggerJustPressedSecondTool=triggerJustPressedSecondTool,
            triggerValueFirstTool=triggerValueFirstTool,
            triggerValueSecondTool=triggerValueSecondTool,
            useBothTools=useBothTools,
            displayTools=displayTools,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "RazerHydraDriver", params

    @sofa_component
    def ManifoldEdgeSetGeometryAlgorithms(self, **kwargs):
        """
        ManifoldEdgeSetGeometryAlgorithms
        """
        params = dict()
        return "ManifoldEdgeSetGeometryAlgorithms", params

    @sofa_component
    def ManifoldEdgeSetTopologyAlgorithms(self, **kwargs):
        """
        ManifoldEdgeSetTopologyAlgorithms
        """
        params = dict()
        return "ManifoldEdgeSetTopologyAlgorithms", params

    @sofa_component
    def ManifoldEdgeSetTopologyContainer(self, **kwargs):
        """
        ManifoldEdgeSetTopologyContainer
        """
        params = dict()
        return "ManifoldEdgeSetTopologyContainer", params

    @sofa_component
    def ManifoldEdgeSetTopologyModifier(self, **kwargs):
        """
        ManifoldEdgeSetTopologyModifier
        """
        params = dict()
        return "ManifoldEdgeSetTopologyModifier", params

    @sofa_component
    def ManifoldTetrahedronSetTopologyContainer(
        self,
        debugViewTriangleIndices=None,
        debugViewTetraIndices=None,
        debugViewShells=None,
        **kwargs
    ):
        """
        ManifoldTetrahedronSetTopologyContainer

        :param debugViewTriangleIndices: Debug : view triangles indices
        :param debugViewTetraIndices: Debug : view tetra indices
        :param debugViewShells: Debug : view shells tetra
        """
        params = dict(
            debugViewTriangleIndices=debugViewTriangleIndices,
            debugViewTetraIndices=debugViewTetraIndices,
            debugViewShells=debugViewShells,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ManifoldTetrahedronSetTopologyContainer", params

    @sofa_component
    def ManifoldTriangleSetTopologyAlgorithms(self, **kwargs):
        """
        ManifoldTriangleSetTopologyAlgorithms
        """
        params = dict()
        return "ManifoldTriangleSetTopologyAlgorithms", params

    @sofa_component
    def ManifoldTriangleSetTopologyContainer(self, **kwargs):
        """
        ManifoldTriangleSetTopologyContainer
        """
        params = dict()
        return "ManifoldTriangleSetTopologyContainer", params

    @sofa_component
    def ManifoldTriangleSetTopologyModifier(self, **kwargs):
        """
        ManifoldTriangleSetTopologyModifier
        """
        params = dict()
        return "ManifoldTriangleSetTopologyModifier", params

    @sofa_component
    def Interactor(self, **kwargs):
        """
        Interactor
        """
        params = dict()
        return "Interactor", params

    @sofa_component
    def SofaGL(self, **kwargs):
        """
        SofaGL
        """
        params = dict()
        return "SofaGL", params

    @sofa_component
    def SofaScene(self, **kwargs):
        """
        SofaScene
        """
        params = dict()
        return "SofaScene", params

    @sofa_component
    def SpringInteractor(self, **kwargs):
        """
        SpringInteractor
        """
        params = dict()
        return "SpringInteractor", params

    @sofa_component
    def VisualPickVisitor(self, **kwargs):
        """
        VisualPickVisitor
        """
        params = dict()
        return "VisualPickVisitor", params

    @sofa_component
    def SparsePARDISOSolver(
        self,
        symmetric=None,
        verbose=None,
        exportDataToDir=None,
        iterativeSolverNumbering=None,
        saveDataToFile=None,
        **kwargs
    ):
        """
        SparsePARDISOSolver

        :param symmetric: 0 = nonsymmetric arbitrary matrix, 1 = symmetric matrix, 2 = symmetric positive definite, -1 = structurally symmetric matrix
        :param verbose: Dump system state at each iteration
        :param exportDataToDir: export data (matrix, RHS, solution) to files in given directory
        :param iterativeSolverNumbering: if true, the naming convention is incN_itM where N is the time step and M is the iteration inside the step
        :param saveDataToFile: if true, export the data to the current directory (if exportDataToDir not set)
        """
        params = dict(
            symmetric=symmetric,
            verbose=verbose,
            exportDataToDir=exportDataToDir,
            iterativeSolverNumbering=iterativeSolverNumbering,
            saveDataToFile=saveDataToFile,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SparsePARDISOSolver", params

    @sofa_component
    def SphereSurface(self, **kwargs):
        """
        SphereSurface
        """
        params = dict()
        return "SphereSurface", params

    @sofa_component
    def DiscreteGridField(
        self,
        filename=None,
        nx=None,
        ny=None,
        nz=None,
        scale=None,
        sampling=None,
        file=None,
        maxDomains=None,
        dx=None,
        dy=None,
        dz=None,
        **kwargs
    ):
        """
        DiscreteGridField

        :param filename: filename
        :param nx: in_nx
        :param ny: in_ny
        :param nz: in_nz
        :param scale: in_scale
        :param sampling: in_sampling
        :param file: MHD file for the distance map
        :param maxDomains: Number of domains available for caching
        :param dx: x translation
        :param dy: y translation
        :param dz: z translation
        """
        params = dict(
            filename=filename,
            nx=nx,
            ny=ny,
            nz=nz,
            scale=scale,
            sampling=sampling,
            file=file,
            maxDomains=maxDomains,
            dx=dx,
            dy=dy,
            dz=dz,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "DiscreteGridField", params

    @sofa_component
    def SphericalField(self, inside=None, radius=None, center=None, **kwargs):
        """
        SphericalField

        :param inside: If true the field is oriented inside (resp. outside) the sphere. (default = false)
        :param radius: Radius of Sphere emitting the field. (default = 1)
        :param center: Position of the Sphere Surface. (default=0 0 0)
        """
        params = dict(inside=inside, radius=radius, center=center)
        params = {k: v for k, v in params.items() if v is not None}
        return "SphericalField", params

    @sofa_component
    def ScalarField(self, **kwargs):
        """
        ScalarField
        """
        params = dict()
        return "ScalarField", params

    @sofa_component
    def ImplicitSurfaceMapping(self, **kwargs):
        """
        ImplicitSurfaceMapping
        """
        params = dict()
        return "ImplicitSurfaceMapping", params

    @sofa_component
    def THMPGHashTable(self, **kwargs):
        """
        THMPGHashTable
        """
        params = dict()
        return "THMPGHashTable", params

    @sofa_component
    def THMPGSpatialHashing(self, **kwargs):
        """
        THMPGSpatialHashing
        """
        params = dict()
        return "THMPGSpatialHashing", params

    @sofa_component
    def ManualLinearMapping(self, **kwargs):
        """
        ManualLinearMapping
        """
        params = dict()
        return "ManualLinearMapping", params

    @sofa_component
    def DistanceGrid(self, **kwargs):
        """
        DistanceGrid
        """
        params = dict()
        return "DistanceGrid", params

    @sofa_component
    def FFDDistanceGridDiscreteIntersection(self, **kwargs):
        """
        FFDDistanceGridDiscreteIntersection
        """
        params = dict()
        return "FFDDistanceGridDiscreteIntersection", params

    @sofa_component
    def RigidDistanceGridDiscreteIntersection(self, **kwargs):
        """
        RigidDistanceGridDiscreteIntersection
        """
        params = dict()
        return "RigidDistanceGridDiscreteIntersection", params

    @sofa_component
    def DistanceGridCollisionModel(
        self,
        filename=None,
        scale=None,
        translation=None,
        rotation=None,
        sampling=None,
        box=None,
        nx=None,
        ny=None,
        nz=None,
        dumpfilename=None,
        usePoints=None,
        flipNormals=None,
        showMeshPoints=None,
        showGridPoints=None,
        showMinDist=None,
        showMaxDist=None,
        singleContact=None,
        **kwargs
    ):
        """
        DistanceGridCollisionModel

        :param filename: Load distance grid from specified file
        :param scale: scaling factor for input file
        :param translation: translation to apply to input file
        :param rotation: rotation to apply to input file
        :param sampling: if not zero: sample the surface with points approximately separated by the given sampling distance (expressed in voxels if the value is negative)
        :param box: Field bounding box defined by xmin,ymin,zmin, xmax,ymax,zmax
        :param nx: number of values on X axis
        :param ny: number of values on Y axis
        :param nz: number of values on Z axis
        :param dumpfilename: write distance grid to specified file
        :param usePoints: use mesh vertices for collision detection
        :param flipNormals: reverse surface direction, i.e. points are considered in collision if they move outside of the object instead of inside
        :param showMeshPoints: Enable rendering of mesh points
        :param showGridPoints: Enable rendering of grid points
        :param showMinDist: Min distance to render gradients
        :param showMaxDist: Max distance to render gradients
        :param singleContact: keep only the deepest contact in each cell
        """
        params = dict(
            filename=filename,
            scale=scale,
            translation=translation,
            rotation=rotation,
            sampling=sampling,
            box=box,
            nx=nx,
            ny=ny,
            nz=nz,
            dumpfilename=dumpfilename,
            usePoints=usePoints,
            flipNormals=flipNormals,
            showMeshPoints=showMeshPoints,
            showGridPoints=showGridPoints,
            showMinDist=showMinDist,
            showMaxDist=showMaxDist,
            singleContact=singleContact,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "DistanceGridCollisionModel", params

    @sofa_component
    def DistanceGridForceField(self, **kwargs):
        """
        DistanceGridForceField
        """
        params = dict()
        return "DistanceGridForceField", params

    @sofa_component
    def Binding(self, **kwargs):
        """
        Binding
        """
        params = dict()
        return "Binding", params

    @sofa_component
    def Binding_Base(self, **kwargs):
        """
        Binding_Base
        """
        params = dict()
        return "Binding_Base", params

    @sofa_component
    def Binding_BaseContext(self, **kwargs):
        """
        Binding_BaseContext
        """
        params = dict()
        return "Binding_BaseContext", params

    @sofa_component
    def Binding_BaseLoader(self, **kwargs):
        """
        Binding_BaseLoader
        """
        params = dict()
        return "Binding_BaseLoader", params

    @sofa_component
    def Binding_BaseMapping(self, **kwargs):
        """
        Binding_BaseMapping
        """
        params = dict()
        return "Binding_BaseMapping", params

    @sofa_component
    def Binding_BaseMechanicalState(self, **kwargs):
        """
        Binding_BaseMechanicalState
        """
        params = dict()
        return "Binding_BaseMechanicalState", params

    @sofa_component
    def Binding_BaseMeshTopology(self, **kwargs):
        """
        Binding_BaseMeshTopology
        """
        params = dict()
        return "Binding_BaseMeshTopology", params

    @sofa_component
    def Binding_BaseObject(self, **kwargs):
        """
        Binding_BaseObject
        """
        params = dict()
        return "Binding_BaseObject", params

    @sofa_component
    def Binding_BaseState(self, **kwargs):
        """
        Binding_BaseState
        """
        params = dict()
        return "Binding_BaseState", params

    @sofa_component
    def Binding_BaseTopologyObject(self, **kwargs):
        """
        Binding_BaseTopologyObject
        """
        params = dict()
        return "Binding_BaseTopologyObject", params

    @sofa_component
    def Binding_Context(self, **kwargs):
        """
        Binding_Context
        """
        params = dict()
        return "Binding_Context", params

    @sofa_component
    def Binding_Data(self, **kwargs):
        """
        Binding_Data
        """
        params = dict()
        return "Binding_Data", params

    @sofa_component
    def Binding_DataEngine(self, **kwargs):
        """
        Binding_DataEngine
        """
        params = dict()
        return "Binding_DataEngine", params

    @sofa_component
    def Binding_DataFileName(self, **kwargs):
        """
        Binding_DataFileName
        """
        params = dict()
        return "Binding_DataFileName", params

    @sofa_component
    def Binding_DataFileNameVector(self, **kwargs):
        """
        Binding_DataFileNameVector
        """
        params = dict()
        return "Binding_DataFileNameVector", params

    @sofa_component
    def Binding_DisplayFlagsData(self, **kwargs):
        """
        Binding_DisplayFlagsData
        """
        params = dict()
        return "Binding_DisplayFlagsData", params

    @sofa_component
    def Binding_OptionsGroupData(self, **kwargs):
        """
        Binding_OptionsGroupData
        """
        params = dict()
        return "Binding_OptionsGroupData", params

    @sofa_component
    def Binding_BoundingBoxData(self, **kwargs):
        """
        Binding_BoundingBoxData
        """
        params = dict()
        return "Binding_BoundingBoxData", params

    @sofa_component
    def Binding_GridTopology(self, **kwargs):
        """
        Binding_GridTopology
        """
        params = dict()
        return "Binding_GridTopology", params

    @sofa_component
    def Binding_LinearSpring(self, **kwargs):
        """
        Binding_LinearSpring
        """
        params = dict()
        return "Binding_LinearSpring", params

    @sofa_component
    def Binding_Link(self, **kwargs):
        """
        Binding_Link
        """
        params = dict()
        return "Binding_Link", params

    @sofa_component
    def Binding_Mapping(self, **kwargs):
        """
        Binding_Mapping
        """
        params = dict()
        return "Binding_Mapping", params

    @sofa_component
    def Binding_MeshLoader(self, **kwargs):
        """
        Binding_MeshLoader
        """
        params = dict()
        return "Binding_MeshLoader", params

    @sofa_component
    def Binding_TopologyChange(self, **kwargs):
        """
        Binding_TopologyChange
        """
        params = dict()
        return "Binding_TopologyChange", params

    @sofa_component
    def Binding_PointSetTopologyModifier(self, **kwargs):
        """
        Binding_PointSetTopologyModifier
        """
        params = dict()
        return "Binding_PointSetTopologyModifier", params

    @sofa_component
    def Binding_TriangleSetTopologyModifier(self, **kwargs):
        """
        Binding_TriangleSetTopologyModifier
        """
        params = dict()
        return "Binding_TriangleSetTopologyModifier", params

    @sofa_component
    def Binding_MeshTopology(self, **kwargs):
        """
        Binding_MeshTopology
        """
        params = dict()
        return "Binding_MeshTopology", params

    @sofa_component
    def Binding_MultiMapping(self, **kwargs):
        """
        Binding_MultiMapping
        """
        params = dict()
        return "Binding_MultiMapping", params

    @sofa_component
    def Binding_Node(self, **kwargs):
        """
        Binding_Node
        """
        params = dict()
        return "Binding_Node", params

    @sofa_component
    def Binding_PythonScriptController(self, **kwargs):
        """
        Binding_PythonScriptController
        """
        params = dict()
        return "Binding_PythonScriptController", params

    @sofa_component
    def Binding_PythonScriptDataEngine(self, **kwargs):
        """
        Binding_PythonScriptDataEngine
        """
        params = dict()
        return "Binding_PythonScriptDataEngine", params

    @sofa_component
    def Binding_RegularGridTopology(self, **kwargs):
        """
        Binding_RegularGridTopology
        """
        params = dict()
        return "Binding_RegularGridTopology", params

    @sofa_component
    def Binding_RigidMapping(self, **kwargs):
        """
        Binding_RigidMapping
        """
        params = dict()
        return "Binding_RigidMapping", params

    @sofa_component
    def Binding_SofaModule(self, **kwargs):
        """
        Binding_SofaModule
        """
        params = dict()
        return "Binding_SofaModule", params

    @sofa_component
    def Binding_SparseGridTopology(self, **kwargs):
        """
        Binding_SparseGridTopology
        """
        params = dict()
        return "Binding_SparseGridTopology", params

    @sofa_component
    def Binding_Topology(self, **kwargs):
        """
        Binding_Topology
        """
        params = dict()
        return "Binding_Topology", params

    @sofa_component
    def Binding_Vector(self, **kwargs):
        """
        Binding_Vector
        """
        params = dict()
        return "Binding_Vector", params

    @sofa_component
    def Binding_VectorLinearSpringData(self, **kwargs):
        """
        Binding_VectorLinearSpringData
        """
        params = dict()
        return "Binding_VectorLinearSpringData", params

    @sofa_component
    def Binding_VisualModel(self, **kwargs):
        """
        Binding_VisualModel
        """
        params = dict()
        return "Binding_VisualModel", params

    @sofa_component
    def PythonEnvironment(self, **kwargs):
        """
        PythonEnvironment
        """
        params = dict()
        return "PythonEnvironment", params

    @sofa_component
    def PythonFactory(self, **kwargs):
        """
        PythonFactory
        """
        params = dict()
        return "PythonFactory", params

    @sofa_component
    def PythonMacros(self, **kwargs):
        """
        PythonMacros
        """
        params = dict()
        return "PythonMacros", params

    @sofa_component
    def PythonMainScriptController(self, **kwargs):
        """
        PythonMainScriptController
        """
        params = dict()
        return "PythonMainScriptController", params

    @sofa_component
    def PythonScriptController(self, **kwargs):
        """
        PythonScriptController
        """
        params = dict()
        return "PythonScriptController", params

    @sofa_component
    def PythonScriptControllerHelper(self, **kwargs):
        """
        PythonScriptControllerHelper
        """
        params = dict()
        return "PythonScriptControllerHelper", params

    @sofa_component
    def PythonScriptDataEngine(self, **kwargs):
        """
        PythonScriptDataEngine
        """
        params = dict()
        return "PythonScriptDataEngine", params

    @sofa_component
    def PythonScriptEvent(self, **kwargs):
        """
        PythonScriptEvent
        """
        params = dict()
        return "PythonScriptEvent", params

    @sofa_component
    def PythonScriptFunction(self, **kwargs):
        """
        PythonScriptFunction
        """
        params = dict()
        return "PythonScriptFunction", params

    @sofa_component
    def PythonVisitor(self, **kwargs):
        """
        PythonVisitor
        """
        params = dict()
        return "PythonVisitor", params

    @sofa_component
    def SceneLoaderPY(self, **kwargs):
        """
        SceneLoaderPY
        """
        params = dict()
        return "SceneLoaderPY", params

    @sofa_component
    def ScriptController(self, **kwargs):
        """
        ScriptController
        """
        params = dict()
        return "ScriptController", params

    @sofa_component
    def ScriptDataEngine(self, **kwargs):
        """
        ScriptDataEngine
        """
        params = dict()
        return "ScriptDataEngine", params

    @sofa_component
    def ScriptFunction(self, **kwargs):
        """
        ScriptFunction
        """
        params = dict()
        return "ScriptFunction", params

    @sofa_component
    def AnimationLoopParallelScheduler(
        self, scheduler=None, threadNumber=None, **kwargs
    ):
        """
        AnimationLoopParallelScheduler

        :param scheduler: name of the scheduler to use
        :param threadNumber: number of thread
        """
        params = dict(scheduler=scheduler, threadNumber=threadNumber)
        params = {k: v for k, v in params.items() if v is not None}
        return "AnimationLoopParallelScheduler", params

    @sofa_component
    def AnimationLoopTasks(self, **kwargs):
        """
        AnimationLoopTasks
        """
        params = dict()
        return "AnimationLoopTasks", params

    @sofa_component
    def BeamLinearMapping_mt(self, granularity=None, **kwargs):
        """
        BeamLinearMapping_mt

        :param granularity: minimum number of Beam points for task creation
        """
        params = dict(granularity=granularity)
        params = {k: v for k, v in params.items() if v is not None}
        return "BeamLinearMapping_mt", params

    @sofa_component
    def DataExchange(self, to=None, **kwargs):
        """
        DataExchange

        :param to: destination object to copy
        """
        params = dict(to=to)
        params = {k: v for k, v in params.items() if v is not None}
        return "DataExchange", params

    @sofa_component
    def MeanComputation(self, input=None, result=None, **kwargs):
        """
        MeanComputation

        :param input: List of all input values for mean computation
        :param result: Result: mean computed from the input values
        """
        params = dict(input=input, result=result)
        params = {k: v for k, v in params.items() if v is not None}
        return "MeanComputation", params

    @sofa_component
    def SceneColladaLoader(
        self,
        animationSpeed=None,
        generateCollisionModels=None,
        useFlexible=None,
        generateShapeFunction=None,
        voxelSize=None,
        **kwargs
    ):
        """
        SceneColladaLoader

        :param animationSpeed: animation speed
        :param generateCollisionModels: generate point/line/triangle collision models for imported meshes
        :param useFlexible: Use the Flexible plugin (it will replace the SkinningMapping with a LinearMapping)
        :param generateShapeFunction: Generate a shape function that could be used in another simulation
        :param voxelSize: voxelSize used for shape function generation
        """
        params = dict(
            animationSpeed=animationSpeed,
            generateCollisionModels=generateCollisionModels,
            useFlexible=useFlexible,
            generateShapeFunction=generateShapeFunction,
            voxelSize=voxelSize,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SceneColladaLoader", params

    @sofa_component
    def StereoOglModel(
        self,
        textureleft=None,
        textureright=None,
        fileMesh=None,
        translation=None,
        rotation=None,
        scale3d=None,
        scaleTex=None,
        translationTex=None,
        **kwargs
    ):
        """
        StereoOglModel

        :param textureleft: Name of the Left Texture
        :param textureright: Name of the Right Texture
        :param fileMesh:  Path to the model
        :param translation: Initial Translation of the object
        :param rotation: Initial Rotation of the object
        :param scale3d: Initial Scale of the object
        :param scaleTex: Scale of the texture
        :param translationTex: Translation of the texture
        """
        params = dict(
            textureleft=textureleft,
            textureright=textureright,
            fileMesh=fileMesh,
            translation=translation,
            rotation=rotation,
            scale3d=scale3d,
            scaleTex=scaleTex,
            translationTex=translationTex,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "StereoOglModel", params

    @sofa_component
    def StereoCamera(
        self, enabled=None, mode=None, strategy=None, baseline=None, **kwargs
    ):
        """
        StereoCamera

        :param enabled: Is the stereo mode initially enabled?
        :param mode: Stereo Mode: STEREO_AUTO = 0, STEREO_INTERLACED = 1, STEREO_FRAME_PACKING = 2, STEREO_SIDE_BY_SIDE = 3, STEREO_TOP_BOTTOM = 4, STEREO_SIDE_BY_SIDE_HALF = 5, STEREO_TOP_BOTTOM_HALF = 6, STEREO_NONE = 7
        :param strategy: Stereo Strategy: PARALLEL = 0 OR TOEDIN = 1
        :param baseline: Stereoscopic Baseline
        """
        params = dict(enabled=enabled, mode=mode, strategy=strategy, baseline=baseline)
        params = {k: v for k, v in params.items() if v is not None}
        return "StereoCamera", params

    @sofa_component
    def ClosestPointRegistrationForceField(
        self,
        stiffness=None,
        damping=None,
        cacheSize=None,
        blendingFactor=None,
        outlierThreshold=None,
        normalThreshold=None,
        projectToPlane=None,
        rejectBorders=None,
        rejectOutsideBbox=None,
        sourceTriangles=None,
        sourceNormals=None,
        position=None,
        normals=None,
        triangles=None,
        showArrowSize=None,
        drawMode=None,
        drawColorMap=None,
        theCloserTheStiffer=None,
        **kwargs
    ):
        """
        ClosestPointRegistrationForceField

        :param stiffness: uniform stiffness for the all springs.
        :param damping: uniform damping for the all springs.
        :param cacheSize: number of closest points used in the cache to speed up closest point computation.
        :param blendingFactor: blending between projection (=0) and attraction (=1) forces.
        :param outlierThreshold: suppress outliers when distance > (meandistance + threshold*stddev).
        :param normalThreshold: suppress outliers when normal.closestPointNormal < threshold.
        :param projectToPlane: project closest points in the plane defined by the normal.
        :param rejectBorders: ignore border vertices.
        :param rejectOutsideBbox: ignore source points outside bounding box of target points.
        :param sourceTriangles: Triangles of the source mesh.
        :param sourceNormals: Normals of the source mesh.
        :param position: Vertices of the target mesh.
        :param normals: Normals of the target mesh.
        :param triangles: Triangles of the target mesh.
        :param showArrowSize: size of the axis.
        :param drawMode: The way springs will be drawn:\n- 0: Line\n- 1:Cylinder\n- 2: Arrow.
        :param drawColorMap: Hue mapping of distances to closest point
        :param theCloserTheStiffer: Modify stiffness according to distance
        """
        params = dict(
            stiffness=stiffness,
            damping=damping,
            cacheSize=cacheSize,
            blendingFactor=blendingFactor,
            outlierThreshold=outlierThreshold,
            normalThreshold=normalThreshold,
            projectToPlane=projectToPlane,
            rejectBorders=rejectBorders,
            rejectOutsideBbox=rejectOutsideBbox,
            sourceTriangles=sourceTriangles,
            sourceNormals=sourceNormals,
            position=position,
            normals=normals,
            triangles=triangles,
            showArrowSize=showArrowSize,
            drawMode=drawMode,
            drawColorMap=drawColorMap,
            theCloserTheStiffer=theCloserTheStiffer,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ClosestPointRegistrationForceField", params

    @sofa_component
    def GroupwiseRegistrationEngine(self, nbInputs=None, **kwargs):
        """
        GroupwiseRegistrationEngine

        :param nbInputs: Number of input vectors
        """
        params = dict(nbInputs=nbInputs)
        params = {k: v for k, v in params.items() if v is not None}
        return "GroupwiseRegistrationEngine", params

    @sofa_component
    def InertiaAlign(
        self,
        targetCenter=None,
        sourceCenter=None,
        targetInertiaMatrix=None,
        sourceInertiaMatrix=None,
        targetPosition=None,
        sourcePosition=None,
        **kwargs
    ):
        """
        InertiaAlign

        :param targetCenter: input: the gravity center of the target mesh
        :param sourceCenter: input: the gravity center of the source mesh
        :param targetInertiaMatrix: input: the inertia matrix of the target mesh
        :param sourceInertiaMatrix: input: the inertia matrix of the source mesh
        :param targetPosition: input: positions of the target vertices
        :param sourcePosition: input: positions of the source vertices
        """
        params = dict(
            targetCenter=targetCenter,
            sourceCenter=sourceCenter,
            targetInertiaMatrix=targetInertiaMatrix,
            sourceInertiaMatrix=sourceInertiaMatrix,
            targetPosition=targetPosition,
            sourcePosition=sourcePosition,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "InertiaAlign", params

    @sofa_component
    def RegistrationContact(self, **kwargs):
        """
        RegistrationContact
        """
        params = dict()
        return "RegistrationContact", params

    @sofa_component
    def RegistrationContactForceField(self, contacts=None, **kwargs):
        """
        RegistrationContactForceField

        :param contacts: Contacts
        """
        params = dict(contacts=contacts)
        params = {k: v for k, v in params.items() if v is not None}
        return "RegistrationContactForceField", params

    @sofa_component
    def RegistrationExporter(
        self,
        path=None,
        position=None,
        applyInverseTransform=None,
        exportEveryNumberOfSteps=None,
        exportAtBegin=None,
        exportAtEnd=None,
        **kwargs
    ):
        """
        RegistrationExporter

        :param path: output path
        :param position: points position (will use mechanical state if this is empty)
        :param applyInverseTransform: apply inverse transform specified in loaders
        :param exportEveryNumberOfSteps: export file only at specified number of steps (0=disable)
        :param exportAtBegin: export file at the initialization
        :param exportAtEnd: export file when the simulation is finished
        """
        params = dict(
            path=path,
            position=position,
            applyInverseTransform=applyInverseTransform,
            exportEveryNumberOfSteps=exportEveryNumberOfSteps,
            exportAtBegin=exportAtBegin,
            exportAtEnd=exportAtEnd,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "RegistrationExporter", params

    @sofa_component
    def EnslavementForceFeedback(
        self,
        d_relativeStiffness=None,
        d_attractionDistance=None,
        d_normalsPointOut=None,
        d_contactScale=None,
        penetrationOffset=None,
        **kwargs
    ):
        """
        EnslavementForceFeedback

        :param d_relativeStiffness: Relative Stiffness
        :param d_attractionDistance: Distance at which the Omni is attracted to the contact point.
        :param d_normalsPointOut: True if the normals of objects point outwards, false if they point inwards.
        :param d_contactScale: Scales the maximum penetration depth.
        :param penetrationOffset: Distance at which there is no reaction force.
        """
        params = dict(
            d_relativeStiffness=d_relativeStiffness,
            d_attractionDistance=d_attractionDistance,
            d_normalsPointOut=d_normalsPointOut,
            d_contactScale=d_contactScale,
            penetrationOffset=penetrationOffset,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "EnslavementForceFeedback", params

    @sofa_component
    def NewOmniDriver(
        self,
        forceScale=None,
        scale=None,
        positionBase=None,
        orientationBase=None,
        positionTool=None,
        orientationTool=None,
        permanent=None,
        omniVisu=None,
        posDevice=None,
        posStylus=None,
        locDOF=None,
        deviceName=None,
        deviceIndex=None,
        openTool=None,
        maxTool=None,
        minTool=None,
        openSpeedTool=None,
        closeSpeedTool=None,
        useScheduler=None,
        setRestShape=None,
        applyMappings=None,
        alignOmniWithCamera=None,
        stateButton1=None,
        stateButton2=None,
        **kwargs
    ):
        """
        NewOmniDriver

        :param forceScale: Default forceScale applied to the force feedback.
        :param scale: Default scale applied to the Phantom Coordinates.
        :param positionBase: Position of the interface base in the scene world coordinates
        :param orientationBase: Orientation of the interface base in the scene world coordinates
        :param positionTool: Position of the tool in the omni end effector frame
        :param orientationTool: Orientation of the tool in the omni end effector frame
        :param permanent: Apply the force feedback permanently
        :param omniVisu: Visualize the position of the interface in the virtual scene
        :param posDevice: position of the base of the part of the device
        :param posStylus: position of the base of the stylus
        :param locDOF: localisation of the DOFs MechanicalObject
        :param deviceName: name of the device
        :param deviceIndex: index of the device
        :param openTool: opening of the tool
        :param maxTool: maxTool value
        :param minTool: minTool value
        :param openSpeedTool: openSpeedTool value
        :param closeSpeedTool: closeSpeedTool value
        :param useScheduler: Enable use of OpenHaptics Scheduler methods to synchronize haptics thread
        :param setRestShape: True to control the rest position instead of the current position directly
        :param applyMappings: True to enable applying the mappings after setting the position
        :param alignOmniWithCamera: True to keep the Omni's movements in the same reference frame as the camera
        :param stateButton1: True if the First button of the Omni is pressed
        :param stateButton2: True if the Second button of the Omni is pressed
        """
        params = dict(
            forceScale=forceScale,
            scale=scale,
            positionBase=positionBase,
            orientationBase=orientationBase,
            positionTool=positionTool,
            orientationTool=orientationTool,
            permanent=permanent,
            omniVisu=omniVisu,
            posDevice=posDevice,
            posStylus=posStylus,
            locDOF=locDOF,
            deviceName=deviceName,
            deviceIndex=deviceIndex,
            openTool=openTool,
            maxTool=maxTool,
            minTool=minTool,
            openSpeedTool=openSpeedTool,
            closeSpeedTool=closeSpeedTool,
            useScheduler=useScheduler,
            setRestShape=setRestShape,
            applyMappings=applyMappings,
            alignOmniWithCamera=alignOmniWithCamera,
            stateButton1=stateButton1,
            stateButton2=stateButton2,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "NewOmniDriver", params

    @sofa_component
    def OmniDriver(
        self,
        scale=None,
        forceScale=None,
        positionBase=None,
        orientationBase=None,
        positionTool=None,
        orientationTool=None,
        permanent=None,
        omniVisu=None,
        toolSelector=None,
        toolCount=None,
        **kwargs
    ):
        """
        OmniDriver

        :param scale: Default scale applied to the Phantom Coordinates.
        :param forceScale: Default forceScale applied to the force feedback.
        :param positionBase: Position of the interface base in the scene world coordinates
        :param orientationBase: Orientation of the interface base in the scene world coordinates
        :param positionTool: Position of the tool in the omni end effector frame
        :param orientationTool: Orientation of the tool in the omni end effector frame
        :param permanent: Apply the force feedback permanently
        :param omniVisu: Visualize the position of the interface in the virtual scene
        :param toolSelector: Switch tools with 2nd button
        :param toolCount: Number of tools to switch between
        """
        params = dict(
            scale=scale,
            forceScale=forceScale,
            positionBase=positionBase,
            orientationBase=orientationBase,
            positionTool=positionTool,
            orientationTool=orientationTool,
            permanent=permanent,
            omniVisu=omniVisu,
            toolSelector=toolSelector,
            toolCount=toolCount,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "OmniDriver", params

    @sofa_component
    def AssembledSystem(self, **kwargs):
        """
        AssembledSystem
        """
        params = dict()
        return "AssembledSystem", params

    @sofa_component
    def AssemblyVisitor(self, **kwargs):
        """
        AssemblyVisitor
        """
        params = dict()
        return "AssemblyVisitor", params

    @sofa_component
    def DampingCompliance(self, damping=None, **kwargs):
        """
        DampingCompliance

        :param damping: damping value
        """
        params = dict(damping=damping)
        params = {k: v for k, v in params.items() if v is not None}
        return "DampingCompliance", params

    @sofa_component
    def DiagonalCompliance(self, damping=None, **kwargs):
        """
        DiagonalCompliance

        :param damping: viscous damping.
        """
        params = dict(damping=damping)
        params = {k: v for k, v in params.items() if v is not None}
        return "DiagonalCompliance", params

    @sofa_component
    def LinearDiagonalCompliance(self, complianceMin=None, errorMin=None, **kwargs):
        """
        LinearDiagonalCompliance

        :param complianceMin: Minimum compliance
        :param errorMin: complianceMin is reached for this error value
        """
        params = dict(complianceMin=complianceMin, errorMin=errorMin)
        params = {k: v for k, v in params.items() if v is not None}
        return "LinearDiagonalCompliance", params

    @sofa_component
    def UniformCompliance(
        self, compliance=None, damping=None, resizable=None, **kwargs
    ):
        """
        UniformCompliance

        :param compliance: Compliance value uniformly applied to all the DOF.
        :param damping: uniform viscous damping.
        :param resizable: can the associated dofs can be resized? (in which case the matrices must be updated)
        """
        params = dict(compliance=compliance, damping=damping, resizable=resizable)
        params = {k: v for k, v in params.items() if v is not None}
        return "UniformCompliance", params

    @sofa_component
    def FullCompliance(self, C=None, K=None, damping=None, **kwargs):
        """
        FullCompliance

        :param C: Compliance Matrix (PSD)
        :param K: Stiffness Matrix (PSD)
        :param damping: uniform viscous damping.
        """
        params = dict(C=C, K=K, damping=damping)
        params = {k: v for k, v in params.items() if v is not None}
        return "FullCompliance", params

    @sofa_component
    def ClosureConstraint(self, **kwargs):
        """
        ClosureConstraint
        """
        params = dict()
        return "ClosureConstraint", params

    @sofa_component
    def Constraint(self, **kwargs):
        """
        Constraint
        """
        params = dict()
        return "Constraint", params

    @sofa_component
    def ConstraintValue(self, **kwargs):
        """
        ConstraintValue
        """
        params = dict()
        return "ConstraintValue", params

    @sofa_component
    def CoulombConstraint(self, **kwargs):
        """
        CoulombConstraint
        """
        params = dict()
        return "CoulombConstraint", params

    @sofa_component
    def DampingValue(self, **kwargs):
        """
        DampingValue
        """
        params = dict()
        return "DampingValue", params

    @sofa_component
    def HolonomicConstraintValue(self, **kwargs):
        """
        HolonomicConstraintValue
        """
        params = dict()
        return "HolonomicConstraintValue", params

    @sofa_component
    def OffsettedConstraintValue(self, offset=None, **kwargs):
        """
        OffsettedConstraintValue

        :param offset: Offset to add to the constraint value
        """
        params = dict(offset=offset)
        params = {k: v for k, v in params.items() if v is not None}
        return "OffsettedConstraintValue", params

    @sofa_component
    def ResistanceConstraint(self, threshold=None, **kwargs):
        """
        ResistanceConstraint

        :param threshold: The resistance force
        """
        params = dict(threshold=threshold)
        params = {k: v for k, v in params.items() if v is not None}
        return "ResistanceConstraint", params

    @sofa_component
    def Restitution(self, mask=None, restitution=None, **kwargs):
        """
        Restitution

        :param mask: violated constraint
        :param restitution: restitution coefficient
        """
        params = dict(mask=mask, restitution=restitution)
        params = {k: v for k, v in params.items() if v is not None}
        return "Restitution", params

    @sofa_component
    def Stabilization(self, mask=None, **kwargs):
        """
        Stabilization

        :param mask: dofs to be stabilized
        """
        params = dict(mask=mask)
        params = {k: v for k, v in params.items() if v is not None}
        return "Stabilization", params

    @sofa_component
    def UnilateralConstraint(self, **kwargs):
        """
        UnilateralConstraint
        """
        params = dict()
        return "UnilateralConstraint", params

    @sofa_component
    def VelocityConstraintValue(self, velocities=None, **kwargs):
        """
        VelocityConstraintValue

        :param velocities: The velocities to enforce
        """
        params = dict(velocities=velocities)
        params = {k: v for k, v in params.items() if v is not None}
        return "VelocityConstraintValue", params

    @sofa_component
    def BaumgarteStabilization(self, alpha=None, **kwargs):
        """
        BaumgarteStabilization

        :param alpha: The constraint violation coefficient
        """
        params = dict(alpha=alpha)
        params = {k: v for k, v in params.items() if v is not None}
        return "BaumgarteStabilization", params

    @sofa_component
    def CompliantContact(self, viscousFriction=None, **kwargs):
        """
        CompliantContact

        :param viscousFriction: 0 <= viscousFriction <= 1
        """
        params = dict(viscousFriction=viscousFriction)
        params = {k: v for k, v in params.items() if v is not None}
        return "CompliantContact", params

    @sofa_component
    def FrictionCompliantContact(
        self, mu=None, horizontal=None, frictionCoefficientMixingMethod=None, **kwargs
    ):
        """
        FrictionCompliantContact

        :param mu: global friction coefficient. Warning it overrides everything. (0 for frictionless contacts, <0 -default- to blend coefficients given in collision models)
        :param horizontal: horizontal cone projection, else orthogonal
        :param frictionCoefficientMixingMethod: how to blend the friction coefficients from two collision models?
        """
        params = dict(
            mu=mu,
            horizontal=horizontal,
            frictionCoefficientMixingMethod=frictionCoefficientMixingMethod,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "FrictionCompliantContact", params

    @sofa_component
    def PenaltyCompliantContact(self, stiffness=None, **kwargs):
        """
        PenaltyCompliantContact

        :param stiffness: Contact Stiffness
        """
        params = dict(stiffness=stiffness)
        params = {k: v for k, v in params.items() if v is not None}
        return "PenaltyCompliantContact", params

    @sofa_component
    def CompliantSleepController(self, **kwargs):
        """
        CompliantSleepController
        """
        params = dict()
        return "CompliantSleepController", params

    @sofa_component
    def PotentialEnergy(self, sign=None, **kwargs):
        """
        PotentialEnergy

        :param sign: scalar factor
        """
        params = dict(sign=sign)
        params = {k: v for k, v in params.items() if v is not None}
        return "PotentialEnergy", params

    @sofa_component
    def UniformLinearPotentialEnergy(self, factor=None, **kwargs):
        """
        UniformLinearPotentialEnergy

        :param factor: scalar factor
        """
        params = dict(factor=factor)
        params = {k: v for k, v in params.items() if v is not None}
        return "UniformLinearPotentialEnergy", params

    @sofa_component
    def CompliantPenaltyForceField(self, stiffness=None, damping=None, **kwargs):
        """
        CompliantPenaltyForceField

        :param stiffness: uniform stiffness value applied to all the DOF
        :param damping: uniform viscous damping
        """
        params = dict(stiffness=stiffness, damping=damping)
        params = {k: v for k, v in params.items() if v is not None}
        return "CompliantPenaltyForceField", params

    @sofa_component
    def UniformStiffness(self, stiffness=None, damping=None, resizable=None, **kwargs):
        """
        UniformStiffness

        :param stiffness: stiffness value uniformly applied to all the DOF.
        :param damping: uniform viscous damping.
        :param resizable: can the associated dofs can be resized? (in which case the matrices must be updated)
        """
        params = dict(stiffness=stiffness, damping=damping, resizable=resizable)
        params = {k: v for k, v in params.items() if v is not None}
        return "UniformStiffness", params

    @sofa_component
    def DiagonalStiffness(self, damping=None, **kwargs):
        """
        DiagonalStiffness

        :param damping: viscous damping.
        """
        params = dict(damping=damping)
        params = {k: v for k, v in params.items() if v is not None}
        return "DiagonalStiffness", params

    @sofa_component
    def AdditionMapping(
        self, pairs=None, showObjectScale=None, showColor=None, **kwargs
    ):
        """
        AdditionMapping

        :param pairs: index pairs for computing deltas
        :param showObjectScale: Scale for object display
        :param showColor: Color for object display. (default=[1.0,1.0,0.0,1.0])
        """
        params = dict(pairs=pairs, showObjectScale=showObjectScale, showColor=showColor)
        params = {k: v for k, v in params.items() if v is not None}
        return "AdditionMapping", params

    @sofa_component
    def AffineMultiMapping(self, matrix=None, value=None, **kwargs):
        """
        AffineMultiMapping

        :param matrix: matrix for the mapping (row-major)
        :param value: offset value
        """
        params = dict(matrix=matrix, value=value)
        params = {k: v for k, v in params.items() if v is not None}
        return "AffineMultiMapping", params

    @sofa_component
    def AssembledRigidRigidMapping(self, source=None, **kwargs):
        """
        AssembledRigidRigidMapping

        :param source: input dof and rigid offset for each output dof
        """
        params = dict(source=source)
        params = {k: v for k, v in params.items() if v is not None}
        return "AssembledRigidRigidMapping", params

    @sofa_component
    def ContactMapping(self, normal=None, **kwargs):
        """
        ContactMapping

        :param normal: contact normals
        """
        params = dict(normal=normal)
        params = {k: v for k, v in params.items() if v is not None}
        return "ContactMapping", params

    @sofa_component
    def DifferenceFromTargetMapping(
        self,
        indices=None,
        targets=None,
        targetIndices=None,
        inverted=None,
        showObjectScale=None,
        showColor=None,
        **kwargs
    ):
        """
        DifferenceFromTargetMapping

        :param indices: indices of the parent points
        :param targets: target positions which who computes deltas
        :param targetIndices: target indices in target positions which who computes deltas
        :param inverted: target-p (rather than p-target)
        :param showObjectScale: Scale for object display
        :param showColor: Color for object display. (default=[1.0,1.0,0.0,1.0])
        """
        params = dict(
            indices=indices,
            targets=targets,
            targetIndices=targetIndices,
            inverted=inverted,
            showObjectScale=showObjectScale,
            showColor=showColor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "DifferenceFromTargetMapping", params

    @sofa_component
    def DifferenceMapping(
        self, pairs=None, showObjectScale=None, showColor=None, **kwargs
    ):
        """
        DifferenceMapping

        :param pairs: index pairs for computing deltas
        :param showObjectScale: Scale for object display
        :param showColor: Color for object display. (default=[1.0,1.0,0.0,1.0])
        """
        params = dict(pairs=pairs, showObjectScale=showObjectScale, showColor=showColor)
        params = {k: v for k, v in params.items() if v is not None}
        return "DifferenceMapping", params

    @sofa_component
    def DotProductMapping(self, pairs=None, indices=None, targets=None, **kwargs):
        """
        DotProductMapping

        :param pairs: index pairs for computing deltas
        :param indices: indices of the dofs used to compute a dot product
        :param targets: targets to compute the dot products with
        """
        params = dict(pairs=pairs, indices=indices, targets=targets)
        params = {k: v for k, v in params.items() if v is not None}
        return "DotProductMapping", params

    @sofa_component
    def GearMapping(self, pairs=None, ratio=None, **kwargs):
        """
        GearMapping

        :param pairs: index pairs for computing deltas, 4 values per pair (dofindex0,kinematicdofindex0,dofindex1,kinematicdofindex1)
        :param ratio: gear link ratio (can be negative)
        """
        params = dict(pairs=pairs, ratio=ratio)
        params = {k: v for k, v in params.items() if v is not None}
        return "GearMapping", params

    @sofa_component
    def MaskMapping(self, **kwargs):
        """
        MaskMapping
        """
        params = dict()
        return "MaskMapping", params

    @sofa_component
    def NormalizationMapping(self, indices=None, **kwargs):
        """
        NormalizationMapping

        :param indices: indices of vector to normalize
        """
        params = dict(indices=indices)
        params = {k: v for k, v in params.items() if v is not None}
        return "NormalizationMapping", params

    @sofa_component
    def PairingMultiMapping(self, sign=None, **kwargs):
        """
        PairingMultiMapping

        :param sign: scalar factor
        """
        params = dict(sign=sign)
        params = {k: v for k, v in params.items() if v is not None}
        return "PairingMultiMapping", params

    @sofa_component
    def ProjectionMapping(self, **kwargs):
        """
        ProjectionMapping
        """
        params = dict()
        return "ProjectionMapping", params

    @sofa_component
    def QuadraticMapping(self, stiffness=None, **kwargs):
        """
        QuadraticMapping

        :param stiffness: scalar factor
        """
        params = dict(stiffness=stiffness)
        params = {k: v for k, v in params.items() if v is not None}
        return "QuadraticMapping", params

    @sofa_component
    def RigidComMultiMapping(self, **kwargs):
        """
        RigidComMultiMapping
        """
        params = dict()
        return "RigidComMultiMapping", params

    @sofa_component
    def RigidJointMapping(self, pairs=None, rotation=None, translation=None, **kwargs):
        """
        RigidJointMapping

        :param pairs: pairs of rigid frames defining joint in source dofs
        :param rotation: compute relative rotation
        :param translation: compute relative translation
        """
        params = dict(pairs=pairs, rotation=rotation, translation=translation)
        params = {k: v for k, v in params.items() if v is not None}
        return "RigidJointMapping", params

    @sofa_component
    def RigidRestJointMapping(self, rotation=None, translation=None, **kwargs):
        """
        RigidRestJointMapping

        :param rotation: compute relative rotation
        :param translation: compute relative translation
        """
        params = dict(rotation=rotation, translation=translation)
        params = {k: v for k, v in params.items() if v is not None}
        return "RigidRestJointMapping", params

    @sofa_component
    def RigidJointMultiMapping(self, pairs=None, **kwargs):
        """
        RigidJointMultiMapping

        :param pairs: index pairs (parent, child) for each joint
        """
        params = dict(pairs=pairs)
        params = {k: v for k, v in params.items() if v is not None}
        return "RigidJointMultiMapping", params

    @sofa_component
    def RigidJointFromTargetMapping(
        self, targets=None, rotation=None, translation=None, **kwargs
    ):
        """
        RigidJointFromTargetMapping

        :param targets: target positions which who computes deltas
        :param rotation: compute relative rotation
        :param translation: compute relative translation
        """
        params = dict(targets=targets, rotation=rotation, translation=translation)
        params = {k: v for k, v in params.items() if v is not None}
        return "RigidJointFromTargetMapping", params

    @sofa_component
    def SafeDistanceMapping(
        self,
        pairs=None,
        restLengths=None,
        epsilonLength=None,
        geometricStiffness=None,
        showObjectScale=None,
        showColor=None,
        indices=None,
        targets=None,
        directions=None,
        **kwargs
    ):
        """
        SafeDistanceMapping

        :param pairs: index pairs for computing distance
        :param restLengths: rest lengths
        :param epsilonLength: Threshold to consider a length too close to 0
        :param geometricStiffness: 0 -> no GS, 1 -> exact GS, 2 -> stabilized GS (default)
        :param showObjectScale: Scale for object display
        :param showColor: Color for object display
        :param indices: index of dof to compute the distance
        :param targets: positions the distances are measured from
        :param directions: Given directions (must be colinear with the vector formed by the points)
        """
        params = dict(
            pairs=pairs,
            restLengths=restLengths,
            epsilonLength=epsilonLength,
            geometricStiffness=geometricStiffness,
            showObjectScale=showObjectScale,
            showColor=showColor,
            indices=indices,
            targets=targets,
            directions=directions,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SafeDistanceMapping", params

    @sofa_component
    def CompliantAttachButtonSetting(
        self,
        compliance=None,
        isCompliance=None,
        arrowSize=None,
        color=None,
        visualmodel=None,
        **kwargs
    ):
        """
        CompliantAttachButtonSetting

        :param compliance: Compliance of the manipulator. 0 is rigid, the bigger the softer. Negative values make no sense.
        :param isCompliance: Is the mouse interaction treated as a compliance? (otherwise as a stiffness)
        :param arrowSize:
        :param color:
        :param visualmodel:
        """
        params = dict(
            compliance=compliance,
            isCompliance=isCompliance,
            arrowSize=arrowSize,
            color=color,
            visualmodel=visualmodel,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CompliantAttachButtonSetting", params

    @sofa_component
    def CompliantSolverMerger(self, **kwargs):
        """
        CompliantSolverMerger
        """
        params = dict()
        return "CompliantSolverMerger", params

    @sofa_component
    def FailNode(self, **kwargs):
        """
        FailNode
        """
        params = dict()
        return "FailNode", params

    @sofa_component
    def RigidMass(
        self, mass=None, inertia=None, inertia_forces=None, draw=None, **kwargs
    ):
        """
        RigidMass

        :param mass: mass of each rigid body
        :param inertia: inertia of each rigid body
        :param inertia_forces: compute (explicit) inertia forces
        :param draw: debug drawing of the inertia matrix
        """
        params = dict(
            mass=mass, inertia=inertia, inertia_forces=inertia_forces, draw=draw
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "RigidMass", params

    @sofa_component
    def SimpleAnimationLoop(self, **kwargs):
        """
        SimpleAnimationLoop
        """
        params = dict()
        return "SimpleAnimationLoop", params

    @sofa_component
    def AnalysisSolver(self, condest=None, eigenvaluesign=None, dump_qp=None, **kwargs):
        """
        AnalysisSolver

        :param condest: compute condition number with svd
        :param eigenvaluesign: computing the sign of the eigenvalues (of the implicit matrix H)
        :param dump_qp: dump qp to file if non-empty
        """
        params = dict(condest=condest, eigenvaluesign=eigenvaluesign, dump_qp=dump_qp)
        params = {k: v for k, v in params.items() if v is not None}
        return "AnalysisSolver", params

    @sofa_component
    def Benchmark(
        self,
        factor=None,
        primal=None,
        dual=None,
        complementarity=None,
        optimality=None,
        duration=None,
        **kwargs
    ):
        """
        Benchmark

        :param factor: time elapsed during factor
        :param primal: primal error
        :param dual: dual error
        :param complementarity: complementarity error
        :param optimality: optimality error
        :param duration: cumulated solve time
        """
        params = dict(
            factor=factor,
            primal=primal,
            dual=dual,
            complementarity=complementarity,
            optimality=optimality,
            duration=duration,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "Benchmark", params

    @sofa_component
    def BenchmarkSolver(self, **kwargs):
        """
        BenchmarkSolver
        """
        params = dict()
        return "BenchmarkSolver", params

    @sofa_component
    def BiCgStabSolver(self, **kwargs):
        """
        BiCgStabSolver
        """
        params = dict()
        return "BiCgStabSolver", params

    @sofa_component
    def CgSolver(self, **kwargs):
        """
        CgSolver
        """
        params = dict()
        return "CgSolver", params

    @sofa_component
    def DiagonalResponse(self, constant=None, **kwargs):
        """
        DiagonalResponse

        :param constant: reuse first factorization
        """
        params = dict(constant=constant)
        params = {k: v for k, v in params.items() if v is not None}
        return "DiagonalResponse", params

    @sofa_component
    def EigenSparseResponse(
        self,
        regularize=None,
        constant=None,
        trackSparsityPattern=None,
        iterations=None,
        tolerance=None,
        **kwargs
    ):
        """
        EigenSparseResponse

        :param regularize: add identity*regularize to matrix H to make it definite.
        :param constant: reuse first factorization
        :param trackSparsityPattern: if the sparsity pattern remains similar from one step to the other, the factorization can be faster
        :param iterations: max iterations
        :param tolerance: tolerance
        """
        params = dict(
            regularize=regularize,
            constant=constant,
            trackSparsityPattern=trackSparsityPattern,
            iterations=iterations,
            tolerance=tolerance,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "EigenSparseResponse", params

    @sofa_component
    def EigenSparseSolver(
        self,
        regularization=None,
        trackSparsityPattern=None,
        iterations=None,
        tolerance=None,
        **kwargs
    ):
        """
        EigenSparseSolver

        :param regularization: Optional diagonal Tikhonov regularization on constraints
        :param trackSparsityPattern: if the sparsity pattern remains similar from one step to the other, the factorization can be faster
        :param iterations: max iterations
        :param tolerance: tolerance
        """
        params = dict(
            regularization=regularization,
            trackSparsityPattern=trackSparsityPattern,
            iterations=iterations,
            tolerance=tolerance,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "EigenSparseSolver", params

    @sofa_component
    def IterativeSolver(self, relative=None, **kwargs):
        """
        IterativeSolver

        :param relative: use relative precision
        """
        params = dict(relative=relative)
        params = {k: v for k, v in params.items() if v is not None}
        return "IterativeSolver", params

    @sofa_component
    def KrylovSolver(self, verbose=None, restart=None, parallel=None, **kwargs):
        """
        KrylovSolver

        :param verbose: print debug stuff on std::cerr
        :param restart: restart every n steps
        :param parallel: use openmp to parallelize matrix-vector products when use_schur is false (parallelization per KKT blocks, 4 threads)
        """
        params = dict(verbose=verbose, restart=restart, parallel=parallel)
        params = {k: v for k, v in params.items() if v is not None}
        return "KrylovSolver", params

    @sofa_component
    def LumpedResponse(self, **kwargs):
        """
        LumpedResponse
        """
        params = dict()
        return "LumpedResponse", params

    @sofa_component
    def MinresSolver(self, **kwargs):
        """
        MinresSolver
        """
        params = dict()
        return "MinresSolver", params

    @sofa_component
    def ModulusSolver(self, **kwargs):
        """
        ModulusSolver
        """
        params = dict()
        return "ModulusSolver", params

    @sofa_component
    def NNCGSolver(self, verbose=None, **kwargs):
        """
        NNCGSolver

        :param verbose: print stuff
        """
        params = dict(verbose=verbose)
        params = {k: v for k, v in params.items() if v is not None}
        return "NNCGSolver", params

    @sofa_component
    def PreconditionedCgSolver(self, **kwargs):
        """
        PreconditionedCgSolver
        """
        params = dict()
        return "PreconditionedCgSolver", params

    @sofa_component
    def PreconditionedSolver(self, **kwargs):
        """
        PreconditionedSolver
        """
        params = dict()
        return "PreconditionedSolver", params

    @sofa_component
    def SequentialSolver(
        self, omega=None, iterateOnBilaterals=None, regularization=None, **kwargs
    ):
        """
        SequentialSolver

        :param omega: SOR parameter:  omega < 1 : better, slower convergence, omega = 1 : vanilla gauss-seidel, 2 > omega > 1 : faster convergence, ok for SPD systems, omega > 2 : will probably explode
        :param iterateOnBilaterals: Should the bilateral constraint must be solved iteratively or factorized with the dynamics?
        :param regularization: Optional diagonal Tikhonov regularization on bilateral constraints
        """
        params = dict(
            omega=omega,
            iterateOnBilaterals=iterateOnBilaterals,
            regularization=regularization,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SequentialSolver", params

    @sofa_component
    def SubKKT(self, **kwargs):
        """
        SubKKT
        """
        params = dict()
        return "SubKKT", params

    @sofa_component
    def CompliantImplicitSolver(self, **kwargs):
        """
        CompliantImplicitSolver
        """
        params = dict()
        return "CompliantImplicitSolver", params

    @sofa_component
    def CompliantNLImplicitSolver(self, relative=None, **kwargs):
        """
        CompliantNLImplicitSolver

        :param relative: use relative precision
        """
        params = dict(relative=relative)
        params = {k: v for k, v in params.items() if v is not None}
        return "CompliantNLImplicitSolver", params

    @sofa_component
    def CompliantPostStabilizationAnimationLoop(self, **kwargs):
        """
        CompliantPostStabilizationAnimationLoop
        """
        params = dict()
        return "CompliantPostStabilizationAnimationLoop", params

    @sofa_component
    def CompliantPseudoStaticSolver(self, **kwargs):
        """
        CompliantPseudoStaticSolver
        """
        params = dict()
        return "CompliantPseudoStaticSolver", params

    @sofa_component
    def CompliantStaticSolver(
        self, epsilon=None, conjugate=None, ls_precision=None, **kwargs
    ):
        """
        CompliantStaticSolver

        :param epsilon: division by zero threshold
        :param conjugate: conjugate descent directions
        :param ls_precision: line search precision
        """
        params = dict(epsilon=epsilon, conjugate=conjugate, ls_precision=ls_precision)
        params = {k: v for k, v in params.items() if v is not None}
        return "CompliantStaticSolver", params

    @sofa_component
    def ConstantCompliantImplicitSolver(self, **kwargs):
        """
        ConstantCompliantImplicitSolver
        """
        params = dict()
        return "ConstantCompliantImplicitSolver", params

    @sofa_component
    def CompliantJacobiPreconditioner(self, **kwargs):
        """
        CompliantJacobiPreconditioner
        """
        params = dict()
        return "CompliantJacobiPreconditioner", params

    @sofa_component
    def CompliantLDLTPreconditioner(self, **kwargs):
        """
        CompliantLDLTPreconditioner
        """
        params = dict()
        return "CompliantLDLTPreconditioner", params

    @sofa_component
    def IncompleteCholeskyPreconditioner(self, constant=None, shift=None, **kwargs):
        """
        IncompleteCholeskyPreconditioner

        :param constant: reuse first factorization
        :param shift: initial shift
        """
        params = dict(constant=constant, shift=shift)
        params = {k: v for k, v in params.items() if v is not None}
        return "IncompleteCholeskyPreconditioner", params

    @sofa_component
    def anderson(self, **kwargs):
        """
        anderson
        """
        params = dict()
        return "anderson", params

    @sofa_component
    def nlnscg(self, **kwargs):
        """
        nlnscg
        """
        params = dict()
        return "nlnscg", params

    @sofa_component
    def sub_kkt(self, **kwargs):
        """
        sub_kkt
        """
        params = dict()
        return "sub_kkt", params

    @sofa_component
    def PythonMultiMapping(
        self, apply_callback=None, jacobian_callback=None, gs_callback=None, **kwargs
    ):
        """
        PythonMultiMapping

        :param apply_callback: apply callback
        :param jacobian_callback: jacobian callback
        :param gs_callback: geometric stiffness callback
        """
        params = dict(
            apply_callback=apply_callback,
            jacobian_callback=jacobian_callback,
            gs_callback=gs_callback,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PythonMultiMapping", params

    @sofa_component
    def Binding_AssembledSystem(self, **kwargs):
        """
        Binding_AssembledSystem
        """
        params = dict()
        return "Binding_AssembledSystem", params

    @sofa_component
    def python(self, **kwargs):
        """
        python
        """
        params = dict()
        return "python", params

    @sofa_component
    def QCompliantMouseOperations(self, **kwargs):
        """
        QCompliantMouseOperations
        """
        params = dict()
        return "QCompliantMouseOperations", params

    @sofa_component
    def CompliantAttachPerformer(self, **kwargs):
        """
        CompliantAttachPerformer
        """
        params = dict()
        return "CompliantAttachPerformer", params

    @sofa_component
    def GetAssembledSizeVisitor(self, **kwargs):
        """
        GetAssembledSizeVisitor
        """
        params = dict()
        return "GetAssembledSizeVisitor", params

    @sofa_component
    def GetVectorVisitor(self, **kwargs):
        """
        GetVectorVisitor
        """
        params = dict()
        return "GetVectorVisitor", params

    @sofa_component
    def SceneCreator(self, **kwargs):
        """
        SceneCreator
        """
        params = dict()
        return "SceneCreator", params

    @sofa_component
    def SceneUtils(self, **kwargs):
        """
        SceneUtils
        """
        params = dict()
        return "SceneUtils", params

    @sofa_component
    def OptiTrackNatNetClient(
        self,
        serverName=None,
        clientName=None,
        scale=None,
        trackedMarkers=None,
        otherMarkers=None,
        drawTrackedMarkersSize=None,
        drawTrackedMarkersColor=None,
        drawOtherMarkersSize=None,
        drawOtherMarkersColor=None,
        **kwargs
    ):
        """
        OptiTrackNatNetClient

        :param serverName: NatNet server address (default to localhost)
        :param clientName: IP to bind this client to (default to localhost)
        :param scale: Scale factor to apply to coordinates (using the global frame as fixed point)
        :param trackedMarkers: Position of received known markers
        :param otherMarkers: Position of received unknown markers
        :param drawTrackedMarkersSize: Size of displayed markers
        :param drawTrackedMarkersColor: Color of displayed markers
        :param drawOtherMarkersSize: Size of displayed unknown markers
        :param drawOtherMarkersColor: Color of displayed unknown markers
        """
        params = dict(
            serverName=serverName,
            clientName=clientName,
            scale=scale,
            trackedMarkers=trackedMarkers,
            otherMarkers=otherMarkers,
            drawTrackedMarkersSize=drawTrackedMarkersSize,
            drawTrackedMarkersColor=drawTrackedMarkersColor,
            drawOtherMarkersSize=drawOtherMarkersSize,
            drawOtherMarkersColor=drawOtherMarkersColor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "OptiTrackNatNetClient", params

    @sofa_component
    def OptiTrackNatNetDevice(
        self,
        trackableName=None,
        trackableID=None,
        setRestShape=None,
        applyMappings=None,
        controlNode=None,
        isGlobalFrame=None,
        inMarkersMeshFile=None,
        simMarkersMeshFile=None,
        tracked=None,
        trackedFrame=None,
        frame=None,
        position=None,
        orientation=None,
        simGlobalFrame=None,
        inGlobalFrame=None,
        simLocalFrame=None,
        inLocalFrame=None,
        markers=None,
        markersID=None,
        markersSize=None,
        distanceMarkersID=None,
        distanceMarkersPos=None,
        openDistance=None,
        closedDistance=None,
        distance=None,
        distanceFactor=None,
        open=None,
        closed=None,
        jointCenter=None,
        jointAxis=None,
        jointOpenAngle=None,
        jointClosedAngle=None,
        drawAxisSize=None,
        drawMarkersSize=None,
        drawMarkersIDSize=None,
        drawMarkersColor=None,
        **kwargs
    ):
        """
        OptiTrackNatNetDevice

        :param trackableName: NatNet trackable name
        :param trackableID: NatNet trackable number (ignored if trackableName is set)
        :param setRestShape: True to control the rest position instead of the current position directly
        :param applyMappings: True to enable applying the mappings after setting the position
        :param controlNode: True to enable activating and disabling the node when this device appears and disappears
        :param isGlobalFrame: True if this trackable should be considered as the global frame (i.e. all other trackables are computed relative to its position). This requires linking other trackables' inGlobalFrame to this frame)
        :param inMarkersMeshFile: OBJ file where markers in the object's input local frame are written. This file is created if it does not exist and/or when Ctrl+M is pressed
        :param simMarkersMeshFile: OBJ file where markers in the object's simulation local frame are loaded. If this file does exist, it is used to compute transformation applied to tracked frame (inLocalFrame/simLocalFrame)
        :param tracked: Output: true when this device is visible and tracked by the cameras
        :param trackedFrame: Output: rigid frame, as given by OptiTrack
        :param frame: Output: rigid frame
        :param position: Output: rigid position (Vec3)
        :param orientation: Output: rigid orientation (Quat)
        :param simGlobalFrame: Input: world position and orientation of the reference point in the simulation
        :param inGlobalFrame: Input: world position and orientation of the reference point in the real (camera) space
        :param simLocalFrame: Input: position and orientation of the center of the simulated object in the simulation
        :param inLocalFrame: Input: position and orientation of the center of the simulated object in the real (camera) space
        :param markers: Output: markers as tracked by the cameras
        :param markersID: Output: markers IDs
        :param markersSize: Output: markers sizes
        :param distanceMarkersID: Input: ID of markers ID used to measure distance (for articulated instruments)
        :param distanceMarkersPos: Output: Positions of markers used to measure distance (for articulated instruments)
        :param openDistance: Input: Distance considered as open
        :param closedDistance: Input: Distance considered as closed
        :param distance: Output: Measured distance
        :param distanceFactor: Output: distance factor (0 = closed, 1 = open)
        :param open: Output: true if measured distance is above openDistance
        :param closed: Output: true if measured distance is below closedDistance
        :param jointCenter: Input: rotation center (for articulated instruments)
        :param jointAxis: Input: rotation axis (for articulated instruments)
        :param jointOpenAngle: Input: rotation angle when opened (for articulated instruments)
        :param jointClosedAngle: Input: rotation angle when closed (for articulated instruments)
        :param drawAxisSize: Size of displayed axis
        :param drawMarkersSize: Size of displayed markers
        :param drawMarkersIDSize: Size of displayed markers ID
        :param drawMarkersColor: Color of displayed markers
        """
        params = dict(
            trackableName=trackableName,
            trackableID=trackableID,
            setRestShape=setRestShape,
            applyMappings=applyMappings,
            controlNode=controlNode,
            isGlobalFrame=isGlobalFrame,
            inMarkersMeshFile=inMarkersMeshFile,
            simMarkersMeshFile=simMarkersMeshFile,
            tracked=tracked,
            trackedFrame=trackedFrame,
            frame=frame,
            position=position,
            orientation=orientation,
            simGlobalFrame=simGlobalFrame,
            inGlobalFrame=inGlobalFrame,
            simLocalFrame=simLocalFrame,
            inLocalFrame=inLocalFrame,
            markers=markers,
            markersID=markersID,
            markersSize=markersSize,
            distanceMarkersID=distanceMarkersID,
            distanceMarkersPos=distanceMarkersPos,
            openDistance=openDistance,
            closedDistance=closedDistance,
            distance=distance,
            distanceFactor=distanceFactor,
            open=open,
            closed=closed,
            jointCenter=jointCenter,
            jointAxis=jointAxis,
            jointOpenAngle=jointOpenAngle,
            jointClosedAngle=jointClosedAngle,
            drawAxisSize=drawAxisSize,
            drawMarkersSize=drawMarkersSize,
            drawMarkersIDSize=drawMarkersIDSize,
            drawMarkersColor=drawMarkersColor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "OptiTrackNatNetDevice", params

    @sofa_component
    def PersistentContactBarycentricMapping(self, **kwargs):
        """
        PersistentContactBarycentricMapping
        """
        params = dict()
        return "PersistentContactBarycentricMapping", params

    @sofa_component
    def PersistentContactMapping(self, nameOfInputMap=None, **kwargs):
        """
        PersistentContactMapping

        :param nameOfInputMap: if contactDuplicate == true, it provides the name of the input mapping
        """
        params = dict(nameOfInputMap=nameOfInputMap)
        params = {k: v for k, v in params.items() if v is not None}
        return "PersistentContactMapping", params

    @sofa_component
    def PersistentContactRigidMapping(self, **kwargs):
        """
        PersistentContactRigidMapping
        """
        params = dict()
        return "PersistentContactRigidMapping", params

    @sofa_component
    def PersistentFrictionContact(self, **kwargs):
        """
        PersistentFrictionContact
        """
        params = dict()
        return "PersistentFrictionContact", params

    @sofa_component
    def PersistentUnilateralInteractionConstraint(self, **kwargs):
        """
        PersistentUnilateralInteractionConstraint
        """
        params = dict()
        return "PersistentUnilateralInteractionConstraint", params

    @sofa_component
    def CarvingManager(
        self,
        toolModelPath=None,
        surfaceModelPath=None,
        carvingDistance=None,
        active=None,
        key=None,
        keySwitch=None,
        mouseEvent=None,
        omniEvent=None,
        activatorName=None,
        **kwargs
    ):
        """
        CarvingManager

        :param toolModelPath: Tool model path
        :param surfaceModelPath: TriangleSetModel or SphereCollisionModel<sofa::defaulttype::Vec3Types> path
        :param carvingDistance: Collision distance at which cavring will start. Equal to contactDistance by default.
        :param active: Activate this object.\nNote that this can be dynamically controlled by using a key
        :param key: key to press to activate this object until the key is released
        :param keySwitch: key to activate this object until the key is pressed again
        :param mouseEvent: Activate carving with middle mouse button
        :param omniEvent: Activate carving with omni button
        :param activatorName: Name to active the script event parsing. Will look for 'pressed' or 'release' keyword. For example: 'button1_pressed'
        """
        params = dict(
            toolModelPath=toolModelPath,
            surfaceModelPath=surfaceModelPath,
            carvingDistance=carvingDistance,
            active=active,
            key=key,
            keySwitch=keySwitch,
            mouseEvent=mouseEvent,
            omniEvent=omniEvent,
            activatorName=activatorName,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CarvingManager", params

    @sofa_component
    def BaseDeformationMapping(
        self,
        shapeFunction=None,
        indices=None,
        weights=None,
        weightGradients=None,
        weightHessians=None,
        M=None,
        cell=None,
        assemble=None,
        restPosition=None,
        showDeformationGradientScale=None,
        showDeformationGradientStyle=None,
        showColorOnTopology=None,
        showColorScale=None,
        geometricStiffness=None,
        parallel=None,
        **kwargs
    ):
        """
        BaseDeformationMapping

        :param shapeFunction: name of shape function (optional)
        :param indices: parent indices for each child
        :param weights: influence weights of the Dofs
        :param weightGradients: weight gradients
        :param weightHessians: weight Hessians
        :param M: Linear transformations from material to 3d space
        :param cell: indices required by shape function in case of overlapping elements
        :param assemble: Assemble the matrices (Jacobian/Geometric Stiffness) or use optimized Jacobian/vector multiplications
        :param restPosition: initial spatial positions of children
        :param showDeformationGradientScale: Scale for deformation gradient display
        :param showDeformationGradientStyle: Visualization style for deformation gradients
        :param showColorOnTopology: Color mapping method
        :param showColorScale: Color mapping scale
        :param geometricStiffness: 0=no GS, 1=non symmetric, 2=symmetrized
        :param parallel: use openmp parallelisation?
        """
        params = dict(
            shapeFunction=shapeFunction,
            indices=indices,
            weights=weights,
            weightGradients=weightGradients,
            weightHessians=weightHessians,
            M=M,
            cell=cell,
            assemble=assemble,
            restPosition=restPosition,
            showDeformationGradientScale=showDeformationGradientScale,
            showDeformationGradientStyle=showDeformationGradientStyle,
            showColorOnTopology=showColorOnTopology,
            showColorScale=showColorScale,
            geometricStiffness=geometricStiffness,
            parallel=parallel,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "BaseDeformationMapping", params

    @sofa_component
    def BaseDeformationMultiMapping(
        self,
        shapeFunction=None,
        indices=None,
        indices1=None,
        indices2=None,
        weights=None,
        weightGradients=None,
        weightHessians=None,
        M=None,
        cell=None,
        assemble=None,
        restPosition=None,
        showDeformationGradientScale=None,
        showDeformationGradientStyle=None,
        showColorOnTopology=None,
        showColorScale=None,
        geometricStiffness=None,
        parallel=None,
        **kwargs
    ):
        """
        BaseDeformationMultiMapping

        :param shapeFunction: name of shape function (optional)
        :param indices: parent indices for each child
        :param indices1: parent1 indices for each child
        :param indices2: parent2 indices for each child
        :param weights: influence weights of the Dofs
        :param weightGradients: weight gradients
        :param weightHessians: weight Hessians
        :param M: Linear transformations from material to 3d space
        :param cell: indices required by shape function in case of overlapping elements
        :param assemble: Assemble the matrices (Jacobian/Geometric Stiffness) or use optimized Jacobian/vector multiplications
        :param restPosition: initial spatial positions of children
        :param showDeformationGradientScale: Scale for deformation gradient display
        :param showDeformationGradientStyle: Visualization style for deformation gradients
        :param showColorOnTopology: Color mapping method
        :param showColorScale: Color mapping scale
        :param geometricStiffness: 0=no GS, 1=non symmetric, 2=symmetrized
        :param parallel: use openmp parallelisation?
        """
        params = dict(
            shapeFunction=shapeFunction,
            indices=indices,
            indices1=indices1,
            indices2=indices2,
            weights=weights,
            weightGradients=weightGradients,
            weightHessians=weightHessians,
            M=M,
            cell=cell,
            assemble=assemble,
            restPosition=restPosition,
            showDeformationGradientScale=showDeformationGradientScale,
            showDeformationGradientStyle=showDeformationGradientStyle,
            showColorOnTopology=showColorOnTopology,
            showColorScale=showColorScale,
            geometricStiffness=geometricStiffness,
            parallel=parallel,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "BaseDeformationMultiMapping", params

    @sofa_component
    def CorotationalMeshMapping(
        self,
        inputTetrahedra=None,
        inputHexahedra=None,
        inputTriangles=None,
        inputQuads=None,
        inputEdges=None,
        tetrahedra=None,
        hexahedra=None,
        triangles=None,
        quads=None,
        edges=None,
        **kwargs
    ):
        """
        CorotationalMeshMapping

        :param inputTetrahedra: input tetrahedra
        :param inputHexahedra: input hexahedra
        :param inputTriangles: input triangles
        :param inputQuads: input quads
        :param inputEdges: input edges
        :param tetrahedra: output tetrahedra
        :param hexahedra: output hexahedra
        :param triangles: output triangles
        :param quads: output quads
        :param edges: output edges
        """
        params = dict(
            inputTetrahedra=inputTetrahedra,
            inputHexahedra=inputHexahedra,
            inputTriangles=inputTriangles,
            inputQuads=inputQuads,
            inputEdges=inputEdges,
            tetrahedra=tetrahedra,
            hexahedra=hexahedra,
            triangles=triangles,
            quads=quads,
            edges=edges,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CorotationalMeshMapping", params

    @sofa_component
    def TetrahedronVolumeMapping(self, offsets=None, volumePerNodes=None, **kwargs):
        """
        TetrahedronVolumeMapping

        :param offsets: offsets removed from output volume
        :param volumePerNodes: Dispatch the volume on nodes
        """
        params = dict(offsets=offsets, volumePerNodes=volumePerNodes)
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedronVolumeMapping", params

    @sofa_component
    def TriangleDeformationMapping(self, restLengths=None, scaleView=None, **kwargs):
        """
        TriangleDeformationMapping

        :param restLengths: Rest lengths of the connections.
        :param scaleView: Scale the display of the deformation gradients.
        """
        params = dict(restLengths=restLengths, scaleView=scaleView)
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangleDeformationMapping", params

    @sofa_component
    def TriangleStrainAverageMapping(
        self, triangleIndices=None, endIndices=None, weights=None, **kwargs
    ):
        """
        TriangleStrainAverageMapping

        :param triangleIndices: For each node, index of the adjacent triangles.
        :param endIndices: For each node, end index of its triangle list
        :param weights: For each node, weight of each triangle in the average
        """
        params = dict(
            triangleIndices=triangleIndices, endIndices=endIndices, weights=weights
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangleStrainAverageMapping", params

    @sofa_component
    def VolumeMapping(
        self, offset=None, nbMeshes=None, geometricStiffness=None, **kwargs
    ):
        """
        VolumeMapping

        :param offset: offsets added to output volumes
        :param nbMeshes: number of meshes to compute the volume for
        :param geometricStiffness: Should geometricStiffness be considered?
        """
        params = dict(
            offset=offset, nbMeshes=nbMeshes, geometricStiffness=geometricStiffness
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "VolumeMapping", params

    @sofa_component
    def ComputeDualQuatEngine(self, x0=None, x=None, dualQuats=None, **kwargs):
        """
        ComputeDualQuatEngine

        :param x0: Rest position
        :param x: Current position
        :param dualQuats: Dual quaternions, computed from x (or x*x0^-1 if x0 is provided). DualQuats are stored as two vec4f elements, first the orientation, then the dual.
        """
        params = dict(x0=x0, x=x, dualQuats=dualQuats)
        params = {k: v for k, v in params.items() if v is not None}
        return "ComputeDualQuatEngine", params

    @sofa_component
    def ComputeWeightEngine(self, indices=None, weights=None, **kwargs):
        """
        ComputeWeightEngine

        :param indices: Indices
        :param weights: Weights
        """
        params = dict(indices=indices, weights=weights)
        params = {k: v for k, v in params.items() if v is not None}
        return "ComputeWeightEngine", params

    @sofa_component
    def FlexibleCorotationalFEMForceField(
        self,
        method=None,
        order=None,
        youngModulus=None,
        poissonRatio=None,
        viscosity=None,
        geometricStiffness=None,
        **kwargs
    ):
        """
        FlexibleCorotationalFEMForceField

        :param method: Decomposition method
        :param order: Order of quadrature method
        :param youngModulus: Young Modulus
        :param poissonRatio: Poisson Ratio
        :param viscosity: Viscosity (stress/strainRate)
        :param geometricStiffness: Should geometricStiffness be considered?
        """
        params = dict(
            method=method,
            order=order,
            youngModulus=youngModulus,
            poissonRatio=poissonRatio,
            viscosity=viscosity,
            geometricStiffness=geometricStiffness,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "FlexibleCorotationalFEMForceField", params

    @sofa_component
    def FlexibleCorotationalMeshFEMForceField(
        self,
        method=None,
        order=None,
        youngModulus=None,
        poissonRatio=None,
        viscosity=None,
        geometricStiffness=None,
        **kwargs
    ):
        """
        FlexibleCorotationalMeshFEMForceField

        :param method: Decomposition method
        :param order: Order of quadrature method
        :param youngModulus: Young Modulus
        :param poissonRatio: Poisson Ratio
        :param viscosity: Viscosity (stress/strainRate)
        :param geometricStiffness: Should geometricStiffness be considered?
        """
        params = dict(
            method=method,
            order=order,
            youngModulus=youngModulus,
            poissonRatio=poissonRatio,
            viscosity=viscosity,
            geometricStiffness=geometricStiffness,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "FlexibleCorotationalMeshFEMForceField", params

    @sofa_component
    def AffineMass(self, massMatrix=None, **kwargs):
        """
        AffineMass

        :param massMatrix: Mass Matrix
        """
        params = dict(massMatrix=massMatrix)
        params = {k: v for k, v in params.items() if v is not None}
        return "AffineMass", params

    @sofa_component
    def BaseMaterialForceField(self, assemble=None, **kwargs):
        """
        BaseMaterialForceField

        :param assemble: Assemble the needed material matrices (compliance C,stiffness K,damping B)
        """
        params = dict(assemble=assemble)
        params = {k: v for k, v in params.items() if v is not None}
        return "BaseMaterialForceField", params

    @sofa_component
    def HEMLStVKForceField(self, youngModulus=None, poissonRatio=None, **kwargs):
        """
        HEMLStVKForceField

        :param youngModulus: Young Modulus
        :param poissonRatio: Poisson Ratio ]-1,0.5[
        """
        params = dict(youngModulus=youngModulus, poissonRatio=poissonRatio)
        params = {k: v for k, v in params.items() if v is not None}
        return "HEMLStVKForceField", params

    @sofa_component
    def HookeForceField(
        self,
        youngModulus=None,
        poissonRatio=None,
        viscosity=None,
        youngModulusX=None,
        youngModulusY=None,
        youngModulusZ=None,
        poissonRatioXY=None,
        poissonRatioYZ=None,
        poissonRatioZX=None,
        shearModulusXY=None,
        shearModulusYZ=None,
        shearModulusZX=None,
        **kwargs
    ):
        """
        HookeForceField

        :param youngModulus: Young Modulus
        :param poissonRatio: Poisson Ratio ]-1,0.5[
        :param viscosity: Viscosity (stress/strainRate)
        :param youngModulusX: Young Modulus along X
        :param youngModulusY: Young Modulus along Y
        :param youngModulusZ: Young Modulus along Z
        :param poissonRatioXY: Poisson Ratio about XY plane ]-1,0.5[
        :param poissonRatioYZ: Poisson Ratio about YZ plane ]-1,0.5[
        :param poissonRatioZX: Poisson Ratio about ZX plane ]-1,0.5[
        :param shearModulusXY: Shear Modulus about XY plane
        :param shearModulusYZ: Shear Modulus about YZ plane
        :param shearModulusZX: Shear Modulus about ZX plane
        """
        params = dict(
            youngModulus=youngModulus,
            poissonRatio=poissonRatio,
            viscosity=viscosity,
            youngModulusX=youngModulusX,
            youngModulusY=youngModulusY,
            youngModulusZ=youngModulusZ,
            poissonRatioXY=poissonRatioXY,
            poissonRatioYZ=poissonRatioYZ,
            poissonRatioZX=poissonRatioZX,
            shearModulusXY=shearModulusXY,
            shearModulusYZ=shearModulusYZ,
            shearModulusZX=shearModulusZX,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "HookeForceField", params

    @sofa_component
    def HookeMaterialBlock(self, **kwargs):
        """
        HookeMaterialBlock
        """
        params = dict()
        return "HookeMaterialBlock", params

    @sofa_component
    def MooneyRivlinForceField(
        self, C1=None, C2=None, bulk=None, PSDStabilization=None, **kwargs
    ):
        """
        MooneyRivlinForceField

        :param C1: weight of (~I1-3) term in energy
        :param C2: weight of (~I2-3) term in energy
        :param bulk: bulk modulus (working on I3=J=detF=volume variation)
        :param PSDStabilization: project stiffness matrix to its nearest symmetric, positive semi-definite matrix
        """
        params = dict(C1=C1, C2=C2, bulk=bulk, PSDStabilization=PSDStabilization)
        params = {k: v for k, v in params.items() if v is not None}
        return "MooneyRivlinForceField", params

    @sofa_component
    def MuscleMaterialForceField(
        self,
        lambda0=None,
        sigmaMax=None,
        a=None,
        b=None,
        Vvm=None,
        Ver=None,
        Vsh=None,
        **kwargs
    ):
        """
        MuscleMaterialForceField

        :param lambda0: optimal fiber stretch
        :param sigmaMax: maximum isometric stress
        :param a: activation level
        :param b:
        :param Vvm:
        :param Ver:
        :param Vsh:
        """
        params = dict(
            lambda0=lambda0, sigmaMax=sigmaMax, a=a, b=b, Vvm=Vvm, Ver=Ver, Vsh=Vsh
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MuscleMaterialForceField", params

    @sofa_component
    def NeoHookeanForceField(
        self,
        tetrahedronInfo=None,
        edgeInfo=None,
        ParameterMu=None,
        ParameterKo=None,
        **kwargs
    ):
        """
        NeoHookeanForceField

        :param tetrahedronInfo: Data to handle topology on tetrahedra
        :param edgeInfo: Data to handle topology on edges
        :param ParameterMu: Shear modulus the material
        :param ParameterKo: Bulk modulus
        """
        params = dict(
            tetrahedronInfo=tetrahedronInfo,
            edgeInfo=edgeInfo,
            ParameterMu=ParameterMu,
            ParameterKo=ParameterKo,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "NeoHookeanForceField", params

    @sofa_component
    def OgdenForceField(
        self,
        mu1=None,
        mu2=None,
        mu3=None,
        alpha1=None,
        alpha2=None,
        alpha3=None,
        d1=None,
        d2=None,
        d3=None,
        PSDStabilization=None,
        **kwargs
    ):
        """
        OgdenForceField

        :param mu1:
        :param mu2:
        :param mu3:
        :param alpha1:
        :param alpha2:
        :param alpha3:
        :param d1:
        :param d2:
        :param d3:
        :param PSDStabilization: project stiffness matrix to its nearest symmetric, positive semi-definite matrix
        """
        params = dict(
            mu1=mu1,
            mu2=mu2,
            mu3=mu3,
            alpha1=alpha1,
            alpha2=alpha2,
            alpha3=alpha3,
            d1=d1,
            d2=d2,
            d3=d3,
            PSDStabilization=PSDStabilization,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "OgdenForceField", params

    @sofa_component
    def PolynomialMaterialForceField(
        self,
        C10=None,
        C01=None,
        C20=None,
        C02=None,
        C30=None,
        C03=None,
        C11=None,
        bulk=None,
        **kwargs
    ):
        """
        PolynomialMaterialForceField

        :param C10: weight of (~I1-3) term in energy
        :param C01: weight of (~I2-3) term in energy
        :param C20: weight of (~I1-3)^2 term in energy
        :param C02: weight of (~I2-3)^2 term in energy
        :param C30: weight of (~I1-3)^3 term in energy
        :param C03: weight of (~I2-3)^3 term in energy
        :param C11: weight of (~I1-3)(~I2-3) term in energy
        :param bulk: bulk modulus (working on I3=J=detF=volume variation)
        """
        params = dict(
            C10=C10, C01=C01, C20=C20, C02=C02, C30=C30, C03=C03, C11=C11, bulk=bulk
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PolynomialMaterialForceField", params

    @sofa_component
    def ProjectiveForceField(self, youngModulus=None, viscosity=None, **kwargs):
        """
        ProjectiveForceField

        :param youngModulus: Young Modulus
        :param viscosity: Viscosity (stress/strainRate)
        """
        params = dict(youngModulus=youngModulus, viscosity=viscosity)
        params = {k: v for k, v in params.items() if v is not None}
        return "ProjectiveForceField", params

    @sofa_component
    def StabilizedHookeForceField(self, youngModulus=None, poissonRatio=None, **kwargs):
        """
        StabilizedHookeForceField

        :param youngModulus: Young Modulus
        :param poissonRatio: Poisson Ratio ]-1,0.5[
        """
        params = dict(youngModulus=youngModulus, poissonRatio=poissonRatio)
        params = {k: v for k, v in params.items() if v is not None}
        return "StabilizedHookeForceField", params

    @sofa_component
    def StabilizedNeoHookeanForceField(
        self, youngModulus=None, poissonRatio=None, **kwargs
    ):
        """
        StabilizedNeoHookeanForceField

        :param youngModulus: stiffness
        :param poissonRatio: incompressibility ]-1,0.5[
        """
        params = dict(youngModulus=youngModulus, poissonRatio=poissonRatio)
        params = {k: v for k, v in params.items() if v is not None}
        return "StabilizedNeoHookeanForceField", params

    @sofa_component
    def TendonMaterialForceField(self, L1=None, L2=None, lambdaL=None, **kwargs):
        """
        TendonMaterialForceField

        :param L1:
        :param L2:
        :param lambdaL: stretch above which behavior becomes linear
        """
        params = dict(L1=L1, L2=L2, lambdaL=lambdaL)
        params = {k: v for k, v in params.items() if v is not None}
        return "TendonMaterialForceField", params

    @sofa_component
    def VolumePreservationForceField(self, method=None, k=None, **kwargs):
        """
        VolumePreservationForceField

        :param method: energy form
        :param k: bulk modulus: weight ln(J)^2/2 term in energy
        """
        params = dict(method=method, k=k)
        params = {k: v for k, v in params.items() if v is not None}
        return "VolumePreservationForceField", params

    @sofa_component
    def VolumePreservationMaterialBlock(self, **kwargs):
        """
        VolumePreservationMaterialBlock
        """
        params = dict()
        return "VolumePreservationMaterialBlock", params

    @sofa_component
    def BaseGaussPointSampler(
        self,
        method=None,
        position=None,
        transforms=None,
        order=None,
        volume=None,
        showSamplesScale=None,
        drawMode=None,
        showIndicesScale=None,
        **kwargs
    ):
        """
        BaseGaussPointSampler

        :param method: quadrature method
        :param position: output sample positions
        :param transforms: output sample orientations
        :param order: order of quadrature method
        :param volume: output weighted volume
        :param showSamplesScale: show samples scale
        :param drawMode: 0: Green points; 1: Green spheres
        :param showIndicesScale: show indices scale
        """
        params = dict(
            method=method,
            position=position,
            transforms=transforms,
            order=order,
            volume=volume,
            showSamplesScale=showSamplesScale,
            drawMode=drawMode,
            showIndicesScale=showIndicesScale,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "BaseGaussPointSampler", params

    @sofa_component
    def GaussPointContainer(self, volumeDim=None, inputVolume=None, **kwargs):
        """
        GaussPointContainer

        :param volumeDim: dimension of quadrature weight vectors
        :param inputVolume: weighted volumes (=quadrature weights)
        """
        params = dict(volumeDim=volumeDim, inputVolume=inputVolume)
        params = {k: v for k, v in params.items() if v is not None}
        return "GaussPointContainer", params

    @sofa_component
    def TopologyGaussPointSampler(
        self,
        inPosition=None,
        cell=None,
        indices=None,
        orientation=None,
        useLocalOrientation=None,
        fineVolumes=None,
        **kwargs
    ):
        """
        TopologyGaussPointSampler

        :param inPosition: input node positions
        :param cell: cell index associated with each sample
        :param indices: list of cells where sampling is performed (all by default)
        :param orientation: input orientation (Euler angles) inside each cell
        :param useLocalOrientation: tells if orientations are defined in the local basis on each cell
        :param fineVolumes: input cell volumes (typically computed from a fine model)
        """
        params = dict(
            inPosition=inPosition,
            cell=cell,
            indices=indices,
            orientation=orientation,
            useLocalOrientation=useLocalOrientation,
            fineVolumes=fineVolumes,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TopologyGaussPointSampler", params

    @sofa_component
    def GaussPointSmoother(
        self,
        inputTransforms=None,
        inputVolume=None,
        indices=None,
        weights=None,
        **kwargs
    ):
        """
        GaussPointSmoother

        :param inputTransforms: sample orientations
        :param inputVolume: sample volume
        :param indices: parent indices for each child
        :param weights: influence weights
        """
        params = dict(
            inputTransforms=inputTransforms,
            inputVolume=inputVolume,
            indices=indices,
            weights=weights,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "GaussPointSmoother", params

    @sofa_component
    def BarycentricShapeFunction(self, tolerance=None, **kwargs):
        """
        BarycentricShapeFunction

        :param tolerance: minimum weight (allows for mapping outside elements)
        """
        params = dict(tolerance=tolerance)
        params = {k: v for k, v in params.items() if v is not None}
        return "BarycentricShapeFunction", params

    @sofa_component
    def BaseShapeFunction(self, nbRef=None, position=None, **kwargs):
        """
        BaseShapeFunction

        :param nbRef: maximum number of parents per child
        :param position: position of parent nodes
        """
        params = dict(nbRef=nbRef, position=position)
        params = {k: v for k, v in params.items() if v is not None}
        return "BaseShapeFunction", params

    @sofa_component
    def HatShapeFunction(self, method=None, param=None, **kwargs):
        """
        HatShapeFunction

        :param method: method
        :param param: param
        """
        params = dict(method=method, param=param)
        params = {k: v for k, v in params.items() if v is not None}
        return "HatShapeFunction", params

    @sofa_component
    def ShepardShapeFunction(self, power=None, **kwargs):
        """
        ShepardShapeFunction

        :param power: power of the inverse distance
        """
        params = dict(power=power)
        params = {k: v for k, v in params.items() if v is not None}
        return "ShepardShapeFunction", params

    @sofa_component
    def BaseStrainMapping(self, assemble=None, parallel=None, **kwargs):
        """
        BaseStrainMapping

        :param assemble: Assemble the matrices (Jacobian and Geometric Stiffness) or use optimized matrix/vector multiplications
        :param parallel: use openmp parallelisation?
        """
        params = dict(assemble=assemble, parallel=parallel)
        params = {k: v for k, v in params.items() if v is not None}
        return "BaseStrainMapping", params

    @sofa_component
    def CauchyStrainMapping(self, **kwargs):
        """
        CauchyStrainMapping
        """
        params = dict()
        return "CauchyStrainMapping", params

    @sofa_component
    def CorotationalStrainJacobianBlock(self, **kwargs):
        """
        CorotationalStrainJacobianBlock
        """
        params = dict()
        return "CorotationalStrainJacobianBlock", params

    @sofa_component
    def CorotationalStrainMapping(self, method=None, geometricStiffness=None, **kwargs):
        """
        CorotationalStrainMapping

        :param method: Decomposition method
        :param geometricStiffness: Should geometricStiffness be considered?
        """
        params = dict(method=method, geometricStiffness=geometricStiffness)
        params = {k: v for k, v in params.items() if v is not None}
        return "CorotationalStrainMapping", params

    @sofa_component
    def GreenStrainMapping(self, geometricStiffness=None, **kwargs):
        """
        GreenStrainMapping

        :param geometricStiffness: Should geometricStiffness be considered?
        """
        params = dict(geometricStiffness=geometricStiffness)
        params = {k: v for k, v in params.items() if v is not None}
        return "GreenStrainMapping", params

    @sofa_component
    def InvariantJacobianBlock(self, **kwargs):
        """
        InvariantJacobianBlock
        """
        params = dict()
        return "InvariantJacobianBlock", params

    @sofa_component
    def InvariantMapping(self, **kwargs):
        """
        InvariantMapping
        """
        params = dict()
        return "InvariantMapping", params

    @sofa_component
    def PlasticStrainMapping(self, method=None, max=None, creep=None, **kwargs):
        """
        PlasticStrainMapping

        :param method:
        :param max: Plastic Max Threshold (2-norm of the strain)
        :param creep: Plastic Creep Factor * dt [0,1]. 1 <-> pure plastic ; <1 <-> visco-plastic (warning depending on dt)
        """
        params = dict(method=method, max=max, creep=creep)
        params = {k: v for k, v in params.items() if v is not None}
        return "PlasticStrainMapping", params

    @sofa_component
    def PrincipalStretchesMapping(
        self, asStrain=None, threshold=None, PSDStabilization=None, **kwargs
    ):
        """
        PrincipalStretchesMapping

        :param asStrain: compute principal stretches - 1
        :param threshold: threshold the principal stretches to ensure detF=J=U1*U2*U3 is not too close or < 0
        :param PSDStabilization: project geometric stiffness sub-matrices to their nearest symmetric, positive semi-definite matrices
        """
        params = dict(
            asStrain=asStrain, threshold=threshold, PSDStabilization=PSDStabilization
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PrincipalStretchesMapping", params

    @sofa_component
    def RelativeStrainMapping(self, offset=None, inverted=None, **kwargs):
        """
        RelativeStrainMapping

        :param offset: Strain offset
        :param inverted: offset-Strain (rather than Strain-offset )
        """
        params = dict(offset=offset, inverted=inverted)
        params = {k: v for k, v in params.items() if v is not None}
        return "RelativeStrainMapping", params

    @sofa_component
    def LinearStrainMapping(
        self, assemble=None, parallel=None, indices=None, weights=None, **kwargs
    ):
        """
        LinearStrainMapping

        :param assemble: Assemble the matrices (Jacobian and Geometric Stiffness) or use optimized matrix/vector multiplications
        :param parallel: use openmp parallelisation?
        :param indices: parent indices for each child
        :param weights: influence weights of the Dofs
        """
        params = dict(
            assemble=assemble, parallel=parallel, indices=indices, weights=weights
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "LinearStrainMapping", params

    @sofa_component
    def AffineComponents(self, **kwargs):
        """
        AffineComponents
        """
        params = dict()
        return "AffineComponents", params

    @sofa_component
    def DeformationGradientTypes(self, **kwargs):
        """
        DeformationGradientTypes
        """
        params = dict()
        return "DeformationGradientTypes", params

    @sofa_component
    def QuadraticComponents(self, **kwargs):
        """
        QuadraticComponents
        """
        params = dict()
        return "QuadraticComponents", params

    @sofa_component
    def RigidConstraint(self, indices=None, method=None, drawSize=None, **kwargs):
        """
        RigidConstraint

        :param indices: Indices of the constrained frames
        :param method: 0: polar, 1: svd, 2: approximation
        :param drawSize: 0 -> point based rendering, >0 -> radius of spheres
        """
        params = dict(indices=indices, method=method, drawSize=drawSize)
        params = {k: v for k, v in params.items() if v is not None}
        return "RigidConstraint", params

    @sofa_component
    def StrainTypes(self, **kwargs):
        """
        StrainTypes
        """
        params = dict()
        return "StrainTypes", params

    @sofa_component
    def ImageDeformation(
        self,
        deformationMethod=None,
        interpolation=None,
        weightByVolumeChange=None,
        dimensions=None,
        param=None,
        inputImage=None,
        inputTransform=None,
        outputImage=None,
        outputTransform=None,
        **kwargs
    ):
        """
        ImageDeformation

        :param deformationMethod:
        :param interpolation:
        :param weightByVolumeChange: for images representing densities, weight intensities according to the local volume variation
        :param dimensions: output image dimensions
        :param param: Parameters
        :param inputImage:
        :param inputTransform:
        :param outputImage:
        :param outputTransform:
        """
        params = dict(
            deformationMethod=deformationMethod,
            interpolation=interpolation,
            weightByVolumeChange=weightByVolumeChange,
            dimensions=dimensions,
            param=param,
            inputImage=inputImage,
            inputTransform=inputTransform,
            outputImage=outputImage,
            outputTransform=outputTransform,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageDeformation", params

    @sofa_component
    def ImageDensityMass(
        self,
        densityImage=None,
        transform=None,
        lumping=None,
        printMassMatrix=None,
        **kwargs
    ):
        """
        ImageDensityMass

        :param densityImage: A density map (ratio kg/dm^3)
        :param transform: The density map transform
        :param lumping: Should the mass matrix be lumped? 0->no, 1->by bloc, 2->diagonal matrix
        :param printMassMatrix: Should the mass matrix be print in console after being precomputed?
        """
        params = dict(
            densityImage=densityImage,
            transform=transform,
            lumping=lumping,
            printMassMatrix=printMassMatrix,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageDensityMass", params

    @sofa_component
    def MassFromDensity(
        self, image=None, transform=None, massMatrix=None, lumping=None, **kwargs
    ):
        """
        MassFromDensity

        :param image:
        :param transform:
        :param massMatrix: Mass Matrix
        :param lumping: Should the mass matrix be lumped? 0->no, 1->by bloc, 2->diagonal matrix
        """
        params = dict(
            image=image, transform=transform, massMatrix=massMatrix, lumping=lumping
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MassFromDensity", params

    @sofa_component
    def ImageGaussPointSampler(
        self,
        indices=None,
        weights=None,
        mask=None,
        maskLabels=None,
        transform=None,
        region=None,
        error=None,
        clearData=None,
        targetNumber=None,
        useDijkstra=None,
        iterations=None,
        evaluateShapeFunction=None,
        sampleRigidParts=None,
        fillOrder=None,
        **kwargs
    ):
        """
        ImageGaussPointSampler

        :param indices: image of dof indices
        :param weights: weight image
        :param mask: optional mask to restrict the sampling region
        :param maskLabels: Mask labels where sampling is restricted
        :param transform:
        :param region: sample region : labeled image with sample indices
        :param error: weigth fitting error
        :param clearData: clear region and error images after computation
        :param targetNumber: target number of samples
        :param useDijkstra: Use Dijkstra for geodesic distance computation (use fastmarching otherwise)
        :param iterations: maximum number of Lloyd iterations
        :param evaluateShapeFunction: evaluate shape functions over integration regions for the mapping? (otherwise they will be interpolated at sample locations)
        :param sampleRigidParts: sample parts influenced only by one dofs? (otherwise put only one Gauss point)
        :param fillOrder: fill order
        """
        params = dict(
            indices=indices,
            weights=weights,
            mask=mask,
            maskLabels=maskLabels,
            transform=transform,
            region=region,
            error=error,
            clearData=clearData,
            targetNumber=targetNumber,
            useDijkstra=useDijkstra,
            iterations=iterations,
            evaluateShapeFunction=evaluateShapeFunction,
            sampleRigidParts=sampleRigidParts,
            fillOrder=fillOrder,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageGaussPointSampler", params

    @sofa_component
    def DiffusionShapeFunction(
        self,
        distances=None,
        nbBoundaryConditions=None,
        solver=None,
        iterations=None,
        tolerance=None,
        weightThreshold=None,
        bias=None,
        clearData=None,
        outsideDiffusion=None,
        **kwargs
    ):
        """
        DiffusionShapeFunction

        :param distances:
        :param nbBoundaryConditions: Number of boundary condition images provided
        :param solver: solver (param)
        :param iterations: Max number of iterations for iterative solvers
        :param tolerance: Error tolerance for iterative solvers
        :param weightThreshold: Thresold to neglect too small weights
        :param bias: Bias distances using inverse pixel values
        :param clearData: clear diffusion image after computation?
        :param outsideDiffusion: propagate shape function outside of the object? (can be useful for embeddings)
        """
        params = dict(
            distances=distances,
            nbBoundaryConditions=nbBoundaryConditions,
            solver=solver,
            iterations=iterations,
            tolerance=tolerance,
            weightThreshold=weightThreshold,
            bias=bias,
            clearData=clearData,
            outsideDiffusion=outsideDiffusion,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "DiffusionShapeFunction", params

    @sofa_component
    def ImageShapeFunctionSelectNode(
        self,
        shapeFunctionWeights=None,
        shapeFunctionIndices=None,
        nodeIndex=None,
        nodeWeights=None,
        **kwargs
    ):
        """
        ImageShapeFunctionSelectNode

        :param shapeFunctionWeights: shapeFunction weights image
        :param shapeFunctionIndices: shapeFunction indices image
        :param nodeIndex: index of parent node to select
        :param nodeWeights: selected node weights image
        """
        params = dict(
            shapeFunctionWeights=shapeFunctionWeights,
            shapeFunctionIndices=shapeFunctionIndices,
            nodeIndex=nodeIndex,
            nodeWeights=nodeWeights,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageShapeFunctionSelectNode", params

    @sofa_component
    def ImageShapeFunctionContainer(self, **kwargs):
        """
        ImageShapeFunctionContainer
        """
        params = dict()
        return "ImageShapeFunctionContainer", params

    @sofa_component
    def ShapeFunctionDiscretizer(
        self, image=None, transform=None, indices=None, weights=None, **kwargs
    ):
        """
        ShapeFunctionDiscretizer

        :param image:
        :param transform:
        :param indices:
        :param weights:
        """
        params = dict(
            image=image, transform=transform, indices=indices, weights=weights
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ShapeFunctionDiscretizer", params

    @sofa_component
    def VoronoiShapeFunction(
        self,
        distances=None,
        voronoi=None,
        clearData=None,
        method=None,
        bias=None,
        useDijkstra=None,
        **kwargs
    ):
        """
        VoronoiShapeFunction

        :param distances:
        :param voronoi:
        :param clearData: clear voronoi and distance images after computation
        :param method: method (param)
        :param bias: Bias distances using inverse pixel values
        :param useDijkstra: Use Dijkstra for geodesic distance computation (use fastmarching otherwise)
        """
        params = dict(
            distances=distances,
            voronoi=voronoi,
            clearData=clearData,
            method=method,
            bias=bias,
            useDijkstra=useDijkstra,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "VoronoiShapeFunction", params

    @sofa_component
    def InvertibleFVMForceField(
        self,
        initialPoints=None,
        poissonRatio=None,
        youngModulus=None,
        localStiffnessFactor=None,
        drawHeterogeneousTetra=None,
        drawAsEdges=None,
        verbose=None,
        **kwargs
    ):
        """
        InvertibleFVMForceField

        :param initialPoints: Initial Position
        :param poissonRatio: FEM Poisson Ratio [0,0.5[
        :param youngModulus: FEM Young Modulus
        :param localStiffnessFactor: Allow specification of different stiffness per element. If there are N element and M values are specified, the youngModulus factor for element i would be localStiffnessFactor[i*M/N]
        :param drawHeterogeneousTetra: Draw Heterogeneous Tetra in different color
        :param drawAsEdges: Draw as edges instead of tetrahedra
        :param verbose: Print debug stuff
        """
        params = dict(
            initialPoints=initialPoints,
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            localStiffnessFactor=localStiffnessFactor,
            drawHeterogeneousTetra=drawHeterogeneousTetra,
            drawAsEdges=drawAsEdges,
            verbose=verbose,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "InvertibleFVMForceField", params

    @sofa_component
    def CollisionToCarvingEngine(
        self,
        inputImage=None,
        inputTransform=None,
        outputImage=None,
        outputTransform=None,
        trackedPosition=None,
        **kwargs
    ):
        """
        CollisionToCarvingEngine

        :param inputImage:
        :param inputTransform:
        :param outputImage:
        :param outputTransform:
        :param trackedPosition: Position de test pour la collision
        """
        params = dict(
            inputImage=inputImage,
            inputTransform=inputTransform,
            outputImage=outputImage,
            outputTransform=outputTransform,
            trackedPosition=trackedPosition,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CollisionToCarvingEngine", params

    @sofa_component
    def DepthMapToMeshEngine(
        self,
        depthFactor=None,
        minThreshold=None,
        diffThreshold=None,
        image=None,
        transform=None,
        texImage=None,
        position=None,
        texCoord=None,
        texOffset=None,
        triangles=None,
        **kwargs
    ):
        """
        DepthMapToMeshEngine

        :param depthFactor: Intensity to depth factor
        :param minThreshold: minimal depth for point creation
        :param diffThreshold: maximal depth variation for triangle creation
        :param image:
        :param transform:
        :param texImage:
        :param position: output positions
        :param texCoord: output texture coordinates
        :param texOffset: texture offsets (in [0,1])
        :param triangles: output triangles
        """
        params = dict(
            depthFactor=depthFactor,
            minThreshold=minThreshold,
            diffThreshold=diffThreshold,
            image=image,
            transform=transform,
            texImage=texImage,
            position=position,
            texCoord=texCoord,
            texOffset=texOffset,
            triangles=triangles,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "DepthMapToMeshEngine", params

    @sofa_component
    def ImageAccumulator(
        self,
        accumulate=None,
        inputImage=None,
        inputTransform=None,
        outputImage=None,
        outputTransform=None,
        **kwargs
    ):
        """
        ImageAccumulator

        :param accumulate: accumulate ?
        :param inputImage:
        :param inputTransform:
        :param outputImage:
        :param outputTransform:
        """
        params = dict(
            accumulate=accumulate,
            inputImage=inputImage,
            inputTransform=inputTransform,
            outputImage=outputImage,
            outputTransform=outputTransform,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageAccumulator", params

    @sofa_component
    def ImageContainer(
        self,
        image=None,
        transform=None,
        filename=None,
        drawBB=None,
        sequence=None,
        numberOfFrames=None,
        **kwargs
    ):
        """
        ImageContainer

        :param image: image
        :param transform: 12-param vector for trans, rot, scale, ...
        :param filename: Image file
        :param drawBB: draw bounding box
        :param sequence: load a sequence of images
        :param numberOfFrames: The number of frames of the sequence to be loaded. Default is the entire sequence.
        """
        params = dict(
            image=image,
            transform=transform,
            filename=filename,
            drawBB=drawBB,
            sequence=sequence,
            numberOfFrames=numberOfFrames,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageContainer", params

    @sofa_component
    def GenerateImage(self, image=None, **kwargs):
        """
        GenerateImage

        :param image:
        """
        params = dict(image=image)
        params = {k: v for k, v in params.items() if v is not None}
        return "GenerateImage", params

    @sofa_component
    def ImageDataDisplay(
        self, inputImage=None, outputImage=None, VoxelData=None, **kwargs
    ):
        """
        ImageDataDisplay

        :param inputImage:
        :param outputImage:
        :param VoxelData: Data associed to each non null input voxel
        """
        params = dict(
            inputImage=inputImage, outputImage=outputImage, VoxelData=VoxelData
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageDataDisplay", params

    @sofa_component
    def ImageExporter(
        self,
        image=None,
        transform=None,
        filename=None,
        exportEveryNumberOfSteps=None,
        exportAtBegin=None,
        exportAtEnd=None,
        **kwargs
    ):
        """
        ImageExporter

        :param image: image
        :param transform:
        :param filename: output file
        :param exportEveryNumberOfSteps: export file only at specified number of steps (0=disable)
        :param exportAtBegin: export file at the initialization
        :param exportAtEnd: export file when the simulation is finished
        """
        params = dict(
            image=image,
            transform=transform,
            filename=filename,
            exportEveryNumberOfSteps=exportEveryNumberOfSteps,
            exportAtBegin=exportAtBegin,
            exportAtEnd=exportAtEnd,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageExporter", params

    @sofa_component
    def ImageFilter(
        self,
        filter=None,
        param=None,
        inputImage=None,
        inputTransform=None,
        outputImage=None,
        outputTransform=None,
        **kwargs
    ):
        """
        ImageFilter

        :param filter: Filter
        :param param: Parameters
        :param inputImage:
        :param inputTransform:
        :param outputImage:
        :param outputTransform:
        """
        params = dict(
            filter=filter,
            param=param,
            inputImage=inputImage,
            inputTransform=inputTransform,
            outputImage=outputImage,
            outputTransform=outputTransform,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageFilter", params

    @sofa_component
    def ImageOperation(
        self,
        operation=None,
        inputImage1=None,
        inputImage2=None,
        outputImage=None,
        **kwargs
    ):
        """
        ImageOperation

        :param operation: operation
        :param inputImage1:
        :param inputImage2:
        :param outputImage:
        """
        params = dict(
            operation=operation,
            inputImage1=inputImage1,
            inputImage2=inputImage2,
            outputImage=outputImage,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageOperation", params

    @sofa_component
    def ImageSampler(
        self,
        image=None,
        transform=None,
        method=None,
        computeRecursive=None,
        param=None,
        position=None,
        fixedPosition=None,
        edges=None,
        graphEdges=None,
        hexahedra=None,
        distances=None,
        voronoi=None,
        clearData=None,
        showSamplesScale=None,
        drawMode=None,
        showEdges=None,
        showGraph=None,
        showFaces=None,
        **kwargs
    ):
        """
        ImageSampler

        :param image:
        :param transform:
        :param method: method (param)
        :param computeRecursive: if true: insert nodes recursively and build the graph
        :param param: Parameters
        :param position: output positions
        :param fixedPosition: user defined sample positions
        :param edges: edges connecting neighboring nodes
        :param graphEdges: oriented graph connecting parent to child nodes
        :param hexahedra: output hexahedra
        :param distances:
        :param voronoi:
        :param clearData: clear distance image after computation
        :param showSamplesScale: show samples
        :param drawMode: 0: points, 1: spheres
        :param showEdges: show edges
        :param showGraph: show graph
        :param showFaces: show the faces of cubes
        """
        params = dict(
            image=image,
            transform=transform,
            method=method,
            computeRecursive=computeRecursive,
            param=param,
            position=position,
            fixedPosition=fixedPosition,
            edges=edges,
            graphEdges=graphEdges,
            hexahedra=hexahedra,
            distances=distances,
            voronoi=voronoi,
            clearData=clearData,
            showSamplesScale=showSamplesScale,
            drawMode=drawMode,
            showEdges=showEdges,
            showGraph=showGraph,
            showFaces=showFaces,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageSampler", params

    @sofa_component
    def ImageToRigidMassEngine(
        self,
        image=None,
        transform=None,
        position=None,
        mass=None,
        inertia=None,
        rigidMass=None,
        density=None,
        multiply=None,
        **kwargs
    ):
        """
        ImageToRigidMassEngine

        :param image:
        :param transform:
        :param position: position
        :param mass: mass
        :param inertia: axis-aligned inertia tensor
        :param rigidMass: rigidMass
        :param density: density (in kg/m^3)
        :param multiply: multiply density by image intensity?
        """
        params = dict(
            image=image,
            transform=transform,
            position=position,
            mass=mass,
            inertia=inertia,
            rigidMass=rigidMass,
            density=density,
            multiply=multiply,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageToRigidMassEngine", params

    @sofa_component
    def ImageTransform(
        self,
        translation=None,
        euler=None,
        scale=None,
        isPerspective=None,
        timeOffset=None,
        timeScale=None,
        update=None,
        **kwargs
    ):
        """
        ImageTransform

        :param translation: Translation
        :param euler: Euler angles
        :param scale: Voxel size
        :param isPerspective: Is perspective?
        :param timeOffset: Time offset
        :param timeScale: Time scale
        :param update: Type of update
        """
        params = dict(
            translation=translation,
            euler=euler,
            scale=scale,
            isPerspective=isPerspective,
            timeOffset=timeOffset,
            timeScale=timeScale,
            update=update,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageTransform", params

    @sofa_component
    def ImageTransformEngine(
        self,
        inputTransform=None,
        outputTransform=None,
        translation=None,
        rotation=None,
        scale=None,
        inverse=None,
        **kwargs
    ):
        """
        ImageTransformEngine

        :param inputTransform:
        :param outputTransform:
        :param translation: translation vector
        :param rotation: rotation vector
        :param scale: scale factor
        :param inverse: true to apply inverse transformation
        """
        params = dict(
            inputTransform=inputTransform,
            outputTransform=outputTransform,
            translation=translation,
            rotation=rotation,
            scale=scale,
            inverse=inverse,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageTransformEngine", params

    @sofa_component
    def ImageTypes(self, **kwargs):
        """
        ImageTypes
        """
        params = dict()
        return "ImageTypes", params

    @sofa_component
    def ImageValuesFromPositions(
        self,
        image=None,
        transform=None,
        position=None,
        interpolation=None,
        values=None,
        outValue=None,
        **kwargs
    ):
        """
        ImageValuesFromPositions

        :param image:
        :param transform:
        :param position: input positions
        :param interpolation: Interpolation method.
        :param values: Interpolated values.
        :param outValue: default value outside image
        """
        params = dict(
            image=image,
            transform=transform,
            position=position,
            interpolation=interpolation,
            values=values,
            outValue=outValue,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageValuesFromPositions", params

    @sofa_component
    def ImageCoordValuesFromPositions(
        self,
        image=None,
        transform=None,
        position=None,
        interpolation=None,
        values=None,
        outValue=None,
        addPosition=None,
        **kwargs
    ):
        """
        ImageCoordValuesFromPositions

        :param image:
        :param transform:
        :param position: input positions
        :param interpolation: Interpolation method.
        :param values: Interpolated values.
        :param outValue: default value outside image
        :param addPosition: add positions to interpolated values (to get translated positions)
        """
        params = dict(
            image=image,
            transform=transform,
            position=position,
            interpolation=interpolation,
            values=values,
            outValue=outValue,
            addPosition=addPosition,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ImageCoordValuesFromPositions", params

    @sofa_component
    def MarchingCubesEngine(
        self,
        isoValue=None,
        subdiv=None,
        invertNormals=None,
        showMesh=None,
        image=None,
        transform=None,
        position=None,
        triangles=None,
        **kwargs
    ):
        """
        MarchingCubesEngine

        :param isoValue: pixel value to extract isosurface
        :param subdiv: number of subdividions in x,y,z directions (use image dimension if =0)
        :param invertNormals: invert triangle vertex order
        :param showMesh: show reconstructed mesh
        :param image:
        :param transform:
        :param position: output positions
        :param triangles: output triangles
        """
        params = dict(
            isoValue=isoValue,
            subdiv=subdiv,
            invertNormals=invertNormals,
            showMesh=showMesh,
            image=image,
            transform=transform,
            position=position,
            triangles=triangles,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MarchingCubesEngine", params

    @sofa_component
    def MergeImages(
        self,
        overlap=None,
        interpolation=None,
        nbImages=None,
        image=None,
        transform=None,
        **kwargs
    ):
        """
        MergeImages

        :param overlap: method for handling overlapping regions
        :param interpolation: Interpolation method.
        :param nbImages: number of images to merge
        :param image: Image
        :param transform: Transform
        """
        params = dict(
            overlap=overlap,
            interpolation=interpolation,
            nbImages=nbImages,
            image=image,
            transform=transform,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MergeImages", params

    @sofa_component
    def MeshToImageEngine(
        self,
        voxelSize=None,
        nbVoxels=None,
        rotateImage=None,
        padSize=None,
        subdiv=None,
        image=None,
        transform=None,
        backgroundValue=None,
        nbMeshes=None,
        gridSnap=None,
        worldGridAligned=None,
        **kwargs
    ):
        """
        MeshToImageEngine

        :param voxelSize: voxel Size (redondant with and not priority over nbVoxels)
        :param nbVoxels: number of voxel (redondant with and priority over voxelSize)
        :param rotateImage: orient the image bounding box according to the mesh (OBB)
        :param padSize: size of border in number of voxels
        :param subdiv: number of subdivisions for face rasterization (if needed, increase to avoid holes)
        :param image:
        :param transform:
        :param backgroundValue: pixel value at background
        :param nbMeshes: number of meshes to voxelize (Note that the last one write on the previous ones)
        :param gridSnap: align voxel centers on voxelSize multiples for perfect image merging (nbVoxels and rotateImage should be off)
        :param worldGridAligned: perform rasterization on a world aligned grid using nbVoxels and voxelSize
        """
        params = dict(
            voxelSize=voxelSize,
            nbVoxels=nbVoxels,
            rotateImage=rotateImage,
            padSize=padSize,
            subdiv=subdiv,
            image=image,
            transform=transform,
            backgroundValue=backgroundValue,
            nbMeshes=nbMeshes,
            gridSnap=gridSnap,
            worldGridAligned=worldGridAligned,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshToImageEngine", params

    @sofa_component
    def TransferFunction(
        self, filter=None, param=None, inputImage=None, outputImage=None, **kwargs
    ):
        """
        TransferFunction

        :param filter: Filter
        :param param: Parameters
        :param inputImage:
        :param outputImage:
        """
        params = dict(
            filter=filter, param=param, inputImage=inputImage, outputImage=outputImage
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TransferFunction", params

    @sofa_component
    def VoronoiToMeshEngine(
        self,
        showMesh=None,
        image=None,
        background=None,
        transform=None,
        position=None,
        edges=None,
        triangles=None,
        minLength=None,
        **kwargs
    ):
        """
        VoronoiToMeshEngine

        :param showMesh: show reconstructed mesh
        :param image: Voronoi image
        :param background: Optional Voronoi image of the background to surface details
        :param transform:
        :param position: output positions
        :param edges: output edges
        :param triangles: output triangles
        :param minLength: minimun edge length in pixels
        """
        params = dict(
            showMesh=showMesh,
            image=image,
            background=background,
            transform=transform,
            position=position,
            edges=edges,
            triangles=triangles,
            minLength=minLength,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "VoronoiToMeshEngine", params

    @sofa_component
    def TestImageEngine(self, inputImage=None, outputImage=None, **kwargs):
        """
        TestImageEngine

        :param inputImage: input image
        :param outputImage: ouput image
        """
        params = dict(inputImage=inputImage, outputImage=outputImage)
        params = {k: v for k, v in params.items() if v is not None}
        return "TestImageEngine", params

    @sofa_component
    def ImageTransformWidget(self, **kwargs):
        """
        ImageTransformWidget
        """
        params = dict()
        return "ImageTransformWidget", params

    @sofa_component
    def HistogramWidget(self, **kwargs):
        """
        HistogramWidget
        """
        params = dict()
        return "HistogramWidget", params

    @sofa_component
    def ImagePlaneWidget(self, **kwargs):
        """
        ImagePlaneWidget
        """
        params = dict()
        return "ImagePlaneWidget", params

    @sofa_component
    def VectorVisualizationWidget(self, **kwargs):
        """
        VectorVisualizationWidget
        """
        params = dict()
        return "VectorVisualizationWidget", params

    @sofa_component
    def MeshSTEPLoader(
        self,
        uv=None,
        deflection=None,
        debug=None,
        keepDuplicate=None,
        indicesComponents=None,
        **kwargs
    ):
        """
        MeshSTEPLoader

        :param uv: UV coordinates
        :param deflection: Deflection parameter for tesselation
        :param debug: if true, print information for debug mode
        :param keepDuplicate: if true, keep duplicated vertices
        :param indicesComponents: Shape # | number of nodes | number of triangles
        """
        params = dict(
            uv=uv,
            deflection=deflection,
            debug=debug,
            keepDuplicate=keepDuplicate,
            indicesComponents=indicesComponents,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshSTEPLoader", params

    @sofa_component
    def ParametricTriangleTopologyContainer(self, uv=None, **kwargs):
        """
        ParametricTriangleTopologyContainer

        :param uv: The uv coordinates for every triangle vertices.
        """
        params = dict(uv=uv)
        params = {k: v for k, v in params.items() if v is not None}
        return "ParametricTriangleTopologyContainer", params

    @sofa_component
    def STEPShapeMapping(
        self, shapeNumber=None, indexBegin=None, indexEnd=None, **kwargs
    ):
        """
        STEPShapeMapping

        :param shapeNumber: Shape number to be loaded
        :param indexBegin: The begin index for this shape with respect to the global mesh
        :param indexEnd: The end index for this shape with respect to the global mesh
        """
        params = dict(shapeNumber=shapeNumber, indexBegin=indexBegin, indexEnd=indexEnd)
        params = {k: v for k, v in params.items() if v is not None}
        return "STEPShapeMapping", params

    @sofa_component
    def SingleComponent(
        self,
        positionsI=None,
        positionsO=None,
        edgesI=None,
        edgesO=None,
        trianglesI=None,
        trianglesO=None,
        normalsI=None,
        normalsO=None,
        uvI=None,
        uvO=None,
        indicesComponents=None,
        numberShape=None,
        **kwargs
    ):
        """
        SingleComponent

        :param positionsI: input: vertices position of whole mesh
        :param positionsO: output: vertices position of the component
        :param edgesI: input: edges of whole mesh
        :param edgesO: output: edges of the component
        :param trianglesI: input: triangles of whole mesh
        :param trianglesO: output: triangles of the component
        :param normalsI: input: normals of the whole mesh
        :param normalsO: output: normals of the component
        :param uvI: input: UV coordinates of the whole mesh
        :param uvO: output: UV coordinates of the component
        :param indicesComponents: Shape # | number of nodes | number of triangles
        :param numberShape: Shape number to be loaded (see Outputs tab of STEPLoader for a description of the shapes)
        """
        params = dict(
            positionsI=positionsI,
            positionsO=positionsO,
            edgesI=edgesI,
            edgesO=edgesO,
            trianglesI=trianglesI,
            trianglesO=trianglesO,
            normalsI=normalsI,
            normalsO=normalsO,
            uvI=uvI,
            uvO=uvO,
            indicesComponents=indicesComponents,
            numberShape=numberShape,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SingleComponent", params

    @sofa_component
    def SofaHAPIForceFeedbackEffect(self, **kwargs):
        """
        SofaHAPIForceFeedbackEffect
        """
        params = dict()
        return "SofaHAPIForceFeedbackEffect", params

    @sofa_component
    def SofaHAPIHapticsDevice(
        self,
        scale=None,
        forceScale=None,
        positionBase=None,
        orientationBase=None,
        positionTool=None,
        orientationTool=None,
        permanent=None,
        toolSelector=None,
        toolCount=None,
        toolIndex=None,
        toolTransitionSpringStiffness=None,
        driverName=None,
        drawDevice=None,
        drawHandleSize=None,
        drawForceScale=None,
        **kwargs
    ):
        """
        SofaHAPIHapticsDevice

        :param scale: Default scale applied to the Phantom Coordinates.
        :param forceScale: Default forceScale applied to the force feedback.
        :param positionBase: Position of the interface base in the scene world coordinates
        :param orientationBase: Orientation of the interface base in the scene world coordinates
        :param positionTool: Position of the tool in the device end effector frame
        :param orientationTool: Orientation of the tool in the device end effector frame
        :param permanent: Apply the force feedback permanently
        :param toolSelector: Switch tools with 2nd button
        :param toolCount: Number of tools to switch between
        :param toolIndex: Current tool index
        :param toolTransitionSpringStiffness: Stiffness of haptic springs when switching instruments (0 to disable)
        :param driverName: Name of the HAPI device driver
        :param drawDevice: Visualize the position of the interface in the virtual scene
        :param drawHandleSize: Visualize the handle direction of the interface in the virtual scene
        :param drawForceScale: Visualize the haptics force in the virtual scene
        """
        params = dict(
            scale=scale,
            forceScale=forceScale,
            positionBase=positionBase,
            orientationBase=orientationBase,
            positionTool=positionTool,
            orientationTool=orientationTool,
            permanent=permanent,
            toolSelector=toolSelector,
            toolCount=toolCount,
            toolIndex=toolIndex,
            toolTransitionSpringStiffness=toolTransitionSpringStiffness,
            driverName=driverName,
            drawDevice=drawDevice,
            drawHandleSize=drawHandleSize,
            drawForceScale=drawForceScale,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SofaHAPIHapticsDevice", params

    @sofa_component
    def AssimpLoader(self, **kwargs):
        """
        AssimpLoader
        """
        params = dict()
        return "AssimpLoader", params

    @sofa_component
    def RigidScaleToAffineMultiMapping(
        self, index=None, autoInit=None, useGeometricStiffness=None, **kwargs
    ):
        """
        RigidScaleToAffineMultiMapping

        :param index: list of couples (index in rigid DOF + index in scale with the type Vec3d)
        :param autoInit: Init the scale and affine mechanical state, and the index data.
        :param useGeometricStiffness: To specify if the geometric stiffness is used or not.
        """
        params = dict(
            index=index, autoInit=autoInit, useGeometricStiffness=useGeometricStiffness
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "RigidScaleToAffineMultiMapping", params

    @sofa_component
    def RigidScaleToRigidMultiMapping(
        self, index=None, useGeometricStiffness=None, **kwargs
    ):
        """
        RigidScaleToRigidMultiMapping

        :param index: list of couples (index in rigid DOF + index in scale with the type Vec3d)
        :param useGeometricStiffness: To specify if the geometric stiffness is used or not.
        """
        params = dict(index=index, useGeometricStiffness=useGeometricStiffness)
        params = {k: v for k, v in params.items() if v is not None}
        return "RigidScaleToRigidMultiMapping", params

    @sofa_component
    def InterpolatedImplicitSurface(self, **kwargs):
        """
        InterpolatedImplicitSurface
        """
        params = dict()
        return "InterpolatedImplicitSurface", params

    @sofa_component
    def IHPDriver(self, **kwargs):
        """
        IHPDriver
        """
        params = dict()
        return "IHPDriver", params

    @sofa_component
    def ITPDriver(self, **kwargs):
        """
        ITPDriver
        """
        params = dict()
        return "ITPDriver", params

    @sofa_component
    def PaceMaker(self, **kwargs):
        """
        PaceMaker
        """
        params = dict()
        return "PaceMaker", params

    @sofa_component
    def DiffusionSolver(self, **kwargs):
        """
        DiffusionSolver
        """
        params = dict()
        return "DiffusionSolver", params

    @sofa_component
    def SceneLoaderPSL(self, **kwargs):
        """
        SceneLoaderPSL
        """
        params = dict()
        return "SceneLoaderPSL", params

    @sofa_component
    def Import(self, **kwargs):
        """
        Import
        """
        params = dict()
        return "Import", params

    @sofa_component
    def Python(self, **kwargs):
        """
        Python
        """
        params = dict()
        return "Python", params

    @sofa_component
    def TestResult(self, result=None, **kwargs):
        """
        TestResult

        :param result:
        """
        params = dict(result=result)
        params = {k: v for k, v in params.items() if v is not None}
        return "TestResult", params

    @sofa_component
    def PSLVersion(self, **kwargs):
        """
        PSLVersion
        """
        params = dict()
        return "PSLVersion", params

    @sofa_component
    def Template(self, psl_source=None, **kwargs):
        """
        Template

        :param psl_source: Current template source
        """
        params = dict(psl_source=psl_source)
        params = {k: v for k, v in params.items() if v is not None}
        return "Template", params

    @sofa_component
    def starthere(self, **kwargs):
        """
        starthere
        """
        params = dict()
        return "starthere", params

    @sofa_component
    def caduceus(self, **kwargs):
        """
        caduceus
        """
        params = dict()
        return "caduceus", params

    @sofa_component
    def test_emptyfile(self, **kwargs):
        """
        test_emptyfile
        """
        params = dict()
        return "test_emptyfile", params

    @sofa_component
    def test_brokenfile(self, **kwargs):
        """
        test_brokenfile
        """
        params = dict()
        return "test_brokenfile", params

    @sofa_component
    def test_node(self, **kwargs):
        """
        test_node
        """
        params = dict()
        return "test_node", params

    @sofa_component
    def test_ast(self, **kwargs):
        """
        test_ast
        """
        params = dict()
        return "test_ast", params

    @sofa_component
    def test_caduceus(self, **kwargs):
        """
        test_caduceus
        """
        params = dict()
        return "test_caduceus", params

    @sofa_component
    def ImageCImg(self, **kwargs):
        """
        ImageCImg
        """
        params = dict()
        return "ImageCImg", params

    @sofa_component
    def HaptionDriver(
        self,
        Scale=None,
        state_button=None,
        haptionVisu=None,
        positionBase=None,
        torqueScale=None,
        forceScale=None,
        ip_haption=None,
        **kwargs
    ):
        """
        HaptionDriver

        :param Scale: Default scale applied to the Haption Coordinates.
        :param state_button: state of the first button
        :param haptionVisu: Visualize the position of the interface in the virtual scene
        :param positionBase: Position of the interface base in the scene world coordinates
        :param torqueScale: Default scale applied to the Haption torque.
        :param forceScale: Default scale applied to the Haption force.
        :param ip_haption: ip of the device
        """
        params = dict(
            Scale=Scale,
            state_button=state_button,
            haptionVisu=haptionVisu,
            positionBase=positionBase,
            torqueScale=torqueScale,
            forceScale=forceScale,
            ip_haption=ip_haption,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "HaptionDriver", params

    @sofa_component
    def ARTrackController(
        self,
        virtualTime=None,
        step1=None,
        step2=None,
        step3=None,
        maxMotion=None,
        **kwargs
    ):
        """
        ARTrackController

        :param virtualTime: Time found for the BVH
        :param step1: time at initial position
        :param step2: time at intermediate position
        :param step3: time at final position
        :param maxMotion: Displacement amplitude
        """
        params = dict(
            virtualTime=virtualTime,
            step1=step1,
            step2=step2,
            step3=step3,
            maxMotion=maxMotion,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ARTrackController", params

    @sofa_component
    def ARTrackDriver(
        self, aRTrackScale=None, localTrackerPos=None, scaleAngleFinger=None, **kwargs
    ):
        """
        ARTrackDriver

        :param aRTrackScale: ARTrack scale
        :param localTrackerPos: Local tracker position
        :param scaleAngleFinger: Angle Finger scale
        """
        params = dict(
            aRTrackScale=aRTrackScale,
            localTrackerPos=localTrackerPos,
            scaleAngleFinger=scaleAngleFinger,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ARTrackDriver", params

    @sofa_component
    def ARTrackEvent(self, **kwargs):
        """
        ARTrackEvent
        """
        params = dict()
        return "ARTrackEvent", params

    @sofa_component
    def CudaBarycentricMapping(self, **kwargs):
        """
        CudaBarycentricMapping
        """
        params = dict()
        return "CudaBarycentricMapping", params

    @sofa_component
    def CudaBarycentricMappingRigid(self, **kwargs):
        """
        CudaBarycentricMappingRigid
        """
        params = dict()
        return "CudaBarycentricMappingRigid", params

    @sofa_component
    def CudaBaseVector(self, **kwargs):
        """
        CudaBaseVector
        """
        params = dict()
        return "CudaBaseVector", params

    @sofa_component
    def CudaDiagonalMass(self, **kwargs):
        """
        CudaDiagonalMass
        """
        params = dict()
        return "CudaDiagonalMass", params

    @sofa_component
    def CudaEllipsoidForceField(self, **kwargs):
        """
        CudaEllipsoidForceField
        """
        params = dict()
        return "CudaEllipsoidForceField", params

    @sofa_component
    def CudaFixedConstraint(self, **kwargs):
        """
        CudaFixedConstraint
        """
        params = dict()
        return "CudaFixedConstraint", params

    @sofa_component
    def CudaHexahedronTLEDForceField(
        self,
        poissonRatio=None,
        youngModulus=None,
        timestep=None,
        isViscoelastic=None,
        isAnisotropic=None,
        preferredDirection=None,
        **kwargs
    ):
        """
        CudaHexahedronTLEDForceField

        :param poissonRatio: Poisson ratio in Hooke's law
        :param youngModulus: Young modulus in Hooke's law
        :param timestep: Simulation timestep
        :param isViscoelastic: Viscoelasticity flag
        :param isAnisotropic: Anisotropy flag
        :param preferredDirection: Transverse isotropy direction
        """
        params = dict(
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            timestep=timestep,
            isViscoelastic=isViscoelastic,
            isAnisotropic=isAnisotropic,
            preferredDirection=preferredDirection,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CudaHexahedronTLEDForceField", params

    @sofa_component
    def CudaIdentityMapping(self, **kwargs):
        """
        CudaIdentityMapping
        """
        params = dict()
        return "CudaIdentityMapping", params

    @sofa_component
    def CudaLineModel(self, **kwargs):
        """
        CudaLineModel
        """
        params = dict()
        return "CudaLineModel", params

    @sofa_component
    def CudaLinearForceField(self, **kwargs):
        """
        CudaLinearForceField
        """
        params = dict()
        return "CudaLinearForceField", params

    @sofa_component
    def CudaLinearMovementConstraint(self, **kwargs):
        """
        CudaLinearMovementConstraint
        """
        params = dict()
        return "CudaLinearMovementConstraint", params

    @sofa_component
    def CudaMath(self, **kwargs):
        """
        CudaMath
        """
        params = dict()
        return "CudaMath", params

    @sofa_component
    def CudaMathRigid(self, **kwargs):
        """
        CudaMathRigid
        """
        params = dict()
        return "CudaMathRigid", params

    @sofa_component
    def CudaMechanicalObject(self, **kwargs):
        """
        CudaMechanicalObject
        """
        params = dict()
        return "CudaMechanicalObject", params

    @sofa_component
    def CudaMeshMatrixMass(self, **kwargs):
        """
        CudaMeshMatrixMass
        """
        params = dict()
        return "CudaMeshMatrixMass", params

    @sofa_component
    def CudaParticleSource(self, **kwargs):
        """
        CudaParticleSource
        """
        params = dict()
        return "CudaParticleSource", params

    @sofa_component
    def CudaPenalityContactForceField(self, **kwargs):
        """
        CudaPenalityContactForceField
        """
        params = dict()
        return "CudaPenalityContactForceField", params

    @sofa_component
    def CudaPlaneForceField(self, **kwargs):
        """
        CudaPlaneForceField
        """
        params = dict()
        return "CudaPlaneForceField", params

    @sofa_component
    def CudaPointModel(self, groupSize=None, **kwargs):
        """
        CudaPointModel

        :param groupSize: number of point per collision element
        """
        params = dict(groupSize=groupSize)
        params = {k: v for k, v in params.items() if v is not None}
        return "CudaPointModel", params

    @sofa_component
    def CudaRigidMapping(self, **kwargs):
        """
        CudaRigidMapping
        """
        params = dict()
        return "CudaRigidMapping", params

    @sofa_component
    def CudaScan(self, **kwargs):
        """
        CudaScan
        """
        params = dict()
        return "CudaScan", params

    @sofa_component
    def CudaSort(self, **kwargs):
        """
        CudaSort
        """
        params = dict()
        return "CudaSort", params

    @sofa_component
    def CudaSphereForceField(self, **kwargs):
        """
        CudaSphereForceField
        """
        params = dict()
        return "CudaSphereForceField", params

    @sofa_component
    def CudaSphereModel(self, **kwargs):
        """
        CudaSphereModel
        """
        params = dict()
        return "CudaSphereModel", params

    @sofa_component
    def CudaSpringForceField(self, **kwargs):
        """
        CudaSpringForceField
        """
        params = dict()
        return "CudaSpringForceField", params

    @sofa_component
    def CudaStandardTetrahedralFEMForceField(self, **kwargs):
        """
        CudaStandardTetrahedralFEMForceField
        """
        params = dict()
        return "CudaStandardTetrahedralFEMForceField", params

    @sofa_component
    def CudaSubsetMapping(self, **kwargs):
        """
        CudaSubsetMapping
        """
        params = dict()
        return "CudaSubsetMapping", params

    @sofa_component
    def CudaTetrahedralTensorMassForceField(self, **kwargs):
        """
        CudaTetrahedralTensorMassForceField
        """
        params = dict()
        return "CudaTetrahedralTensorMassForceField", params

    @sofa_component
    def CudaTetrahedronFEMForceField(self, gatherPt=None, gatherBsize=None, **kwargs):
        """
        CudaTetrahedronFEMForceField

        :param gatherPt: number of dof accumulated per threads during the gather operation (Only use in GPU version)
        :param gatherBsize: number of dof accumulated per threads during the gather operation (Only use in GPU version)
        """
        params = dict(gatherPt=gatherPt, gatherBsize=gatherBsize)
        params = {k: v for k, v in params.items() if v is not None}
        return "CudaTetrahedronFEMForceField", params

    @sofa_component
    def CudaTetrahedronTLEDForceField(
        self,
        poissonRatio=None,
        youngModulus=None,
        timestep=None,
        isViscoelastic=None,
        isAnisotropic=None,
        preferredDirection=None,
        **kwargs
    ):
        """
        CudaTetrahedronTLEDForceField

        :param poissonRatio: Poisson ratio in Hooke's law
        :param youngModulus: Young modulus in Hooke's law
        :param timestep: Simulation timestep
        :param isViscoelastic: Viscoelasticity flag
        :param isAnisotropic: Anisotropy flag
        :param preferredDirection: Transverse isotropy direction
        """
        params = dict(
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            timestep=timestep,
            isViscoelastic=isViscoelastic,
            isAnisotropic=isAnisotropic,
            preferredDirection=preferredDirection,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CudaTetrahedronTLEDForceField", params

    @sofa_component
    def CudaTriangleModel(self, **kwargs):
        """
        CudaTriangleModel
        """
        params = dict()
        return "CudaTriangleModel", params

    @sofa_component
    def CudaTriangularFEMForceFieldOptim(self, **kwargs):
        """
        CudaTriangularFEMForceFieldOptim
        """
        params = dict()
        return "CudaTriangularFEMForceFieldOptim", params

    @sofa_component
    def CudaTypes(self, **kwargs):
        """
        CudaTypes
        """
        params = dict()
        return "CudaTypes", params

    @sofa_component
    def CudaUniformMass(self, **kwargs):
        """
        CudaUniformMass
        """
        params = dict()
        return "CudaUniformMass", params

    @sofa_component
    def mycuda(self, **kwargs):
        """
        mycuda
        """
        params = dict()
        return "mycuda", params

    @sofa_component
    def CudaVisualModel(
        self,
        ambient=None,
        diffuse=None,
        specular=None,
        emissive=None,
        shininess=None,
        useVBO=None,
        computeNormals=None,
        **kwargs
    ):
        """
        CudaVisualModel

        :param ambient: material ambient color
        :param diffuse: material diffuse color and alpha
        :param specular: material specular color
        :param emissive: material emissive color
        :param shininess: material specular shininess
        :param useVBO: true to activate Vertex Buffer Object
        :param computeNormals: true to compute smooth normals
        """
        params = dict(
            ambient=ambient,
            diffuse=diffuse,
            specular=specular,
            emissive=emissive,
            shininess=shininess,
            useVBO=useVBO,
            computeNormals=computeNormals,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CudaVisualModel", params

    @sofa_component
    def CudaDistanceGridCollisionModel(
        self,
        fileCudaRigidDistanceGrid=None,
        scale=None,
        sampling=None,
        box=None,
        nx=None,
        ny=None,
        nz=None,
        dumpfilename=None,
        usePoints=None,
        **kwargs
    ):
        """
        CudaDistanceGridCollisionModel

        :param fileCudaRigidDistanceGrid: load distance grid from specified file
        :param scale: scaling factor for input file
        :param sampling: if not zero: sample the surface with points approximately separated by the given sampling distance (expressed in voxels if the value is negative)
        :param box: Field bounding box defined by xmin,ymin,zmin, xmax,ymax,zmax
        :param nx: number of values on X axis
        :param ny: number of values on Y axis
        :param nz: number of values on Z axis
        :param dumpfilename: write distance grid to specified file
        :param usePoints: use mesh vertices for collision detection
        """
        params = dict(
            fileCudaRigidDistanceGrid=fileCudaRigidDistanceGrid,
            scale=scale,
            sampling=sampling,
            box=box,
            nx=nx,
            ny=ny,
            nz=nz,
            dumpfilename=dumpfilename,
            usePoints=usePoints,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CudaDistanceGridCollisionModel", params

    @sofa_component
    def CudaContactMapper(self, **kwargs):
        """
        CudaContactMapper
        """
        params = dict()
        return "CudaContactMapper", params

    @sofa_component
    def CudaSPHFluidForceField(self, **kwargs):
        """
        CudaSPHFluidForceField
        """
        params = dict()
        return "CudaSPHFluidForceField", params

    @sofa_component
    def CudaParticlesRepulsionForceField(self, **kwargs):
        """
        CudaParticlesRepulsionForceField
        """
        params = dict()
        return "CudaParticlesRepulsionForceField", params

    @sofa_component
    def CudaSpatialGridContainer(self, **kwargs):
        """
        CudaSpatialGridContainer
        """
        params = dict()
        return "CudaSpatialGridContainer", params

    @sofa_component
    def Fluid2D(
        self,
        nx=None,
        ny=None,
        cellwidth=None,
        height=None,
        dir=None,
        tstart=None,
        tstop=None,
        **kwargs
    ):
        """
        Fluid2D

        :param nx: grid size along x axis
        :param ny: grid size along y axis
        :param cellwidth: width of each cell
        :param height: initial fluid height
        :param dir: initial fluid surface normal
        :param tstart: starting time for fluid source
        :param tstop: stopping time for fluid source
        """
        params = dict(
            nx=nx,
            ny=ny,
            cellwidth=cellwidth,
            height=height,
            dir=dir,
            tstart=tstart,
            tstop=tstop,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "Fluid2D", params

    @sofa_component
    def Fluid3D(
        self,
        nx=None,
        ny=None,
        nz=None,
        cellwidth=None,
        center=None,
        height=None,
        dir=None,
        tstart=None,
        tstop=None,
        **kwargs
    ):
        """
        Fluid3D

        :param nx: grid size along x axis
        :param ny: grid size along y axis
        :param nz: grid size along z axis
        :param cellwidth: width of each cell
        :param center: position of grid center
        :param height: initial fluid height
        :param dir: initial fluid surface normal
        :param tstart: starting time for fluid source
        :param tstop: stopping time for fluid source
        """
        params = dict(
            nx=nx,
            ny=ny,
            nz=nz,
            cellwidth=cellwidth,
            center=center,
            height=height,
            dir=dir,
            tstart=tstart,
            tstop=tstop,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "Fluid3D", params

    @sofa_component
    def Grid2D(self, **kwargs):
        """
        Grid2D
        """
        params = dict()
        return "Grid2D", params

    @sofa_component
    def Grid3D(self, **kwargs):
        """
        Grid3D
        """
        params = dict()
        return "Grid3D", params

    @sofa_component
    def OmniDriverEmu(
        self,
        forceScale=None,
        scale=None,
        positionBase=None,
        orientationBase=None,
        positionTool=None,
        orientationTool=None,
        permanent=None,
        omniVisu=None,
        simuFreq=None,
        simulateTranslation=None,
        trajPoints=None,
        trajTiming=None,
        **kwargs
    ):
        """
        OmniDriverEmu

        :param forceScale: Default forceScale applied to the force feedback.
        :param scale: Default scale applied to the Phantom Coordinates.
        :param positionBase: Position of the interface base in the scene world coordinates
        :param orientationBase: Orientation of the interface base in the scene world coordinates
        :param positionTool: Position of the tool in the omni end effector frame
        :param orientationTool: Orientation of the tool in the omni end effector frame
        :param permanent: Apply the force feedback permanently
        :param omniVisu: Visualize the position of the interface in the virtual scene
        :param simuFreq: frequency of the simulated Omni
        :param simulateTranslation: do very naive translation simulation of omni, with constant orientation <0 0 0 1>
        :param trajPoints: Trajectory positions
        :param trajTiming: Trajectory timing
        """
        params = dict(
            forceScale=forceScale,
            scale=scale,
            positionBase=positionBase,
            orientationBase=orientationBase,
            positionTool=positionTool,
            orientationTool=orientationTool,
            permanent=permanent,
            omniVisu=omniVisu,
            simuFreq=simuFreq,
            simulateTranslation=simulateTranslation,
            trajPoints=trajPoints,
            trajTiming=trajTiming,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "OmniDriverEmu", params

    @sofa_component
    def XrayVisualManager(
        self,
        zNear=None,
        zFar=None,
        clearColor=None,
        depthInternalformat=None,
        colorInternalformat=None,
        colorFormat=None,
        colorType=None,
        depthTexture=None,
        enableDepth=None,
        enableColor=None,
        **kwargs
    ):
        """
        XrayVisualManager

        :param zNear: Set zNear distance (for Depth Buffer)
        :param zFar: Set zFar distance (for Depth Buffer)
        :param clearColor: specify clear values for the color buffers
        :param depthInternalformat:
        :param colorInternalformat:
        :param colorFormat:
        :param colorType:
        :param depthTexture: Enable depth texture
        :param enableDepth: Enable depth buffer
        :param enableColor: Enable color buffer
        """
        params = dict(
            zNear=zNear,
            zFar=zFar,
            clearColor=clearColor,
            depthInternalformat=depthInternalformat,
            colorInternalformat=colorInternalformat,
            colorFormat=colorFormat,
            colorType=colorType,
            depthTexture=depthTexture,
            enableDepth=enableDepth,
            enableColor=enableColor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "XrayVisualManager", params

    @sofa_component
    def OglBackGroundNoise(self, **kwargs):
        """
        OglBackGroundNoise
        """
        params = dict()
        return "OglBackGroundNoise", params

    @sofa_component
    def OglMesh(self, useVBO=None, **kwargs):
        """
        OglMesh

        :param useVBO: Use VBO for rendering
        """
        params = dict(useVBO=useVBO)
        params = {k: v for k, v in params.items() if v is not None}
        return "OglMesh", params

    @sofa_component
    def OglRenderPass(
        self,
        writeZTransparent=None,
        alphaBlend=None,
        depthTest=None,
        cullFace=None,
        blendEquation=None,
        sfactor=None,
        dfactor=None,
        **kwargs
    ):
        """
        OglRenderPass

        :param writeZTransparent: Write into Z Buffer for Transparent Object
        :param alphaBlend: Enable alpha blending
        :param depthTest: Enable depth testing
        :param cullFace: Face culling (0 = no culling, 1 = cull back faces, 2 = cull front faces)
        :param blendEquation: if alpha blending is enabled this specifies how source and destination colors are combined
        :param sfactor: if alpha blending is enabled this specifies how the red, green, blue, and alpha source blending factors are computed
        :param dfactor: if alpha blending is enabled this specifies how the red, green, blue, and alpha destination blending factors are computed
        """
        params = dict(
            writeZTransparent=writeZTransparent,
            alphaBlend=alphaBlend,
            depthTest=depthTest,
            cullFace=cullFace,
            blendEquation=blendEquation,
            sfactor=sfactor,
            dfactor=dfactor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "OglRenderPass", params

    @sofa_component
    def PostProcessingVisualModel(
        self,
        zNear=None,
        zFar=None,
        clearColor=None,
        depthInternalformat=None,
        colorInternalformat=None,
        colorFormat=None,
        colorType=None,
        depthTexture=None,
        enableDepth=None,
        enableColor=None,
        **kwargs
    ):
        """
        PostProcessingVisualModel

        :param zNear: Set zNear distance (for Depth Buffer)
        :param zFar: Set zFar distance (for Depth Buffer)
        :param clearColor: specify clear values for the color buffers
        :param depthInternalformat:
        :param colorInternalformat:
        :param colorFormat:
        :param colorType:
        :param depthTexture: Enable depth texture
        :param enableDepth: Enable depth buffer
        :param enableColor: Enable color buffer
        """
        params = dict(
            zNear=zNear,
            zFar=zFar,
            clearColor=clearColor,
            depthInternalformat=depthInternalformat,
            colorInternalformat=colorInternalformat,
            colorFormat=colorFormat,
            colorType=colorType,
            depthTexture=depthTexture,
            enableDepth=enableDepth,
            enableColor=enableColor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PostProcessingVisualModel", params

    @sofa_component
    def TipCatheterCamera(
        self, positions=None, positionIndex=None, offset=None, **kwargs
    ):
        """
        TipCatheterCamera

        :param positions: position coordinates of the degrees of freedom of the catheter
        :param positionIndex: Index of the tip of the catheter in the mechanical object position vector
        :param offset: offset from the mIndex point along the longitudinal direction
        """
        params = dict(positions=positions, positionIndex=positionIndex, offset=offset)
        params = {k: v for k, v in params.items() if v is not None}
        return "TipCatheterCamera", params

    @sofa_component
    def OglMultiModel(self, **kwargs):
        """
        OglMultiModel
        """
        params = dict()
        return "OglMultiModel", params

    @sofa_component
    def TorsoCamera(
        self,
        orientationIn=None,
        positions=None,
        positionIndex=None,
        offset=None,
        **kwargs
    ):
        """
        TorsoCamera

        :param orientationIn: input orientation from another camera
        :param positions: position coordinates of the degrees of freedom of the catheter
        :param positionIndex: Index of the tip of the catheter in the mechanical object position vector
        :param offset: offset from the mIndex point along the longitudinal direction
        """
        params = dict(
            orientationIn=orientationIn,
            positions=positions,
            positionIndex=positionIndex,
            offset=offset,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TorsoCamera", params

    @sofa_component
    def HeartMappingModel(
        self,
        numberDetectionPoints=None,
        textureColor=None,
        textureSize=None,
        plotMap=None,
        key=None,
        display=None,
        activationTimes=None,
        plotActivationMap=None,
        resetMapEvent=None,
        **kwargs
    ):
        """
        HeartMappingModel

        :param numberDetectionPoints: number of points in the collision model 1 creating the 3d map
        :param textureColor: width and height of the texture to create
        :param textureSize: width and height of the texture to create
        :param plotMap: activate the 3d model reconstruction
        :param key: key to press to display the model
        :param display: display the model
        :param activationTimes: Vector containing the activation Times
        :param plotActivationMap: Boolean to plot the activation time map
        :param resetMapEvent: Boolean to reset the activation map
        """
        params = dict(
            numberDetectionPoints=numberDetectionPoints,
            textureColor=textureColor,
            textureSize=textureSize,
            plotMap=plotMap,
            key=key,
            display=display,
            activationTimes=activationTimes,
            plotActivationMap=plotActivationMap,
            resetMapEvent=resetMapEvent,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "HeartMappingModel", params

    @sofa_component
    def Plane2ROI(
        self,
        plane=None,
        point=None,
        normal=None,
        position=None,
        edges=None,
        triangles=None,
        tetrahedra=None,
        computeEdges=None,
        computeTriangles=None,
        computeTetrahedra=None,
        indices=None,
        edgeIndices=None,
        triangleIndices=None,
        tetrahedronIndices=None,
        pointsInROI=None,
        edgesInROI=None,
        trianglesInROI=None,
        tetrahedraInROI=None,
        drawBoxes=None,
        drawPoints=None,
        drawEdges=None,
        drawTriangles=None,
        drawTetrahedra=None,
        drawSize=None,
        translation=None,
        rotationEuler=None,
        rotationQuat=None,
        scale=None,
        **kwargs
    ):
        """
        Plane2ROI

        :param plane: Plane defined by 3 points and a depth distance
        :param point: point in the plane
        :param normal: normal
        :param position: Rest position coordinates of the degrees of freedom
        :param edges: Edge Topology
        :param triangles: Triangle Topology
        :param tetrahedra: Tetrahedron Topology
        :param computeEdges: If true, will compute edge list and index list inside the ROI.
        :param computeTriangles: If true, will compute triangle list and index list inside the ROI.
        :param computeTetrahedra: If true, will compute tetrahedra list and index list inside the ROI.
        :param indices: Indices of the points contained in the ROI
        :param edgeIndices: Indices of the edges contained in the ROI
        :param triangleIndices: Indices of the triangles contained in the ROI
        :param tetrahedronIndices: Indices of the tetrahedra contained in the ROI
        :param pointsInROI: Points contained in the ROI
        :param edgesInROI: Edges contained in the ROI
        :param trianglesInROI: Triangles contained in the ROI
        :param tetrahedraInROI: Tetrahedra contained in the ROI
        :param drawBoxes: Draw Box(es)
        :param drawPoints: Draw Points
        :param drawEdges: Draw Edges
        :param drawTriangles: Draw Triangles
        :param drawTetrahedra: Draw Tetrahedra
        :param drawSize: rendering size for box and topological elements
        :param translation: Translation
        :param rotationEuler: Rotation
        :param rotationQuat: Rotation
        :param scale: Scale
        """
        params = dict(
            plane=plane,
            point=point,
            normal=normal,
            position=position,
            edges=edges,
            triangles=triangles,
            tetrahedra=tetrahedra,
            computeEdges=computeEdges,
            computeTriangles=computeTriangles,
            computeTetrahedra=computeTetrahedra,
            indices=indices,
            edgeIndices=edgeIndices,
            triangleIndices=triangleIndices,
            tetrahedronIndices=tetrahedronIndices,
            pointsInROI=pointsInROI,
            edgesInROI=edgesInROI,
            trianglesInROI=trianglesInROI,
            tetrahedraInROI=tetrahedraInROI,
            drawBoxes=drawBoxes,
            drawPoints=drawPoints,
            drawEdges=drawEdges,
            drawTriangles=drawTriangles,
            drawTetrahedra=drawTetrahedra,
            drawSize=drawSize,
            translation=translation,
            rotationEuler=rotationEuler,
            rotationQuat=rotationQuat,
            scale=scale,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "Plane2ROI", params

    @sofa_component
    def ContractionInitialization(
        self,
        input_values=None,
        tagContraction=None,
        outputs=None,
        filename=None,
        secondaryValues=None,
        **kwargs
    ):
        """
        ContractionInitialization

        :param input_values: input array of manual potential values <index of tetrahedra ,contraction,stiffness>.
        :param tagContraction: Tag of the contraction node
        :param outputs: output array of initial condition contraction and stiffness values.
        :param filename: name of file where to write initial condition potential values.
        :param secondaryValues: default value given to other dimension fields.
        """
        params = dict(
            input_values=input_values,
            tagContraction=tagContraction,
            outputs=outputs,
            filename=filename,
            secondaryValues=secondaryValues,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ContractionInitialization", params

    @sofa_component
    def ContractionForceField(
        self,
        tagContraction=None,
        tagSolver=None,
        DesactivateElastoIfNoElec=None,
        useCoupling=None,
        heartPeriod=None,
        tetraContractivityParam=None,
        fiberDirections=None,
        addElastometry=None,
        elasticModulus=None,
        viscosityParameter=None,
        tetraPloted=None,
        graph=None,
        graph2=None,
        depolarisationTimes=None,
        APD=None,
        file=None,
        useVerdandi=None,
        calculateStress=None,
        stressFile=None,
        SecSPK_passive=None,
        tetrahedronInfo=None,
        edgeInfo=None,
        **kwargs
    ):
        """
        ContractionForceField

        :param tagContraction: Tag of the contraction node
        :param tagSolver: Tag of the Solver Object
        :param DesactivateElastoIfNoElec: set to 1 for calculating the cauchy stress
        :param useCoupling: if the contraction is couple
        :param heartPeriod: heart Period
        :param tetraContractivityParam: <Contractivity,contractionRate,relaxationrate> by tetra
        :param fiberDirections:  file with fibers at each tetra
        :param addElastometry: If we want the elastic component in series
        :param elasticModulus: modulus for the elastic component in series
        :param viscosityParameter: for passive relaxation
        :param tetraPloted: tetra index of values display in graph for each iteration.
        :param graph: Vertex state value per iteration
        :param graph2: Vertex state value per iteration
        :param depolarisationTimes: depolarisationTimes at each node
        :param APD: APD at each node
        :param file: File where to store the Monitoring
        :param useVerdandi: useVerdandi
        :param calculateStress: set to 1 for calculating the cauchy stress
        :param stressFile: name of the output cauchy stress file
        :param SecSPK_passive: second piola kirshoff tensor of passive part
        :param tetrahedronInfo: Data to handle topology on tetrahedra
        :param edgeInfo: Data to handle topology on edges
        """
        params = dict(
            tagContraction=tagContraction,
            tagSolver=tagSolver,
            DesactivateElastoIfNoElec=DesactivateElastoIfNoElec,
            useCoupling=useCoupling,
            heartPeriod=heartPeriod,
            tetraContractivityParam=tetraContractivityParam,
            fiberDirections=fiberDirections,
            addElastometry=addElastometry,
            elasticModulus=elasticModulus,
            viscosityParameter=viscosityParameter,
            tetraPloted=tetraPloted,
            graph=graph,
            graph2=graph2,
            depolarisationTimes=depolarisationTimes,
            APD=APD,
            file=file,
            useVerdandi=useVerdandi,
            calculateStress=calculateStress,
            stressFile=stressFile,
            SecSPK_passive=SecSPK_passive,
            tetrahedronInfo=tetrahedronInfo,
            edgeInfo=edgeInfo,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ContractionForceField", params

    @sofa_component
    def ContractionCouplingForceField(
        self,
        tetraInfo=None,
        tetraContractivityParam=None,
        depolarisationTimes=None,
        uniquedepolarisationTimes=None,
        APD=None,
        n0=None,
        n1=None,
        n2=None,
        file=None,
        StarlingEffect=None,
        alpha=None,
        useSimple=None,
        withFile=None,
        tagMechanics=None,
        withVT=None,
        APDVT=None,
        TdVT=None,
        useVerdandi=None,
        **kwargs
    ):
        """
        ContractionCouplingForceField

        :param tetraInfo: Data to handle topology on tetrahedra
        :param tetraContractivityParam: <Contractivity,stiffness,contractionRate,relaxationrate> by tetra
        :param depolarisationTimes: depolarisationTimes at each node
        :param uniquedepolarisationTimes: depolarisationTimes at each node
        :param APD: APD at each node
        :param n0: reduction parameter between 0 and 1
        :param n1: reduction parameter between 0 and 1
        :param n2: reduction parameter between 0 and 1
        :param file: File where to store the Monitoring
        :param StarlingEffect: if used with verdandi
        :param alpha: alpha
        :param useSimple: If the model should be simplified
        :param withFile: if the electrophysiology is precomputed
        :param tagMechanics: Tag of the Mechanical Object
        :param withVT: if VT TD are used
        :param APDVT: APDVT
        :param TdVT: TdVT
        :param useVerdandi: if used with verdandi
        """
        params = dict(
            tetraInfo=tetraInfo,
            tetraContractivityParam=tetraContractivityParam,
            depolarisationTimes=depolarisationTimes,
            uniquedepolarisationTimes=uniquedepolarisationTimes,
            APD=APD,
            n0=n0,
            n1=n1,
            n2=n2,
            file=file,
            StarlingEffect=StarlingEffect,
            alpha=alpha,
            useSimple=useSimple,
            withFile=withFile,
            tagMechanics=tagMechanics,
            withVT=withVT,
            APDVT=APDVT,
            TdVT=TdVT,
            useVerdandi=useVerdandi,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ContractionCouplingForceField", params

    @sofa_component
    def PressureConstraintForceField(
        self,
        Kiso=None,
        heartPeriod=None,
        atriumParam=None,
        aorticParam=None,
        windkessel=None,
        Pv0=None,
        loadername=None,
        tagSolver=None,
        file=None,
        SurfaceZone=None,
        graphPressure=None,
        graphVolume=None,
        graphFlow=None,
        useProjection=None,
        DisableFirstAtriumContraction=None,
        edgeInfo=None,
        volume=None,
        pressurePv=None,
        pressurePat=None,
        pressurePar=None,
        flowQ=None,
        useVerdandi=None,
        displayName=None,
        loaderZoneNames=None,
        loaderZones=None,
        trianglesSurf=None,
        pointZoneName=None,
        pointZones=None,
        ZoneType=None,
        EdgesOnBorder=None,
        BoundaryEdgesPath=None,
        BoundaryEdgesKey=None,
        **kwargs
    ):
        """
        PressureConstraintForceField

        :param Kiso: parameter K isovolumic
        :param heartPeriod: heart period
        :param atriumParam: Kat, Pat0, Patm, alpha1, alpha2, tof, tm, tc
        :param aorticParam: Kar, Par0, Pve,tau=Rp*C,Rp,Zc,L
        :param windkessel: which model of windkessel (2,3,4)?
        :param Pv0: minimal Pressure ventricule
        :param loadername: give ATET3D or VTK
        :param tagSolver: Tag of the Solver Object
        :param file: File name to register pressures
        :param SurfaceZone: List of triangles on the surface
        :param graphPressure: Pressures per iteration
        :param graphVolume: Volume per iteration
        :param graphFlow: Flow per iteration
        :param useProjection: useProjection
        :param DisableFirstAtriumContraction: DisableFirstAtriumContraction
        :param edgeInfo: Data to handle topology on edges
        :param volume: Volume.
        :param pressurePv: Pressure Pv
        :param pressurePat: Pressure Pat
        :param pressurePar: Pressure Par
        :param flowQ: Flow Q
        :param useVerdandi: useVerdandi
        :param displayName: ONLY used for the Cardiac GUI: name displayed in the GUI
        :param loaderZoneNames: name of the surface zone from the loader
        :param loaderZones: loaderZones
        :param trianglesSurf: list of surface triangles
        :param pointZoneName: list of point zone
        :param pointZones: list of points
        :param ZoneType: Triangles or Points
        :param EdgesOnBorder: List of holes. A hole is an orderred list of point id pairs
        :param BoundaryEdgesPath: Path to the json file containing holes as orderred list of point id pairs
        :param BoundaryEdgesKey: Key (LV|RV) of the ventricle to retrieve edges in json file
        """
        params = dict(
            Kiso=Kiso,
            heartPeriod=heartPeriod,
            atriumParam=atriumParam,
            aorticParam=aorticParam,
            windkessel=windkessel,
            Pv0=Pv0,
            loadername=loadername,
            tagSolver=tagSolver,
            file=file,
            SurfaceZone=SurfaceZone,
            graphPressure=graphPressure,
            graphVolume=graphVolume,
            graphFlow=graphFlow,
            useProjection=useProjection,
            DisableFirstAtriumContraction=DisableFirstAtriumContraction,
            edgeInfo=edgeInfo,
            volume=volume,
            pressurePv=pressurePv,
            pressurePat=pressurePat,
            pressurePar=pressurePar,
            flowQ=flowQ,
            useVerdandi=useVerdandi,
            displayName=displayName,
            loaderZoneNames=loaderZoneNames,
            loaderZones=loaderZones,
            trianglesSurf=trianglesSurf,
            pointZoneName=pointZoneName,
            pointZones=pointZones,
            ZoneType=ZoneType,
            EdgesOnBorder=EdgesOnBorder,
            BoundaryEdgesPath=BoundaryEdgesPath,
            BoundaryEdgesKey=BoundaryEdgesKey,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PressureConstraintForceField", params

    @sofa_component
    def BaseConstraintForceField(
        self,
        normal=None,
        Zone=None,
        kn=None,
        kp=None,
        useForce=None,
        temporaryForce=None,
        temporaryTimes=None,
        heartPeriod=None,
        loadername=None,
        tagSolver=None,
        **kwargs
    ):
        """
        BaseConstraintForceField

        :param normal: vec3d of the normal direction of the spring
        :param Zone: List of tetra on a base
        :param kn: stiffness in the normal direction
        :param kp: stiffness in the parallel direction
        :param useForce: if a force has to be added
        :param temporaryForce: temporaryForce
        :param temporaryTimes: vec3d of the 3 times of force
        :param heartPeriod: heart period
        :param loadername: loader name
        :param tagSolver: Tag of the Solver Object
        """
        params = dict(
            normal=normal,
            Zone=Zone,
            kn=kn,
            kp=kp,
            useForce=useForce,
            temporaryForce=temporaryForce,
            temporaryTimes=temporaryTimes,
            heartPeriod=heartPeriod,
            loadername=loadername,
            tagSolver=tagSolver,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "BaseConstraintForceField", params

    @sofa_component
    def ProjectivePressureConstraint(
        self,
        optimiser=None,
        tagMeca=None,
        FFNames=None,
        phaseNew=None,
        tagSolver=None,
        updateSteps=None,
        **kwargs
    ):
        """
        ProjectivePressureConstraint

        :param optimiser: if the correction should be optimized
        :param tagMeca: tagMeca
        :param FFNames: Names of the pressure forcefields
        :param phaseNew: phaseNew
        :param tagSolver: Tag of the Solver Object
        :param updateSteps: the number of steps after which the projection should be updated
        """
        params = dict(
            optimiser=optimiser,
            tagMeca=tagMeca,
            FFNames=FFNames,
            phaseNew=phaseNew,
            tagSolver=tagSolver,
            updateSteps=updateSteps,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ProjectivePressureConstraint", params

    @sofa_component
    def VolumeRegional(
        self,
        volume=None,
        meshA=None,
        sizemin=None,
        observation=None,
        file=None,
        exception=None,
        **kwargs
    ):
        """
        VolumeRegional

        :param volume: ..
        :param meshA: give mesh with AHA surf zones
        :param sizemin: number of triangles minumum per zones
        :param observation: give 0 for LV_endo, 1 for LVepi, 2 for LV, 3 for RV, 4 for Total
        :param file: file
        :param exception: exception
        """
        params = dict(
            volume=volume,
            meshA=meshA,
            sizemin=sizemin,
            observation=observation,
            file=file,
            exception=exception,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "VolumeRegional", params

    @sofa_component
    def EnergyMonitor(self, file=None, **kwargs):
        """
        EnergyMonitor

        :param file: file
        """
        params = dict(file=file)
        params = {k: v for k, v in params.items() if v is not None}
        return "EnergyMonitor", params

    @sofa_component
    def GeometryMonitor(
        self,
        file=None,
        PointMitralExtremal=None,
        PointTricuspidExtremal=None,
        PointTopSeptum=None,
        PointApexRV=None,
        PointApexLV=None,
        AxisHeart=None,
        AxisRings=None,
        AxisLV=None,
        AxisRV=None,
        BarycentreMesh=None,
        BarycentreTwoRings=None,
        BarycentreRingMitral=None,
        BarycentreRingTricuspid=None,
        BarycentreLVendo=None,
        **kwargs
    ):
        """
        GeometryMonitor

        :param file: file
        :param PointMitralExtremal: PointMitralExtremal
        :param PointTricuspidExtremal: PointTricuspidExtremal
        :param PointTopSeptum: PointTopSeptum
        :param PointApexRV: PointApexRV
        :param PointApexLV: PointApexLV
        :param AxisHeart: AxisHeart
        :param AxisRings: AxisRings
        :param AxisLV: AxisLV
        :param AxisRV: AxisRV
        :param BarycentreMesh: BarycentreMesh
        :param BarycentreTwoRings: BarycentreTwoRings
        :param BarycentreRingMitral: BarycentreRingMitral
        :param BarycentreRingTricuspid: BarycentreRingTricuspid
        :param BarycentreLVendo: BarycentreLVendo
        """
        params = dict(
            file=file,
            PointMitralExtremal=PointMitralExtremal,
            PointTricuspidExtremal=PointTricuspidExtremal,
            PointTopSeptum=PointTopSeptum,
            PointApexRV=PointApexRV,
            PointApexLV=PointApexLV,
            AxisHeart=AxisHeart,
            AxisRings=AxisRings,
            AxisLV=AxisLV,
            AxisRV=AxisRV,
            BarycentreMesh=BarycentreMesh,
            BarycentreTwoRings=BarycentreTwoRings,
            BarycentreRingMitral=BarycentreRingMitral,
            BarycentreRingTricuspid=BarycentreRingTricuspid,
            BarycentreLVendo=BarycentreLVendo,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "GeometryMonitor", params

    @sofa_component
    def MRForceField(
        self,
        matrixRegularization=None,
        ParameterSet=None,
        tetrahedronInfo=None,
        edgeInfo=None,
        file=None,
        useVerdandi=None,
        depolarisationTimes=None,
        APD=None,
        heartPeriod=None,
        activeRelaxation=None,
        MaxPeakActiveRelaxation=None,
        calculateStress=None,
        MRStressPK=None,
        **kwargs
    ):
        """
        MRForceField

        :param matrixRegularization: Regularization of the Stiffness Matrix (true or false)
        :param ParameterSet: The global parameters specifying the Mooney-rivlin material
        :param tetrahedronInfo: Data to handle topology on tetrahedra
        :param edgeInfo: Data to handle topology on edges
        :param file: File where to store the Jacobian
        :param useVerdandi: useVerdandi
        :param depolarisationTimes: depolarisationTimes at each node
        :param APD: APD at each node
        :param heartPeriod: heart Period
        :param activeRelaxation: Use or not an active relaxation triggering after the end of depolarisation
        :param MaxPeakActiveRelaxation: Multiplicative factor in front of each c1 c2 I in active realxation
        :param calculateStress: set to 1 for calculating the cauchy stress
        :param MRStressPK: Second Piola-Kirshoff stress from MR part (= passive part)
        """
        params = dict(
            matrixRegularization=matrixRegularization,
            ParameterSet=ParameterSet,
            tetrahedronInfo=tetrahedronInfo,
            edgeInfo=edgeInfo,
            file=file,
            useVerdandi=useVerdandi,
            depolarisationTimes=depolarisationTimes,
            APD=APD,
            heartPeriod=heartPeriod,
            activeRelaxation=activeRelaxation,
            MaxPeakActiveRelaxation=MaxPeakActiveRelaxation,
            calculateStress=calculateStress,
            MRStressPK=MRStressPK,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MRForceField", params

    @sofa_component
    def CostaForceField(
        self,
        tensorDirections=None,
        fiberDirections=None,
        matrixRegularization=None,
        ParameterSet=None,
        file=None,
        tetrahedronInfo=None,
        edgeInfo=None,
        **kwargs
    ):
        """
        CostaForceField

        :param tensorDirections:  file with DTI tensor at each tetra
        :param fiberDirections:  file with fibers at each tetra
        :param matrixRegularization: Regularization of the Stiffness Matrix (true or false)
        :param ParameterSet: The global parameters specifying the material
        :param file: File where to store the Jacobian
        :param tetrahedronInfo: Data to handle topology on tetrahedra
        :param edgeInfo: Data to handle topology on edges
        """
        params = dict(
            tensorDirections=tensorDirections,
            fiberDirections=fiberDirections,
            matrixRegularization=matrixRegularization,
            ParameterSet=ParameterSet,
            file=file,
            tetrahedronInfo=tetrahedronInfo,
            edgeInfo=edgeInfo,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CostaForceField", params

    @sofa_component
    def GenerateCardiacCylinder(
        self,
        output_position=None,
        tetrahedra=None,
        radius=None,
        height=None,
        origin=None,
        resCircumferential=None,
        resRadial=None,
        resHeight=None,
        facetFibers=None,
        depolarisationTimes=None,
        APD=None,
        APD_input=None,
        **kwargs
    ):
        """
        GenerateCardiacCylinder

        :param output_position: output array of 3d points
        :param tetrahedra: output mesh tetrahedra
        :param radius: input cylinder radius
        :param height: input cylinder height
        :param origin: cylinder origin point
        :param resCircumferential: Resolution in the circumferential direction
        :param resRadial: Resolution in the radial direction
        :param resHeight: Resolution in the height direction
        :param facetFibers: Fiber par facet of the mesh loaded.
        :param depolarisationTimes: depolarisationTimes at each node
        :param APD: APD at each node
        :param APD_input: Action potential duration given as input
        """
        params = dict(
            output_position=output_position,
            tetrahedra=tetrahedra,
            radius=radius,
            height=height,
            origin=origin,
            resCircumferential=resCircumferential,
            resRadial=resRadial,
            resHeight=resHeight,
            facetFibers=facetFibers,
            depolarisationTimes=depolarisationTimes,
            APD=APD,
            APD_input=APD_input,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "GenerateCardiacCylinder", params

    @sofa_component
    def CardiacViewer(self, **kwargs):
        """
        CardiacViewer
        """
        params = dict()
        return "CardiacViewer", params

    @sofa_component
    def MainWindow(self, **kwargs):
        """
        MainWindow
        """
        params = dict()
        return "MainWindow", params

    @sofa_component
    def StiffnessContractionParams(self, **kwargs):
        """
        StiffnessContractionParams
        """
        params = dict()
        return "StiffnessContractionParams", params

    @sofa_component
    def BoundaryConditionParams(self, **kwargs):
        """
        BoundaryConditionParams
        """
        params = dict()
        return "BoundaryConditionParams", params

    @sofa_component
    def SimParams(self, **kwargs):
        """
        SimParams
        """
        params = dict()
        return "SimParams", params

    @sofa_component
    def ExportParams(self, **kwargs):
        """
        ExportParams
        """
        params = dict()
        return "ExportParams", params

    @sofa_component
    def CardiacAnimationControls(self, **kwargs):
        """
        CardiacAnimationControls
        """
        params = dict()
        return "CardiacAnimationControls", params

    @sofa_component
    def CardiacVideoRecorderManager(self, **kwargs):
        """
        CardiacVideoRecorderManager
        """
        params = dict()
        return "CardiacVideoRecorderManager", params

    @sofa_component
    def CardiacGUI(self, **kwargs):
        """
        CardiacGUI
        """
        params = dict()
        return "CardiacGUI", params

    @sofa_component
    def qDebugStream(self, **kwargs):
        """
        qDebugStream
        """
        params = dict()
        return "qDebugStream", params

    @sofa_component
    def CircularBuffer(self, **kwargs):
        """
        CircularBuffer
        """
        params = dict()
        return "CircularBuffer", params

    @sofa_component
    def PressuresPlot(
        self,
        interval=None,
        subSteps=None,
        displayPv=None,
        displayPat=None,
        displayPar=None,
        indiceToPlot=None,
        plotEveryNbSteps=None,
        color=None,
        lineWidth=None,
        axisScale=None,
        origin=None,
        exportPv=None,
        exportPat=None,
        exportPar=None,
        **kwargs
    ):
        """
        PressuresPlot

        :param interval: Time interval to display in seconds
        :param subSteps: Number of substeps, use only with the MultiStepAnimationLoop
        :param displayPv: Path of the value to plot
        :param displayPat: Path of the value to plot
        :param displayPar: Path of the value to plot
        :param indiceToPlot: Indice of potential to plot
        :param plotEveryNbSteps: Plot only at specified number of steps (0=disable)
        :param color: Color used to display the curve
        :param lineWidth: width of the line used to display the curve
        :param axisScale: [Xmin,Xmax,Ymin,Ymax] scale for X and Y axis
        :param origin: [X0, Y0] origin point
        :param exportPv: to connect to the CardiacSimulationExporter
        :param exportPat: to connect to the CardiacSimulationExporter
        :param exportPar: to connect to the CardiacSimulationExporter
        """
        params = dict(
            interval=interval,
            subSteps=subSteps,
            displayPv=displayPv,
            displayPat=displayPat,
            displayPar=displayPar,
            indiceToPlot=indiceToPlot,
            plotEveryNbSteps=plotEveryNbSteps,
            color=color,
            lineWidth=lineWidth,
            axisScale=axisScale,
            origin=origin,
            exportPv=exportPv,
            exportPat=exportPat,
            exportPar=exportPar,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PressuresPlot", params

    @sofa_component
    def VolumePlot(
        self,
        interval=None,
        subSteps=None,
        display=None,
        export=None,
        indiceToPlot=None,
        plotEveryNbSteps=None,
        color=None,
        lineWidth=None,
        axisScale=None,
        origin=None,
        **kwargs
    ):
        """
        VolumePlot

        :param interval: Time interval to display in seconds
        :param subSteps: Number of substeps, use only with the MultiStepAnimationLoop
        :param display: Path of the value to plot
        :param export: to connect to the CardiacSimulationExporter
        :param indiceToPlot: Indice of potential to plot
        :param plotEveryNbSteps: Plot only at specified number of steps (0=disable)
        :param color: Color used to display the curve
        :param lineWidth: width of the line used to display the curve
        :param axisScale: [Xmin,Xmax,Ymin,Ymax] scale for X and Y axis
        :param origin: [X0, Y0] origin point
        """
        params = dict(
            interval=interval,
            subSteps=subSteps,
            display=display,
            export=export,
            indiceToPlot=indiceToPlot,
            plotEveryNbSteps=plotEveryNbSteps,
            color=color,
            lineWidth=lineWidth,
            axisScale=axisScale,
            origin=origin,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "VolumePlot", params

    @sofa_component
    def FlowQPlot(
        self,
        interval=None,
        subSteps=None,
        display=None,
        export=None,
        indiceToPlot=None,
        plotEveryNbSteps=None,
        color=None,
        lineWidth=None,
        axisScale=None,
        origin=None,
        **kwargs
    ):
        """
        FlowQPlot

        :param interval: Time interval to display in seconds
        :param subSteps: Number of substeps, use only with the MultiStepAnimationLoop
        :param display: Path of the value to plot
        :param export: to connect to the CardiacSimulationExporter
        :param indiceToPlot: Indice of potential to plot
        :param plotEveryNbSteps: Plot only at specified number of steps (0=disable)
        :param color: Color used to display the curve
        :param lineWidth: width of the line used to display the curve
        :param axisScale: [Xmin,Xmax,Ymin,Ymax] scale for X and Y axis
        :param origin: [X0, Y0] origin point
        """
        params = dict(
            interval=interval,
            subSteps=subSteps,
            display=display,
            export=export,
            indiceToPlot=indiceToPlot,
            plotEveryNbSteps=plotEveryNbSteps,
            color=color,
            lineWidth=lineWidth,
            axisScale=axisScale,
            origin=origin,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "FlowQPlot", params

    @sofa_component
    def CardiacAnimation(
        self,
        animationFile=None,
        indices=None,
        frequency=None,
        keyframeInterpolation=None,
        synchronized=None,
        inputPosition=None,
        outputPosition=None,
        inputElectro=None,
        outputElectro=None,
        **kwargs
    ):
        """
        CardiacAnimation

        :param animationFile:  Path to the binary file storing the animation
        :param indices: Indices of the animated points
        :param frequency: heartbeat frequency
        :param keyframeInterpolation: play the animation with a linear interpolation between the keyframes
        :param synchronized: synchronize the animation with simulation time step
        :param inputPosition: source object to copy
        :param outputPosition: output position. link as parent to mechanical object position attrribute
        :param inputElectro: source object to copy
        :param outputElectro: output position. link as parent to mechanical object position attrribute
        """
        params = dict(
            animationFile=animationFile,
            indices=indices,
            frequency=frequency,
            keyframeInterpolation=keyframeInterpolation,
            synchronized=synchronized,
            inputPosition=inputPosition,
            outputPosition=outputPosition,
            inputElectro=inputElectro,
            outputElectro=outputElectro,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CardiacAnimation", params

    @sofa_component
    def CardiacAnimationExporter(self, **kwargs):
        """
        CardiacAnimationExporter
        """
        params = dict()
        return "CardiacAnimationExporter", params

    @sofa_component
    def CardiacAnimationData(self, **kwargs):
        """
        CardiacAnimationData
        """
        params = dict()
        return "CardiacAnimationData", params

    @sofa_component
    def CardiacAnimationFileSerializer(self, **kwargs):
        """
        CardiacAnimationFileSerializer
        """
        params = dict()
        return "CardiacAnimationFileSerializer", params

    @sofa_component
    def SceneDataExchange(self, to=None, **kwargs):
        """
        SceneDataExchange

        :param to: destination object to copy
        """
        params = dict(to=to)
        params = {k: v for k, v in params.items() if v is not None}
        return "SceneDataExchange", params

    @sofa_component
    def CardiacPickHandler(self, **kwargs):
        """
        CardiacPickHandler
        """
        params = dict()
        return "CardiacPickHandler", params

    @sofa_component
    def ClipPlaneRigid(
        self,
        position=None,
        normal=None,
        displaySize=None,
        id=None,
        active=None,
        **kwargs
    ):
        """
        ClipPlaneRigid

        :param position: Point crossed by the clipping plane
        :param normal: Normal of the clipping plane, pointing toward the clipped region
        :param displaySize: size of the display plane
        :param id: Clipping plane OpenGL ID
        :param active: Control whether the clipping plane should be applied or not
        """
        params = dict(
            position=position,
            normal=normal,
            displaySize=displaySize,
            id=id,
            active=active,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ClipPlaneRigid", params

    @sofa_component
    def FibersVisualModel(
        self, tetraFibers=None, tetraBFibers=None, fiberLength=None, **kwargs
    ):
        """
        FibersVisualModel

        :param tetraFibers: Tetrahedral fibers in world coordinates.
        :param tetraBFibers: Tetrahedal fibers in barycentric coordinates.
        :param fiberLength: Fiber length visualisation.
        """
        params = dict(
            tetraFibers=tetraFibers, tetraBFibers=tetraBFibers, fiberLength=fiberLength
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "FibersVisualModel", params

    @sofa_component
    def euHeartViewer(self, **kwargs):
        """
        euHeartViewer
        """
        params = dict()
        return "euHeartViewer", params

    @sofa_component
    def RenderWindowViewer(self, **kwargs):
        """
        RenderWindowViewer
        """
        params = dict()
        return "RenderWindowViewer", params

    @sofa_component
    def PluginManagerWindowGUI(self, **kwargs):
        """
        PluginManagerWindowGUI
        """
        params = dict()
        return "PluginManagerWindowGUI", params

    @sofa_component
    def ElectroSignalsViewer(self, **kwargs):
        """
        ElectroSignalsViewer
        """
        params = dict()
        return "ElectroSignalsViewer", params

    @sofa_component
    def mainWindowGUI(self, **kwargs):
        """
        mainWindowGUI
        """
        params = dict()
        return "mainWindowGUI", params

    @sofa_component
    def SecondWindow(self, screen=None, size=None, title=None, **kwargs):
        """
        SecondWindow

        :param screen: id number of the screen in case of multi-screen app
        :param size: width and height of the window. set to 0 for full screen window
        :param title: title of the second window
        """
        params = dict(screen=screen, size=size, title=title)
        params = {k: v for k, v in params.items() if v is not None}
        return "SecondWindow", params

    @sofa_component
    def StaticRenderViewer(self, **kwargs):
        """
        StaticRenderViewer
        """
        params = dict()
        return "StaticRenderViewer", params

    @sofa_component
    def TaskSchedulerBoost(self, **kwargs):
        """
        TaskSchedulerBoost
        """
        params = dict()
        return "TaskSchedulerBoost", params

    @sofa_component
    def GUIeuHeart(self, **kwargs):
        """
        GUIeuHeart
        """
        params = dict()
        return "GUIeuHeart", params

    @sofa_component
    def euHeartViewerSetting(self, updateVisual=None, **kwargs):
        """
        euHeartViewerSetting

        :param updateVisual: Boolean activating the visual update visitor
        """
        params = dict(updateVisual=updateVisual)
        params = {k: v for k, v in params.items() if v is not None}
        return "euHeartViewerSetting", params

    @sofa_component
    def SubWindow(
        self, screen=None, title=None, viewer=None, size=None, view=None, **kwargs
    ):
        """
        SubWindow

        :param screen: id number of the screen in case of multi-screen app
        :param title: title of the subwindow
        :param viewer: name of the viewer used to display
        :param size: width and height of the window. set to 0 for full screen window
        :param view: id number of the view in case of multi-view app
        """
        params = dict(screen=screen, title=title, viewer=viewer, size=size, view=view)
        params = {k: v for k, v in params.items() if v is not None}
        return "SubWindow", params

    @sofa_component
    def ElectrophysiologyPlot(
        self,
        interval=None,
        subSteps=None,
        samplingFrequency=None,
        display=None,
        indiceToPlot=None,
        bipolarSignal=None,
        plotEveryNbSteps=None,
        color=None,
        lineWidth=None,
        axisScale=None,
        origin=None,
        XaxisTitle=None,
        YaxisTitle=None,
        **kwargs
    ):
        """
        ElectrophysiologyPlot

        :param interval: Time interval to display in seconds
        :param subSteps: Number of substeps, use only with the MultiStepAnimationLoop
        :param samplingFrequency: Frequency to update the display values
        :param display: Path of the value to plot
        :param indiceToPlot: Indice of potential to plot
        :param bipolarSignal: display bipolar signals
        :param plotEveryNbSteps: Plot only at specified number of steps (0=disable)
        :param color: Color used to display the curve
        :param lineWidth: width of the line used to display the curve
        :param axisScale: [Xmin,Xmax,Ymin,Ymax] scale for X and Y axis
        :param origin: [X0, Y0] origin point
        :param XaxisTitle: Define the X label of the plot
        :param YaxisTitle: Define the Y label of the plot
        """
        params = dict(
            interval=interval,
            subSteps=subSteps,
            samplingFrequency=samplingFrequency,
            display=display,
            indiceToPlot=indiceToPlot,
            bipolarSignal=bipolarSignal,
            plotEveryNbSteps=plotEveryNbSteps,
            color=color,
            lineWidth=lineWidth,
            axisScale=axisScale,
            origin=origin,
            XaxisTitle=XaxisTitle,
            YaxisTitle=YaxisTitle,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ElectrophysiologyPlot", params

    @sofa_component
    def circularbuffer(self, **kwargs):
        """
        circularbuffer
        """
        params = dict()
        return "circularbuffer", params

    @sofa_component
    def Signal(self, **kwargs):
        """
        Signal
        """
        params = dict()
        return "Signal", params

    @sofa_component
    def SignalsState(self, **kwargs):
        """
        SignalsState
        """
        params = dict()
        return "SignalsState", params

    @sofa_component
    def SignalsStateEngine(
        self,
        polarizationState=None,
        atrialPolarizationState=None,
        output=None,
        samplingFrequency=None,
        depolarizationSignal=None,
        repolarizationSignal=None,
        restSignal=None,
        noisySignal=None,
        atrialDepolarizationSignal=None,
        depolSignalScale=None,
        repolSignalScale=None,
        restSignalScale=None,
        noisySignalScale=None,
        atrialDepolSignalScale=None,
        **kwargs
    ):
        """
        SignalsStateEngine

        :param polarizationState: depolarization or repolarization state
        :param atrialPolarizationState: atrial depolarization (0) or repolarization (1) state
        :param output: signal output values
        :param samplingFrequency: Frequency to update the display values
        :param depolarizationSignal: .txt file defined the a signal template
        :param repolarizationSignal: .txt file defined the a signal template
        :param restSignal: .txt file defined the a signal template
        :param noisySignal: .txt file defined the a signal template
        :param atrialDepolarizationSignal: .txt file defined the atrial depolarization signal template
        :param depolSignalScale: scale the depol signal display values
        :param repolSignalScale: scale the repol signal display values
        :param restSignalScale: scale the rest signal display values
        :param noisySignalScale: scale the noisy signal display values
        :param atrialDepolSignalScale: scale the atrial depol signal display values
        """
        params = dict(
            polarizationState=polarizationState,
            atrialPolarizationState=atrialPolarizationState,
            output=output,
            samplingFrequency=samplingFrequency,
            depolarizationSignal=depolarizationSignal,
            repolarizationSignal=repolarizationSignal,
            restSignal=restSignal,
            noisySignal=noisySignal,
            atrialDepolarizationSignal=atrialDepolarizationSignal,
            depolSignalScale=depolSignalScale,
            repolSignalScale=repolSignalScale,
            restSignalScale=restSignalScale,
            noisySignalScale=noisySignalScale,
            atrialDepolSignalScale=atrialDepolSignalScale,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SignalsStateEngine", params

    @sofa_component
    def AtrialStateEngine(
        self,
        polarizationState=None,
        heartPeriod=None,
        depolDelay=None,
        depolDuration=None,
        **kwargs
    ):
        """
        AtrialStateEngine

        :param polarizationState: depolarization (0) or repolarization (1) state
        :param heartPeriod: heart period
        :param depolDelay: the delay before the start of depolarization
        :param depolDuration:  the duration of depolarization
        """
        params = dict(
            polarizationState=polarizationState,
            heartPeriod=heartPeriod,
            depolDelay=depolDelay,
            depolDuration=depolDuration,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "AtrialStateEngine", params

    @sofa_component
    def MeshTriangulation(
        self,
        neighborTable=None,
        edgesOnBorder=None,
        trianglesOnBorderList=None,
        m_zoneNames=None,
        **kwargs
    ):
        """
        MeshTriangulation

        :param neighborTable: Vertices of the mesh loaded
        :param edgesOnBorder: Edges of the mesh on the border
        :param trianglesOnBorderList: List of triangles on the border
        :param m_zoneNames: See zones Name.
        """
        params = dict(
            neighborTable=neighborTable,
            edgesOnBorder=edgesOnBorder,
            trianglesOnBorderList=trianglesOnBorderList,
            m_zoneNames=m_zoneNames,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshTriangulation", params

    @sofa_component
    def MeshTetrahedrisationLoader(
        self,
        neighborTable=None,
        tetrahedraOnBorderList=None,
        edgesOnBorder=None,
        trianglesOnBorder=None,
        numberOfZone=None,
        zoneNames=None,
        zoneSizes=None,
        numberOfSurfaceZone=None,
        surfaceZoneNames=None,
        surfaceZoneSizes=None,
        surfaceZones=None,
        FileNodeFiber=None,
        nodeFibers=None,
        FileFacetFiber=None,
        facetFibers=None,
        FileFacetBFiber=None,
        facetBFibers=None,
        FileTetraTensor=None,
        tetraTensor=None,
        FileContractionParameters=None,
        ContractionParameters=None,
        InputContractionParameters=None,
        ContractionParametersZones=None,
        FileStiffnessParameters=None,
        StiffnessParameters=None,
        StiffnessParametersZones=None,
        FileTetraConductivity=None,
        tetraConductivity=None,
        InputStiffnessParameters=None,
        ElectroFile=None,
        velocityFile=None,
        velocities=None,
        unitTime=None,
        startContraction=None,
        depoTimes=None,
        APDTimes=None,
        APDTimesZones=None,
        APDTimesString=None,
        APDTimesFile=None,
        APDdefault=None,
        createZones=None,
        planZone=None,
        outputMesh=None,
        MSinitSurfaceZoneNames=None,
        MSinitVertices=None,
        **kwargs
    ):
        """
        MeshTetrahedrisationLoader

        :param neighborTable: Vertices of the mesh loaded
        :param tetrahedraOnBorderList: List of tetrahedra on the border
        :param edgesOnBorder: Edges of the mesh on the border
        :param trianglesOnBorder: Edges of the mesh on the border
        :param numberOfZone: Vertices of the mesh loaded
        :param zoneNames: See zones Name.
        :param zoneSizes: See zones Size.
        :param numberOfSurfaceZone: Vertices of the mesh loaded
        :param surfaceZoneNames: See surface zones Name.
        :param surfaceZoneSizes: See surface zones Size.
        :param surfaceZones: See surface zones Size.
        :param FileNodeFiber: Filename of the fiber par node of the mesh loaded (.bb file).
        :param nodeFibers: Fiber par node of the mesh loaded.
        :param FileFacetFiber: Filename of the fiber par facet of the mesh loaded (.tbb file).
        :param facetFibers: Fiber par facet of the mesh loaded.
        :param FileFacetBFiber: Filename of the fiber par facet of the mesh loaded, described in barycentric coordinates (.lbb file).
        :param facetBFibers: Fiber par facet of the mesh loaded, described in barycentric coordinates.
        :param FileTetraTensor: Filename of the tensor for each vertex on a tetra (.ttsr file)
        :param tetraTensor: tensor for each vertex on a tetra
        :param FileContractionParameters: Filename of the .txt containing the contraction parameters per zonename
        :param ContractionParameters: Parameter for linking to ContractionParameters from other components.
        :param InputContractionParameters: contraction parameter at each tetra
        :param ContractionParametersZones: contraction parameter per zone
        :param FileStiffnessParameters: Filename of the .txt containing the stiffness parameters per zonename
        :param StiffnessParameters: Parameter for linking to StiffnessParameters from other components.
        :param StiffnessParametersZones: Parameter for linking to StiffnessParameters from other components.
        :param FileTetraConductivity: FileTetraConductivity
        :param tetraConductivity:  Conductivity per tetra for MF electrical wave
        :param InputStiffnessParameters: stiffness parameter at each tetra
        :param ElectroFile: File with precomputed electrophysiology
        :param velocityFile: File with intial velocities
        :param velocities: initial velocities
        :param unitTime: unit of the time scale use for electrophysiology (s or ms)
        :param startContraction: time at which the contraction starts
        :param depoTimes: Times of depolarization per node
        :param APDTimes: Times of APD per node
        :param APDTimesZones: Times of APD per node
        :param APDTimesString: Times of APD per node
        :param APDTimesFile: Times of APD per node
        :param APDdefault: APDdefault
        :param createZones: if the loader must create the base and LV_endo, RV_endo
        :param planZone: plan z=b above which the base is defined, for 2 valves model only
        :param outputMesh: output atet3D mesh with created zones
        :param MSinitSurfaceZoneNames: Input-names of the surface zones for the init pacing of Mitchell Shaeffer (need for coupling)
        :param MSinitVertices: Output-list of vertices of the init pacing of Mitchell Shaeffer (need for coupling)
        """
        params = dict(
            neighborTable=neighborTable,
            tetrahedraOnBorderList=tetrahedraOnBorderList,
            edgesOnBorder=edgesOnBorder,
            trianglesOnBorder=trianglesOnBorder,
            numberOfZone=numberOfZone,
            zoneNames=zoneNames,
            zoneSizes=zoneSizes,
            numberOfSurfaceZone=numberOfSurfaceZone,
            surfaceZoneNames=surfaceZoneNames,
            surfaceZoneSizes=surfaceZoneSizes,
            surfaceZones=surfaceZones,
            FileNodeFiber=FileNodeFiber,
            nodeFibers=nodeFibers,
            FileFacetFiber=FileFacetFiber,
            facetFibers=facetFibers,
            FileFacetBFiber=FileFacetBFiber,
            facetBFibers=facetBFibers,
            FileTetraTensor=FileTetraTensor,
            tetraTensor=tetraTensor,
            FileContractionParameters=FileContractionParameters,
            ContractionParameters=ContractionParameters,
            InputContractionParameters=InputContractionParameters,
            ContractionParametersZones=ContractionParametersZones,
            FileStiffnessParameters=FileStiffnessParameters,
            StiffnessParameters=StiffnessParameters,
            StiffnessParametersZones=StiffnessParametersZones,
            FileTetraConductivity=FileTetraConductivity,
            tetraConductivity=tetraConductivity,
            InputStiffnessParameters=InputStiffnessParameters,
            ElectroFile=ElectroFile,
            velocityFile=velocityFile,
            velocities=velocities,
            unitTime=unitTime,
            startContraction=startContraction,
            depoTimes=depoTimes,
            APDTimes=APDTimes,
            APDTimesZones=APDTimesZones,
            APDTimesString=APDTimesString,
            APDTimesFile=APDTimesFile,
            APDdefault=APDdefault,
            createZones=createZones,
            planZone=planZone,
            outputMesh=outputMesh,
            MSinitSurfaceZoneNames=MSinitSurfaceZoneNames,
            MSinitVertices=MSinitVertices,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshTetrahedrisationLoader", params

    @sofa_component
    def MeshDxfLoader(self, **kwargs):
        """
        MeshDxfLoader
        """
        params = dict()
        return "MeshDxfLoader", params

    @sofa_component
    def MeshExporter(self, saveMesh=None, filename=None, saveFibers=None, **kwargs):
        """
        MeshExporter

        :param saveMesh: if true save mesh
        :param filename: output file name. Extension available are atr3D or atet3D
        :param saveFibers: if true save fibers. In the same name as mesh file, with the extension lbb
        """
        params = dict(saveMesh=saveMesh, filename=filename, saveFibers=saveFibers)
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshExporter", params

    @sofa_component
    def MeshINPLoader(self, readResults=None, filenameRpt=None, **kwargs):
        """
        MeshINPLoader

        :param readResults: Read results of abaqus simulation .rpt file
        :param filenameRpt: Filename of the rpt result file of abaqus
        """
        params = dict(readResults=readResults, filenameRpt=filenameRpt)
        params = {k: v for k, v in params.items() if v is not None}
        return "MeshINPLoader", params

    @sofa_component
    def TopologyVisualisation(
        self,
        computeDisplay=None,
        positions=None,
        edges=None,
        triangles=None,
        tetrahedra=None,
        numberOfZone=None,
        drawZones=None,
        zones=None,
        zoneSizes=None,
        numberOfSurfaceZone=None,
        drawSurfaceZones=None,
        wireFrame=None,
        surfaceZones=None,
        surfaceZoneSizes=None,
        FiberLength=None,
        drawFibers=None,
        nodeFibers=None,
        drawTetraFibers=None,
        facetFibers=None,
        drawTetraBFibers=None,
        facetBFibers=None,
        **kwargs
    ):
        """
        TopologyVisualisation

        :param computeDisplay: Debug : recompute display lists.
        :param positions: Data to handle topology on points
        :param edges: Data to handle topology on points
        :param triangles: Data to handle topology on points
        :param tetrahedra: Data to handle topology on points
        :param numberOfZone: Vertices of the mesh loaded
        :param drawZones: Debug : allow visualisations for Mesh zones.
        :param zones: See zones Name.
        :param zoneSizes: See zones Size.
        :param numberOfSurfaceZone: Vertices of the mesh loaded
        :param drawSurfaceZones: Debug : allow visualisations for Mesh surface zones.
        :param wireFrame: Debug : allow visualisations for Mesh surface zones in wire frame.
        :param surfaceZones: See surface zones Name.
        :param surfaceZoneSizes: See surface zones Size.
        :param FiberLength: Debug : Fiber length visualisation.
        :param drawFibers: Debug : Fiber visualisation.
        :param nodeFibers: Fiber par node of the mesh loaded.
        :param drawTetraFibers: Debug : Tetra Fiber visualisation.
        :param facetFibers: Fiber par facet of the mesh loaded.
        :param drawTetraBFibers: Debug : Tetra barycentrique Fiber visualisation.
        :param facetBFibers: Fiber par facet of the mesh loaded, described in barycentric coordinates.
        """
        params = dict(
            computeDisplay=computeDisplay,
            positions=positions,
            edges=edges,
            triangles=triangles,
            tetrahedra=tetrahedra,
            numberOfZone=numberOfZone,
            drawZones=drawZones,
            zones=zones,
            zoneSizes=zoneSizes,
            numberOfSurfaceZone=numberOfSurfaceZone,
            drawSurfaceZones=drawSurfaceZones,
            wireFrame=wireFrame,
            surfaceZones=surfaceZones,
            surfaceZoneSizes=surfaceZoneSizes,
            FiberLength=FiberLength,
            drawFibers=drawFibers,
            nodeFibers=nodeFibers,
            drawTetraFibers=drawTetraFibers,
            facetFibers=facetFibers,
            drawTetraBFibers=drawTetraBFibers,
            facetBFibers=facetBFibers,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TopologyVisualisation", params

    @sofa_component
    def CardiacVTKLoader(
        self,
        numberOfZone=None,
        m_zoneNames=None,
        m_zoneSizes=None,
        numberOfSurfaceZone=None,
        m_surfaceZoneNames=None,
        m_surfaceZoneSizes=None,
        FileNodeFiber=None,
        nodeFibers=None,
        FileFacetFiber=None,
        facetFibers=None,
        FileFacetBFiber=None,
        facetBFibers=None,
        FileTetraTensor=None,
        tetraTensor=None,
        FileContractionParameters=None,
        ContractionParameters=None,
        InputContractionParameters=None,
        FileStiffnessParameters=None,
        StiffnessParameters=None,
        InputStiffnessParameters=None,
        ElectroFile=None,
        velocityFile=None,
        velocities=None,
        unitTime=None,
        startContraction=None,
        depoTimes=None,
        APDTimes=None,
        FileTetraConductivity=None,
        tetraConductivity=None,
        APDTimesZones=None,
        APDTimesString=None,
        APDTimesFile=None,
        MSinitSurfaceZoneNames=None,
        CellTypes=None,
        createFibers=None,
        planZone=None,
        outputNodeFibers=None,
        outputTetraFibers=None,
        angleEpi=None,
        angleEndo=None,
        withAHA=None,
        TetraZoneName=None,
        AHAzoneName=None,
        TriZoneName=None,
        TetraTriangle=None,
        LVRVBase=None,
        PointZoneName=None,
        **kwargs
    ):
        """
        CardiacVTKLoader

        :param numberOfZone: Vertices of the mesh loaded
        :param m_zoneNames: See zones Name.
        :param m_zoneSizes: See zones Size.
        :param numberOfSurfaceZone: Vertices of the mesh loaded
        :param m_surfaceZoneNames: See surface zones Name.
        :param m_surfaceZoneSizes: See surface zones Size.
        :param FileNodeFiber: Filename of the fiber par node of the mesh loaded (.bb file).
        :param nodeFibers: Fiber par node of the mesh loaded.
        :param FileFacetFiber: Filename of the fiber par facet of the mesh loaded (.tbb file).
        :param facetFibers: Fiber par facet of the mesh loaded.
        :param FileFacetBFiber: Filename of the fiber par facet of the mesh loaded, described in barycentric coordinates (.lbb file).
        :param facetBFibers: Fiber par facet of the mesh loaded, described in barycentric coordinates.
        :param FileTetraTensor: Filename of the tensor for each vertex on a tetra (.ttsr file)
        :param tetraTensor: tensor for each vertex on a tetra
        :param FileContractionParameters: Filename of the .txt containing the contraction parameters per zonename
        :param ContractionParameters: Parameter for linking to ContractionParameters from other components.
        :param InputContractionParameters: contraction parameter at each tetra
        :param FileStiffnessParameters: Filename of the .txt containing the stiffness parameters per zonename
        :param StiffnessParameters: Parameter for linking to StiffnessParameters from other components.
        :param InputStiffnessParameters: stiffness parameter at each tetra
        :param ElectroFile: File with precomputed electrophysiology
        :param velocityFile: File with intial velocities
        :param velocities: initial velocities
        :param unitTime: unit of the time scale use for electrophysiology (s or ms)
        :param startContraction: time at which the contraction starts
        :param depoTimes: Times of depolarization per node
        :param APDTimes: Times of APD per node
        :param FileTetraConductivity: FileTetraConductivity
        :param tetraConductivity:  Conductivity per tetra for MF electrical wave
        :param APDTimesZones: Times of APD per node
        :param APDTimesString: Times of APD per node
        :param APDTimesFile: Times of APD per node
        :param MSinitSurfaceZoneNames: Input-names of the surface zones for the init pacing of Mitchell Shaeffer (need for coupling)
        :param CellTypes: Type of each cell element
        :param createFibers: if the loader must create the Fibers
        :param planZone: plan z=b above which the base is defined, for 2 valves model only
        :param outputNodeFibers: output Fibers
        :param outputTetraFibers: output Tetra Fibers
        :param angleEpi: if the loader must create the Fibers
        :param angleEndo: if the loader must create the Fibers
        :param withAHA: with AHA zones
        :param TetraZoneName: name of the tetra data
        :param AHAzoneName: name of the tetra data
        :param TriZoneName: name of the endo epi data
        :param TetraTriangle: Tetra or Triangle mesh
        :param LVRVBase: int vector with the number of the zones in LV,RV,Base order for TetraZoneName
        :param PointZoneName: PointZoneName
        """
        params = dict(
            numberOfZone=numberOfZone,
            m_zoneNames=m_zoneNames,
            m_zoneSizes=m_zoneSizes,
            numberOfSurfaceZone=numberOfSurfaceZone,
            m_surfaceZoneNames=m_surfaceZoneNames,
            m_surfaceZoneSizes=m_surfaceZoneSizes,
            FileNodeFiber=FileNodeFiber,
            nodeFibers=nodeFibers,
            FileFacetFiber=FileFacetFiber,
            facetFibers=facetFibers,
            FileFacetBFiber=FileFacetBFiber,
            facetBFibers=facetBFibers,
            FileTetraTensor=FileTetraTensor,
            tetraTensor=tetraTensor,
            FileContractionParameters=FileContractionParameters,
            ContractionParameters=ContractionParameters,
            InputContractionParameters=InputContractionParameters,
            FileStiffnessParameters=FileStiffnessParameters,
            StiffnessParameters=StiffnessParameters,
            InputStiffnessParameters=InputStiffnessParameters,
            ElectroFile=ElectroFile,
            velocityFile=velocityFile,
            velocities=velocities,
            unitTime=unitTime,
            startContraction=startContraction,
            depoTimes=depoTimes,
            APDTimes=APDTimes,
            FileTetraConductivity=FileTetraConductivity,
            tetraConductivity=tetraConductivity,
            APDTimesZones=APDTimesZones,
            APDTimesString=APDTimesString,
            APDTimesFile=APDTimesFile,
            MSinitSurfaceZoneNames=MSinitSurfaceZoneNames,
            CellTypes=CellTypes,
            createFibers=createFibers,
            planZone=planZone,
            outputNodeFibers=outputNodeFibers,
            outputTetraFibers=outputTetraFibers,
            angleEpi=angleEpi,
            angleEndo=angleEndo,
            withAHA=withAHA,
            TetraZoneName=TetraZoneName,
            AHAzoneName=AHAzoneName,
            TriZoneName=TriZoneName,
            TetraTriangle=TetraTriangle,
            LVRVBase=LVRVBase,
            PointZoneName=PointZoneName,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CardiacVTKLoader", params

    @sofa_component
    def CardiacPointsData(self, **kwargs):
        """
        CardiacPointsData
        """
        params = dict()
        return "CardiacPointsData", params

    @sofa_component
    def CardiacSimulationExporter(
        self,
        depolarizationTime=None,
        localMeasurementPoints=None,
        Filename=None,
        ExportSeparateFiles=None,
        ExportStartStep=None,
        ExportFileType=None,
        ExportEveryNSteps=None,
        ExportDepolarizationTime=None,
        ExportDepolarizationTimeOnce=None,
        ExportAPD=None,
        ExportElapsedTime=None,
        ExportEc=None,
        ExportE1d=None,
        ExportSigmaC=None,
        ExportScale=None,
        Points=None,
        Edges=None,
        Triangles=None,
        Quads=None,
        Tetras=None,
        Hexas=None,
        RightVolume=None,
        LeftVolume=None,
        RightPressurePv=None,
        LeftPressurePv=None,
        RightPressurePat=None,
        LeftPressurePat=None,
        RightPressurePar=None,
        LeftPressurePar=None,
        RightFlowQ=None,
        LeftFlowQ=None,
        Potential=None,
        APD90=None,
        stopDepolarizationTime=None,
        **kwargs
    ):
        """
        CardiacSimulationExporter

        :param depolarizationTime: Time of depolarization for each point
        :param localMeasurementPoints: Optional vector containing the ids \n of the local points that are \n studied for depolarization
        :param Filename: Filename
        :param ExportSeparateFiles: True if each type of data is to be exported in its own file
        :param ExportStartStep: The step at which exporting begins.
        :param ExportFileType: Export File Type
        :param ExportEveryNSteps: Export a file every N steps
        :param ExportDepolarizationTime: True if the depolarization times are to be exported.
        :param ExportDepolarizationTimeOnce: True if the depolarization time is to be exported separately once at the end of calculation.
        :param ExportAPD: True if the APD is to be exported.
        :param ExportElapsedTime: True if the overall time elapsed and the time for N steps to elapse is exported.
        :param ExportEc: ExportEc.
        :param ExportE1d: ExportE1d.
        :param ExportSigmaC: ExportSigmaC.
        :param ExportScale: Scale the MechanicalState by the given value.
        :param Points: Point data
        :param Edges: Edge Data
        :param Triangles: Triangle Data
        :param Quads: Quad Data
        :param Tetras: Tetra Data
        :param Hexas: Hexa Data
        :param RightVolume: Right Volume
        :param LeftVolume: Left Volume
        :param RightPressurePv: Right Pressure Pv
        :param LeftPressurePv: Left Pressure Pv
        :param RightPressurePat: Right Pressure Pat
        :param LeftPressurePat: Left Pressure Pat
        :param RightPressurePar: Left Pressure Par
        :param LeftPressurePar: Left Pressure Par
        :param RightFlowQ: Right Flow Q
        :param LeftFlowQ: Left Flow Q
        :param Potential: Electric Potential
        :param APD90: Action Potential Duration 90%
        :param stopDepolarizationTime: Time at which the depolarization times should all be computed.
        """
        params = dict(
            depolarizationTime=depolarizationTime,
            localMeasurementPoints=localMeasurementPoints,
            Filename=Filename,
            ExportSeparateFiles=ExportSeparateFiles,
            ExportStartStep=ExportStartStep,
            ExportFileType=ExportFileType,
            ExportEveryNSteps=ExportEveryNSteps,
            ExportDepolarizationTime=ExportDepolarizationTime,
            ExportDepolarizationTimeOnce=ExportDepolarizationTimeOnce,
            ExportAPD=ExportAPD,
            ExportElapsedTime=ExportElapsedTime,
            ExportEc=ExportEc,
            ExportE1d=ExportE1d,
            ExportSigmaC=ExportSigmaC,
            ExportScale=ExportScale,
            Points=Points,
            Edges=Edges,
            Triangles=Triangles,
            Quads=Quads,
            Tetras=Tetras,
            Hexas=Hexas,
            RightVolume=RightVolume,
            LeftVolume=LeftVolume,
            RightPressurePv=RightPressurePv,
            LeftPressurePv=LeftPressurePv,
            RightPressurePat=RightPressurePat,
            LeftPressurePat=LeftPressurePat,
            RightPressurePar=RightPressurePar,
            LeftPressurePar=LeftPressurePar,
            RightFlowQ=RightFlowQ,
            LeftFlowQ=LeftFlowQ,
            Potential=Potential,
            APD90=APD90,
            stopDepolarizationTime=stopDepolarizationTime,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CardiacSimulationExporter", params

    @sofa_component
    def CardiacFieldData(self, **kwargs):
        """
        CardiacFieldData
        """
        params = dict()
        return "CardiacFieldData", params

    @sofa_component
    def CardiacFiletypeExporter(self, **kwargs):
        """
        CardiacFiletypeExporter
        """
        params = dict()
        return "CardiacFiletypeExporter", params

    @sofa_component
    def CardiacSpreadsheetExporter(self, **kwargs):
        """
        CardiacSpreadsheetExporter
        """
        params = dict()
        return "CardiacSpreadsheetExporter", params

    @sofa_component
    def CardiacVisualizationToolkitExporter(self, **kwargs):
        """
        CardiacVisualizationToolkitExporter
        """
        params = dict()
        return "CardiacVisualizationToolkitExporter", params

    @sofa_component
    def CardiacVtkExporter(self, **kwargs):
        """
        CardiacVtkExporter
        """
        params = dict()
        return "CardiacVtkExporter", params

    @sofa_component
    def CardiacVtuExporter(self, **kwargs):
        """
        CardiacVtuExporter
        """
        params = dict()
        return "CardiacVtuExporter", params

    @sofa_component
    def CardiacImpulseController(
        self,
        heartSignal=None,
        potentialOutput=None,
        initTime=None,
        impulseTime=None,
        restTime=None,
        oneLoopTime=None,
        factor=None,
        graph=None,
        **kwargs
    ):
        """
        CardiacImpulseController

        :param heartSignal: True = apply real heart impulses\n False = apply a periodic rectangular function.
        :param potentialOutput: Value of the controlled potential
        :param initTime: Time at which the first stimulus is applied.
        :param impulseTime: Duration of the stimulus.
        :param restTime: Duration of the rest period.
        :param oneLoopTime: Duration of one loop.
        :param factor: Multiplying the reference curve.
        :param graph: Graph of the controlled potential
        """
        params = dict(
            heartSignal=heartSignal,
            potentialOutput=potentialOutput,
            initTime=initTime,
            impulseTime=impulseTime,
            restTime=restTime,
            oneLoopTime=oneLoopTime,
            factor=factor,
            graph=graph,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CardiacImpulseController", params

    @sofa_component
    def CardiacImpulseConstraint(
        self,
        indices=None,
        indicesSecondStimulus=None,
        amplitude=None,
        secondVariableInput=None,
        singleVelocity=None,
        initTriangleFunction=None,
        tagMechanics=None,
        tolerance=None,
        computeJstim=None,
        JstimOut=None,
        startTime=None,
        stimuliDuration=None,
        stimuliPeriod=None,
        adaptGlobalTimeStep=None,
        stimulusValue=None,
        **kwargs
    ):
        """
        CardiacImpulseConstraint

        :param indices: Indices of the nodes used for the stimuli.
        :param indicesSecondStimulus: Indices of the nodes used for a possible second stimulus.
        :param amplitude: Value of the amplitude of the controlled potential
        :param secondVariableInput: Value of a possible second variable
        :param singleVelocity: Single velocity constraint applied uniformly
        :param initTriangleFunction: Max value of the triangular function (computed from abscissa X)
        :param tagMechanics: Tag of the Mechanical Object.
        :param tolerance: Real for the threshold used for the correction. \n(No correction if = 0.0)
        :param computeJstim: Boolean activating the computation of an initial Jstim
        :param JstimOut: Output vector for the stimulation
        :param startTime: Time at which the constraint starts to be applied
        :param stimuliDuration: Time during which the constraint is applied
        :param stimuliPeriod: Time elapsed between two stimuli
        :param adaptGlobalTimeStep: Real defining the new global time step to impose
        :param stimulusValue: Value of the stimulus to apply (output)
        """
        params = dict(
            indices=indices,
            indicesSecondStimulus=indicesSecondStimulus,
            amplitude=amplitude,
            secondVariableInput=secondVariableInput,
            singleVelocity=singleVelocity,
            initTriangleFunction=initTriangleFunction,
            tagMechanics=tagMechanics,
            tolerance=tolerance,
            computeJstim=computeJstim,
            JstimOut=JstimOut,
            startTime=startTime,
            stimuliDuration=stimuliDuration,
            stimuliPeriod=stimuliPeriod,
            adaptGlobalTimeStep=adaptGlobalTimeStep,
            stimulusValue=stimulusValue,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CardiacImpulseConstraint", params

    @sofa_component
    def EikonalIntegrationScheme(
        self,
        flagContainer=None,
        depolarisationTime=None,
        repolarisationTime=None,
        electricalConductivity=None,
        electricalAnisotropy=None,
        nbrIter=None,
        tetraBFibers=None,
        tetraFibers=None,
        tetraConductivity=None,
        init=None,
        drawConduc=None,
        unitScale=None,
        loaderZoneNames=None,
        loaderZones=None,
        loaderZoneNamesPoint=None,
        loaderZonesPoint=None,
        ZoneType=None,
        actionPotentialDurationHomogeneous=None,
        APD_default_homogeneous=None,
        outputFile_homogeneous=None,
        **kwargs
    ):
        """
        EikonalIntegrationScheme

        :param flagContainer: Rayleigh damping coefficient related to stiffness
        :param depolarisationTime: Depolarization time in sec
        :param repolarisationTime: Rayleigh damping coefficient related to mass
        :param electricalConductivity: Rayleigh damping coefficient related to mass
        :param electricalAnisotropy: Rayleigh damping coefficient related to mass
        :param nbrIter: Rayleigh damping coefficient related to mass
        :param tetraBFibers: Rayleigh damping coefficient related to mass
        :param tetraFibers: Rayleigh damping coefficient related to mass
        :param tetraConductivity: Conductivity for each tetrahedron,, by default equal to electricalConductivity.
        :param init: Rayleigh damping coefficient related to mass
        :param drawConduc: Rayleigh damping coefficient related to mass
        :param unitScale: scale by comparison with the geometry (for instance if geometry is 1e-3, this is 1e3
        :param loaderZoneNames: name of the surface zone from the loader
        :param loaderZones: loaderZones
        :param loaderZoneNamesPoint: name of the surface zone from the loader
        :param loaderZonesPoint: loaderZones
        :param ZoneType: Tetra, tri or Point
        :param actionPotentialDurationHomogeneous: Homogeneous APD, only for Eikonal without Multi Front
        :param APD_default_homogeneous: Input of the homogeneous APD, only for Eikonal without Multi Front
        :param outputFile_homogeneous: output file with Td and APD per node, only for Eikonal without Multi Front. Default is Null
        """
        params = dict(
            flagContainer=flagContainer,
            depolarisationTime=depolarisationTime,
            repolarisationTime=repolarisationTime,
            electricalConductivity=electricalConductivity,
            electricalAnisotropy=electricalAnisotropy,
            nbrIter=nbrIter,
            tetraBFibers=tetraBFibers,
            tetraFibers=tetraFibers,
            tetraConductivity=tetraConductivity,
            init=init,
            drawConduc=drawConduc,
            unitScale=unitScale,
            loaderZoneNames=loaderZoneNames,
            loaderZones=loaderZones,
            loaderZoneNamesPoint=loaderZoneNamesPoint,
            loaderZonesPoint=loaderZonesPoint,
            ZoneType=ZoneType,
            actionPotentialDurationHomogeneous=actionPotentialDurationHomogeneous,
            APD_default_homogeneous=APD_default_homogeneous,
            outputFile_homogeneous=outputFile_homogeneous,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "EikonalIntegrationScheme", params

    @sofa_component
    def EikonalIntegrationScheme_optimized(
        self,
        m_dataVertices=None,
        flagContainer=None,
        nbrIter=None,
        initNodes=None,
        initNodes2=None,
        electricalConductivity=None,
        tetraConductivity=None,
        electricalAnisotropy=None,
        tetraBFibers=None,
        tetraFibers=None,
        useSyntheticFibers=None,
        fiberDirection=None,
        drawTime=None,
        drawConduc=None,
        drawInterpol=None,
        drawFibers=None,
        fiberLength=None,
        loaderSurfaceZoneNames=None,
        loaderSurfaceZones=None,
        loaderZoneNames=None,
        loaderZones=None,
        heartMesh=None,
        RightV=None,
        LeftV=None,
        scars=None,
        isthmus=None,
        isthmusConductivity=None,
        exportData=None,
        filename=None,
        dataVertices=None,
        **kwargs
    ):
        """
        EikonalIntegrationScheme_optimized

        :param m_dataVertices: Data to handle topology on vertices.
        :param flagContainer: Container of Eikonal flag for each node.
        :param nbrIter: Number of iteration of FMM to be perfomed for 1 timestep
        :param initNodes: Initial zone paced. If empty, will do nothing.
        :param initNodes2: Initial zone paced. If empty, will do nothing.
        :param electricalConductivity: Global tetrahedral conductivity.
        :param tetraConductivity: Conductivity for each tetrahedron,, by default equal to electricalConductivity.
        :param electricalAnisotropy: Anisotropy ratio, (longitudinal conductivity)/(transverse conductivity). Default is 1 = isotropy.
        :param tetraBFibers: Tetrahedal fibers in barycentric coordinates.
        :param tetraFibers: Tetrahedral fibers in world coordinates.
        :param useSyntheticFibers: To use simulate a single synthetic fiber direction.
        :param fiberDirection: To simulate a single synthetic fiber direction.
        :param drawTime: To display real time values instead of eikonal state.
        :param drawConduc: To display conductivity map.
        :param drawInterpol: To display conductivity map interpolated regarding APD duration.
        :param drawFibers: To display Fiber directions.
        :param fiberLength: Fiber length visualisation.
        :param loaderSurfaceZoneNames: See surface zones Name loaded from MeshTetrahedrisationLoader.
        :param loaderSurfaceZones: See surface zones Size loaded from MeshTetrahedrisationLoader.
        :param loaderZoneNames: See zones Name loaded from MeshTetrahedrisationLoader.
        :param loaderZones: Zones loaded from MeshTetrahedrisationLoader.
        :param heartMesh: If true, will use meshLoader and use Scars, LV RV,...
        :param RightV: Rayleigh damping coefficient related to mass
        :param LeftV: Rayleigh damping coefficient related to mass
        :param scars: Rayleigh damping coefficient related to mass
        :param isthmus: Rayleigh damping coefficient related to mass
        :param isthmusConductivity: Rayleigh damping coefficient related to mass
        :param exportData: To data at each timestep.
        :param filename: output file name. Extension csv will be added.
        :param dataVertices: Rayleigh damping coefficient related to mass
        """
        params = dict(
            m_dataVertices=m_dataVertices,
            flagContainer=flagContainer,
            nbrIter=nbrIter,
            initNodes=initNodes,
            initNodes2=initNodes2,
            electricalConductivity=electricalConductivity,
            tetraConductivity=tetraConductivity,
            electricalAnisotropy=electricalAnisotropy,
            tetraBFibers=tetraBFibers,
            tetraFibers=tetraFibers,
            useSyntheticFibers=useSyntheticFibers,
            fiberDirection=fiberDirection,
            drawTime=drawTime,
            drawConduc=drawConduc,
            drawInterpol=drawInterpol,
            drawFibers=drawFibers,
            fiberLength=fiberLength,
            loaderSurfaceZoneNames=loaderSurfaceZoneNames,
            loaderSurfaceZones=loaderSurfaceZones,
            loaderZoneNames=loaderZoneNames,
            loaderZones=loaderZones,
            heartMesh=heartMesh,
            RightV=RightV,
            LeftV=LeftV,
            scars=scars,
            isthmus=isthmus,
            isthmusConductivity=isthmusConductivity,
            exportData=exportData,
            filename=filename,
            dataVertices=dataVertices,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "EikonalIntegrationScheme_optimized", params

    @sofa_component
    def ExplicitBDFSolver(self, **kwargs):
        """
        ExplicitBDFSolver
        """
        params = dict()
        return "ExplicitBDFSolver", params

    @sofa_component
    def ExportState(
        self,
        filename=None,
        finalTime=None,
        dtExport=None,
        uniqueNode=None,
        secondVariable=None,
        velocityExport=None,
        onlyTdepoAPD=None,
        noAPD=None,
        interpolationLine=None,
        nbPoints=None,
        tagMechanics=None,
        exportInitValues=None,
        fixedGeometry=None,
        **kwargs
    ):
        """
        ExportState

        :param filename: Name of the file to write
        :param finalTime: Value of the final time of the export
        :param dtExport: Time step between two exports \n(if 0 only one export at finalTime)
        :param uniqueNode: ID of the node we want to export the state
        :param secondVariable: Export the second Variable
        :param velocityExport: Export Velocity !! only on ONE node !!
        :param onlyTdepoAPD: Boolean to export Tdepo,Xdepo and APD
        :param noAPD: Boolean coupled with onlyTdepoAPD, not to wait for APD
        :param interpolationLine: Give two values to define a line \nwhere 'nbPoints' points are going to be exported
        :param nbPoints: Nb of interpolation points (default = 200)
        :param tagMechanics: Tag of the Mechanical Object.
        :param exportInitValues: Boolean to export initial values init.csv
        :param fixedGeometry: Boolean to consider the geometry as fix
        """
        params = dict(
            filename=filename,
            finalTime=finalTime,
            dtExport=dtExport,
            uniqueNode=uniqueNode,
            secondVariable=secondVariable,
            velocityExport=velocityExport,
            onlyTdepoAPD=onlyTdepoAPD,
            noAPD=noAPD,
            interpolationLine=interpolationLine,
            nbPoints=nbPoints,
            tagMechanics=tagMechanics,
            exportInitValues=exportInitValues,
            fixedGeometry=fixedGeometry,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ExportState", params

    @sofa_component
    def GearOdeSolver(
        self,
        verbose=None,
        precompute=None,
        tagDiffusion=None,
        tagReaction=None,
        **kwargs
    ):
        """
        GearOdeSolver

        :param verbose: Dump system state at each iteration
        :param precompute: Boolean true if the linear solver use a preconditioner.
        :param tagDiffusion: Tag of the Diffusion Force Field
        :param tagReaction: Tag of the Reaction Force Field
        """
        params = dict(
            verbose=verbose,
            precompute=precompute,
            tagDiffusion=tagDiffusion,
            tagReaction=tagReaction,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "GearOdeSolver", params

    @sofa_component
    def HeartSimulationPerformer(self, **kwargs):
        """
        HeartSimulationPerformer
        """
        params = dict()
        return "HeartSimulationPerformer", params

    @sofa_component
    def HeartSimulationManager(
        self,
        modelTool=None,
        modelSurface=None,
        active=None,
        key=None,
        keySwitch=None,
        conductivity=None,
        scaleValue=None,
        **kwargs
    ):
        """
        HeartSimulationManager

        :param modelTool: Tool model path
        :param modelSurface: TriangleSetModel or SphereModel path
        :param active: Activate this object.\nNote that this can be dynamically controlled by using a key
        :param key: key to press to activate this object until the key is released
        :param keySwitch: key to activate this object until the key is pressed again
        :param conductivity: change conductivity (%)
        :param scaleValue: scale value of selector
        """
        params = dict(
            modelTool=modelTool,
            modelSurface=modelSurface,
            active=active,
            key=key,
            keySwitch=keySwitch,
            conductivity=conductivity,
            scaleValue=scaleValue,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "HeartSimulationManager", params

    @sofa_component
    def ImplicitIonicTermSolver(self, tagDiffusion=None, tagReaction=None, **kwargs):
        """
        ImplicitIonicTermSolver

        :param tagDiffusion: Tag of the Diffusion Force Field
        :param tagReaction: Tag of the Mitchell Schaeffer Force Field
        """
        params = dict(tagDiffusion=tagDiffusion, tagReaction=tagReaction)
        params = {k: v for k, v in params.items() if v is not None}
        return "ImplicitIonicTermSolver", params

    @sofa_component
    def MCNABOdeSolver(
        self,
        verbose=None,
        precompute=None,
        tagDiffusion=None,
        tagReaction=None,
        useSingleOptimization=None,
        **kwargs
    ):
        """
        MCNABOdeSolver

        :param verbose: Dump system state at each iteration
        :param precompute: Boolean true if the linear solver use a preconditioner.
        :param tagDiffusion: Tag of the Diffusion Force Field
        :param tagReaction: Tag of the Reaction Force Field
        :param useSingleOptimization: Boolean allowing the use of single-operation optimizations
        """
        params = dict(
            verbose=verbose,
            precompute=precompute,
            tagDiffusion=tagDiffusion,
            tagReaction=tagReaction,
            useSingleOptimization=useSingleOptimization,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MCNABOdeSolver", params

    @sofa_component
    def MultiFrontEikonalIntegrationScheme(
        self,
        refractoryPeriod=None,
        diastolicInterval=None,
        actionPotentialDuration=None,
        heartPeriod=None,
        activated=None,
        electricalConductivity=None,
        APD_default=None,
        fixedHeartPeriod=None,
        startcontraction=None,
        outputFile=None,
        **kwargs
    ):
        """
        MultiFrontEikonalIntegrationScheme

        :param refractoryPeriod: Rayleigh damping coefficient related to stiffness
        :param diastolicInterval: Rayleigh damping coefficient related to mass
        :param actionPotentialDuration: Rayleigh damping coefficient related to mass
        :param heartPeriod: Rayleigh damping coefficient related to mass
        :param activated: Rayleigh damping coefficient related to mass
        :param electricalConductivity: Rayleigh damping coefficient related to mass
        :param APD_default: Action potential duration default
        :param fixedHeartPeriod:  set to true if the period is fixed
        :param startcontraction: time to start contraction
        :param outputFile: output file with Td and APD per node
        """
        params = dict(
            refractoryPeriod=refractoryPeriod,
            diastolicInterval=diastolicInterval,
            actionPotentialDuration=actionPotentialDuration,
            heartPeriod=heartPeriod,
            activated=activated,
            electricalConductivity=electricalConductivity,
            APD_default=APD_default,
            fixedHeartPeriod=fixedHeartPeriod,
            startcontraction=startcontraction,
            outputFile=outputFile,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MultiFrontEikonalIntegrationScheme", params

    @sofa_component
    def MultiFrontEikonalIntegrationScheme_optimized(
        self,
        waveStart=None,
        wavePeriod=None,
        interactivePacing=None,
        nbrWave=None,
        **kwargs
    ):
        """
        MultiFrontEikonalIntegrationScheme_optimized

        :param waveStart: First front time start.
        :param wavePeriod: Time duration of a heart periode
        :param interactivePacing: If true, will start only with events.
        :param nbrWave: Number of front to generate.
        """
        params = dict(
            waveStart=waveStart,
            wavePeriod=wavePeriod,
            interactivePacing=interactivePacing,
            nbrWave=nbrWave,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "MultiFrontEikonalIntegrationScheme_optimized", params

    @sofa_component
    def PotentielInitialization(
        self,
        input_values=None,
        outputsPotentiel=None,
        writeFile=None,
        filename=None,
        secondaryValues=None,
        initTime=None,
        inputConstantValue=None,
        **kwargs
    ):
        """
        PotentielInitialization

        :param input_values: input array of manual potential values <index , value>.
        :param outputsPotentiel: output array of initial condition potential values.
        :param writeFile: write initial condition potential values in a file.
        :param filename: name of file where to write initial condition potential values.
        :param secondaryValues: default value given to other dimension fields.
        :param initTime: duration of injection of init values.
        :param inputConstantValue: Input value for the whole state.
        """
        params = dict(
            input_values=input_values,
            outputsPotentiel=outputsPotentiel,
            writeFile=writeFile,
            filename=filename,
            secondaryValues=secondaryValues,
            initTime=initTime,
            inputConstantValue=inputConstantValue,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "PotentielInitialization", params

    @sofa_component
    def SBDFOdeSolver(
        self,
        verbose=None,
        precompute=None,
        tagDiffusion=None,
        tagReaction=None,
        fullExplicit=None,
        **kwargs
    ):
        """
        SBDFOdeSolver

        :param verbose: Dump system state at each iteration
        :param precompute: Boolean true if the linear solver use a preconditioner.
        :param tagDiffusion: Tag of the Diffusion Force Field
        :param tagReaction: Tag of the Reaction Force Field
        :param fullExplicit: Boolean enabling to switch from semi-implicit to full explicit scheme
        """
        params = dict(
            verbose=verbose,
            precompute=precompute,
            tagDiffusion=tagDiffusion,
            tagReaction=tagReaction,
            fullExplicit=fullExplicit,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SBDFOdeSolver", params

    @sofa_component
    def SyntheticHeartBeats(
        self,
        filename=None,
        timeStart=None,
        timeStep=None,
        maxStep=None,
        position=None,
        potentials=None,
        applyTrans=None,
        **kwargs
    ):
        """
        SyntheticHeartBeats

        :param filename: Filename of the object
        :param timeStart: Rayleigh damping coefficient related to mass
        :param timeStep: Rayleigh damping coefficient related to mass
        :param maxStep: Rayleigh damping coefficient related to mass
        :param position: positions values
        :param potentials: potential values
        :param applyTrans: Apply a magic transfo for HeC
        """
        params = dict(
            filename=filename,
            timeStart=timeStart,
            timeStep=timeStep,
            maxStep=maxStep,
            position=position,
            potentials=potentials,
            applyTrans=applyTrans,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SyntheticHeartBeats", params

    @sofa_component
    def TetrahedralDiffusionForceField(
        self,
        edgeInfo=None,
        tagMechanics=None,
        diffusivity=None,
        scalarDiffusion=None,
        tetraDiffusivity=None,
        vertexDiffusivity=None,
        dimensionless=None,
        multiplyingTetraCoefficient=None,
        anisotropyRatio=None,
        transverseAnisotropyArray=None,
        adaptiveDiffusivity=None,
        numberOfZone=None,
        zoneSizes=None,
        zones=None,
        diffusionPerZone=None,
        drawConduc=None,
        atomicGPU=None,
        nbThreadX=None,
        explicitDiffusion=None,
        **kwargs
    ):
        """
        TetrahedralDiffusionForceField

        :param edgeInfo: Data to handle topology on edges
        :param tagMechanics: Tag of the Mechanical Object.
        :param diffusivity: Diffusion Coefficient
        :param scalarDiffusion: if true, diffuse only on the first dimension.
        :param tetraDiffusivity: Diffusivity for each tetrahedron, by default equal to diffusivity.
        :param vertexDiffusivity: Diffusivity for each vertex, by default non-defined.
        :param dimensionless: Coefficient enabling the equation to be dimensionless
        :param multiplyingTetraCoefficient: Vector multiplying the diffusivity inside the tetrahedra
        :param anisotropyRatio: Anisotropy ratio (r²>1).\n Default is 1.0 = isotropy.
        :param transverseAnisotropyArray: Data to handle topology on tetrahedra
        :param adaptiveDiffusivity: if true, compute diffusivity depending on\n the volume of each tetrahedra.
        :param numberOfZone: Number of zones in the mesh.
        :param zoneSizes: Vector of the size of each zone.
        :param zones: Vector containing all the tetrahedra for each zones.
        :param diffusionPerZone: Diffusion coefficient associated at each zone.
        :param drawConduc: To display conductivity map.
        :param atomicGPU: True if the GPU can handle atomic operations (CUDA version > 2.0)
        :param nbThreadX: Number of threads (<=8) to use for the loop to accumulate for on points (Cuda version, non atomic)
        :param explicitDiffusion: Boolean true if explicit only
        """
        params = dict(
            edgeInfo=edgeInfo,
            tagMechanics=tagMechanics,
            diffusivity=diffusivity,
            scalarDiffusion=scalarDiffusion,
            tetraDiffusivity=tetraDiffusivity,
            vertexDiffusivity=vertexDiffusivity,
            dimensionless=dimensionless,
            multiplyingTetraCoefficient=multiplyingTetraCoefficient,
            anisotropyRatio=anisotropyRatio,
            transverseAnisotropyArray=transverseAnisotropyArray,
            adaptiveDiffusivity=adaptiveDiffusivity,
            numberOfZone=numberOfZone,
            zoneSizes=zoneSizes,
            zones=zones,
            diffusionPerZone=diffusionPerZone,
            drawConduc=drawConduc,
            atomicGPU=atomicGPU,
            nbThreadX=nbThreadX,
            explicitDiffusion=explicitDiffusion,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralDiffusionForceField", params

    @sofa_component
    def TetrahedralFitzhughNagumoForceField(
        self,
        vertexInfo=None,
        tetrahedronInfo=None,
        repolFactor=None,
        polyFactor=None,
        polyRoot=None,
        repolRate=None,
        lumpMassMatrix=None,
        tagMechanics=None,
        integrationOrder=None,
        **kwargs
    ):
        """
        TetrahedralFitzhughNagumoForceField

        :param vertexInfo: Data to handle topology on vertices
        :param tetrahedronInfo: Data to handle topology on tetrahedra
        :param repolFactor: repolarization_factor
        :param polyFactor: polyFactor Coefficient
        :param polyRoot: polyRoot Coefficient
        :param repolRate: repolarization_rate
        :param lumpMassMatrix: whether the mass matrix should be lumped (true) or not (false)
        :param tagMechanics: Tag of the Mechanical Object
        :param integrationOrder: Order of the integration of the reaction part
        """
        params = dict(
            vertexInfo=vertexInfo,
            tetrahedronInfo=tetrahedronInfo,
            repolFactor=repolFactor,
            polyFactor=polyFactor,
            polyRoot=polyRoot,
            repolRate=repolRate,
            lumpMassMatrix=lumpMassMatrix,
            tagMechanics=tagMechanics,
            integrationOrder=integrationOrder,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralFitzhughNagumoForceField", params

    @sofa_component
    def TetrahedralMitchellSchaefferForceField(
        self,
        vertexInfo=None,
        tetrahedronInfo=None,
        inwardTime=None,
        vertexInwardTime=None,
        outwardTime=None,
        vertexOutwardTime=None,
        openingTime=None,
        vertexOpeningTime=None,
        closingTime=None,
        vertexClosingTime=None,
        tauCloseFactor=None,
        uGate=None,
        vertexUGate=None,
        amplitudeAP=None,
        vertexAmplitudeAP=None,
        repolFactor=None,
        tagMechanics=None,
        amplitudeSinus=None,
        startTime=None,
        endTime=None,
        stimuliDuration=None,
        stimuliPeriod=None,
        indicesSinus=None,
        stimulus=None,
        bidomain=None,
        implicitComputation=None,
        forceNoStimulus=None,
        **kwargs
    ):
        """
        TetrahedralMitchellSchaefferForceField

        :param vertexInfo: Data to handle topology on vertices
        :param tetrahedronInfo: Data to handle topology on tetrahedra
        :param inwardTime: inwardTime constant
        :param vertexInwardTime: Vector containing values of tau_in at each vertex
        :param outwardTime: outwardTime constant
        :param vertexOutwardTime: Vector containing values of tau_out at each vertex
        :param openingTime: openingTime constant
        :param vertexOpeningTime: Vector containing values of tau_open at each vertex
        :param closingTime: closingTime constant
        :param vertexClosingTime: Vector containing values of tau_close at each vertex
        :param tauCloseFactor: Factor modifying globally the tauClose value
        :param uGate: uGate
        :param vertexUGate: Vector containing values of u_gate at each vertex
        :param amplitudeAP: Value of action potential (AP) amplitude. Default: 1.0
        :param vertexAmplitudeAP: Value of action potential (AP) amplitude at each vertex (A lower value can be used to simulate GZ/scar)
        :param repolFactor: repolFactor (should be = 1)
        :param tagMechanics: Tag of the Mechanical Object
        :param amplitudeSinus: Value of the amplitude of the sinus node
        :param startTime: Time at which the constraint starts to be applied
        :param endTime: Time at which the constraint ends to be applied (inf=-1)
        :param stimuliDuration: Time during which the constraint is applied
        :param stimuliPeriod: Time elapsed between two stimuli
        :param indicesSinus: Points used for the stimulation using Jstim
        :param stimulus: Vector of the stimulation using Jstim
        :param bidomain: Boolean option for computing bidomain Mitchell Schaeffer (ONLY CPU).
        :param implicitComputation: Boolean option for computing the addDForce in case of implicit computation
        :param forceNoStimulus: Boolean preventing from taking into account any stimulus
        """
        params = dict(
            vertexInfo=vertexInfo,
            tetrahedronInfo=tetrahedronInfo,
            inwardTime=inwardTime,
            vertexInwardTime=vertexInwardTime,
            outwardTime=outwardTime,
            vertexOutwardTime=vertexOutwardTime,
            openingTime=openingTime,
            vertexOpeningTime=vertexOpeningTime,
            closingTime=closingTime,
            vertexClosingTime=vertexClosingTime,
            tauCloseFactor=tauCloseFactor,
            uGate=uGate,
            vertexUGate=vertexUGate,
            amplitudeAP=amplitudeAP,
            vertexAmplitudeAP=vertexAmplitudeAP,
            repolFactor=repolFactor,
            tagMechanics=tagMechanics,
            amplitudeSinus=amplitudeSinus,
            startTime=startTime,
            endTime=endTime,
            stimuliDuration=stimuliDuration,
            stimuliPeriod=stimuliPeriod,
            indicesSinus=indicesSinus,
            stimulus=stimulus,
            bidomain=bidomain,
            implicitComputation=implicitComputation,
            forceNoStimulus=forceNoStimulus,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralMitchellSchaefferForceField", params

    @sofa_component
    def TetrahedralMitchellSchaefferIonicField(
        self,
        inwardTime=None,
        outwardTime=None,
        openingTime=None,
        closingTime=None,
        uGate=None,
        repolFactor=None,
        **kwargs
    ):
        """
        TetrahedralMitchellSchaefferIonicField

        :param inwardTime: inwardTime constant
        :param outwardTime: outwardTime constant
        :param openingTime: openingTime constant
        :param closingTime: closingTime constant
        :param uGate: uGate
        :param repolFactor: repolFactor (should be = 1)
        """
        params = dict(
            inwardTime=inwardTime,
            outwardTime=outwardTime,
            openingTime=openingTime,
            closingTime=closingTime,
            uGate=uGate,
            repolFactor=repolFactor,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralMitchellSchaefferIonicField", params

    @sofa_component
    def TetrahedralMitchellSchaefferCellMLCurrentField(
        self,
        J_in_tau_in=None,
        J_in_h_gate_tau_open=None,
        J_in_h_gate_tau_close=None,
        J_in_h_gate_V_gate=None,
        J_out_tau_out=None,
        **kwargs
    ):
        """
        TetrahedralMitchellSchaefferCellMLCurrentField

        :param J_in_tau_in: J_in_tau_in
        :param J_in_h_gate_tau_open: J_in_h_gate_tau_open
        :param J_in_h_gate_tau_close: J_in_h_gate_tau_close
        :param J_in_h_gate_V_gate: J_in_h_gate_V_gate
        :param J_out_tau_out: J_out_tau_out
        """
        params = dict(
            J_in_tau_in=J_in_tau_in,
            J_in_h_gate_tau_open=J_in_h_gate_tau_open,
            J_in_h_gate_tau_close=J_in_h_gate_tau_close,
            J_in_h_gate_V_gate=J_in_h_gate_V_gate,
            J_out_tau_out=J_out_tau_out,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralMitchellSchaefferCellMLCurrentField", params

    @sofa_component
    def TetrahedralFitzhughNagumoCellMLCurrentField(
        self, Main_alpha=None, Main_gamma=None, Main_epsilon=None, **kwargs
    ):
        """
        TetrahedralFitzhughNagumoCellMLCurrentField

        :param Main_alpha: Main_alpha
        :param Main_gamma: Main_gamma
        :param Main_epsilon: Main_epsilon
        """
        params = dict(
            Main_alpha=Main_alpha, Main_gamma=Main_gamma, Main_epsilon=Main_epsilon
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralFitzhughNagumoCellMLCurrentField", params

    @sofa_component
    def TetrahedralNobleCellMLCurrentField(
        self,
        membrane_Cm=None,
        sodium_channel_g_Na_max=None,
        sodium_channel_E_Na=None,
        leakage_current_g_L=None,
        leakage_current_E_L=None,
        **kwargs
    ):
        """
        TetrahedralNobleCellMLCurrentField

        :param membrane_Cm: membrane_Cm
        :param sodium_channel_g_Na_max: sodium_channel_g_Na_max
        :param sodium_channel_E_Na: sodium_channel_E_Na
        :param leakage_current_g_L: leakage_current_g_L
        :param leakage_current_E_L: leakage_current_E_L
        """
        params = dict(
            membrane_Cm=membrane_Cm,
            sodium_channel_g_Na_max=sodium_channel_g_Na_max,
            sodium_channel_E_Na=sodium_channel_E_Na,
            leakage_current_g_L=leakage_current_g_L,
            leakage_current_E_L=leakage_current_E_L,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralNobleCellMLCurrentField", params

    @sofa_component
    def TetrahedralHodgkinHuxleyCellMLCurrentField(
        self,
        membrane_E_R=None,
        membrane_Cm=None,
        sodium_channel_g_Na=None,
        potassium_channel_g_K=None,
        leakage_current_g_L=None,
        sodium_channel_E_Na=None,
        potassium_channel_E_K=None,
        leakage_current_E_L=None,
        **kwargs
    ):
        """
        TetrahedralHodgkinHuxleyCellMLCurrentField

        :param membrane_E_R: membrane_E_R
        :param membrane_Cm: membrane_Cm
        :param sodium_channel_g_Na: sodium_channel_g_Na
        :param potassium_channel_g_K: potassium_channel_g_K
        :param leakage_current_g_L: leakage_current_g_L
        :param sodium_channel_E_Na: sodium_channel_E_Na
        :param potassium_channel_E_K: potassium_channel_E_K
        :param leakage_current_E_L: leakage_current_E_L
        """
        params = dict(
            membrane_E_R=membrane_E_R,
            membrane_Cm=membrane_Cm,
            sodium_channel_g_Na=sodium_channel_g_Na,
            potassium_channel_g_K=potassium_channel_g_K,
            leakage_current_g_L=leakage_current_g_L,
            sodium_channel_E_Na=sodium_channel_E_Na,
            potassium_channel_E_K=potassium_channel_E_K,
            leakage_current_E_L=leakage_current_E_L,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralHodgkinHuxleyCellMLCurrentField", params

    @sofa_component
    def TetrahedralFentonKarmaBRCellMLCurrentField(
        self,
        membrane_Cm=None,
        membrane_V_0=None,
        membrane_V_fi=None,
        p_u_c=None,
        q_u_v=None,
        fast_inward_current_g_fi_max=None,
        fast_inward_current_v_gate_tau_v1_minus=None,
        fast_inward_current_v_gate_tau_v2_minus=None,
        fast_inward_current_v_gate_tau_v_plus=None,
        slow_outward_current_tau_0=None,
        slow_outward_current_tau_r=None,
        slow_inward_current_tau_si=None,
        slow_inward_current_u_csi=None,
        slow_inward_current_k=None,
        slow_inward_current_w_gate_tau_w_minus=None,
        slow_inward_current_w_gate_tau_w_plus=None,
        fast_inward_current_tau_d=None,
        **kwargs
    ):
        """
        TetrahedralFentonKarmaBRCellMLCurrentField

        :param membrane_Cm: membrane_Cm
        :param membrane_V_0: membrane_V_0
        :param membrane_V_fi: membrane_V_fi
        :param p_u_c: p_u_c
        :param q_u_v: q_u_v
        :param fast_inward_current_g_fi_max: fast_inward_current_g_fi_max
        :param fast_inward_current_v_gate_tau_v1_minus: fast_inward_current_v_gate_tau_v1_minus
        :param fast_inward_current_v_gate_tau_v2_minus: fast_inward_current_v_gate_tau_v2_minus
        :param fast_inward_current_v_gate_tau_v_plus: fast_inward_current_v_gate_tau_v_plus
        :param slow_outward_current_tau_0: slow_outward_current_tau_0
        :param slow_outward_current_tau_r: slow_outward_current_tau_r
        :param slow_inward_current_tau_si: slow_inward_current_tau_si
        :param slow_inward_current_u_csi: slow_inward_current_u_csi
        :param slow_inward_current_k: slow_inward_current_k
        :param slow_inward_current_w_gate_tau_w_minus: slow_inward_current_w_gate_tau_w_minus
        :param slow_inward_current_w_gate_tau_w_plus: slow_inward_current_w_gate_tau_w_plus
        :param fast_inward_current_tau_d: fast_inward_current_tau_d
        """
        params = dict(
            membrane_Cm=membrane_Cm,
            membrane_V_0=membrane_V_0,
            membrane_V_fi=membrane_V_fi,
            p_u_c=p_u_c,
            q_u_v=q_u_v,
            fast_inward_current_g_fi_max=fast_inward_current_g_fi_max,
            fast_inward_current_v_gate_tau_v1_minus=fast_inward_current_v_gate_tau_v1_minus,
            fast_inward_current_v_gate_tau_v2_minus=fast_inward_current_v_gate_tau_v2_minus,
            fast_inward_current_v_gate_tau_v_plus=fast_inward_current_v_gate_tau_v_plus,
            slow_outward_current_tau_0=slow_outward_current_tau_0,
            slow_outward_current_tau_r=slow_outward_current_tau_r,
            slow_inward_current_tau_si=slow_inward_current_tau_si,
            slow_inward_current_u_csi=slow_inward_current_u_csi,
            slow_inward_current_k=slow_inward_current_k,
            slow_inward_current_w_gate_tau_w_minus=slow_inward_current_w_gate_tau_w_minus,
            slow_inward_current_w_gate_tau_w_plus=slow_inward_current_w_gate_tau_w_plus,
            fast_inward_current_tau_d=fast_inward_current_tau_d,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralFentonKarmaBRCellMLCurrentField", params

    @sofa_component
    def TetrahedralFentonKarmaGPCellMLCurrentField(
        self,
        membrane_Cm=None,
        membrane_V_0=None,
        membrane_V_fi=None,
        p_u_c=None,
        q_u_v=None,
        fast_inward_current_g_fi_max=None,
        fast_inward_current_v_gate_tau_v1_minus=None,
        fast_inward_current_v_gate_tau_v2_minus=None,
        fast_inward_current_v_gate_tau_v_plus=None,
        slow_outward_current_tau_0=None,
        slow_outward_current_tau_r=None,
        slow_inward_current_tau_si=None,
        slow_inward_current_u_csi=None,
        slow_inward_current_k=None,
        slow_inward_current_w_gate_tau_w_minus=None,
        slow_inward_current_w_gate_tau_w_plus=None,
        fast_inward_current_tau_d=None,
        **kwargs
    ):
        """
        TetrahedralFentonKarmaGPCellMLCurrentField

        :param membrane_Cm: membrane_Cm
        :param membrane_V_0: membrane_V_0
        :param membrane_V_fi: membrane_V_fi
        :param p_u_c: p_u_c
        :param q_u_v: q_u_v
        :param fast_inward_current_g_fi_max: fast_inward_current_g_fi_max
        :param fast_inward_current_v_gate_tau_v1_minus: fast_inward_current_v_gate_tau_v1_minus
        :param fast_inward_current_v_gate_tau_v2_minus: fast_inward_current_v_gate_tau_v2_minus
        :param fast_inward_current_v_gate_tau_v_plus: fast_inward_current_v_gate_tau_v_plus
        :param slow_outward_current_tau_0: slow_outward_current_tau_0
        :param slow_outward_current_tau_r: slow_outward_current_tau_r
        :param slow_inward_current_tau_si: slow_inward_current_tau_si
        :param slow_inward_current_u_csi: slow_inward_current_u_csi
        :param slow_inward_current_k: slow_inward_current_k
        :param slow_inward_current_w_gate_tau_w_minus: slow_inward_current_w_gate_tau_w_minus
        :param slow_inward_current_w_gate_tau_w_plus: slow_inward_current_w_gate_tau_w_plus
        :param fast_inward_current_tau_d: fast_inward_current_tau_d
        """
        params = dict(
            membrane_Cm=membrane_Cm,
            membrane_V_0=membrane_V_0,
            membrane_V_fi=membrane_V_fi,
            p_u_c=p_u_c,
            q_u_v=q_u_v,
            fast_inward_current_g_fi_max=fast_inward_current_g_fi_max,
            fast_inward_current_v_gate_tau_v1_minus=fast_inward_current_v_gate_tau_v1_minus,
            fast_inward_current_v_gate_tau_v2_minus=fast_inward_current_v_gate_tau_v2_minus,
            fast_inward_current_v_gate_tau_v_plus=fast_inward_current_v_gate_tau_v_plus,
            slow_outward_current_tau_0=slow_outward_current_tau_0,
            slow_outward_current_tau_r=slow_outward_current_tau_r,
            slow_inward_current_tau_si=slow_inward_current_tau_si,
            slow_inward_current_u_csi=slow_inward_current_u_csi,
            slow_inward_current_k=slow_inward_current_k,
            slow_inward_current_w_gate_tau_w_minus=slow_inward_current_w_gate_tau_w_minus,
            slow_inward_current_w_gate_tau_w_plus=slow_inward_current_w_gate_tau_w_plus,
            fast_inward_current_tau_d=fast_inward_current_tau_d,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralFentonKarmaGPCellMLCurrentField", params

    @sofa_component
    def TetrahedralFentonKarmaMBRCellMLCurrentField(
        self,
        membrane_Cm=None,
        membrane_V_0=None,
        membrane_V_fi=None,
        p_u_c=None,
        q_u_v=None,
        fast_inward_current_g_fi_max=None,
        fast_inward_current_v_gate_tau_v1_minus=None,
        fast_inward_current_v_gate_tau_v2_minus=None,
        fast_inward_current_v_gate_tau_v_plus=None,
        slow_outward_current_tau_0=None,
        slow_outward_current_tau_r=None,
        slow_inward_current_tau_si=None,
        slow_inward_current_u_csi=None,
        slow_inward_current_k=None,
        slow_inward_current_w_gate_tau_w_minus=None,
        slow_inward_current_w_gate_tau_w_plus=None,
        fast_inward_current_tau_d=None,
        **kwargs
    ):
        """
        TetrahedralFentonKarmaMBRCellMLCurrentField

        :param membrane_Cm: membrane_Cm
        :param membrane_V_0: membrane_V_0
        :param membrane_V_fi: membrane_V_fi
        :param p_u_c: p_u_c
        :param q_u_v: q_u_v
        :param fast_inward_current_g_fi_max: fast_inward_current_g_fi_max
        :param fast_inward_current_v_gate_tau_v1_minus: fast_inward_current_v_gate_tau_v1_minus
        :param fast_inward_current_v_gate_tau_v2_minus: fast_inward_current_v_gate_tau_v2_minus
        :param fast_inward_current_v_gate_tau_v_plus: fast_inward_current_v_gate_tau_v_plus
        :param slow_outward_current_tau_0: slow_outward_current_tau_0
        :param slow_outward_current_tau_r: slow_outward_current_tau_r
        :param slow_inward_current_tau_si: slow_inward_current_tau_si
        :param slow_inward_current_u_csi: slow_inward_current_u_csi
        :param slow_inward_current_k: slow_inward_current_k
        :param slow_inward_current_w_gate_tau_w_minus: slow_inward_current_w_gate_tau_w_minus
        :param slow_inward_current_w_gate_tau_w_plus: slow_inward_current_w_gate_tau_w_plus
        :param fast_inward_current_tau_d: fast_inward_current_tau_d
        """
        params = dict(
            membrane_Cm=membrane_Cm,
            membrane_V_0=membrane_V_0,
            membrane_V_fi=membrane_V_fi,
            p_u_c=p_u_c,
            q_u_v=q_u_v,
            fast_inward_current_g_fi_max=fast_inward_current_g_fi_max,
            fast_inward_current_v_gate_tau_v1_minus=fast_inward_current_v_gate_tau_v1_minus,
            fast_inward_current_v_gate_tau_v2_minus=fast_inward_current_v_gate_tau_v2_minus,
            fast_inward_current_v_gate_tau_v_plus=fast_inward_current_v_gate_tau_v_plus,
            slow_outward_current_tau_0=slow_outward_current_tau_0,
            slow_outward_current_tau_r=slow_outward_current_tau_r,
            slow_inward_current_tau_si=slow_inward_current_tau_si,
            slow_inward_current_u_csi=slow_inward_current_u_csi,
            slow_inward_current_k=slow_inward_current_k,
            slow_inward_current_w_gate_tau_w_minus=slow_inward_current_w_gate_tau_w_minus,
            slow_inward_current_w_gate_tau_w_plus=slow_inward_current_w_gate_tau_w_plus,
            fast_inward_current_tau_d=fast_inward_current_tau_d,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralFentonKarmaMBRCellMLCurrentField", params

    @sofa_component
    def TetrahedralFentonKarmaMLR1CellMLCurrentField(
        self,
        membrane_Cm=None,
        membrane_V_0=None,
        membrane_V_fi=None,
        p_u_c=None,
        q_u_v=None,
        fast_inward_current_g_fi_max=None,
        fast_inward_current_v_gate_tau_v1_minus=None,
        fast_inward_current_v_gate_tau_v2_minus=None,
        fast_inward_current_v_gate_tau_v_plus=None,
        slow_outward_current_tau_0=None,
        slow_outward_current_tau_r=None,
        slow_inward_current_tau_si=None,
        slow_inward_current_u_csi=None,
        slow_inward_current_k=None,
        slow_inward_current_w_gate_tau_w_minus=None,
        slow_inward_current_w_gate_tau_w_plus=None,
        fast_inward_current_tau_d=None,
        **kwargs
    ):
        """
        TetrahedralFentonKarmaMLR1CellMLCurrentField

        :param membrane_Cm: membrane_Cm
        :param membrane_V_0: membrane_V_0
        :param membrane_V_fi: membrane_V_fi
        :param p_u_c: p_u_c
        :param q_u_v: q_u_v
        :param fast_inward_current_g_fi_max: fast_inward_current_g_fi_max
        :param fast_inward_current_v_gate_tau_v1_minus: fast_inward_current_v_gate_tau_v1_minus
        :param fast_inward_current_v_gate_tau_v2_minus: fast_inward_current_v_gate_tau_v2_minus
        :param fast_inward_current_v_gate_tau_v_plus: fast_inward_current_v_gate_tau_v_plus
        :param slow_outward_current_tau_0: slow_outward_current_tau_0
        :param slow_outward_current_tau_r: slow_outward_current_tau_r
        :param slow_inward_current_tau_si: slow_inward_current_tau_si
        :param slow_inward_current_u_csi: slow_inward_current_u_csi
        :param slow_inward_current_k: slow_inward_current_k
        :param slow_inward_current_w_gate_tau_w_minus: slow_inward_current_w_gate_tau_w_minus
        :param slow_inward_current_w_gate_tau_w_plus: slow_inward_current_w_gate_tau_w_plus
        :param fast_inward_current_tau_d: fast_inward_current_tau_d
        """
        params = dict(
            membrane_Cm=membrane_Cm,
            membrane_V_0=membrane_V_0,
            membrane_V_fi=membrane_V_fi,
            p_u_c=p_u_c,
            q_u_v=q_u_v,
            fast_inward_current_g_fi_max=fast_inward_current_g_fi_max,
            fast_inward_current_v_gate_tau_v1_minus=fast_inward_current_v_gate_tau_v1_minus,
            fast_inward_current_v_gate_tau_v2_minus=fast_inward_current_v_gate_tau_v2_minus,
            fast_inward_current_v_gate_tau_v_plus=fast_inward_current_v_gate_tau_v_plus,
            slow_outward_current_tau_0=slow_outward_current_tau_0,
            slow_outward_current_tau_r=slow_outward_current_tau_r,
            slow_inward_current_tau_si=slow_inward_current_tau_si,
            slow_inward_current_u_csi=slow_inward_current_u_csi,
            slow_inward_current_k=slow_inward_current_k,
            slow_inward_current_w_gate_tau_w_minus=slow_inward_current_w_gate_tau_w_minus,
            slow_inward_current_w_gate_tau_w_plus=slow_inward_current_w_gate_tau_w_plus,
            fast_inward_current_tau_d=fast_inward_current_tau_d,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralFentonKarmaMLR1CellMLCurrentField", params

    @sofa_component
    def GenericTetrahedralIonicCurrentField(
        self,
        vertexInfo=None,
        tagMechanics=None,
        amplitudeSinus=None,
        startTime=None,
        endTime=None,
        stimuliDuration=None,
        stimuliPeriod=None,
        indicesSinus=None,
        stimulus=None,
        **kwargs
    ):
        """
        GenericTetrahedralIonicCurrentField

        :param vertexInfo: Data to handle topology on vertices
        :param tagMechanics: Tag of the Mechanical Object
        :param amplitudeSinus: Value of the amplitude of the sinus node
        :param startTime: Time at which the constraint starts to be applied
        :param endTime: Time at which the constraint ends to be applied (inf=-1)
        :param stimuliDuration: Time during which the constraint is applied
        :param stimuliPeriod: Time elapsed between two stimuli
        :param indicesSinus: Points used for the stimulation using Jstim
        :param stimulus: Vector of the stimulation using Jstim
        """
        params = dict(
            vertexInfo=vertexInfo,
            tagMechanics=tagMechanics,
            amplitudeSinus=amplitudeSinus,
            startTime=startTime,
            endTime=endTime,
            stimuliDuration=stimuliDuration,
            stimuliPeriod=stimuliPeriod,
            indicesSinus=indicesSinus,
            stimulus=stimulus,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "GenericTetrahedralIonicCurrentField", params

    @sofa_component
    def TetrahedralPanfilovForceField(
        self,
        vertexInfo=None,
        tetrahedronInfo=None,
        repolFactor=None,
        polyFactor=None,
        polyRoot=None,
        lumpMassMatrix=None,
        tagMechanics=None,
        integrationOrder=None,
        **kwargs
    ):
        """
        TetrahedralPanfilovForceField

        :param vertexInfo: Data to handle topology on vertices
        :param tetrahedronInfo: Data to handle topology on tetrahedra
        :param repolFactor: repolarization_factor
        :param polyFactor: polyFactor Coefficient
        :param polyRoot: polyRoot Coefficient
        :param lumpMassMatrix: whether the mass matrix should be lumped (true) or not (false)
        :param tagMechanics: Tag of the Mechanical Object
        :param integrationOrder: Order of the integration of the reaction part
        """
        params = dict(
            vertexInfo=vertexInfo,
            tetrahedronInfo=tetrahedronInfo,
            repolFactor=repolFactor,
            polyFactor=polyFactor,
            polyRoot=polyRoot,
            lumpMassMatrix=lumpMassMatrix,
            tagMechanics=tagMechanics,
            integrationOrder=integrationOrder,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralPanfilovForceField", params

    @sofa_component
    def TetrahedralReactionForceField(
        self,
        vertexInfo=None,
        reactivity=None,
        tagMechanics=None,
        tagMass=None,
        integrationMethod=None,
        integrationOrder=None,
        integrationScheme=None,
        correction=None,
        volumeTetra=None,
        **kwargs
    ):
        """
        TetrahedralReactionForceField

        :param vertexInfo: Data to handle topology on vertices
        :param reactivity: Reaction Coefficient
        :param tagMechanics: Tag of the Mechanical Object
        :param tagMass: Tag of the Mass
        :param integrationMethod: Determine the integration method used:\n 'lumping', 'ICI', 'SVI'
        :param integrationOrder: Order of the integration of the reaction
        :param integrationScheme: integer if 0 = explicit, \nif 1 = fully implicit
        :param correction: Boolean to des-/activate the potential correction
        :param volumeTetra: Data to handle topology on tetrahedra
        """
        params = dict(
            vertexInfo=vertexInfo,
            reactivity=reactivity,
            tagMechanics=tagMechanics,
            tagMass=tagMass,
            integrationMethod=integrationMethod,
            integrationOrder=integrationOrder,
            integrationScheme=integrationScheme,
            correction=correction,
            volumeTetra=volumeTetra,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralReactionForceField", params

    @sofa_component
    def TriangularDiffusionForceField(
        self,
        edgeInfo=None,
        diffusivity=None,
        tagMechanics=None,
        drawPotentiels=None,
        scalarDiffusion=None,
        **kwargs
    ):
        """
        TriangularDiffusionForceField

        :param edgeInfo: Data to handle topology on edges
        :param diffusivity: Diffusion Coefficient
        :param tagMechanics: Tag of the Mechanical Object
        :param drawPotentiels: if true, draw the potentiels in the mesh
        :param scalarDiffusion: if true, diffuse only on the first dimension.
        """
        params = dict(
            edgeInfo=edgeInfo,
            diffusivity=diffusivity,
            tagMechanics=tagMechanics,
            drawPotentiels=drawPotentiels,
            scalarDiffusion=scalarDiffusion,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangularDiffusionForceField", params

    @sofa_component
    def TriangularReactionForceField(
        self,
        vertexInfo=None,
        edgeInfo=None,
        reactivity=None,
        lumpMassMatrix=None,
        tagMechanics=None,
        drawPotentiels=None,
        **kwargs
    ):
        """
        TriangularReactionForceField

        :param vertexInfo: Data to handle topology on vertices
        :param edgeInfo: Data to handle topology on edges
        :param reactivity: Reaction Coefficient
        :param lumpMassMatrix: whether the mass matrix should be lumped (false) or not (true)
        :param tagMechanics: Tag of the Mechanical Object
        :param drawPotentiels: if true, draw the potentiels in the mesh
        """
        params = dict(
            vertexInfo=vertexInfo,
            edgeInfo=edgeInfo,
            reactivity=reactivity,
            lumpMassMatrix=lumpMassMatrix,
            tagMechanics=tagMechanics,
            drawPotentiels=drawPotentiels,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangularReactionForceField", params

    @sofa_component
    def VolumetricDiffusionForceField(
        self, nodeInfo=None, tetInfo=None, timeStep=None, tagMechanics=None, **kwargs
    ):
        """
        VolumetricDiffusionForceField

        :param nodeInfo: Data to handle topology on tetrahedra about nodes
        :param tetInfo: Data to handle topology on tetrahedra about tetra
        :param timeStep: time step
        :param tagMechanics: Tag of the Mechanical Object
        """
        params = dict(
            nodeInfo=nodeInfo,
            tetInfo=tetInfo,
            timeStep=timeStep,
            tagMechanics=tagMechanics,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "VolumetricDiffusionForceField", params

    @sofa_component
    def ElectrophysiologyInteractionEngine(
        self,
        indicesAblation=None,
        totalAblationTime=None,
        applyAblation=None,
        indicesStimulation=None,
        stimulusCurrent=None,
        applyStimulation=None,
        maxStimulus=None,
        startTime=None,
        endTime=None,
        stimuliDuration=None,
        stimuliPeriod=None,
        endMeasurementTime=None,
        computeQuality=None,
        **kwargs
    ):
        """
        ElectrophysiologyInteractionEngine

        :param indicesAblation: Indices of the points defining \n the region of ablation
        :param totalAblationTime: Time to complete local ablation (s)
        :param applyAblation: Boolean activating the ablation
        :param indicesStimulation: Indices of the points where \n a stimulation can be applied (i button)
        :param stimulusCurrent: Value of the current J_stim \n that can be applied (i button)
        :param applyStimulation: Boolean activating the stimulation
        :param maxStimulus: Maximum value wanted for the potential\n due to stimulus (if 0, no limit)
        :param startTime: Time at which the constraint starts to be applied
        :param endTime: Time at which the constraint ends to be applied (inf=-1)
        :param stimuliDuration: Time during which the constraint is applied
        :param stimuliPeriod: Time elapsed between two stimuli
        :param endMeasurementTime: Time at which the performance are computed (s)
        :param computeQuality: Compute the shortest and longest edges
        """
        params = dict(
            indicesAblation=indicesAblation,
            totalAblationTime=totalAblationTime,
            applyAblation=applyAblation,
            indicesStimulation=indicesStimulation,
            stimulusCurrent=stimulusCurrent,
            applyStimulation=applyStimulation,
            maxStimulus=maxStimulus,
            startTime=startTime,
            endTime=endTime,
            stimuliDuration=stimuliDuration,
            stimuliPeriod=stimuliPeriod,
            endMeasurementTime=endMeasurementTime,
            computeQuality=computeQuality,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ElectrophysiologyInteractionEngine", params

    @sofa_component
    def ElectrophysiologySignalEngine(
        self,
        idNodalMeasurement=None,
        indicesMeasurements=None,
        gradient=None,
        useGradientOption=None,
        outputPotential=None,
        nbOutput=None,
        filename=None,
        measureEveryNbSteps=None,
        computeActivationTime=None,
        buttonActivationTime=None,
        isReference=None,
        referenceActivationTime=None,
        activationTimes=None,
        polarizationState=None,
        **kwargs
    ):
        """
        ElectrophysiologySignalEngine

        :param idNodalMeasurement: Indice of the point used for /n transmembrane potential measurement
        :param indicesMeasurements: Indices of the points where \n the extraC potential is computed
        :param gradient: Gradient of shape function
        :param useGradientOption: Option to compute simplified potential \n if no gradient information
        :param outputPotential: Potential computed
        :param nbOutput: Number of output
        :param filename: Name of the exported CSV file
        :param measureEveryNbSteps: Measure only at specified number of steps (0=disable)
        :param computeActivationTime: boolean activating the computation of activation times
        :param buttonActivationTime: Boolean for external control
        :param isReference: If the component must just compute a reference time (activation of the [0] component)
        :param referenceActivationTime: Value of the reference activation time
        :param activationTimes: Vector containing all activation times
        :param polarizationState: Vector containing the state of polarization of each electrode
        """
        params = dict(
            idNodalMeasurement=idNodalMeasurement,
            indicesMeasurements=indicesMeasurements,
            gradient=gradient,
            useGradientOption=useGradientOption,
            outputPotential=outputPotential,
            nbOutput=nbOutput,
            filename=filename,
            measureEveryNbSteps=measureEveryNbSteps,
            computeActivationTime=computeActivationTime,
            buttonActivationTime=buttonActivationTime,
            isReference=isReference,
            referenceActivationTime=referenceActivationTime,
            activationTimes=activationTimes,
            polarizationState=polarizationState,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "ElectrophysiologySignalEngine", params

    @sofa_component
    def EctopicFocus(
        self,
        indicesStimulation=None,
        stimulusCurrent=None,
        stimulationPeriod=None,
        stimulationDuration=None,
        ectopicBeatPeriod=None,
        ectopicBeatPeriodDeviation=None,
        ectopicBeatDelay=None,
        isEctopicCycle=None,
        extrasystoleTime=None,
        **kwargs
    ):
        """
        EctopicFocus

        :param indicesStimulation: Indices of the points where \n the stimulation is applied
        :param stimulusCurrent: Value of the current J_stim is applied
        :param stimulationPeriod: Period of the stimulus
        :param stimulationDuration: Time during which the stimulation is delivered
        :param ectopicBeatPeriod: Number of periods between 2 ectopic beats in average
        :param ectopicBeatPeriodDeviation: Deviation of the number of periods between 2 ectopic beats in average
        :param ectopicBeatDelay: Delay of the ectopic beat between the initiation of the depolarization
        :param isEctopicCycle: Boolean indicating if this is an ectopic cycle
        :param extrasystoleTime: Starting time of the extrasystole
        """
        params = dict(
            indicesStimulation=indicesStimulation,
            stimulusCurrent=stimulusCurrent,
            stimulationPeriod=stimulationPeriod,
            stimulationDuration=stimulationDuration,
            ectopicBeatPeriod=ectopicBeatPeriod,
            ectopicBeatPeriodDeviation=ectopicBeatPeriodDeviation,
            ectopicBeatDelay=ectopicBeatDelay,
            isEctopicCycle=isEctopicCycle,
            extrasystoleTime=extrasystoleTime,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "EctopicFocus", params

    @sofa_component
    def PointFixedConstraint(self, indices=None, values=None, **kwargs):
        """
        PointFixedConstraint

        :param indices: Indices of the constrained nodes
        :param values: Values to be set
        """
        params = dict(indices=indices, values=values)
        params = {k: v for k, v in params.items() if v is not None}
        return "PointFixedConstraint", params

    @sofa_component
    def CatheterPotentialEngine(
        self,
        catheterPosition=None,
        measuredPotential=None,
        Filename=None,
        stepRecording=None,
        electrodeLocation=None,
        writeH=None,
        NbparamVerdandi=None,
        HmatrixOutfile=None,
        fileDipoleName=None,
        **kwargs
    ):
        """
        CatheterPotentialEngine

        :param catheterPosition: A 3d point where the potential will be measured
        :param measuredPotential: Output array of time varying potentials at catheterPosition
        :param Filename: Filename
        :param stepRecording: Time step for prinitng in the file. Default is the same as time step of the simulation
        :param electrodeLocation: string 'blood' or 'torso', where are located the electrodes. Changes the conductivity constant
        :param writeH: true to write the H matrix for Verdandi at the beginning of the cycle
        :param NbparamVerdandi: Number of parameters estimated by Verdandi (to write H matrix)
        :param HmatrixOutfile: String as output filename of the H matrix (.bin)
        :param fileDipoleName: Filename for the output as dipole ASCII file (for OpenMEEG)
        """
        params = dict(
            catheterPosition=catheterPosition,
            measuredPotential=measuredPotential,
            Filename=Filename,
            stepRecording=stepRecording,
            electrodeLocation=electrodeLocation,
            writeH=writeH,
            NbparamVerdandi=NbparamVerdandi,
            HmatrixOutfile=HmatrixOutfile,
            fileDipoleName=fileDipoleName,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "CatheterPotentialEngine", params

    @sofa_component
    def SelectorEngine(
        self,
        selectedPoints=None,
        selectedTriangles=None,
        selectTriangles=None,
        selectThrough=None,
        exportSelection=None,
        activateView=None,
        persistentSelection=None,
        **kwargs
    ):
        """
        SelectorEngine

        :param selectedPoints: Vector including all the selected points
        :param selectedTriangles: Vector including all the selected triangles
        :param selectTriangles: Boolean to select triangles in addition to the points
        :param selectThrough: Boolean to select structures through the volume
        :param exportSelection: Boolean to export the selection(s)
        :param activateView: Boolean to freeze the activated status in the camera during the selection occurs
        :param persistentSelection: Boolean to allow the selection in several steps
        """
        params = dict(
            selectedPoints=selectedPoints,
            selectedTriangles=selectedTriangles,
            selectTriangles=selectTriangles,
            selectThrough=selectThrough,
            exportSelection=exportSelection,
            activateView=activateView,
            persistentSelection=persistentSelection,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "SelectorEngine", params

    @sofa_component
    def BoyceArrudaMembraneForceField(
        self,
        triangleInfo=None,
        edgeInfo=None,
        initialPoints=None,
        bulkModulus=None,
        ShearModulus=None,
        dampingRatio=None,
        matrixRegularization=None,
        **kwargs
    ):
        """
        BoyceArrudaMembraneForceField

        :param triangleInfo: Data to handle topology on triangles
        :param edgeInfo: Data to handle topology on edges
        :param initialPoints: Initial Position
        :param bulkModulus: Bulk Modulus
        :param ShearModulus: Shear Modulus
        :param dampingRatio: Ratio damping/stiffness
        :param matrixRegularization: Regularization of the Stiffnes Matrix (between 0 and 1)
        """
        params = dict(
            triangleInfo=triangleInfo,
            edgeInfo=edgeInfo,
            initialPoints=initialPoints,
            bulkModulus=bulkModulus,
            ShearModulus=ShearModulus,
            dampingRatio=dampingRatio,
            matrixRegularization=matrixRegularization,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "BoyceArrudaMembraneForceField", params

    @sofa_component
    def LinearAnisotropicTetrahedralForceField(
        self,
        poissonRatio=None,
        youngModulus=None,
        youngModulusFibers=None,
        Anisotropy=None,
        edgeInfo=None,
        tetraBFibers=None,
        **kwargs
    ):
        """
        LinearAnisotropicTetrahedralForceField

        :param poissonRatio: Poisson ratio in Hooke's law
        :param youngModulus: Young modulus in Hooke's law
        :param youngModulusFibers: Young modulus in the fiber direction
        :param Anisotropy: True or false
        :param edgeInfo: Data to handle topology on edges
        :param tetraBFibers: Fibers direction for each tetrahedra
        """
        params = dict(
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            youngModulusFibers=youngModulusFibers,
            Anisotropy=Anisotropy,
            edgeInfo=edgeInfo,
            tetraBFibers=tetraBFibers,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "LinearAnisotropicTetrahedralForceField", params

    @sofa_component
    def NonlinearSpringForceField(self, spring=None, **kwargs):
        """
        NonlinearSpringForceField

        :param spring: pairs of indices, stiffness, damping, rest length, toe center
        """
        params = dict(spring=spring)
        params = {k: v for k, v in params.items() if v is not None}
        return "NonlinearSpringForceField", params

    @sofa_component
    def FastTetrahedralBiquadraticSpringsForceField(
        self,
        tetrahedronInfo=None,
        triangleInfo=None,
        edgeInfo=None,
        poissonRatio=None,
        youngModulus=None,
        useAngularSprings=None,
        useVolumetricSprings=None,
        compressible=None,
        optimizedStiffness=None,
        matrixRegularization=None,
        **kwargs
    ):
        """
        FastTetrahedralBiquadraticSpringsForceField

        :param tetrahedronInfo: Data to handle topology on tetrahedra
        :param triangleInfo: Data to handle topology on triangles
        :param edgeInfo: Data to handle topology on edges
        :param poissonRatio: Poisson ratio in Hooke's law
        :param youngModulus: Young modulus in Hooke's law
        :param useAngularSprings: If Angular Springs should be used or not
        :param useVolumetricSprings: If Volumetric Springs should be used or not
        :param compressible: If additional energy penalizing compressibility should be used
        :param optimizedStiffness: If the assembly of the stiffness matrix should be optimized
        :param matrixRegularization: Regularization of the Stiffnes Matrix (between 0 and 1)
        """
        params = dict(
            tetrahedronInfo=tetrahedronInfo,
            triangleInfo=triangleInfo,
            edgeInfo=edgeInfo,
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            useAngularSprings=useAngularSprings,
            useVolumetricSprings=useVolumetricSprings,
            compressible=compressible,
            optimizedStiffness=optimizedStiffness,
            matrixRegularization=matrixRegularization,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "FastTetrahedralBiquadraticSpringsForceField", params

    @sofa_component
    def FastTetrahedralQuadraticSpringsForceField(
        self,
        tetrahedronInfo=None,
        triangleInfo=None,
        edgeInfo=None,
        poissonRatio=None,
        youngModulus=None,
        useAngularSprings=None,
        useVolumetricSprings=None,
        compressible=None,
        matrixRegularization=None,
        **kwargs
    ):
        """
        FastTetrahedralQuadraticSpringsForceField

        :param tetrahedronInfo: Data to handle topology on tetrahedra
        :param triangleInfo: Data to handle topology on triangles
        :param edgeInfo: Data to handle topology on edges
        :param poissonRatio: Poisson ratio in Hooke's law
        :param youngModulus: Young modulus in Hooke's law
        :param useAngularSprings: If Angular Springs should be used or not
        :param useVolumetricSprings: If Volumetric Springs should be used or not
        :param compressible: If additional energy penalizing compressibility should be used
        :param matrixRegularization: Regularization of the Stiffnes Matrix (between 0 and 1)
        """
        params = dict(
            tetrahedronInfo=tetrahedronInfo,
            triangleInfo=triangleInfo,
            edgeInfo=edgeInfo,
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            useAngularSprings=useAngularSprings,
            useVolumetricSprings=useVolumetricSprings,
            compressible=compressible,
            matrixRegularization=matrixRegularization,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "FastTetrahedralQuadraticSpringsForceField", params

    @sofa_component
    def YetAnotherTetrahedralForceField(self, **kwargs):
        """
        YetAnotherTetrahedralForceField
        """
        params = dict()
        return "YetAnotherTetrahedralForceField", params

    @sofa_component
    def TetrahedralAnisotropicHyperelasticForceField(
        self, fiberDir=None, tetrahedronInfo=None, edgeInfo=None, **kwargs
    ):
        """
        TetrahedralAnisotropicHyperelasticForceField

        :param fiberDir: Direction of the fibers
        :param tetrahedronInfo: Data to handle topology on tetrahedra
        :param edgeInfo: Data to handle topology on edges
        """
        params = dict(
            fiberDir=fiberDir, tetrahedronInfo=tetrahedronInfo, edgeInfo=edgeInfo
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TetrahedralAnisotropicHyperelasticForceField", params

    @sofa_component
    def VolumetricLiverForceField(
        self,
        tagMechanics=None,
        ParameterSet=None,
        Regularisation=None,
        tetrahedronInfo=None,
        edgeInfo=None,
        **kwargs
    ):
        """
        VolumetricLiverForceField

        :param tagMechanics: Tag of the Mechanical Object
        :param ParameterSet: The global parameters specifying the material
        :param Regularisation: Regularisation of the stiffness matrix
        :param tetrahedronInfo: Data to handle topology on tetrahedra
        :param edgeInfo: Data to handle topology on edges
        """
        params = dict(
            tagMechanics=tagMechanics,
            ParameterSet=ParameterSet,
            Regularisation=Regularisation,
            tetrahedronInfo=tetrahedronInfo,
            edgeInfo=edgeInfo,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "VolumetricLiverForceField", params

    @sofa_component
    def TriangularStVenantKirchhoffForceField(
        self,
        triangleInfo=None,
        edgeInfo=None,
        initialPoints=None,
        poissonRatio=None,
        youngModulus=None,
        dampingRatio=None,
        useAngularSprings=None,
        useCompressionForce=None,
        Regularisation=None,
        **kwargs
    ):
        """
        TriangularStVenantKirchhoffForceField

        :param triangleInfo: Data to handle topology on triangles
        :param edgeInfo: Data to handle topology on edges
        :param initialPoints: Initial Position
        :param poissonRatio: Poisson ratio in Hooke's law
        :param youngModulus: Young modulus in Hooke's law
        :param dampingRatio: Ratio damping/stiffness
        :param useAngularSprings: If Angular Springs should be used or not
        :param useCompressionForce: Number to use for Compression Force
        :param Regularisation: Number to use for Regularisation, between 0 and 1
        """
        params = dict(
            triangleInfo=triangleInfo,
            edgeInfo=edgeInfo,
            initialPoints=initialPoints,
            poissonRatio=poissonRatio,
            youngModulus=youngModulus,
            dampingRatio=dampingRatio,
            useAngularSprings=useAngularSprings,
            useCompressionForce=useCompressionForce,
            Regularisation=Regularisation,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "TriangularStVenantKirchhoffForceField", params

    @sofa_component
    def InitPacingPoints(
        self,
        pace_mode=None,
        pace_zones=None,
        pace_points=None,
        endo=None,
        shiftContraction=None,
        **kwargs
    ):
        """
        InitPacingPoints

        :param pace_mode: ZONES or POINTS
        :param pace_zones: Volume zones to init
        :param pace_points: Points to init
        :param endo: Name of surface zones for endocardium
        :param shiftContraction: Difference (init) time to start pacing (s)
        """
        params = dict(
            pace_mode=pace_mode,
            pace_zones=pace_zones,
            pace_points=pace_points,
            endo=endo,
            shiftContraction=shiftContraction,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "InitPacingPoints", params

    @sofa_component
    def AComponent(self, data=None, **kwargs):
        """
        AComponent

        :param data: description of the data
        """
        params = dict(data=data)
        params = {k: v for k, v in params.items() if v is not None}
        return "AComponent", params

    @sofa_component
    def TestLinks(self, **kwargs):
        """
        TestLinks
        """
        params = dict()
        return "TestLinks", params

    @sofa_component
    def MeasureTwist(self, emptyData=None, **kwargs):
        """
        MeasureTwist

        :param emptyData: description of the data
        """
        params = dict(emptyData=emptyData)
        params = {k: v for k, v in params.items() if v is not None}
        return "MeasureTwist", params

    @sofa_component
    def APD_Wall(
        self,
        axis=None,
        point_top=None,
        barycenter=None,
        APD=None,
        factor=None,
        d_endo_epi=None,
        d_epi_endo=None,
        **kwargs
    ):
        """
        APD_Wall

        :param axis: director vector to heart long axis
        :param point_top: Point id to top septum or above ventricle (used for the plane)
        :param barycenter: Barycenter of the mesh or ventricle
        :param APD: APD value on endocardium
        :param factor: Factor of APD through the wall from endo to epi
        :param d_endo_epi: Distances computed from endo to epi
        :param d_epi_endo: Distances computed from epi to endo
        """
        params = dict(
            axis=axis,
            point_top=point_top,
            barycenter=barycenter,
            APD=APD,
            factor=factor,
            d_endo_epi=d_endo_epi,
            d_epi_endo=d_epi_endo,
        )
        params = {k: v for k, v in params.items() if v is not None}
        return "APD_Wall", params

    @sofa_component
    def ExportDepolAndAPD(self, filename=None, depolTimes=None, APD=None, **kwargs):
        """
        ExportDepolAndAPD

        :param filename:
        :param depolTimes:
        :param APD:
        """
        params = dict(filename=filename, depolTimes=depolTimes, APD=APD)
        params = {k: v for k, v in params.items() if v is not None}
        return "ExportDepolAndAPD", params
