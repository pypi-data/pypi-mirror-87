# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component OglOITShader

.. autofunction:: OglOITShader

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def OglOITShader(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, turnOn=None, passive=None, fileVertexShaders=None, fileFragmentShaders=None, fileGeometryShaders=None, fileTessellationControlShaders=None, fileTessellationEvaluationShaders=None, geometryInputType=None, geometryOutputType=None, geometryVerticesOut=None, tessellationOuterLevel=None, tessellationInnerLevel=None, indexActiveShader=None, backfaceWriting=None, clampVertexColor=None, **kwargs):
    """
    OglOITShader


    :param name: object name  Default value: OglOITShader

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param turnOn: Turn On the shader?  Default value: 1

    :param passive: Will this shader be activated manually or automatically?  Default value: 0

    :param fileVertexShaders: Set the vertex shader filename to load  Default value: [ 'shaders/orderIndependentTransparency/accumulation.vert' ]

    :param fileFragmentShaders: Set the fragment shader filename to load  Default value: [ 'shaders/orderIndependentTransparency/accumulation.frag' ]

    :param fileGeometryShaders: Set the geometry shader filename to load  Default value: []

    :param fileTessellationControlShaders: Set the tessellation control filename to load  Default value: []

    :param fileTessellationEvaluationShaders: Set the tessellation evaluation filename to load  Default value: []

    :param geometryInputType: Set input types for the geometry shader  Default value: -1

    :param geometryOutputType: Set output types for the geometry shader  Default value: -1

    :param geometryVerticesOut: Set max number of vertices in output for the geometry shader  Default value: -1

    :param tessellationOuterLevel: For tessellation without control shader: default outer level (edge subdivisions)  Default value: 1.0

    :param tessellationInnerLevel: For tessellation without control shader: default inner level (face subdivisions)  Default value: 1.0

    :param indexActiveShader: Set current active shader  Default value: 0

    :param backfaceWriting: it enables writing to gl_BackColor inside a GLSL vertex shader  Default value: 0

    :param clampVertexColor: clamp the vertex color between 0 and 1  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, turnOn=turnOn, passive=passive, fileVertexShaders=fileVertexShaders, fileFragmentShaders=fileFragmentShaders, fileGeometryShaders=fileGeometryShaders, fileTessellationControlShaders=fileTessellationControlShaders, fileTessellationEvaluationShaders=fileTessellationEvaluationShaders, geometryInputType=geometryInputType, geometryOutputType=geometryOutputType, geometryVerticesOut=geometryVerticesOut, tessellationOuterLevel=tessellationOuterLevel, tessellationInnerLevel=tessellationInnerLevel, indexActiveShader=indexActiveShader, backfaceWriting=backfaceWriting, clampVertexColor=clampVertexColor)
    return "OglOITShader", params
