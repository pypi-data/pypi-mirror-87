# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component VTKExporter

.. autofunction:: VTKExporter

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def VTKExporter(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, XMLformat=None, position=None, edges=None, triangles=None, quads=None, tetras=None, hexas=None, pointsDataFields=None, cellsDataFields=None, exportEveryNumberOfSteps=None, exportAtBegin=None, exportAtEnd=None, overwrite=None, **kwargs):
    """
    Save State vectors from file at each timestep


    :param name: object name  Default value: VTKExporter

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param filename: output VTK file name  Default value: 

    :param XMLformat: Set to true to use XML format  Default value: 1

    :param position: points position (will use points from topology or mechanical state if this is empty)  Default value: []

    :param edges: write edge topology  Default value: 1

    :param triangles: write triangle topology  Default value: 0

    :param quads: write quad topology  Default value: 0

    :param tetras: write tetra topology  Default value: 0

    :param hexas: write hexa topology  Default value: 0

    :param pointsDataFields: Data to visualize (on points)  Default value: []

    :param cellsDataFields: Data to visualize (on cells)  Default value: []

    :param exportEveryNumberOfSteps: export file only at specified number of steps (0=disable)  Default value: 0

    :param exportAtBegin: export file at the initialization  Default value: 0

    :param exportAtEnd: export file when the simulation is finished  Default value: 0

    :param overwrite: overwrite the file, otherwise create a new file at each export, with suffix in the filename  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, XMLformat=XMLformat, position=position, edges=edges, triangles=triangles, quads=quads, tetras=tetras, hexas=hexas, pointsDataFields=pointsDataFields, cellsDataFields=cellsDataFields, exportEveryNumberOfSteps=exportEveryNumberOfSteps, exportAtBegin=exportAtBegin, exportAtEnd=exportAtEnd, overwrite=overwrite)
    return "VTKExporter", params
