# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TaitSurfacePressureForceField

.. autofunction:: TaitSurfacePressureForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TaitSurfacePressureForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, p0=None, B=None, gamma=None, injectedVolume=None, maxInjectionRate=None, initialVolume=None, currentInjectedVolume=None, v0=None, currentVolume=None, currentPressure=None, currentStiffness=None, pressureTriangles=None, initialSurfaceArea=None, currentSurfaceArea=None, drawForceScale=None, drawForceColor=None, volumeAfterTC=None, surfaceAreaAfterTC=None, **kwargs):
    """
    This component computes the volume enclosed by a surface mesh and apply a pressure force following Tait's equation: $P = P_0 - B((V/V_0)^\gamma - 1)$.
This ForceField can be used to apply :
 * a constant pressure (set $B=0$ and use $P_0$)
 * an ideal gas pressure (set $\gamma=1$ and use $B$)
 * a pressure from water (set $\gamma=7$ and use $B$)


    :param name: object name  Default value: TaitSurfacePressureForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param p0: IN: Rest pressure when V = V0  Default value: 0.0

    :param B: IN: Bulk modulus (resistance to uniform compression)  Default value: 0.0

    :param gamma: IN: Bulk modulus (resistance to uniform compression)  Default value: 0.0

    :param injectedVolume: IN: Injected (or extracted) volume since the start of the simulation  Default value: 0.0

    :param maxInjectionRate: IN: Maximum injection rate (volume per second)  Default value: 1000.0

    :param initialVolume: OUT: Initial volume, as computed from the surface rest position  Default value: 0.0

    :param currentInjectedVolume: OUT: Current injected (or extracted) volume (taking into account maxInjectionRate)  Default value: 0.0

    :param v0: OUT: Rest volume (as computed from initialVolume + injectedVolume)  Default value: 0.0

    :param currentVolume: OUT: Current volume, as computed from the last surface position  Default value: 0.0

    :param currentPressure: OUT: Current pressure, as computed from the last surface position  Default value: 0.0

    :param currentStiffness: OUT: dP/dV at current volume and pressure  Default value: 0.0

    :param pressureTriangles: OUT: list of triangles where a pressure is applied (mesh triangles + tesselated quads)  Default value: []

    :param initialSurfaceArea: OUT: Initial surface area, as computed from the surface rest position  Default value: 0.0

    :param currentSurfaceArea: OUT: Current surface area, as computed from the last surface position  Default value: 0.0

    :param drawForceScale: DEBUG: scale used to render force vectors  Default value: 0.001

    :param drawForceColor: DEBUG: color used to render force vectors  Default value: [[0.0, 1.0, 1.0, 1.0]]

    :param volumeAfterTC: OUT: Volume after a topology change  Default value: 0.0

    :param surfaceAreaAfterTC: OUT: Surface area after a topology change  Default value: 0.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, p0=p0, B=B, gamma=gamma, injectedVolume=injectedVolume, maxInjectionRate=maxInjectionRate, initialVolume=initialVolume, currentInjectedVolume=currentInjectedVolume, v0=v0, currentVolume=currentVolume, currentPressure=currentPressure, currentStiffness=currentStiffness, pressureTriangles=pressureTriangles, initialSurfaceArea=initialSurfaceArea, currentSurfaceArea=currentSurfaceArea, drawForceScale=drawForceScale, drawForceColor=drawForceColor, volumeAfterTC=volumeAfterTC, surfaceAreaAfterTC=surfaceAreaAfterTC)
    return "TaitSurfacePressureForceField", params
