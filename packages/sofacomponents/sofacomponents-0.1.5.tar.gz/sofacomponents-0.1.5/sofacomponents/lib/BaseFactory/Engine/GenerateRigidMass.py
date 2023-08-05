# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component GenerateRigidMass

.. autofunction:: GenerateRigidMass

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def GenerateRigidMass(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, density=None, position=None, triangles=None, quads=None, polygons=None, rigidMass=None, mass=None, volume=None, inertiaMatrix=None, massCenter=None, centerToOrigin=None, **kwargs):
    """
    An engine computing the RigidMass of a mesh : mass, volume and inertia matrix.


    :param name: object name  Default value: GenerateRigidMass

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param density: input: Density of the object  Default value: 1000.0

    :param position: input: positions of the vertices  Default value: []

    :param triangles: input: triangles of the mesh  Default value: []

    :param quads: input: quads of the mesh  Default value: []

    :param polygons: input: polygons of the mesh  Default value: []

    :param rigidMass: output: rigid mass computed  Default value: 1 1 [1 0 0,0 1 0,0 0 1]

    :param mass: output: mass of the mesh  Default value: 0.0

    :param volume: output: volume of the mesh  Default value: 0.0

    :param inertiaMatrix: output: the inertia matrix of the mesh  Default value: [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

    :param massCenter: output: the gravity center of the mesh  Default value: [[0.0, 0.0, 0.0]]

    :param centerToOrigin: output: vector going from the mass center to the space origin  Default value: [[0.0, 0.0, 0.0]]


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, density=density, position=position, triangles=triangles, quads=quads, polygons=polygons, rigidMass=rigidMass, mass=mass, volume=volume, inertiaMatrix=inertiaMatrix, massCenter=massCenter, centerToOrigin=centerToOrigin)
    return "GenerateRigidMass", params
