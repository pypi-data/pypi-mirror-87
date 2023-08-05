# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component OglModel

.. autofunction:: OglModel

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def OglModel(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, position=None, restPosition=None, normal=None, initRestPositions=None, useNormals=None, updateNormals=None, computeTangents=None, updateTangents=None, handleDynamicTopology=None, fixMergedUVSeams=None, keepLines=None, vertices=None, texcoords=None, tangents=None, bitangents=None, edges=None, triangles=None, quads=None, vertPosIdx=None, vertNormIdx=None, filename=None, texturename=None, translation=None, rotation=None, scale3d=None, scaleTex=None, translationTex=None, material=None, putOnlyTexCoords=None, srgbTexturing=None, materials=None, groups=None, blendTranslucency=None, premultipliedAlpha=None, writeZTransparent=None, alphaBlend=None, depthTest=None, cullFace=None, lineWidth=None, pointSize=None, lineSmooth=None, pointSmooth=None, isEnabled=None, primitiveType=None, blendEquation=None, sfactor=None, dfactor=None, **kwargs):
    """
    Generic visual model for OpenGL display


    :param name: object name  Default value: OglModel

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param position: Vertices coordinates  Default value: []

    :param restPosition: Vertices rest coordinates  Default value: []

    :param normal: Normals of the model  Default value: []

    :param initRestPositions: True if rest positions must be initialized with initial positions  Default value: 0

    :param useNormals: True if normal smoothing groups should be read from file  Default value: 1

    :param updateNormals: True if normals should be updated at each iteration  Default value: 1

    :param computeTangents: True if tangents should be computed at startup  Default value: 0

    :param updateTangents: True if tangents should be updated at each iteration  Default value: 1

    :param handleDynamicTopology: True if topological changes should be handled  Default value: 1

    :param fixMergedUVSeams: True if UV seams should be handled even when duplicate UVs are merged  Default value: 1

    :param keepLines: keep and draw lines (false by default)  Default value: 0

    :param vertices: vertices of the model (only if vertices have multiple normals/texcoords, otherwise positions are used)  Default value: []

    :param texcoords: coordinates of the texture  Default value: []

    :param tangents: tangents for normal mapping  Default value: []

    :param bitangents: tangents for normal mapping  Default value: []

    :param edges: edges of the model  Default value: []

    :param triangles: triangles of the model  Default value: []

    :param quads: quads of the model  Default value: []

    :param vertPosIdx: If vertices have multiple normals/texcoords stores vertices position indices  Default value: []

    :param vertNormIdx: If vertices have multiple normals/texcoords stores vertices normal indices  Default value: []

    :param filename:  Path to an ogl model  Default value: 

    :param texturename: Name of the Texture  Default value: 

    :param translation: Initial Translation of the object  Default value: [[0.0, 0.0, 0.0]]

    :param rotation: Initial Rotation of the object  Default value: [[0.0, 0.0, 0.0]]

    :param scale3d: Initial Scale of the object  Default value: [[1.0, 1.0, 1.0]]

    :param scaleTex: Scale of the texture  Default value: [[1.0, 1.0]]

    :param translationTex: Translation of the texture  Default value: [[0.0, 0.0]]

    :param material: Material  Default value: Default Diffuse 1 0.75 0.75 0.75 1 Ambient 1 0.2 0.2 0.2 1 Specular 0 1 1 1 1 Emissive 0 0 0 0 0 Shininess 0 45 

    :param putOnlyTexCoords: Give Texture Coordinates without the texture binding  Default value: 0

    :param srgbTexturing: When sRGB rendering is enabled, is the texture in sRGB colorspace?  Default value: 0

    :param materials: List of materials  Default value: 

    :param groups: Groups of triangles and quads using a given material  Default value: 

    :param blendTranslucency: Blend transparent parts  Default value: 1

    :param premultipliedAlpha: is alpha premultiplied ?  Default value: 0

    :param writeZTransparent: Write into Z Buffer for Transparent Object  Default value: 0

    :param alphaBlend: Enable alpha blending  Default value: 0

    :param depthTest: Enable depth testing  Default value: 1

    :param cullFace: Face culling (0 = no culling, 1 = cull back faces, 2 = cull front faces)  Default value: 0

    :param lineWidth: Line width (set if != 1, only for lines rendering)  Default value: 1.0

    :param pointSize: Point size (set if != 1, only for points rendering)  Default value: 1.0

    :param lineSmooth: Enable smooth line rendering  Default value: 0

    :param pointSmooth: Enable smooth point rendering  Default value: 0

    :param isEnabled: Activate/deactive the component.  Default value: 1

    :param primitiveType: Select types of primitives to send (necessary for some shader types such as geometry or tesselation)  Default value: DEFAULT

    :param blendEquation: if alpha blending is enabled this specifies how source and destination colors are combined  Default value: GL_FUNC_ADD

    :param sfactor: if alpha blending is enabled this specifies how the red, green, blue, and alpha source blending factors are computed  Default value: GL_SRC_ALPHA

    :param dfactor: if alpha blending is enabled this specifies how the red, green, blue, and alpha destination blending factors are computed  Default value: GL_ONE_MINUS_SRC_ALPHA


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, position=position, restPosition=restPosition, normal=normal, initRestPositions=initRestPositions, useNormals=useNormals, updateNormals=updateNormals, computeTangents=computeTangents, updateTangents=updateTangents, handleDynamicTopology=handleDynamicTopology, fixMergedUVSeams=fixMergedUVSeams, keepLines=keepLines, vertices=vertices, texcoords=texcoords, tangents=tangents, bitangents=bitangents, edges=edges, triangles=triangles, quads=quads, vertPosIdx=vertPosIdx, vertNormIdx=vertNormIdx, filename=filename, texturename=texturename, translation=translation, rotation=rotation, scale3d=scale3d, scaleTex=scaleTex, translationTex=translationTex, material=material, putOnlyTexCoords=putOnlyTexCoords, srgbTexturing=srgbTexturing, materials=materials, groups=groups, blendTranslucency=blendTranslucency, premultipliedAlpha=premultipliedAlpha, writeZTransparent=writeZTransparent, alphaBlend=alphaBlend, depthTest=depthTest, cullFace=cullFace, lineWidth=lineWidth, pointSize=pointSize, lineSmooth=lineSmooth, pointSmooth=pointSmooth, isEnabled=isEnabled, primitiveType=primitiveType, blendEquation=blendEquation, sfactor=sfactor, dfactor=dfactor)
    return "OglModel", params
