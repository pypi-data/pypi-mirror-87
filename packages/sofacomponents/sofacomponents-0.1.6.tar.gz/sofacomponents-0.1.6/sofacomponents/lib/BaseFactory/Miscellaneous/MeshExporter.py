# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component MeshExporter

.. autofunction:: MeshExporter

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def MeshExporter(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, saveMesh=None, filename=None, saveFibers=None, **kwargs):
    """
    Export topology and positions into file.   
Supported format are:   
- vtkxml  
- vtk  
- netgen  
- teten  
- gmsh  

Topology exporter


    :param name: object name  Default value: MeshExporter

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param saveMesh: if true save mesh  Default value: 0

    :param filename: output file name. Extension available are atr3D or atet3D  Default value: 

    :param saveFibers: if true save fibers. In the same name as mesh file, with the extension lbb  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, saveMesh=saveMesh, filename=filename, saveFibers=saveFibers)
    return "MeshExporter", params
