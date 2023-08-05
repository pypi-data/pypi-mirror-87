# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ArticulationCenter

.. autofunction:: ArticulationCenter

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ArticulationCenter(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, parentIndex=None, childIndex=None, globalPosition=None, posOnParent=None, posOnChild=None, articulationProcess=None, **kwargs):
    """
    This class defines an articulation center. This contains a set of articulations.


    :param name: object name  Default value: ArticulationCenter

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param parentIndex: Parent of the center articulation  Default value: 0

    :param childIndex: Child of the center articulation  Default value: 0

    :param globalPosition: Global position of the articulation center  Default value: [[0.0, 0.0, 0.0]]

    :param posOnParent: Parent position of the articulation center  Default value: [[0.0, 0.0, 0.0]]

    :param posOnChild: Child position of the articulation center  Default value: [[0.0, 0.0, 0.0]]

    :param articulationProcess:  0 - (default) hierarchy between articulations (euler angles)
 1- ( on Parent) no hierarchy - axis are attached to the parent
 2- (attached on Child) no hierarchy - axis are attached to the child  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, parentIndex=parentIndex, childIndex=childIndex, globalPosition=globalPosition, posOnParent=posOnParent, posOnChild=posOnChild, articulationProcess=articulationProcess)
    return "ArticulationCenter", params
