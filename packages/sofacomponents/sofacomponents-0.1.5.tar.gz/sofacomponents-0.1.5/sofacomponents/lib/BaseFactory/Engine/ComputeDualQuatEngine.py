# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component ComputeDualQuatEngine

.. autofunction:: ComputeDualQuatEngine

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def ComputeDualQuatEngine(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, x0=None, x=None, dualQuats=None, **kwargs):
    """
    Converts a vector of Affine or Rigid to a vector of Dual Quaternions.


    :param name: object name  Default value: ComputeDualQuatEngine

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param x0: Rest position  Default value: []

    :param x: Current position  Default value: []

    :param dualQuats: Dual quaternions, computed from x (or x*x0^-1 if x0 is provided). DualQuats are stored as two vec4f elements, first the orientation, then the dual.  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, x0=x0, x=x, dualQuats=dualQuats)
    return "ComputeDualQuatEngine", params
