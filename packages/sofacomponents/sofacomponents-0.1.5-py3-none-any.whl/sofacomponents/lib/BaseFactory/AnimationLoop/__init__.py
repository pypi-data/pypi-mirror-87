# -*- coding: utf-8 -*-


"""
Module AnimationLoop

Content of the module
**********************

Summary:
========
.. autosummary::
     :toctree: _autosummary

    FreeMotionAnimationLoop

    DefaultAnimationLoop

    ConstraintAnimationLoop

    MultiStepAnimationLoop

    MultiTagAnimationLoop



Content:
========

.. automodule::

    FreeMotionAnimationLoop

    DefaultAnimationLoop

    ConstraintAnimationLoop

    MultiStepAnimationLoop

    MultiTagAnimationLoop



Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
# __all__=['FreeMotionAnimationLoop', 'DefaultAnimationLoop', 'ConstraintAnimationLoop', 'MultiStepAnimationLoop', 'MultiTagAnimationLoop']
class AnimationLoop:
    from .FreeMotionAnimationLoop import FreeMotionAnimationLoop
    from .DefaultAnimationLoop import DefaultAnimationLoop
    from .ConstraintAnimationLoop import ConstraintAnimationLoop
    from .MultiStepAnimationLoop import MultiStepAnimationLoop
    from .MultiTagAnimationLoop import MultiTagAnimationLoop
