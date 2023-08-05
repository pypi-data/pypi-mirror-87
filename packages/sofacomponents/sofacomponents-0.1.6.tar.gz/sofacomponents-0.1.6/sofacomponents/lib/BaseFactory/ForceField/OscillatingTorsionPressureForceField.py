# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component OscillatingTorsionPressureForceField

.. autofunction:: OscillatingTorsionPressureForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def OscillatingTorsionPressureForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, trianglePressureMap=None, moment=None, triangleList=None, axis=None, center=None, penalty=None, frequency=None, dmin=None, dmax=None, showForces=None, **kwargs):
    """
    OscillatingTorsionPressure


    :param name: object name  Default value: OscillatingTorsionPressureForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param trianglePressureMap: map between edge indices and their pressure  Default value: 

    :param moment: Moment force applied on the entire surface  Default value: 0.0

    :param triangleList: Indices of triangles separated with commas where a pressure is applied  Default value: []

    :param axis: Axis of rotation and normal direction for the plane selection of triangles  Default value: [[0.0, 0.0, 1.0]]

    :param center: Center of rotation  Default value: [[0.0, 0.0, 0.0]]

    :param penalty: Strength of the penalty force  Default value: 1000.0

    :param frequency: frequency of oscillation  Default value: 1.0

    :param dmin: Minimum distance from the origin along the normal direction  Default value: 0.0

    :param dmax: Maximum distance from the origin along the normal direction  Default value: 0.0

    :param showForces: draw triangles which have a given pressure  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, trianglePressureMap=trianglePressureMap, moment=moment, triangleList=triangleList, axis=axis, center=center, penalty=penalty, frequency=frequency, dmin=dmin, dmax=dmax, showForces=showForces)
    return "OscillatingTorsionPressureForceField", params
