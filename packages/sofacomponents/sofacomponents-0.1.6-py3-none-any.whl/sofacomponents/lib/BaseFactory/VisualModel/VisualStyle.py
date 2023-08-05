# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component VisualStyle

.. autofunction:: VisualStyle

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def VisualStyle(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, displayFlags=None, **kwargs):
    """
    Edit the visual style.
 Allowed values for displayFlags data are a combination of the following:
showAll, hideAll,
    showVisual, hideVisual,
        showVisualModels, hideVisualModels,
    showBehavior, hideBehavior,
        showBehaviorModels, hideBehaviorModels,
        showForceFields, hideForceFields,
        showInteractionForceFields, hideInteractionForceFields
    showMapping, hideMapping
        showMappings, hideMappings
        showMechanicalMappings, hideMechanicalMappings
    showCollision, hideCollision
        showCollisionModels, hideCollisionModels
        showBoundingCollisionModels, hideBoundingCollisionModels
    showOptions hideOptions
        showRendering hideRendering
        showNormals hideNormals
        showWireframe hideWireframe


    :param name: object name  Default value: VisualStyle

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param displayFlags: Display Flags  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, displayFlags=displayFlags)
    return "VisualStyle", params
