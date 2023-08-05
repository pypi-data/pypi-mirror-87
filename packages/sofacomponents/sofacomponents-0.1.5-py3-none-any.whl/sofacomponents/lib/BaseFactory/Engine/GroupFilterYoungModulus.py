# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component GroupFilterYoungModulus

.. autofunction:: GroupFilterYoungModulus

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def GroupFilterYoungModulus(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, groups=None, primitives=None, elementsGroup=None, youngModulus=None, mapGroupModulus=None, defaultYoungModulus=None, groupModulus=None, **kwargs):
    """
    This class gives a vector of young modulus according of a list of defined groups


    :param name: object name  Default value: GroupFilterYoungModulus

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param groups: Groups  Default value: 

    :param primitives: Vector of primitives (indices)  Default value: []

    :param elementsGroup: Vector of groups (each element gives its group  Default value: []

    :param youngModulus: Vector of young modulus for each primitive  Default value: []

    :param mapGroupModulus: Mapping between groups and modulus  Default value: 

    :param defaultYoungModulus: Default value if the primitive is not in a group  Default value: 10000.0

    :param groupModulus: list of young modulus for each group  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, groups=groups, primitives=primitives, elementsGroup=elementsGroup, youngModulus=youngModulus, mapGroupModulus=mapGroupModulus, defaultYoungModulus=defaultYoungModulus, groupModulus=groupModulus)
    return "GroupFilterYoungModulus", params
