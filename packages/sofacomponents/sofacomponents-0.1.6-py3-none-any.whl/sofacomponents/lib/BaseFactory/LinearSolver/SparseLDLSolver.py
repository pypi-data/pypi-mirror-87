# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component SparseLDLSolver

.. autofunction:: SparseLDLSolver

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def SparseLDLSolver(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, savingMatrixToFile=None, savingFilename=None, savingPrecision=None, **kwargs):
    """
    Direct Linear Solver using a Sparse LDL^T factorization.


    :param name: object name  Default value: SparseLDLSolver

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param savingMatrixToFile: save matrix to a text file (can be very slow, as full matrix is stored  Default value: 0

    :param savingFilename: Name of file where system matrix (mass, stiffness and damping) will be stored.  Default value: MatrixInLDL_%04d.txt

    :param savingPrecision: Number of digits used to store system's matrix. Default is 6.  Default value: 6


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, savingMatrixToFile=savingMatrixToFile, savingFilename=savingFilename, savingPrecision=savingPrecision)
    return "SparseLDLSolver", params
