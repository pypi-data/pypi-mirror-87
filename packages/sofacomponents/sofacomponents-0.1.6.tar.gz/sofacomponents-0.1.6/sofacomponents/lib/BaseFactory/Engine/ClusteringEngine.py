# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ClusteringEngine

.. autofunction:: ClusteringEngine

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ClusteringEngine(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, useTopo=None, radius=None, fixedRadius=None, number=None, fixedPosition=None, position=None, cluster=None, inFile=None, outFile=None, **kwargs):
    """
    Group points into overlapping clusters according to a user defined number of clusters and radius


    :param name: object name  Default value: ClusteringEngine

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param useTopo: Use avalaible topology to compute neighborhood.  Default value: 1

    :param radius: Neighborhood range.  Default value: 1.0

    :param fixedRadius: Neighborhood range (for non mechanical particles).  Default value: 1.0

    :param number: Number of clusters (-1 means that all input points are selected).  Default value: -1

    :param fixedPosition: Input positions of fixed (non mechanical) particles.  Default value: []

    :param position: Input rest positions.  Default value: []

    :param cluster: Computed clusters.  Default value: []

    :param inFile: import precomputed clusters  Default value: 

    :param outFile: export clusters  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, useTopo=useTopo, radius=radius, fixedRadius=fixedRadius, number=number, fixedPosition=fixedPosition, position=position, cluster=cluster, inFile=inFile, outFile=outFile)
    return "ClusteringEngine", params
