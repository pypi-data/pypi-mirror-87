# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ExtraMonitor

.. autofunction:: ExtraMonitor

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ExtraMonitor(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, indices=None, ExportPositions=None, ExportVelocities=None, ExportForces=None, showPositions=None, PositionsColor=None, showVelocities=None, VelocitiesColor=None, showForces=None, ForcesColor=None, showMinThreshold=None, showTrajectories=None, TrajectoriesPrecision=None, TrajectoriesColor=None, sizeFactor=None, fileName=None, ExportWcin=None, ExportWext=None, resultantF=None, minCoord=None, maxCoord=None, dispCoord=None, **kwargs):
    """
    Monitoring of particles
Monitoring of particles
Monitoring of particles


    :param name: object name  Default value: ExtraMonitor

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param indices: MechanicalObject points indices to monitor  Default value: []

    :param ExportPositions: export Monitored positions as gnuplot file  Default value: 0

    :param ExportVelocities: export Monitored velocities as gnuplot file  Default value: 0

    :param ExportForces: export Monitored forces as gnuplot file  Default value: 0

    :param showPositions: see the Monitored positions  Default value: 0

    :param PositionsColor: define the color of positions  Default value: [[1.0, 1.0, 0.0, 1.0]]

    :param showVelocities: see the Monitored velocities  Default value: 0

    :param VelocitiesColor: define the color of velocities  Default value: [[1.0, 1.0, 0.0, 1.0]]

    :param showForces: see the Monitored forces  Default value: 0

    :param ForcesColor: define the color of forces  Default value: [[1.0, 1.0, 0.0, 1.0]]

    :param showMinThreshold: under this value, vectors are not represented  Default value: 0.01

    :param showTrajectories: print the trajectory of Monitored particles  Default value: 0

    :param TrajectoriesPrecision: set the dt between to save of positions  Default value: 0.1

    :param TrajectoriesColor: define the color of the trajectories  Default value: [[1.0, 1.0, 0.0, 1.0]]

    :param sizeFactor: factor to multiply to arrows  Default value: 1.0

    :param fileName: name of the plot files to be generated  Default value: 

    :param ExportWcin: export Wcin of the monitored dofs as gnuplot file  Default value: 0

    :param ExportWext: export Wext of the monitored dofs as gnuplot file  Default value: 0

    :param resultantF: export force resultant of the monitored dofs as gnuplot file instead of all dofs  Default value: 1

    :param minCoord: export minimum displacement on the given coordinate as gnuplot file instead of positions of all dofs  Default value: -1

    :param maxCoord: export minimum displacement on the given coordinate as gnuplot file instead of positions of all dofs  Default value: -1

    :param dispCoord: export displacement on the given coordinate as gnuplot file  Default value: -1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, indices=indices, ExportPositions=ExportPositions, ExportVelocities=ExportVelocities, ExportForces=ExportForces, showPositions=showPositions, PositionsColor=PositionsColor, showVelocities=showVelocities, VelocitiesColor=VelocitiesColor, showForces=showForces, ForcesColor=ForcesColor, showMinThreshold=showMinThreshold, showTrajectories=showTrajectories, TrajectoriesPrecision=TrajectoriesPrecision, TrajectoriesColor=TrajectoriesColor, sizeFactor=sizeFactor, fileName=fileName, ExportWcin=ExportWcin, ExportWext=ExportWext, resultantF=resultantF, minCoord=minCoord, maxCoord=maxCoord, dispCoord=dispCoord)
    return "ExtraMonitor", params
