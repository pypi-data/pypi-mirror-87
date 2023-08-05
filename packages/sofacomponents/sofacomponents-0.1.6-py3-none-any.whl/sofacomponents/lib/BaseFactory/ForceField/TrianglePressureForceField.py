# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TrianglePressureForceField

.. autofunction:: TrianglePressureForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TrianglePressureForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, pressure=None, cauchyStress=None, triangleList=None, normal=None, dmin=None, dmax=None, showForces=None, useConstantForce=None, trianglePressureMap=None, **kwargs):
    """
    TrianglePressure


    :param name: object name  Default value: TrianglePressureForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param pressure: Pressure force per unit area  Default value: [[0.0, 0.0, 0.0]]

    :param cauchyStress: Cauchy Stress applied on the normal of each triangle  Default value: [ 0 0 0 , 0 0 0 , 0 0 0 ,]

    :param triangleList: Indices of triangles separated with commas where a pressure is applied  Default value: []

    :param normal: Normal direction for the plane selection of triangles  Default value: [[0.0, 0.0, 0.0]]

    :param dmin: Minimum distance from the origin along the normal direction  Default value: 0.0

    :param dmax: Maximum distance from the origin along the normal direction  Default value: 0.0

    :param showForces: draw triangles which have a given pressure  Default value: 0

    :param useConstantForce: applied force is computed as the the pressure vector times the area at rest  Default value: 1

    :param trianglePressureMap: map between edge indices and their pressure  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, pressure=pressure, cauchyStress=cauchyStress, triangleList=triangleList, normal=normal, dmin=dmin, dmax=dmax, showForces=showForces, useConstantForce=useConstantForce, trianglePressureMap=trianglePressureMap)
    return "TrianglePressureForceField", params
