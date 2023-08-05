# -*- coding: utf-8 -*-


"""
Module CollisionModel

Content of the module
**********************

Summary:
========
.. autosummary::
     :toctree: _autosummary

    LineCollisionModel

    TetrahedronCollisionModel

    SphereCollisionModel

    TriangleOctreeModel

    CapsuleCollisionModel

    TriangleModelInRegularGrid

    CylinderCollisionModel

    TriangleCollisionModel

    PointCollisionModel

    CubeCollisionModel

    RayCollisionModel



Content:
========

.. automodule::

    LineCollisionModel

    TetrahedronCollisionModel

    SphereCollisionModel

    TriangleOctreeModel

    CapsuleCollisionModel

    TriangleModelInRegularGrid

    CylinderCollisionModel

    TriangleCollisionModel

    PointCollisionModel

    CubeCollisionModel

    RayCollisionModel



Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
# __all__=['LineCollisionModel', 'TetrahedronCollisionModel', 'SphereCollisionModel', 'TriangleOctreeModel', 'CapsuleCollisionModel', 'TriangleModelInRegularGrid', 'CylinderCollisionModel', 'TriangleCollisionModel', 'PointCollisionModel', 'CubeCollisionModel', 'RayCollisionModel']
class CollisionModel:
    from .LineCollisionModel import LineCollisionModel
    from .TetrahedronCollisionModel import TetrahedronCollisionModel
    from .SphereCollisionModel import SphereCollisionModel
    from .TriangleOctreeModel import TriangleOctreeModel
    from .CapsuleCollisionModel import CapsuleCollisionModel
    from .TriangleModelInRegularGrid import TriangleModelInRegularGrid
    from .CylinderCollisionModel import CylinderCollisionModel
    from .TriangleCollisionModel import TriangleCollisionModel
    from .PointCollisionModel import PointCollisionModel
    from .CubeCollisionModel import CubeCollisionModel
    from .RayCollisionModel import RayCollisionModel
