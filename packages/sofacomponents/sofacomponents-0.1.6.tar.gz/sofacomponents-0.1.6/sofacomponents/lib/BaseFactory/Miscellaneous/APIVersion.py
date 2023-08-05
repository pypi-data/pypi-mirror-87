# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component APIVersion

.. autofunction:: APIVersion

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def APIVersion(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, level=None, **kwargs):
    """
    Specify the APIVersion of the component used in a scene.


    :param name: object name  Default value: APIVersion

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param level: The API Level of the scene ('17.06', '17.12', '18.06', ...)  Default value: 17.06


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, level=level)
    return "APIVersion", params
