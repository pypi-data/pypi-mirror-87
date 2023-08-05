# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component RandomPointDistributionInSurface

.. autofunction:: RandomPointDistributionInSurface

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def RandomPointDistributionInSurface(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, randomSeed=None, isVisible=None, drawOutputPoints=None, minDistanceBetweenPoints=None, numberOfInPoints=None, numberOfTests=None, vertices=None, triangles=None, inPoints=None, outPoints=None, **kwargs):
    """
    This class truns on spiral any topological model


    :param name: object name  Default value: RandomPointDistributionInSurface

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param randomSeed: Set a specified seed for random generation (0 for "true pseudo-randomness"   Default value: 0

    :param isVisible: is Visible ?  Default value: 1

    :param drawOutputPoints: Output points visible ?  Default value: 0

    :param minDistanceBetweenPoints: Min Distance between 2 points (-1 for true randomness)  Default value: 0.1

    :param numberOfInPoints: Number of points inside  Default value: 10

    :param numberOfTests: Number of tests to find if the point is inside or not (odd number)  Default value: 5

    :param vertices: Vertices  Default value: []

    :param triangles: Triangles indices  Default value: []

    :param inPoints: Points inside the surface  Default value: []

    :param outPoints: Points outside the surface  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, randomSeed=randomSeed, isVisible=isVisible, drawOutputPoints=drawOutputPoints, minDistanceBetweenPoints=minDistanceBetweenPoints, numberOfInPoints=numberOfInPoints, numberOfTests=numberOfTests, vertices=vertices, triangles=triangles, inPoints=inPoints, outPoints=outPoints)
    return "RandomPointDistributionInSurface", params
