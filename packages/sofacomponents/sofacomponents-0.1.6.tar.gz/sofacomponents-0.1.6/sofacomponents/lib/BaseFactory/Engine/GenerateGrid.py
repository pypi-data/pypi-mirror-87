# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component GenerateGrid

.. autofunction:: GenerateGrid

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def GenerateGrid(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, output_position=None, tetrahedra=None, quads=None, triangles=None, hexahedra=None, min=None, max=None, resolution=None, **kwargs):
    """
    Generate a Grid Tetrahedral or Hexahedral Mesh


    :param name: object name  Default value: GenerateGrid

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param output_position: output array of 3d points  Default value: []

    :param tetrahedra: output mesh tetrahedra  Default value: []

    :param quads: output mesh quads  Default value: []

    :param triangles: output mesh triangles  Default value: []

    :param hexahedra: output mesh hexahedra  Default value: []

    :param min: the 3 coordinates of the minimum corner  Default value: [[0.0, 0.0, 0.0]]

    :param max: the 3 coordinates of the maximum corner  Default value: [[0.0, 0.0, 0.0]]

    :param resolution: the number of cubes in the x,y,z directions. If resolution in the z direction is  0 then a 2D grid is generated  Default value: [[3, 3, 3]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, output_position=output_position, tetrahedra=tetrahedra, quads=quads, triangles=triangles, hexahedra=hexahedra, min=min, max=max, resolution=resolution)
    return "GenerateGrid", params
