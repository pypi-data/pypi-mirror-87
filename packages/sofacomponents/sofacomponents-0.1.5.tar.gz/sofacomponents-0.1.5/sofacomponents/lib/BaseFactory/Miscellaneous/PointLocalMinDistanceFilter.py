# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PointLocalMinDistanceFilter

.. autofunction:: PointLocalMinDistanceFilter

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PointLocalMinDistanceFilter(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, coneExtension=None, coneMinAngle=None, isRigid=None, pointInfo=None, **kwargs):
    """
    This class manages Point collision models cones filters computations and updates.


    :param name: object name  Default value: PointLocalMinDistanceFilter

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param coneExtension: Filtering cone extension angle.  Default value: 0.5

    :param coneMinAngle: Minimal filtering cone angle value, independent from geometry.  Default value: 0.0

    :param isRigid: filters optimization for rigid case.  Default value: 0

    :param pointInfo: point filter data  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, coneExtension=coneExtension, coneMinAngle=coneMinAngle, isRigid=isRigid, pointInfo=pointInfo)
    return "PointLocalMinDistanceFilter", params
