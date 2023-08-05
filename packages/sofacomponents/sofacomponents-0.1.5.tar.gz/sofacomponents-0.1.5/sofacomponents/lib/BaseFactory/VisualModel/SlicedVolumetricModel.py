# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SlicedVolumetricModel

.. autofunction:: SlicedVolumetricModel

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SlicedVolumetricModel(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, alpha=None, color=None, nbSlices=None, **kwargs):
    """
    A simple visualization for a cloud of points.


    :param name: object name  Default value: SlicedVolumetricModel

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param alpha: Opacity of the billboards. 1.0 is 100% opaque.  Default value: 0.20000000298

    :param color: Billboard color.(default=1.0,1.0,1.0,1.0)  Default value: [[1.0, 1.0, 1.0, 1.0]]

    :param nbSlices: Number of billboards.  Default value: 100


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, alpha=alpha, color=color, nbSlices=nbSlices)
    return "SlicedVolumetricModel", params
