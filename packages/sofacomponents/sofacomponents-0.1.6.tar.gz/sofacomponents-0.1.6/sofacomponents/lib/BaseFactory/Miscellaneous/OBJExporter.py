# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component OBJExporter

.. autofunction:: OBJExporter

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def OBJExporter(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, exportEveryNumberOfSteps=None, exportAtBegin=None, exportAtEnd=None, enable=None, **kwargs):
    """
    Export the scene under the Wavefront OBJ format.When several frames are exported the file name have the following pattern: outfile000.obj outfile001.obj.


    :param name: object name  Default value: OBJExporter

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param filename: Path or filename where to export the data.  If missing the name of the component is used.  Default value: 

    :param exportEveryNumberOfSteps: export file only at specified number of steps (0=disable, default=0)  Default value: 0

    :param exportAtBegin: export file at the initialization (default=false)  Default value: 0

    :param exportAtEnd: export file when the simulation is finished (default=false)  Default value: 0

    :param enable: Enable or disable the component. (default=true)  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, exportEveryNumberOfSteps=exportEveryNumberOfSteps, exportAtBegin=exportAtBegin, exportAtEnd=exportAtEnd, enable=enable)
    return "OBJExporter", params
