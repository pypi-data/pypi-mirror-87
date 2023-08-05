# -*- coding: utf-8 -*-

from sofacomponents.lib.base_component import sofa_component


"""
Component CapsuleCollisionModel

.. autofunction:: CapsuleCollisionModel

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


@sofa_component
def CapsuleCollisionModel(self, name=None, printLog=None, tags=None, bbox=None, componentState=None, listening=None, active=None, moving=None, simulated=None, selfCollision=None, proximity=None, contactStiffness=None, contactFriction=None, contactRestitution=None, contactResponse=None, color=None, group=None, listCapsuleRadii=None, defaultRadius=None, **kwargs):
    """
    Collision model which represents a set of Capsules
Collision model which represents a set of rigid capsules


    :param name: object name  Default value: CapsuleCollisionModel

    :param printLog: if true, emits extra messages at runtime.  Default value: 0

    :param tags: list of the subsets the objet belongs to  Default value: []

    :param bbox: this object bounding box  Default value: [[1.7976931348623157e+308, 1.7976931348623157e+308, 1.7976931348623157e+308], [-1.7976931348623157e+308, -1.7976931348623157e+308, -1.7976931348623157e+308]]

    :param componentState: The state of the component among (Dirty, Valid, Undefined, Loading, Invalid).  Default value: Undefined

    :param listening: if true, handle the events, otherwise ignore the events  Default value: 0

    :param active: flag indicating if this collision model is active and should be included in default collision detections  Default value: 1

    :param moving: flag indicating if this object is changing position between iterations  Default value: 1

    :param simulated: flag indicating if this object is controlled by a simulation  Default value: 1

    :param selfCollision: flag indication if the object can self collide  Default value: 0

    :param proximity: Distance to the actual (visual) surface  Default value: 0.0

    :param contactStiffness: Contact stiffness  Default value: 10.0

    :param contactFriction: Contact friction coefficient (dry or viscous or unused depending on the contact method)  Default value: 0.0

    :param contactRestitution: Contact coefficient of restitution  Default value: 0.0

    :param contactResponse: if set, indicate to the ContactManager that this model should use the given class of contacts.
Note that this is only indicative, and in particular if both collision models specify a different class it is up to the manager to choose.  Default value: 

    :param color: color used to display the collision model if requested  Default value: [[1.0, 0.0, 0.0, 1.0]]

    :param group: IDs of the groups containing this model. No collision can occur between collision models included in a common group (e.g. allowing the same object to have multiple collision models)  Default value: []

    :param listCapsuleRadii: Radius of each capsule  Default value: []

    :param defaultRadius: The default radius  Default value: 0.5


    """
    params = dict(name=name, printLog=printLog, tags=tags, bbox=bbox, componentState=componentState, listening=listening, active=active, moving=moving, simulated=simulated, selfCollision=selfCollision, proximity=proximity, contactStiffness=contactStiffness, contactFriction=contactFriction, contactRestitution=contactRestitution, contactResponse=contactResponse, color=color, group=group, listCapsuleRadii=listCapsuleRadii, defaultRadius=defaultRadius)
    return "CapsuleCollisionModel", params
