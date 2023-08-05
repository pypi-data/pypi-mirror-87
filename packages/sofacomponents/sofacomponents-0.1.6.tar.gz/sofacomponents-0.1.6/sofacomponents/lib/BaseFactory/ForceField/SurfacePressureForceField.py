# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SurfacePressureForceField

.. autofunction:: SurfacePressureForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SurfacePressureForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, pressure=None, min=None, max=None, triangleIndices=None, quadIndices=None, pulseMode=None, pressureLowerBound=None, pressureSpeed=None, volumeConservationMode=None, useTangentStiffness=None, defaultVolume=None, mainDirection=None, drawForceScale=None, **kwargs):
    """
    SurfacePressure


    :param name: object name  Default value: SurfacePressureForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param pressure: Pressure force per unit area  Default value: 0.0

    :param min: Lower bond of the selection box  Default value: [[0.0, 0.0, 0.0]]

    :param max: Upper bond of the selection box  Default value: [[0.0, 0.0, 0.0]]

    :param triangleIndices: Indices of affected triangles  Default value: []

    :param quadIndices: Indices of affected quads  Default value: []

    :param pulseMode: Cyclic pressure application  Default value: 0

    :param pressureLowerBound: Pressure lower bound force per unit area (active in pulse mode)  Default value: 0.0

    :param pressureSpeed: Continuous pressure application in Pascal per second. Only active in pulse mode  Default value: 0.0

    :param volumeConservationMode: Pressure variation follow the inverse of the volume variation  Default value: 0

    :param useTangentStiffness: Whether (non-symmetric) stiffness matrix should be used  Default value: 1

    :param defaultVolume: Default Volume  Default value: -1.0

    :param mainDirection: Main direction for pressure application  Default value: [[0.0, 0.0, 0.0]]

    :param drawForceScale: DEBUG: scale used to render force vectors  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, pressure=pressure, min=min, max=max, triangleIndices=triangleIndices, quadIndices=quadIndices, pulseMode=pulseMode, pressureLowerBound=pressureLowerBound, pressureSpeed=pressureSpeed, volumeConservationMode=volumeConservationMode, useTangentStiffness=useTangentStiffness, defaultVolume=defaultVolume, mainDirection=mainDirection, drawForceScale=drawForceScale)
    return "SurfacePressureForceField", params
