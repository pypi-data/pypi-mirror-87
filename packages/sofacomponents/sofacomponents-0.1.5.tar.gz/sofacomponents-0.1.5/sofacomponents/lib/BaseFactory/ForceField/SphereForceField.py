# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SphereForceField

.. autofunction:: SphereForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SphereForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, contacts=None, center=None, radius=None, stiffness=None, damping=None, color=None, localRange=None, bilateral=None, **kwargs):
    """
    Repulsion applied by a sphere toward the exterior


    :param name: object name  Default value: SphereForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param contacts: Contacts  Default value: 

    :param center: sphere center  Default value: [[0.0, 0.0, 0.0]]

    :param radius: sphere radius  Default value: 1.0

    :param stiffness: force stiffness  Default value: 500.0

    :param damping: force damping  Default value: 5.0

    :param color: sphere color. (default=[0,0,1,1])  Default value: [[0.0, 0.0, 1.0, 1.0]]

    :param localRange: optional range of local DOF indices. Any computation involving only indices outside of this range are discarded (useful for parallelization using mesh partitionning)  Default value: [[-1, -1]]

    :param bilateral: if true the sphere force field is applied on both sides  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, contacts=contacts, center=center, radius=radius, stiffness=stiffness, damping=damping, color=color, localRange=localRange, bilateral=bilateral)
    return "SphereForceField", params
