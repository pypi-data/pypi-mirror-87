# -*- coding: utf-8 -*-


"""
Module VisualModel

Content of the module
**********************

Summary:
========
.. autosummary::
     :toctree: _autosummary

    OglIntVector4Variable

    CompositingVisualLoop

    DirectionalLight

    PostProcessManager

    OglFloatVector2Variable

    OglMatrix2x4Variable

    OglIntVectorVariable

    OglFloat2Variable

    OglShadowShader

    OglMatrix2Variable

    OglFloatVectorVariable

    OglFloat4Attribute

    OglInt4Attribute

    OglSceneFrame

    OglTexture2D

    OrderIndependentTransparencyManager

    VisualModelImpl

    OglMatrix3x4Variable

    OglMatrix4x3Variable

    OglFloat4Variable

    OglInt4Variable

    VisualManagerSecondaryPass

    OglInt2Variable

    VisualTransform

    MergeVisualModels

    PointSplatModel

    OglFloat3Variable

    OglIntVector3Variable

    OglFloatVector3Variable

    OglInt3Attribute

    OglUIntAttribute

    OglShader

    OglUInt4Attribute

    ClipPlane

    OglIntAttribute

    OglTexture

    OglColorMap

    OglIntVariable

    OglGrid

    PositionalLight

    LightManager

    VisualManagerPass

    OglUInt3Attribute

    SpotLight

    OglOITShader

    OglTexturePointer

    OglMatrix4Variable

    OglInt2Attribute

    Visual3DText

    OglLineAxis

    OglLabel

    OglIntVector2Variable

    OglFloatAttribute

    OglFloatVariable

    OglFloatVector4Variable

    DataDisplay

    OglMatrix2x3Variable

    DefaultVisualManagerLoop

    OglInt3Variable

    SlicedVolumetricModel

    OglRenderingSRGB

    OglFloat2Attribute

    OglMatrix4VectorVariable

    OglFloat3Attribute

    OglCylinderModel

    VisualStyle

    OglUInt2Attribute

    OglShaderVisualModel

    OglViewport

    OglModel

    OglMatrix3x2Variable

    OglMatrix4x2Variable

    OglMatrix3Variable



Content:
========

.. automodule::

    OglIntVector4Variable

    CompositingVisualLoop

    DirectionalLight

    PostProcessManager

    OglFloatVector2Variable

    OglMatrix2x4Variable

    OglIntVectorVariable

    OglFloat2Variable

    OglShadowShader

    OglMatrix2Variable

    OglFloatVectorVariable

    OglFloat4Attribute

    OglInt4Attribute

    OglSceneFrame

    OglTexture2D

    OrderIndependentTransparencyManager

    VisualModelImpl

    OglMatrix3x4Variable

    OglMatrix4x3Variable

    OglFloat4Variable

    OglInt4Variable

    VisualManagerSecondaryPass

    OglInt2Variable

    VisualTransform

    MergeVisualModels

    PointSplatModel

    OglFloat3Variable

    OglIntVector3Variable

    OglFloatVector3Variable

    OglInt3Attribute

    OglUIntAttribute

    OglShader

    OglUInt4Attribute

    ClipPlane

    OglIntAttribute

    OglTexture

    OglColorMap

    OglIntVariable

    OglGrid

    PositionalLight

    LightManager

    VisualManagerPass

    OglUInt3Attribute

    SpotLight

    OglOITShader

    OglTexturePointer

    OglMatrix4Variable

    OglInt2Attribute

    Visual3DText

    OglLineAxis

    OglLabel

    OglIntVector2Variable

    OglFloatAttribute

    OglFloatVariable

    OglFloatVector4Variable

    DataDisplay

    OglMatrix2x3Variable

    DefaultVisualManagerLoop

    OglInt3Variable

    SlicedVolumetricModel

    OglRenderingSRGB

    OglFloat2Attribute

    OglMatrix4VectorVariable

    OglFloat3Attribute

    OglCylinderModel

    VisualStyle

    OglUInt2Attribute

    OglShaderVisualModel

    OglViewport

    OglModel

    OglMatrix3x2Variable

    OglMatrix4x2Variable

    OglMatrix3Variable



Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
# __all__=['OglIntVector4Variable', 'CompositingVisualLoop', 'DirectionalLight', 'PostProcessManager', 'OglFloatVector2Variable', 'OglMatrix2x4Variable', 'OglIntVectorVariable', 'OglFloat2Variable', 'OglShadowShader', 'OglMatrix2Variable', 'OglFloatVectorVariable', 'OglFloat4Attribute', 'OglInt4Attribute', 'OglSceneFrame', 'OglTexture2D', 'OrderIndependentTransparencyManager', 'VisualModelImpl', 'OglMatrix3x4Variable', 'OglMatrix4x3Variable', 'OglFloat4Variable', 'OglInt4Variable', 'VisualManagerSecondaryPass', 'OglInt2Variable', 'VisualTransform', 'MergeVisualModels', 'PointSplatModel', 'OglFloat3Variable', 'OglIntVector3Variable', 'OglFloatVector3Variable', 'OglInt3Attribute', 'OglUIntAttribute', 'OglShader', 'OglUInt4Attribute', 'ClipPlane', 'OglIntAttribute', 'OglTexture', 'OglColorMap', 'OglIntVariable', 'OglGrid', 'PositionalLight', 'LightManager', 'VisualManagerPass', 'OglUInt3Attribute', 'SpotLight', 'OglOITShader', 'OglTexturePointer', 'OglMatrix4Variable', 'OglInt2Attribute', 'Visual3DText', 'OglLineAxis', 'OglLabel', 'OglIntVector2Variable', 'OglFloatAttribute', 'OglFloatVariable', 'OglFloatVector4Variable', 'DataDisplay', 'OglMatrix2x3Variable', 'DefaultVisualManagerLoop', 'OglInt3Variable', 'SlicedVolumetricModel', 'OglRenderingSRGB', 'OglFloat2Attribute', 'OglMatrix4VectorVariable', 'OglFloat3Attribute', 'OglCylinderModel', 'VisualStyle', 'OglUInt2Attribute', 'OglShaderVisualModel', 'OglViewport', 'OglModel', 'OglMatrix3x2Variable', 'OglMatrix4x2Variable', 'OglMatrix3Variable']
class VisualModel:
    from .OglIntVector4Variable import OglIntVector4Variable
    from .CompositingVisualLoop import CompositingVisualLoop
    from .DirectionalLight import DirectionalLight
    from .PostProcessManager import PostProcessManager
    from .OglFloatVector2Variable import OglFloatVector2Variable
    from .OglMatrix2x4Variable import OglMatrix2x4Variable
    from .OglIntVectorVariable import OglIntVectorVariable
    from .OglFloat2Variable import OglFloat2Variable
    from .OglShadowShader import OglShadowShader
    from .OglMatrix2Variable import OglMatrix2Variable
    from .OglFloatVectorVariable import OglFloatVectorVariable
    from .OglFloat4Attribute import OglFloat4Attribute
    from .OglInt4Attribute import OglInt4Attribute
    from .OglSceneFrame import OglSceneFrame
    from .OglTexture2D import OglTexture2D
    from .OrderIndependentTransparencyManager import OrderIndependentTransparencyManager
    from .VisualModelImpl import VisualModelImpl
    from .OglMatrix3x4Variable import OglMatrix3x4Variable
    from .OglMatrix4x3Variable import OglMatrix4x3Variable
    from .OglFloat4Variable import OglFloat4Variable
    from .OglInt4Variable import OglInt4Variable
    from .VisualManagerSecondaryPass import VisualManagerSecondaryPass
    from .OglInt2Variable import OglInt2Variable
    from .VisualTransform import VisualTransform
    from .MergeVisualModels import MergeVisualModels
    from .PointSplatModel import PointSplatModel
    from .OglFloat3Variable import OglFloat3Variable
    from .OglIntVector3Variable import OglIntVector3Variable
    from .OglFloatVector3Variable import OglFloatVector3Variable
    from .OglInt3Attribute import OglInt3Attribute
    from .OglUIntAttribute import OglUIntAttribute
    from .OglShader import OglShader
    from .OglUInt4Attribute import OglUInt4Attribute
    from .ClipPlane import ClipPlane
    from .OglIntAttribute import OglIntAttribute
    from .OglTexture import OglTexture
    from .OglColorMap import OglColorMap
    from .OglIntVariable import OglIntVariable
    from .OglGrid import OglGrid
    from .PositionalLight import PositionalLight
    from .LightManager import LightManager
    from .VisualManagerPass import VisualManagerPass
    from .OglUInt3Attribute import OglUInt3Attribute
    from .SpotLight import SpotLight
    from .OglOITShader import OglOITShader
    from .OglTexturePointer import OglTexturePointer
    from .OglMatrix4Variable import OglMatrix4Variable
    from .OglInt2Attribute import OglInt2Attribute
    from .Visual3DText import Visual3DText
    from .OglLineAxis import OglLineAxis
    from .OglLabel import OglLabel
    from .OglIntVector2Variable import OglIntVector2Variable
    from .OglFloatAttribute import OglFloatAttribute
    from .OglFloatVariable import OglFloatVariable
    from .OglFloatVector4Variable import OglFloatVector4Variable
    from .DataDisplay import DataDisplay
    from .OglMatrix2x3Variable import OglMatrix2x3Variable
    from .DefaultVisualManagerLoop import DefaultVisualManagerLoop
    from .OglInt3Variable import OglInt3Variable
    from .SlicedVolumetricModel import SlicedVolumetricModel
    from .OglRenderingSRGB import OglRenderingSRGB
    from .OglFloat2Attribute import OglFloat2Attribute
    from .OglMatrix4VectorVariable import OglMatrix4VectorVariable
    from .OglFloat3Attribute import OglFloat3Attribute
    from .OglCylinderModel import OglCylinderModel
    from .VisualStyle import VisualStyle
    from .OglUInt2Attribute import OglUInt2Attribute
    from .OglShaderVisualModel import OglShaderVisualModel
    from .OglViewport import OglViewport
    from .OglModel import OglModel
    from .OglMatrix3x2Variable import OglMatrix3x2Variable
    from .OglMatrix4x2Variable import OglMatrix4x2Variable
    from .OglMatrix3Variable import OglMatrix3Variable
