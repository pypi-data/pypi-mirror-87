# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component OglCylinderModel

.. autofunction:: OglCylinderModel

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def OglCylinderModel(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, position=None, restPosition=None, normal=None, radius=None, color=None, edges=None, **kwargs):
    """
    A simple visualization for set of cylinder.


    :param name: object name  Default value: OglCylinderModel

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param position: Vertices coordinates  Default value: []

    :param restPosition: Vertices rest coordinates  Default value: []

    :param normal: Normals of the model  Default value: []

    :param radius: Radius of the cylinder.  Default value: 1.0

    :param color: Color of the cylinders.  Default value: [[1.0, 1.0, 1.0, 1.0]]

    :param edges: List of edge indices  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, position=position, restPosition=restPosition, normal=normal, radius=radius, color=color, edges=edges)
    return "OglCylinderModel", params
