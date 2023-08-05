# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SmoothMeshEngine

.. autofunction:: SmoothMeshEngine

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SmoothMeshEngine(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, input_position=None, input_indices=None, output_position=None, nb_iterations=None, showInput=None, showOutput=None, **kwargs):
    """
    Compute the laplacian smoothing of a mesh


    :param name: object name  Default value: SmoothMeshEngine

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param input_position: Input position  Default value: []

    :param input_indices: Position indices that need to be smoothed, leave empty for all positions  Default value: []

    :param output_position: Output position  Default value: []

    :param nb_iterations: Number of iterations of laplacian smoothing  Default value: 1

    :param showInput: showInput  Default value: 0

    :param showOutput: showOutput  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, input_position=input_position, input_indices=input_indices, output_position=output_position, nb_iterations=nb_iterations, showInput=showInput, showOutput=showOutput)
    return "SmoothMeshEngine", params
