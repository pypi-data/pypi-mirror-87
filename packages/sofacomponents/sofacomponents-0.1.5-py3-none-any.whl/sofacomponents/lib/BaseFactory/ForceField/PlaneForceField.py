# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PlaneForceField

.. autofunction:: PlaneForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PlaneForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, normal=None, d=None, stiffness=None, damping=None, maxForce=None, bilateral=None, localRange=None, showPlane=None, planeColor=None, showPlaneSize=None, **kwargs):
    """
    Repulsion applied by a plane toward the exterior (half-space)


    :param name: object name  Default value: PlaneForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param normal: plane normal. (default=[0,1,0])  Default value: [[0.0, 1.0, 0.0]]

    :param d: plane d coef. (default=0)  Default value: 0.0

    :param stiffness: force stiffness. (default=500)  Default value: 500.0

    :param damping: force damping. (default=5)  Default value: 5.0

    :param maxForce: if non-null , the max force that can be applied to the object. (default=0)  Default value: 0.0

    :param bilateral: if true the plane force field is applied on both sides. (default=false)  Default value: 0

    :param localRange: optional range of local DOF indices. Any computation involving indices outside of this range are discarded (useful for parallelization using mesh partitionning)  Default value: [[-1, -1]]

    :param showPlane: enable/disable drawing of plane. (default=false)  Default value: 0

    :param planeColor: plane color. (default=[0.0,0.5,0.2,1.0])  Default value: [[0.0, 0.5, 0.20000000298023224, 1.0]]

    :param showPlaneSize: plane display size if draw is enabled. (default=10)  Default value: 10.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, normal=normal, d=d, stiffness=stiffness, damping=damping, maxForce=maxForce, bilateral=bilateral, localRange=localRange, showPlane=showPlane, planeColor=planeColor, showPlaneSize=showPlaneSize)
    return "PlaneForceField", params
