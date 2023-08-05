# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component CardiacSimulationExporter

.. autofunction:: CardiacSimulationExporter

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def CardiacSimulationExporter(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, depolarizationTime=None, localMeasurementPoints=None, Filename=None, ExportSeparateFiles=None, ExportStartStep=None, ExportFileType=None, ExportEveryNSteps=None, ExportDepolarizationTime=None, ExportDepolarizationTimeOnce=None, ExportAPD=None, ExportElapsedTime=None, ExportEc=None, ExportE1d=None, ExportSigmaC=None, ExportScale=None, Potential=None, Points=None, Edges=None, Triangles=None, Quads=None, Tetras=None, Hexas=None, RightVolume=None, LeftVolume=None, RightPressurePv=None, LeftPressurePv=None, RightPressurePat=None, LeftPressurePat=None, RightPressurePar=None, LeftPressurePar=None, RightFlowQ=None, LeftFlowQ=None, APD90=None, stopDepolarizationTime=None, **kwargs):
    """
    Export cardiac information to file at the given time steps.


    :param name: object name  Default value: CardiacSimulationExporter

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param depolarizationTime: Time of depolarization for each point  Default value: []

    :param localMeasurementPoints: Optional vector containing the ids 
 of the local points that are 
 studied for depolarization  Default value: []

    :param Filename: Filename  Default value: 

    :param ExportSeparateFiles: True if each type of data is to be exported in its own file  Default value: 0

    :param ExportStartStep: The step at which exporting begins.  Default value: 0

    :param ExportFileType: Export File Type  Default value: 

    :param ExportEveryNSteps: Export a file every N steps  Default value: 0

    :param ExportDepolarizationTime: True if the depolarization times are to be exported.  Default value: 0

    :param ExportDepolarizationTimeOnce: True if the depolarization time is to be exported separately once at the end of calculation.  Default value: 0

    :param ExportAPD: True if the APD is to be exported.  Default value: 0

    :param ExportElapsedTime: True if the overall time elapsed and the time for N steps to elapse is exported.  Default value: 0

    :param ExportEc: ExportEc.  Default value: 0

    :param ExportE1d: ExportE1d.  Default value: 0

    :param ExportSigmaC: ExportSigmaC.  Default value: 0

    :param ExportScale: Scale the MechanicalState by the given value.  Default value: 1.0

    :param Potential: Electric Potential  Default value: []

    :param Points: Point data  Default value: 1

    :param Edges: Edge Data  Default value: 0

    :param Triangles: Triangle Data  Default value: 0

    :param Quads: Quad Data  Default value: 0

    :param Tetras: Tetra Data  Default value: 0

    :param Hexas: Hexa Data  Default value: 0

    :param RightVolume: Right Volume  Default value: 0.0

    :param LeftVolume: Left Volume  Default value: 0.0

    :param RightPressurePv: Right Pressure Pv  Default value: 0.0

    :param LeftPressurePv: Left Pressure Pv  Default value: 0.0

    :param RightPressurePat: Right Pressure Pat  Default value: 0.0

    :param LeftPressurePat: Left Pressure Pat  Default value: 0.0

    :param RightPressurePar: Left Pressure Par  Default value: 0.0

    :param LeftPressurePar: Left Pressure Par  Default value: 0.0

    :param RightFlowQ: Right Flow Q  Default value: 0.0

    :param LeftFlowQ: Left Flow Q  Default value: 0.0

    :param APD90: Action Potential Duration 90%  Default value: []

    :param stopDepolarizationTime: Time at which the depolarization times should all be computed.  Default value: -1.0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, depolarizationTime=depolarizationTime, localMeasurementPoints=localMeasurementPoints, Filename=Filename, ExportSeparateFiles=ExportSeparateFiles, ExportStartStep=ExportStartStep, ExportFileType=ExportFileType, ExportEveryNSteps=ExportEveryNSteps, ExportDepolarizationTime=ExportDepolarizationTime, ExportDepolarizationTimeOnce=ExportDepolarizationTimeOnce, ExportAPD=ExportAPD, ExportElapsedTime=ExportElapsedTime, ExportEc=ExportEc, ExportE1d=ExportE1d, ExportSigmaC=ExportSigmaC, ExportScale=ExportScale, Potential=Potential, Points=Points, Edges=Edges, Triangles=Triangles, Quads=Quads, Tetras=Tetras, Hexas=Hexas, RightVolume=RightVolume, LeftVolume=LeftVolume, RightPressurePv=RightPressurePv, LeftPressurePv=LeftPressurePv, RightPressurePat=RightPressurePat, LeftPressurePat=LeftPressurePat, RightPressurePar=RightPressurePar, LeftPressurePar=LeftPressurePar, RightFlowQ=RightFlowQ, LeftFlowQ=LeftFlowQ, APD90=APD90, stopDepolarizationTime=stopDepolarizationTime)
    return "CardiacSimulationExporter", params
