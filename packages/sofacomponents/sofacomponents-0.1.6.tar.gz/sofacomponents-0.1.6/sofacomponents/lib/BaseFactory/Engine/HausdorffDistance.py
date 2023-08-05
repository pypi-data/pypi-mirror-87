# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component HausdorffDistance

.. autofunction:: HausdorffDistance

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def HausdorffDistance(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, points1=None, points2=None, d12=None, d21=None, max=None, update=None, **kwargs):
    """
    Compute the Hausdorff distance of two point clouds


    :param name: object name  Default value: HausdorffDistance

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param points1: Points belonging to the first point cloud  Default value: []

    :param points2: Points belonging to the second point cloud  Default value: []

    :param d12: Distance from point cloud 1 to 2  Default value: 0.0

    :param d21: Distance from point cloud 2 to 1  Default value: 0.0

    :param max: Symmetrical Hausdorff distance  Default value: 0.0

    :param update: Recompute every time step  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, points1=points1, points2=points2, d12=d12, d21=d21, max=max, update=update)
    return "HausdorffDistance", params
