# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component HatShapeFunction

.. autofunction:: HatShapeFunction

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def HatShapeFunction(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, nbRef=None, position=None, method=None, param=None, **kwargs):
    """
    Computes compactly supported hat shape functions


    :param name: object name  Default value: HatShapeFunction

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param nbRef: maximum number of parents per child  Default value: 4

    :param position: position of parent nodes  Default value: []

    :param method: method  Default value: 0 - max[0,(1-(dist/R)^p)^n], params=(R,p=2,n=3)

    :param param: param  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, nbRef=nbRef, position=position, method=method, param=param)
    return "HatShapeFunction", params
