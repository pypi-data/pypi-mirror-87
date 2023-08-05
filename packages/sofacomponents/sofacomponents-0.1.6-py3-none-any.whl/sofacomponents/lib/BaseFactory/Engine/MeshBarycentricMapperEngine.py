# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MeshBarycentricMapperEngine

.. autofunction:: MeshBarycentricMapperEngine

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MeshBarycentricMapperEngine(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, inputPositions=None, mappedPointPositions=None, barycentricPositions=None, tableElements=None, computeLinearInterpolation=None, linearInterpolationIndices=None, linearInterpolationValues=None, **kwargs):
    """
    This class maps a set of points in a topological model and provide barycentric coordinates


    :param name: object name  Default value: MeshBarycentricMapperEngine

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param inputPositions: Initial positions of the master points  Default value: []

    :param mappedPointPositions: Initial positions of the mapped points  Default value: []

    :param barycentricPositions: Output : Barycentric positions of the mapped points  Default value: []

    :param tableElements: Output : Table that provides the element index to which each input point belongs  Default value: []

    :param computeLinearInterpolation: if true, computes a linear interpolation (debug)  Default value: 0

    :param linearInterpolationIndices: Indices of a linear interpolation  Default value: []

    :param linearInterpolationValues: Values of a linear interpolation  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, inputPositions=inputPositions, mappedPointPositions=mappedPointPositions, barycentricPositions=barycentricPositions, tableElements=tableElements, computeLinearInterpolation=computeLinearInterpolation, linearInterpolationIndices=linearInterpolationIndices, linearInterpolationValues=linearInterpolationValues)
    return "MeshBarycentricMapperEngine", params
