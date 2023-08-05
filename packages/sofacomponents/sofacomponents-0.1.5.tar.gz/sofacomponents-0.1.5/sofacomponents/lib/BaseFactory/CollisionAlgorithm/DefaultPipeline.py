# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component DefaultPipeline

.. autofunction:: DefaultPipeline

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def DefaultPipeline(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, verbose=None, draw=None, depth=None, **kwargs):
    """
    The default collision detection and modeling pipeline


    :param name: object name  Default value: DefaultPipeline

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param verbose: Display extra informations at each computation step. (default=false)  Default value: 0

    :param draw: Draw the detected collisions. (default=false)  Default value: 0

    :param depth: Max depth of bounding trees. (default=6, min=?, max=?)  Default value: 6


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, verbose=verbose, draw=draw, depth=depth)
    return "DefaultPipeline", params
