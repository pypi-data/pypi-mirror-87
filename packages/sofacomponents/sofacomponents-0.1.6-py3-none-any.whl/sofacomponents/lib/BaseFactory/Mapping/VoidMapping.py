# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component VoidMapping

.. autofunction:: VoidMapping

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def VoidMapping(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, mapForces=None, mapConstraints=None, mapMasses=None, mapMatrices=None, **kwargs):
    """
    Special mapping that 'map' points for void ( no input DOF ). This is useful to be able to create animated objects mixed with real DOFs.


    :param name: object name  Default value: VoidMapping

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param mapForces: Are forces mapped ?  Default value: 0

    :param mapConstraints: Are constraints mapped ?  Default value: 0

    :param mapMasses: Are masses mapped ?  Default value: 0

    :param mapMatrices: Are matrix explicit mapped?  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, mapForces=mapForces, mapConstraints=mapConstraints, mapMasses=mapMasses, mapMatrices=mapMatrices)
    return "VoidMapping", params
