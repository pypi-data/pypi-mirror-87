# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component QuatToRigidEngine

.. autofunction:: QuatToRigidEngine

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def QuatToRigidEngine(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, positions=None, orientations=None, colinearPositions=None, rigids=None, **kwargs):
    """
    Transform a vector of Rigids into two independant vectors for positions (Vec3) and orientations (Quat).


    :param name: object name  Default value: QuatToRigidEngine

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param positions: Positions (Vector of 3)  Default value: []

    :param orientations: Orientations (Quaternion)  Default value: []

    :param colinearPositions: Optional positions to restrict output to be colinear in the quaternion Z direction  Default value: []

    :param rigids: Rigid (Position + Orientation)  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, positions=positions, orientations=orientations, colinearPositions=colinearPositions, rigids=rigids)
    return "QuatToRigidEngine", params
