# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ContractionInitialization

.. autofunction:: ContractionInitialization

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ContractionInitialization(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, input_values=None, outputs=None, filename=None, secondaryValues=None, tagContraction=None, **kwargs):
    """
    Create potentiel array for initial conditions


    :param name: object name  Default value: ContractionInitialization

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param input_values: input array of manual potential values <index of tetrahedra ,contraction,stiffness>.  Default value: []

    :param outputs: output array of initial condition contraction and stiffness values.  Default value: []

    :param filename: name of file where to write initial condition potential values.  Default value: 

    :param secondaryValues: default value given to other dimension fields.  Default value: 0.0

    :param tagContraction: Tag of the contraction node  Default value: tagContraction


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, input_values=input_values, outputs=outputs, filename=filename, secondaryValues=secondaryValues, tagContraction=tagContraction)
    return "ContractionInitialization", params
