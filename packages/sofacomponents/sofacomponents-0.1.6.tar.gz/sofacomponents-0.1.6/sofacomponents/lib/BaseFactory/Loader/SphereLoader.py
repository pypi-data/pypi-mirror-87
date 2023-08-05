# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SphereLoader

.. autofunction:: SphereLoader

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SphereLoader(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, position=None, listRadius=None, scale=None, translation=None, **kwargs):
    """
    Loader for sphere model description files


    :param name: object name  Default value: SphereLoader

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Invalid

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param filename: Filename of the object  Default value: 

    :param position: Sphere centers  Default value: []

    :param listRadius: Radius of each sphere  Default value: []

    :param scale: Scale applied to sphere positions & radius  Default value: [[0.0, 0.0, 0.0]]

    :param translation: Translation applied to sphere positions  Default value: [[0.0, 0.0, 0.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, position=position, listRadius=listRadius, scale=scale, translation=translation)
    return "SphereLoader", params
