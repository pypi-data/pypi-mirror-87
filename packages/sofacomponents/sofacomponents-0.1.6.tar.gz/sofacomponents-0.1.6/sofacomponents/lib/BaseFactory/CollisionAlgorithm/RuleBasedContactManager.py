# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component RuleBasedContactManager

.. autofunction:: RuleBasedContactManager

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def RuleBasedContactManager(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, response=None, responseParams=None, variables=None, rules=None, **kwargs):
    """
    Create different response to the collisions based on a set of rules


    :param name: object name  Default value: RuleBasedContactManager

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param response: contact response class  Default value: default

    :param responseParams: contact response parameters (syntax: name1=value1&name2=value2&...)  Default value: 

    :param variables: Define a list of variables to be used inside the rules  Default value: 

    :param rules: Ordered list of rules, each with a triplet of strings.
The first two define either the name of the collision model, its group number, or * meaning any model.
The last string define the response algorithm to use for contacts matched by this rule.
Rules are applied in the order they are specified. If none match a given contact, the default response is used.
  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, response=response, responseParams=responseParams, variables=variables, rules=rules)
    return "RuleBasedContactManager", params
