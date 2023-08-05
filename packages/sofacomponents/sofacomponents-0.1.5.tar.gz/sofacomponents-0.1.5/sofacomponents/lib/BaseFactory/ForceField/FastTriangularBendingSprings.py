# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component FastTriangularBendingSprings

.. autofunction:: FastTriangularBendingSprings

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def FastTriangularBendingSprings(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, bendingStiffness=None, minDistValidity=None, edgeInfo=None, **kwargs):
    """
    Springs added to a triangular mesh to prevent bending


    :param name: object name  Default value: FastTriangularBendingSprings

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param bendingStiffness: bending stiffness of the material  Default value: 1.0

    :param minDistValidity: Distance under which a spring is not valid  Default value: 1e-06

    :param edgeInfo: Internal edge data  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, bendingStiffness=bendingStiffness, minDistValidity=minDistValidity, edgeInfo=edgeInfo)
    return "FastTriangularBendingSprings", params
