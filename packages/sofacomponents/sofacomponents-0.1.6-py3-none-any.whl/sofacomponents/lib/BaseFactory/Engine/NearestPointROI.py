# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component NearestPointROI

.. autofunction:: NearestPointROI

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def NearestPointROI(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, indices1=None, indices2=None, radius=None, **kwargs):
    """
    Attach given pair of particles, projecting the positions of the second particles to the first ones


    :param name: object name  Default value: NearestPointROI

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param indices1: Indices of the points on the first model  Default value: []

    :param indices2: Indices of the points on the second model  Default value: []

    :param radius: Radius to search corresponding fixed point  Default value: 1.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, indices1=indices1, indices2=indices2, radius=radius)
    return "NearestPointROI", params
