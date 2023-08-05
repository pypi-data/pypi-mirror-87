# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component OglTexture

.. autofunction:: OglTexture

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def OglTexture(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, id=None, indexShader=None, filename=None, textureUnit=None, enabled=None, repeat=None, linearInterpolation=None, generateMipmaps=None, srgbColorspace=None, minLod=None, maxLod=None, proceduralTextureWidth=None, proceduralTextureHeight=None, proceduralTextureNbBits=None, proceduralTextureData=None, cubemapFilenamePosX=None, cubemapFilenamePosY=None, cubemapFilenamePosZ=None, cubemapFilenameNegX=None, cubemapFilenameNegY=None, cubemapFilenameNegZ=None, **kwargs):
    """
    OglTexture


    :param name: object name  Default value: OglTexture

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param id: Set an ID name  Default value: 

    :param indexShader: Set the index of the desired shader you want to apply this parameter  Default value: 0

    :param filename: Texture Filename  Default value: 

    :param textureUnit: Set the texture unit  Default value: 1

    :param enabled: enabled ?  Default value: 1

    :param repeat: Repeat Texture ?  Default value: 0

    :param linearInterpolation: Interpolate Texture ?  Default value: 1

    :param generateMipmaps: Generate mipmaps ?  Default value: 1

    :param srgbColorspace: SRGB colorspace ?  Default value: 0

    :param minLod: Minimum mipmap lod ?  Default value: -1000.0

    :param maxLod: Maximum mipmap lod ?  Default value: 1000.0

    :param proceduralTextureWidth: Width of procedural Texture  Default value: 0

    :param proceduralTextureHeight: Height of procedural Texture  Default value: 0

    :param proceduralTextureNbBits: Nb bits per color  Default value: 1

    :param proceduralTextureData: Data of procedural Texture   Default value: []

    :param cubemapFilenamePosX: Texture filename of positive-X cubemap face  Default value: 

    :param cubemapFilenamePosY: Texture filename of positive-Y cubemap face  Default value: 

    :param cubemapFilenamePosZ: Texture filename of positive-Z cubemap face  Default value: 

    :param cubemapFilenameNegX: Texture filename of negative-X cubemap face  Default value: 

    :param cubemapFilenameNegY: Texture filename of negative-Y cubemap face  Default value: 

    :param cubemapFilenameNegZ: Texture filename of negative-Z cubemap face  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, id=id, indexShader=indexShader, filename=filename, textureUnit=textureUnit, enabled=enabled, repeat=repeat, linearInterpolation=linearInterpolation, generateMipmaps=generateMipmaps, srgbColorspace=srgbColorspace, minLod=minLod, maxLod=maxLod, proceduralTextureWidth=proceduralTextureWidth, proceduralTextureHeight=proceduralTextureHeight, proceduralTextureNbBits=proceduralTextureNbBits, proceduralTextureData=proceduralTextureData, cubemapFilenamePosX=cubemapFilenamePosX, cubemapFilenamePosY=cubemapFilenamePosY, cubemapFilenamePosZ=cubemapFilenamePosZ, cubemapFilenameNegX=cubemapFilenameNegX, cubemapFilenameNegY=cubemapFilenameNegY, cubemapFilenameNegZ=cubemapFilenameNegZ)
    return "OglTexture", params
