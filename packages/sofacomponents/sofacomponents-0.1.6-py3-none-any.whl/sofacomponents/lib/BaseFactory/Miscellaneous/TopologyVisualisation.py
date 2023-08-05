# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TopologyVisualisation

.. autofunction:: TopologyVisualisation

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TopologyVisualisation(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, computeDisplay=None, positions=None, edges=None, triangles=None, tetrahedra=None, numberOfZone=None, drawZones=None, zoneSizes=None, zones=None, numberOfSurfaceZone=None, drawSurfaceZones=None, wireFrame=None, surfaceZoneSizes=None, surfaceZones=None, FiberLength=None, drawFibers=None, nodeFibers=None, drawTetraFibers=None, facetFibers=None, drawTetraBFibers=None, facetBFibers=None, **kwargs):
    """
    Tetrahedron set geometry visualisation


    :param name: object name  Default value: TopologyVisualisation

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param computeDisplay: Debug : recompute display lists.   Default value: 0

    :param positions: Data to handle topology on points  Default value: []

    :param edges: Data to handle topology on points  Default value: []

    :param triangles: Data to handle topology on points  Default value: []

    :param tetrahedra: Data to handle topology on points  Default value: []

    :param numberOfZone: Vertices of the mesh loaded  Default value: 0

    :param drawZones: Debug : allow visualisations for Mesh zones.   Default value: 0

    :param zoneSizes: See zones Size.  Default value: []

    :param zones: See zones Name.  Default value: []

    :param numberOfSurfaceZone: Vertices of the mesh loaded  Default value: 0

    :param drawSurfaceZones: Debug : allow visualisations for Mesh surface zones.   Default value: 0

    :param wireFrame: Debug : allow visualisations for Mesh surface zones in wire frame.   Default value: 0

    :param surfaceZoneSizes: See surface zones Size.  Default value: []

    :param surfaceZones: See surface zones Name.  Default value: []

    :param FiberLength: Debug : Fiber length visualisation.   Default value: 10.0

    :param drawFibers: Debug : Fiber visualisation.   Default value: 0

    :param nodeFibers: Fiber par node of the mesh loaded.  Default value: []

    :param drawTetraFibers: Debug : Tetra Fiber visualisation.   Default value: 0

    :param facetFibers: Fiber par facet of the mesh loaded.  Default value: []

    :param drawTetraBFibers: Debug : Tetra barycentrique Fiber visualisation.   Default value: 0

    :param facetBFibers: Fiber par facet of the mesh loaded, described in barycentric coordinates.  Default value: []


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, computeDisplay=computeDisplay, positions=positions, edges=edges, triangles=triangles, tetrahedra=tetrahedra, numberOfZone=numberOfZone, drawZones=drawZones, zoneSizes=zoneSizes, zones=zones, numberOfSurfaceZone=numberOfSurfaceZone, drawSurfaceZones=drawSurfaceZones, wireFrame=wireFrame, surfaceZoneSizes=surfaceZoneSizes, surfaceZones=surfaceZones, FiberLength=FiberLength, drawFibers=drawFibers, nodeFibers=nodeFibers, drawTetraFibers=drawTetraFibers, facetFibers=facetFibers, drawTetraBFibers=drawTetraBFibers, facetBFibers=facetBFibers)
    return "TopologyVisualisation", params
