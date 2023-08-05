# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component TetrahedronDiffusionFEMForceField

.. autofunction:: TetrahedronDiffusionFEMForceField

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def TetrahedronDiffusionFEMForceField(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, isCompliance=None, rayleighStiffness=None, constantDiffusionCoefficient=None, tetraDiffusionCoefficient=None, scalarDiffusion=None, anisotropyRatio=None, transverseAnisotropyArray=None, tagMechanics=None, drawConduc=None, **kwargs):
    """
    Isotropic or anisotropic diffusion on Tetrahedral Meshes


    :param name: object name  Default value: TetrahedronDiffusionFEMForceField

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 1

    :param isCompliance: Consider the component as a compliance, else as a stiffness  Default value: 0

    :param rayleighStiffness: Rayleigh damping - stiffness matrix coefficient  Default value: 0.0

    :param constantDiffusionCoefficient: Constant diffusion coefficient  Default value: 1.0

    :param tetraDiffusionCoefficient: Diffusion coefficient for each tetrahedron, by default equal to constantDiffusionCoefficient.  Default value: []

    :param scalarDiffusion: if true, diffuse only on the first dimension.  Default value: 0

    :param anisotropyRatio: Anisotropy ratio (r²>1).
 Default is 1.0 = isotropy.  Default value: 1.0

    :param transverseAnisotropyArray: Data to handle topology on tetrahedra  Default value: []

    :param tagMechanics: Tag of the Mechanical Object.  Default value: meca

    :param drawConduc: To display conductivity map.  Default value: 0


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, isCompliance=isCompliance, rayleighStiffness=rayleighStiffness, constantDiffusionCoefficient=constantDiffusionCoefficient, tetraDiffusionCoefficient=tetraDiffusionCoefficient, scalarDiffusion=scalarDiffusion, anisotropyRatio=anisotropyRatio, transverseAnisotropyArray=transverseAnisotropyArray, tagMechanics=tagMechanics, drawConduc=drawConduc)
    return "TetrahedronDiffusionFEMForceField", params
