# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TextureInterpolation

.. autofunction:: TextureInterpolation

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TextureInterpolation(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, input_states=None, input_coordinates=None, output_coordinates=None, scalarField=None, min_value=None, max_value=None, manual_scale=None, drawPotentiels=None, showIndicesScale=None, vertexPloted=None, graph=None, **kwargs):
    """
    Create texture coordinate for a given field


    :param name: object name  Default value: TextureInterpolation

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param input_states: input array of state values.  Default value: []

    :param input_coordinates: input array of coordinates values.  Default value: []

    :param output_coordinates: output array of texture coordinates.  Default value: []

    :param scalarField: To interpolate only the first dimension of input field (useful if this component need to be templated in higher dimension).  Default value: 1

    :param min_value: minimum value of state value for interpolation.  Default value: 0.0

    :param max_value: maximum value of state value for interpolation.  Default value: 0.0

    :param manual_scale: compute texture interpolation on manually scale defined above.  Default value: 0

    :param drawPotentiels: Debug: view state values.  Default value: 0

    :param showIndicesScale: Debug : scale of state values displayed.  Default value: 9.99999974738e-05

    :param vertexPloted: Vertex index of values display in graph for each iteration.  Default value: 0

    :param graph: Vertex state value per iteration  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, input_states=input_states, input_coordinates=input_coordinates, output_coordinates=output_coordinates, scalarField=scalarField, min_value=min_value, max_value=max_value, manual_scale=manual_scale, drawPotentiels=drawPotentiels, showIndicesScale=showIndicesScale, vertexPloted=vertexPloted, graph=graph)
    return "TextureInterpolation", params
