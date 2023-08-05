# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component GenerateCardiacCylinder

.. autofunction:: GenerateCardiacCylinder

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def GenerateCardiacCylinder(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, output_position=None, tetrahedra=None, radius=None, height=None, origin=None, resCircumferential=None, resRadial=None, resHeight=None, facetFibers=None, depolarisationTimes=None, APD=None, APD_input=None, **kwargs):
    """
    Generate a Cylindrical Tetrahedral Mesh


    :param name: object name  Default value: GenerateCardiacCylinder

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param output_position: output array of 3d points  Default value: []

    :param tetrahedra: output mesh tetrahedra  Default value: []

    :param radius: input cylinder radius  Default value: 0.2

    :param height: input cylinder height  Default value: 1.0

    :param origin: cylinder origin point  Default value: [[0.0, 0.0, 0.0]]

    :param resCircumferential: Resolution in the circumferential direction  Default value: 6

    :param resRadial: Resolution in the radial direction  Default value: 3

    :param resHeight: Resolution in the height direction  Default value: 5

    :param facetFibers: Fiber par facet of the mesh loaded.  Default value: []

    :param depolarisationTimes: depolarisationTimes at each node  Default value: []

    :param APD: APD at each node  Default value: []

    :param APD_input: Action potential duration given as input  Default value: 0.2


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, output_position=output_position, tetrahedra=tetrahedra, radius=radius, height=height, origin=origin, resCircumferential=resCircumferential, resRadial=resRadial, resHeight=resHeight, facetFibers=facetFibers, depolarisationTimes=depolarisationTimes, APD=APD, APD_input=APD_input)
    return "GenerateCardiacCylinder", params
