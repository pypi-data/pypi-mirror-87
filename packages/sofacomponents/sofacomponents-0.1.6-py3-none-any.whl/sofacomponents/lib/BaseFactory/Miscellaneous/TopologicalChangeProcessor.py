# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TopologicalChangeProcessor

.. autofunction:: TopologicalChangeProcessor

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TopologicalChangeProcessor(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, filename=None, listChanges=None, interval=None, shift=None, loop=None, useDataInputs=None, timeToRemove=None, edgesToRemove=None, trianglesToRemove=None, quadsToRemove=None, tetrahedraToRemove=None, hexahedraToRemove=None, saveIndicesAtInit=None, epsilonSnapPath=None, epsilonSnapBorder=None, draw=None, **kwargs):
    """
    Read topological Changes and process them.


    :param name: object name  Default value: TopologicalChangeProcessor

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param filename: input file name for topological changes.  Default value: 

    :param listChanges: 0 for adding, 1 for removing, 2 for cutting and associated indices.  Default value: []

    :param interval: time duration between 2 actions  Default value: 0.0

    :param shift: shift between times in the file and times when they will be read  Default value: 0.0

    :param loop: set to 'true' to re-read the file when reaching the end  Default value: 0

    :param useDataInputs: If true, will perform operation using Data input lists rather than text file.  Default value: 0

    :param timeToRemove: If using option useDataInputs, time at which will be done the operations. Possibility to use the interval Data also.  Default value: 0.0

    :param edgesToRemove: List of edge IDs to be removed.  Default value: []

    :param trianglesToRemove: List of triangle IDs to be removed.  Default value: []

    :param quadsToRemove: List of quad IDs to be removed.  Default value: []

    :param tetrahedraToRemove: List of tetrahedron IDs to be removed.  Default value: []

    :param hexahedraToRemove: List of hexahedron IDs to be removed.  Default value: []

    :param saveIndicesAtInit: set to 'true' to save the incision to do in the init to incise even after a movement  Default value: 0

    :param epsilonSnapPath: epsilon snap path  Default value: 0.1

    :param epsilonSnapBorder: epsilon snap path  Default value: 0.25

    :param draw: draw information  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, filename=filename, listChanges=listChanges, interval=interval, shift=shift, loop=loop, useDataInputs=useDataInputs, timeToRemove=timeToRemove, edgesToRemove=edgesToRemove, trianglesToRemove=trianglesToRemove, quadsToRemove=quadsToRemove, tetrahedraToRemove=tetrahedraToRemove, hexahedraToRemove=hexahedraToRemove, saveIndicesAtInit=saveIndicesAtInit, epsilonSnapPath=epsilonSnapPath, epsilonSnapBorder=epsilonSnapBorder, draw=draw)
    return "TopologicalChangeProcessor", params
