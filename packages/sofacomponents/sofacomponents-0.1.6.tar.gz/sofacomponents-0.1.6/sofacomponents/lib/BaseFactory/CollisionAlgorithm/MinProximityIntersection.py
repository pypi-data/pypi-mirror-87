# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MinProximityIntersection

.. autofunction:: MinProximityIntersection

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MinProximityIntersection(self, alarmDistance=None, contactDistance=None, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, useSphereTriangle=None, usePointPoint=None, useSurfaceNormals=None, useLinePoint=None, useLineLine=None, **kwargs):
    """
    A set of methods to compute if two primitives are close enough to consider they collide


    :param name: object name  Default value: MinProximityIntersection

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param alarmDistance: Proximity detection distance  Default value: 1.0

    :param contactDistance: Distance below which a contact is created  Default value: 0.5

    :param useSphereTriangle: activate Sphere-Triangle intersection tests  Default value: 1

    :param usePointPoint: activate Point-Point intersection tests  Default value: 1

    :param useSurfaceNormals: Compute the norms of the Detection Outputs by considering the normals of the surfaces involved.  Default value: 0

    :param useLinePoint: activate Line-Point intersection tests  Default value: 1

    :param useLineLine: activate Line-Line  intersection tests  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, alarmDistance=alarmDistance, contactDistance=contactDistance, useSphereTriangle=useSphereTriangle, usePointPoint=usePointPoint, useSurfaceNormals=useSurfaceNormals, useLinePoint=useLinePoint, useLineLine=useLineLine)
    return "MinProximityIntersection", params
