# -*- coding: utf-8 -*-


"""
Module Engine

Content of the module
**********************

Summary:
========
.. autosummary::
     :toctree: _autosummary

    ExtrudeQuadsAndGenerateHexas

    ExtrudeSurface

    GenerateCylinder

    ProximityROI

    ScaleTransformMatrixEngine

    MergeMeshes

    MergeROIs

    GenerateSphere

    RigidToQuatEngine

    TransformPosition

    MeshClosingEngine

    DisplacementTransformEngine

    MeshSubsetEngine

    ComputeWeightEngine

    TextureInterpolation

    AverageCoord

    TopologyGaussPointSampler

    RandomPointDistributionInSurface

    NormalsFromPoints

    MeshBarycentricMapperEngine

    ComplementaryROI

    MergeSets

    ValuesFromIndices

    DilateEngine

    ValuesFromPositions

    ContractionInitialization

    SphereROI

    SumEngine

    MeshROI

    ExtrudeEdgesAndGenerateQuads

    Vertex2Frame

    TranslateTransformMatrixEngine

    ROIValueMapper

    IndicesFromValues

    GenerateGrid

    PairBoxROI

    TransformEngine

    DifferenceEngine

    ShapeMatching

    DisplacementMatrixEngine

    MeshSampler

    Indices2ValuesMapper

    MergeVectors

    QuatToRigidEngine

    GaussPointSmoother

    GenerateRigidMass

    MeshSplittingEngine

    MapIndices

    PlaneROI

    NormEngine

    SubsetTopology

    Spiral

    MathOp

    ProjectiveTransformEngine

    SelectConnectedLabelsROI

    MeshBoundaryROI

    ClusteringEngine

    PointsFromIndices

    IndexValueMapper

    ComputeDualQuatEngine

    HausdorffDistance

    BoxROI

    GaussPointContainer

    MergePoints

    NearestPointROI

    PythonScriptDataEngine

    RotateTransformMatrixEngine

    SelectLabelROI

    SmoothMeshEngine

    JoinPoints

    InvertTransformMatrixEngine

    GenerateCardiacCylinder

    GroupFilterYoungModulus



Content:
========

.. automodule::

    ExtrudeQuadsAndGenerateHexas

    ExtrudeSurface

    GenerateCylinder

    ProximityROI

    ScaleTransformMatrixEngine

    MergeMeshes

    MergeROIs

    GenerateSphere

    RigidToQuatEngine

    TransformPosition

    MeshClosingEngine

    DisplacementTransformEngine

    MeshSubsetEngine

    ComputeWeightEngine

    TextureInterpolation

    AverageCoord

    TopologyGaussPointSampler

    RandomPointDistributionInSurface

    NormalsFromPoints

    MeshBarycentricMapperEngine

    ComplementaryROI

    MergeSets

    ValuesFromIndices

    DilateEngine

    ValuesFromPositions

    ContractionInitialization

    SphereROI

    SumEngine

    MeshROI

    ExtrudeEdgesAndGenerateQuads

    Vertex2Frame

    TranslateTransformMatrixEngine

    ROIValueMapper

    IndicesFromValues

    GenerateGrid

    PairBoxROI

    TransformEngine

    DifferenceEngine

    ShapeMatching

    DisplacementMatrixEngine

    MeshSampler

    Indices2ValuesMapper

    MergeVectors

    QuatToRigidEngine

    GaussPointSmoother

    GenerateRigidMass

    MeshSplittingEngine

    MapIndices

    PlaneROI

    NormEngine

    SubsetTopology

    Spiral

    MathOp

    ProjectiveTransformEngine

    SelectConnectedLabelsROI

    MeshBoundaryROI

    ClusteringEngine

    PointsFromIndices

    IndexValueMapper

    ComputeDualQuatEngine

    HausdorffDistance

    BoxROI

    GaussPointContainer

    MergePoints

    NearestPointROI

    PythonScriptDataEngine

    RotateTransformMatrixEngine

    SelectLabelROI

    SmoothMeshEngine

    JoinPoints

    InvertTransformMatrixEngine

    GenerateCardiacCylinder

    GroupFilterYoungModulus



Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
# __all__=['ExtrudeQuadsAndGenerateHexas', 'ExtrudeSurface', 'GenerateCylinder', 'ProximityROI', 'ScaleTransformMatrixEngine', 'MergeMeshes', 'MergeROIs', 'GenerateSphere', 'RigidToQuatEngine', 'TransformPosition', 'MeshClosingEngine', 'DisplacementTransformEngine', 'MeshSubsetEngine', 'ComputeWeightEngine', 'TextureInterpolation', 'AverageCoord', 'TopologyGaussPointSampler', 'RandomPointDistributionInSurface', 'NormalsFromPoints', 'MeshBarycentricMapperEngine', 'ComplementaryROI', 'MergeSets', 'ValuesFromIndices', 'DilateEngine', 'ValuesFromPositions', 'ContractionInitialization', 'SphereROI', 'SumEngine', 'MeshROI', 'ExtrudeEdgesAndGenerateQuads', 'Vertex2Frame', 'TranslateTransformMatrixEngine', 'ROIValueMapper', 'IndicesFromValues', 'GenerateGrid', 'PairBoxROI', 'TransformEngine', 'DifferenceEngine', 'ShapeMatching', 'DisplacementMatrixEngine', 'MeshSampler', 'Indices2ValuesMapper', 'MergeVectors', 'QuatToRigidEngine', 'GaussPointSmoother', 'GenerateRigidMass', 'MeshSplittingEngine', 'MapIndices', 'PlaneROI', 'NormEngine', 'SubsetTopology', 'Spiral', 'MathOp', 'ProjectiveTransformEngine', 'SelectConnectedLabelsROI', 'MeshBoundaryROI', 'ClusteringEngine', 'PointsFromIndices', 'IndexValueMapper', 'ComputeDualQuatEngine', 'HausdorffDistance', 'BoxROI', 'GaussPointContainer', 'MergePoints', 'NearestPointROI', 'PythonScriptDataEngine', 'RotateTransformMatrixEngine', 'SelectLabelROI', 'SmoothMeshEngine', 'JoinPoints', 'InvertTransformMatrixEngine', 'GenerateCardiacCylinder', 'GroupFilterYoungModulus']
class Engine:
    from .ExtrudeQuadsAndGenerateHexas import ExtrudeQuadsAndGenerateHexas
    from .ExtrudeSurface import ExtrudeSurface
    from .GenerateCylinder import GenerateCylinder
    from .ProximityROI import ProximityROI
    from .ScaleTransformMatrixEngine import ScaleTransformMatrixEngine
    from .MergeMeshes import MergeMeshes
    from .MergeROIs import MergeROIs
    from .GenerateSphere import GenerateSphere
    from .RigidToQuatEngine import RigidToQuatEngine
    from .TransformPosition import TransformPosition
    from .MeshClosingEngine import MeshClosingEngine
    from .DisplacementTransformEngine import DisplacementTransformEngine
    from .MeshSubsetEngine import MeshSubsetEngine
    from .ComputeWeightEngine import ComputeWeightEngine
    from .TextureInterpolation import TextureInterpolation
    from .AverageCoord import AverageCoord
    from .TopologyGaussPointSampler import TopologyGaussPointSampler
    from .RandomPointDistributionInSurface import RandomPointDistributionInSurface
    from .NormalsFromPoints import NormalsFromPoints
    from .MeshBarycentricMapperEngine import MeshBarycentricMapperEngine
    from .ComplementaryROI import ComplementaryROI
    from .MergeSets import MergeSets
    from .ValuesFromIndices import ValuesFromIndices
    from .DilateEngine import DilateEngine
    from .ValuesFromPositions import ValuesFromPositions
    from .ContractionInitialization import ContractionInitialization
    from .SphereROI import SphereROI
    from .SumEngine import SumEngine
    from .MeshROI import MeshROI
    from .ExtrudeEdgesAndGenerateQuads import ExtrudeEdgesAndGenerateQuads
    from .Vertex2Frame import Vertex2Frame
    from .TranslateTransformMatrixEngine import TranslateTransformMatrixEngine
    from .ROIValueMapper import ROIValueMapper
    from .IndicesFromValues import IndicesFromValues
    from .GenerateGrid import GenerateGrid
    from .PairBoxROI import PairBoxROI
    from .TransformEngine import TransformEngine
    from .DifferenceEngine import DifferenceEngine
    from .ShapeMatching import ShapeMatching
    from .DisplacementMatrixEngine import DisplacementMatrixEngine
    from .MeshSampler import MeshSampler
    from .Indices2ValuesMapper import Indices2ValuesMapper
    from .MergeVectors import MergeVectors
    from .QuatToRigidEngine import QuatToRigidEngine
    from .GaussPointSmoother import GaussPointSmoother
    from .GenerateRigidMass import GenerateRigidMass
    from .MeshSplittingEngine import MeshSplittingEngine
    from .MapIndices import MapIndices
    from .PlaneROI import PlaneROI
    from .NormEngine import NormEngine
    from .SubsetTopology import SubsetTopology
    from .Spiral import Spiral
    from .MathOp import MathOp
    from .ProjectiveTransformEngine import ProjectiveTransformEngine
    from .SelectConnectedLabelsROI import SelectConnectedLabelsROI
    from .MeshBoundaryROI import MeshBoundaryROI
    from .ClusteringEngine import ClusteringEngine
    from .PointsFromIndices import PointsFromIndices
    from .IndexValueMapper import IndexValueMapper
    from .ComputeDualQuatEngine import ComputeDualQuatEngine
    from .HausdorffDistance import HausdorffDistance
    from .BoxROI import BoxROI
    from .GaussPointContainer import GaussPointContainer
    from .MergePoints import MergePoints
    from .NearestPointROI import NearestPointROI
    from .PythonScriptDataEngine import PythonScriptDataEngine
    from .RotateTransformMatrixEngine import RotateTransformMatrixEngine
    from .SelectLabelROI import SelectLabelROI
    from .SmoothMeshEngine import SmoothMeshEngine
    from .JoinPoints import JoinPoints
    from .InvertTransformMatrixEngine import InvertTransformMatrixEngine
    from .GenerateCardiacCylinder import GenerateCardiacCylinder
    from .GroupFilterYoungModulus import GroupFilterYoungModulus
