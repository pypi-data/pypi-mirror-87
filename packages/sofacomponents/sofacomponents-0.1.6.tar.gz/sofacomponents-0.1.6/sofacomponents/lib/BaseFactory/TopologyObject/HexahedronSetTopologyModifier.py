# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component HexahedronSetTopologyModifier

.. autofunction:: HexahedronSetTopologyModifier

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def HexahedronSetTopologyModifier(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, propagateToDOF=None, removeIsolated=None, **kwargs):
    """
    Hexahedron set topology modifier


    :param name: object name  Default value: HexahedronSetTopologyModifier

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param propagateToDOF:  propagate changes to MEchanical object DOFs if true  Default value: 1

    :param removeIsolated: remove Isolated dof  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, propagateToDOF=propagateToDOF, removeIsolated=removeIsolated)
    return "HexahedronSetTopologyModifier", params
