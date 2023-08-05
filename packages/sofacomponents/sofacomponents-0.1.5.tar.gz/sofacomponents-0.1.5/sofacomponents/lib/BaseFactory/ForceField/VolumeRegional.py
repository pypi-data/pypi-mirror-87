# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component VolumeRegional

.. autofunction:: VolumeRegional

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def VolumeRegional(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, meshA=None, observation=None, sizemin=None, exception=None, volume=None, file=None, **kwargs):
    """
    PressureConstraint's law in Tetrahedral finite elements


    :param name: object name  Default value: VolumeRegional

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param meshA: give mesh with AHA surf zones  Default value: 

    :param observation: give 0 for LV_endo, 1 for LVepi, 2 for LV, 3 for RV, 4 for Total  Default value: 0

    :param sizemin: number of triangles minumum per zones  Default value: 0

    :param exception: exception  Default value: 0

    :param volume: ..  Default value: []

    :param file: file  Default value: 


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, meshA=meshA, observation=observation, sizemin=sizemin, exception=exception, volume=volume, file=file)
    return "VolumeRegional", params
