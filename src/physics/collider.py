from ... import debug_flags as debug
from ..component import Component
from . import __collisions__ as collisions


class Collider(Component):
    def __init__(self, gameObject):
        # Parent constructor
        Component.__init__(self, gameObject)

        # Assign to GameObject
        self.gameObject = gameObject
        gameObject.colliders.append(self)

        if debug.DRAW_COLLIDERS:
            gameObject.onRenderListeners.append(self)

    def IsColliding(self, otherCollider):
        return collisions.CheckCollision(self, otherCollider)

    def __GetWorldPos__(self):
        return self.gameObject.position + \
            self.__GetLocalPos__().rotate(-self.gameObject.rotation)
