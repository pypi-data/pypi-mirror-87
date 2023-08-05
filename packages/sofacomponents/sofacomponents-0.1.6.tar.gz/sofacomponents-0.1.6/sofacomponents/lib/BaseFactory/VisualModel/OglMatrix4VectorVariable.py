# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component OglMatrix4VectorVariable

.. autofunction:: OglMatrix4VectorVariable

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def OglMatrix4VectorVariable(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, id=None, indexShader=None, value=None, transpose=None, **kwargs):
    """
    OglMatrix4VectorVariable


    :param name: object name  Default value: OglMatrix4VectorVariable

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param id: Set an ID name  Default value: 

    :param indexShader: Set the index of the desired shader you want to apply this parameter  Default value: 0

    :param value: Set Uniform Value  Default value: []

    :param transpose: Transpose the matrix (e.g. to use row-dominant matrices in OpenGL  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, id=id, indexShader=indexShader, value=value, transpose=transpose)
    return "OglMatrix4VectorVariable", params
