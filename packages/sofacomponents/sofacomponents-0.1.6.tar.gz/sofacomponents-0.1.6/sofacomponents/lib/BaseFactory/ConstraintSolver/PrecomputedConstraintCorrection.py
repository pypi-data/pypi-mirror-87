# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PrecomputedConstraintCorrection

.. autofunction:: PrecomputedConstraintCorrection

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PrecomputedConstraintCorrection(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, rotations=None, restDeformations=None, recompute=None, debugViewFrameScale=None, fileCompliance=None, fileDir=None, **kwargs):
    """
    Component computing constraint forces within a simulated body using the compliance method.


    :param name: object name  Default value: PrecomputedConstraintCorrection

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param rotations: (No help available)  Default value: 0

    :param restDeformations: (No help available)  Default value: 0

    :param recompute: if true, always recompute the compliance  Default value: 0

    :param debugViewFrameScale: Scale on computed node's frame  Default value: 1.0

    :param fileCompliance: Precomputed compliance matrix data file  Default value: 

    :param fileDir: If not empty, the compliance will be saved in this repertory  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, rotations=rotations, restDeformations=restDeformations, recompute=recompute, debugViewFrameScale=debugViewFrameScale, fileCompliance=fileCompliance, fileDir=fileDir)
    return "PrecomputedConstraintCorrection", params
