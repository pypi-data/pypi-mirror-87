# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component OglTexturePointer

.. autofunction:: OglTexturePointer

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def OglTexturePointer(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, id=None, indexShader=None, textureUnit=None, enabled=None, **kwargs):
    """
    OglTexturePointer


    :param name: object name  Default value: OglTexturePointer

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param id: Set an ID name  Default value: 

    :param indexShader: Set the index of the desired shader you want to apply this parameter  Default value: 0

    :param textureUnit: Set the texture unit  Default value: 1

    :param enabled: enabled ?  Default value: 1


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, id=id, indexShader=indexShader, textureUnit=textureUnit, enabled=enabled)
    return "OglTexturePointer", params
