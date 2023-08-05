# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component GeometryMonitor

.. autofunction:: GeometryMonitor

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def GeometryMonitor(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, handleEventTriggersUpdate=None, file=None, PointMitralExtremal=None, PointTricuspidExtremal=None, PointTopSeptum=None, PointApexRV=None, PointApexLV=None, AxisHeart=None, AxisRings=None, AxisLV=None, AxisRV=None, BarycentreMesh=None, BarycentreTwoRings=None, BarycentreRingMitral=None, BarycentreRingTricuspid=None, BarycentreLVendo=None, **kwargs):
    """
    Control the degree of Bezier tetrahedra on AdaptiveBezierTetrahedronContainer


    :param name: object name  Default value: GeometryMonitor

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param handleEventTriggersUpdate: Event handling frequency controls the controller update frequency  Default value: 0

    :param file: file  Default value: 

    :param PointMitralExtremal: PointMitralExtremal  Default value: 0

    :param PointTricuspidExtremal: PointTricuspidExtremal  Default value: 0

    :param PointTopSeptum: PointTopSeptum  Default value: 0

    :param PointApexRV: PointApexRV  Default value: 0

    :param PointApexLV: PointApexLV  Default value: 0

    :param AxisHeart: AxisHeart  Default value: [[0.0, 0.0, 0.0]]

    :param AxisRings: AxisRings  Default value: [[0.0, 0.0, 0.0]]

    :param AxisLV: AxisLV  Default value: [[0.0, 0.0, 0.0]]

    :param AxisRV: AxisRV  Default value: [[0.0, 0.0, 0.0]]

    :param BarycentreMesh: BarycentreMesh  Default value: [[0.0, 0.0, 0.0]]

    :param BarycentreTwoRings: BarycentreTwoRings  Default value: [[0.0, 0.0, 0.0]]

    :param BarycentreRingMitral: BarycentreRingMitral  Default value: [[0.0, 0.0, 0.0]]

    :param BarycentreRingTricuspid: BarycentreRingTricuspid  Default value: [[0.0, 0.0, 0.0]]

    :param BarycentreLVendo: BarycentreLVendo  Default value: [[0.0, 0.0, 0.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, handleEventTriggersUpdate=handleEventTriggersUpdate, file=file, PointMitralExtremal=PointMitralExtremal, PointTricuspidExtremal=PointTricuspidExtremal, PointTopSeptum=PointTopSeptum, PointApexRV=PointApexRV, PointApexLV=PointApexLV, AxisHeart=AxisHeart, AxisRings=AxisRings, AxisLV=AxisLV, AxisRV=AxisRV, BarycentreMesh=BarycentreMesh, BarycentreTwoRings=BarycentreTwoRings, BarycentreRingMitral=BarycentreRingMitral, BarycentreRingTricuspid=BarycentreRingTricuspid, BarycentreLVendo=BarycentreLVendo)
    return "GeometryMonitor", params
