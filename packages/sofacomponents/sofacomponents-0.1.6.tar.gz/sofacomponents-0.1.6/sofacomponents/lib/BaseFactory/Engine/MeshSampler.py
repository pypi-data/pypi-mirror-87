# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MeshSampler

.. autofunction:: MeshSampler

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MeshSampler(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, number=None, position=None, edges=None, maxIter=None, outputIndices=None, outputPosition=None, **kwargs):
    """
    Select uniformly distributed points on a mesh based on Euclidean or Geodesic distance measure


    :param name: object name  Default value: MeshSampler

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param number: Sample number  Default value: 1

    :param position: Input positions.  Default value: []

    :param edges: Input edges for geodesic sampling (Euclidean distances are used if not specified).  Default value: []

    :param maxIter: Max number of Lloyd iterations.  Default value: 100

    :param outputIndices: Computed sample indices.  Default value: []

    :param outputPosition: Computed sample coordinates.  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, number=number, position=position, edges=edges, maxIter=maxIter, outputIndices=outputIndices, outputPosition=outputPosition)
    return "MeshSampler", params
