# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component BlenderExporter

.. autofunction:: BlenderExporter

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def BlenderExporter(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, path=None, baseName=None, simulationType=None, step=None, nbPtsByHair=None, **kwargs):
    """
    Export the simulation result as blender point cache files


    :param name: object name  Default value: BlenderExporter

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param path: output path  Default value: 

    :param baseName: Base name for the output files  Default value: 

    :param simulationType: simulation type (0: soft body, 1: particles, 2:cloth, 3:hair)  Default value: 0

    :param step: save the  simulation result every step frames  Default value: 2

    :param nbPtsByHair: number of element by hair strand  Default value: 20


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, path=path, baseName=baseName, simulationType=simulationType, step=step, nbPtsByHair=nbPtsByHair)
    return "BlenderExporter", params
