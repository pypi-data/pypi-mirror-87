# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ShapeMatching

.. autofunction:: ShapeMatching

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ShapeMatching(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, iterations=None, affineRatio=None, fixedweight=None, fixedPosition0=None, fixedPosition=None, position=None, cluster=None, targetPosition=None, **kwargs):
    """
    Compute target positions using shape matching deformation method by Mueller et al.


    :param name: object name  Default value: ShapeMatching

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param iterations: Number of iterations.  Default value: 1

    :param affineRatio: Blending between affine and rigid.  Default value: 0.0

    :param fixedweight: weight of fixed particles.  Default value: 1.0

    :param fixedPosition0: rest positions of non mechanical particles.  Default value: []

    :param fixedPosition: current (fixed) positions of non mechanical particles.  Default value: []

    :param position: Input positions.  Default value: []

    :param cluster: Input clusters.  Default value: []

    :param targetPosition: Computed target positions.  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, iterations=iterations, affineRatio=affineRatio, fixedweight=fixedweight, fixedPosition0=fixedPosition0, fixedPosition=fixedPosition, position=position, cluster=cluster, targetPosition=targetPosition)
    return "ShapeMatching", params
