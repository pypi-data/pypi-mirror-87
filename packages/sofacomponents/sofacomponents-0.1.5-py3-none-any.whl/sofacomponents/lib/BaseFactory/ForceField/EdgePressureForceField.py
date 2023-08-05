# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component EdgePressureForceField

.. autofunction:: EdgePressureForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def EdgePressureForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, edgePressureMap=None, pressure=None, edgeIndices=None, edges=None, normal=None, dmin=None, dmax=None, arrowSizeCoef=None, p_intensity=None, binormal=None, showForces=None, **kwargs):
    """
    EdgePressure


    :param name: object name  Default value: EdgePressureForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param edgePressureMap: map between edge indices and their pressure  Default value: 

    :param pressure: Pressure force per unit area  Default value: [[0.0, 0.0, 0.0]]

    :param edgeIndices: Indices of edges separated with commas where a pressure is applied  Default value: []

    :param edges: List of edges where a pressure is applied  Default value: []

    :param normal: Normal direction for the plane selection of edges  Default value: [[0.0, 0.0, 0.0]]

    :param dmin: Minimum distance from the origin along the normal direction  Default value: 0.0

    :param dmax: Maximum distance from the origin along the normal direction  Default value: 0.0

    :param arrowSizeCoef: Size of the drawn arrows (0->no arrows, sign->direction of drawing  Default value: 0.0

    :param p_intensity: pressure intensity on edge normal  Default value: []

    :param binormal: Binormal of the 2D plane  Default value: [[0.0, 0.0, 0.0]]

    :param showForces: draw arrows of edge pressures  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, edgePressureMap=edgePressureMap, pressure=pressure, edgeIndices=edgeIndices, edges=edges, normal=normal, dmin=dmin, dmax=dmax, arrowSizeCoef=arrowSizeCoef, p_intensity=p_intensity, binormal=binormal, showForces=showForces)
    return "EdgePressureForceField", params
