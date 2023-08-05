# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TopologyGaussPointSampler

.. autofunction:: TopologyGaussPointSampler

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TopologyGaussPointSampler(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, method=None, position=None, transforms=None, order=None, volume=None, showSamplesScale=None, drawMode=None, showIndicesScale=None, inPosition=None, cell=None, indices=None, orientation=None, useLocalOrientation=None, fineVolumes=None, **kwargs):
    """
    Samples an object represented by a mesh


    :param name: object name  Default value: TopologyGaussPointSampler

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param method: quadrature method  Default value: 0 - Gauss-Legendre

    :param position: output sample positions  Default value: []

    :param transforms: output sample orientations  Default value: []

    :param order: order of quadrature method  Default value: 1

    :param volume: output weighted volume  Default value: []

    :param showSamplesScale: show samples scale  Default value: 0.0

    :param drawMode: 0: Green points; 1: Green spheres  Default value: 0

    :param showIndicesScale: show indices scale  Default value: 0.0

    :param inPosition: input node positions  Default value: []

    :param cell: cell index associated with each sample  Default value: []

    :param indices: list of cells where sampling is performed (all by default)  Default value: []

    :param orientation: input orientation (Euler angles) inside each cell  Default value: []

    :param useLocalOrientation: tells if orientations are defined in the local basis on each cell  Default value: 0

    :param fineVolumes: input cell volumes (typically computed from a fine model)  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, method=method, position=position, transforms=transforms, order=order, volume=volume, showSamplesScale=showSamplesScale, drawMode=drawMode, showIndicesScale=showIndicesScale, inPosition=inPosition, cell=cell, indices=indices, orientation=orientation, useLocalOrientation=useLocalOrientation, fineVolumes=fineVolumes)
    return "TopologyGaussPointSampler", params
