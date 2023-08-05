# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component PressureConstraintForceField

.. autofunction:: PressureConstraintForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def PressureConstraintForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, loadername=None, loaderZoneNames=None, loaderZones=None, pointZoneName=None, pointZones=None, trianglesSurf=None, tagSolver=None, atriumParam=None, aorticParam=None, Pv0=None, heartPeriod=None, file=None, Kiso=None, windkessel=None, SurfaceZone=None, useProjection=None, useVerdandi=None, DisableFirstAtriumContraction=None, ZoneType=None, graphPressure=None, graphVolume=None, graphFlow=None, volume=None, pressurePv=None, pressurePat=None, pressurePar=None, flowQ=None, displayName=None, BoundaryEdgesPath=None, BoundaryEdgesKey=None, edgeInfo=None, **kwargs):
    """
    PressureConstraint's law in Tetrahedral finite elements


    :param name: object name  Default value: PressureConstraintForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param loadername: give ATET3D or VTK  Default value: 

    :param loaderZoneNames: name of the surface zone from the loader  Default value: []

    :param loaderZones: loaderZones  Default value: []

    :param pointZoneName: list of point zone  Default value: []

    :param pointZones: list of points  Default value: []

    :param trianglesSurf: list of surface triangles  Default value: []

    :param tagSolver: Tag of the Solver Object  Default value: solver

    :param atriumParam: Kat, Pat0, Patm, alpha1, alpha2, tof, tm, tc  Default value: []

    :param aorticParam: Kar, Par0, Pve,tau=Rp*C,Rp,Zc,L  Default value: []

    :param Pv0: minimal Pressure ventricule  Default value: 1000.0

    :param heartPeriod: heart period  Default value: 0.0

    :param file: File name to register pressures  Default value: 

    :param Kiso: parameter K isovolumic  Default value: []

    :param windkessel: which model of windkessel (2,3,4)?  Default value: 0

    :param SurfaceZone: List of triangles on the surface  Default value: []

    :param useProjection: useProjection  Default value: 0

    :param useVerdandi: useVerdandi  Default value: 0

    :param DisableFirstAtriumContraction: DisableFirstAtriumContraction  Default value: 0

    :param ZoneType: Triangles or Points  Default value: 

    :param graphPressure: Pressures per iteration  Default value: 

    :param graphVolume: Volume per iteration  Default value: 

    :param graphFlow: Flow per iteration  Default value: 

    :param volume: Volume.  Default value: 0.0

    :param pressurePv: Pressure Pv  Default value: 0.0

    :param pressurePat: Pressure Pat  Default value: 0.0

    :param pressurePar: Pressure Par  Default value: 0.0

    :param flowQ: Flow Q  Default value: 0.0

    :param displayName: ONLY used for the Cardiac GUI: name displayed in the GUI  Default value: 

    :param BoundaryEdgesPath: Path to the json file containing holes as orderred list of point id pairs  Default value: 

    :param BoundaryEdgesKey: Key (LV|RV) of the ventricle to retrieve edges in json file  Default value: 

    :param edgeInfo: Data to handle topology on edges  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, loadername=loadername, loaderZoneNames=loaderZoneNames, loaderZones=loaderZones, pointZoneName=pointZoneName, pointZones=pointZones, trianglesSurf=trianglesSurf, tagSolver=tagSolver, atriumParam=atriumParam, aorticParam=aorticParam, Pv0=Pv0, heartPeriod=heartPeriod, file=file, Kiso=Kiso, windkessel=windkessel, SurfaceZone=SurfaceZone, useProjection=useProjection, useVerdandi=useVerdandi, DisableFirstAtriumContraction=DisableFirstAtriumContraction, ZoneType=ZoneType, graphPressure=graphPressure, graphVolume=graphVolume, graphFlow=graphFlow, volume=volume, pressurePv=pressurePv, pressurePat=pressurePat, pressurePar=pressurePar, flowQ=flowQ, displayName=displayName, BoundaryEdgesPath=BoundaryEdgesPath, BoundaryEdgesKey=BoundaryEdgesKey, edgeInfo=edgeInfo)
    return "PressureConstraintForceField", params
