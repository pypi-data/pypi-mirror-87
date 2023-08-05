# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component VoxelGridLoader

.. autofunction:: VoxelGridLoader

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def VoxelGridLoader(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, position=None, hexahedra=None, voxelSize=None, resolution=None, ROI=None, header=None, segmentationHeader=None, idxInRegularGrid=None, bgValue=None, dataValue=None, generateHexa=None, **kwargs):
    """
    Voxel loader based on RAW files


    :param name: object name  Default value: VoxelGridLoader

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Invalid

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param filename: Filename of the object  Default value: 

    :param position: Coordinates of the nodes loaded  Default value: []

    :param hexahedra: Hexahedra loaded  Default value: []

    :param voxelSize: Dimension of one voxel  Default value: [[1.0, 1.0, 1.0]]

    :param resolution: Resolution of the voxel file  Default value: [[0, 0, 0]]

    :param ROI: Region of interest (xmin, ymin, zmin, xmax, ymax, zmax)  Default value: [[0, 0, 0, 65535, 65535, 65535]]

    :param header: Header size in bytes  Default value: 0

    :param segmentationHeader: Header size in bytes  Default value: 0

    :param idxInRegularGrid: indices of the hexa in the grid.  Default value: []

    :param bgValue: Background values (to be ignored)  Default value: []

    :param dataValue: Active data values  Default value: []

    :param generateHexa: Interpret voxel as either hexa or points  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, position=position, hexahedra=hexahedra, voxelSize=voxelSize, resolution=resolution, ROI=ROI, header=header, segmentationHeader=segmentationHeader, idxInRegularGrid=idxInRegularGrid, bgValue=bgValue, dataValue=dataValue, generateHexa=generateHexa)
    return "VoxelGridLoader", params
