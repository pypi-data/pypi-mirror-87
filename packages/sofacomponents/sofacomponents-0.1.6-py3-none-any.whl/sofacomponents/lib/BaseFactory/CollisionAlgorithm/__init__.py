# -*- coding: utf-8 -*-


"""
Module CollisionAlgorithm

Content of the module
**********************

Summary:
========
.. autosummary::
     :toctree: _autosummary

    DirectSAP

    IncrSAP

    DefaultCollisionGroupManager

    DiscreteIntersection

    NewProximityIntersection

    MinProximityIntersection

    RayTraceDetection

    BruteForceDetection

    LMDNewProximityIntersection

    LocalMinDistance

    DefaultPipeline

    RuleBasedContactManager

    DefaultContactManager



Content:
========

.. automodule::

    DirectSAP

    IncrSAP

    DefaultCollisionGroupManager

    DiscreteIntersection

    NewProximityIntersection

    MinProximityIntersection

    RayTraceDetection

    BruteForceDetection

    LMDNewProximityIntersection

    LocalMinDistance

    DefaultPipeline

    RuleBasedContactManager

    DefaultContactManager



Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
# __all__=['DirectSAP', 'IncrSAP', 'DefaultCollisionGroupManager', 'DiscreteIntersection', 'NewProximityIntersection', 'MinProximityIntersection', 'RayTraceDetection', 'BruteForceDetection', 'LMDNewProximityIntersection', 'LocalMinDistance', 'DefaultPipeline', 'RuleBasedContactManager', 'DefaultContactManager']
class CollisionAlgorithm:
    from .DirectSAP import DirectSAP
    from .IncrSAP import IncrSAP
    from .DefaultCollisionGroupManager import DefaultCollisionGroupManager
    from .DiscreteIntersection import DiscreteIntersection
    from .NewProximityIntersection import NewProximityIntersection
    from .MinProximityIntersection import MinProximityIntersection
    from .RayTraceDetection import RayTraceDetection
    from .BruteForceDetection import BruteForceDetection
    from .LMDNewProximityIntersection import LMDNewProximityIntersection
    from .LocalMinDistance import LocalMinDistance
    from .DefaultPipeline import DefaultPipeline
    from .RuleBasedContactManager import RuleBasedContactManager
    from .DefaultContactManager import DefaultContactManager
