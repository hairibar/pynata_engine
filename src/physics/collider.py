import pygame as pyg
from .. import debug_flags as debug
from ..component import Component


class Collider(Component):
    def __init__(self, gameObject, x, y, radius):
        # Parent constructor
        Component.__init__(self, gameObject)

        # Assign to GameObject
        self.gameObject = gameObject
        gameObject.colliders.append(self)

        if debug.DRAW_COLLIDERS:
            gameObject.onRenderListeners.append(self)

        # Assign properties
        self.localPosition = pyg.math.Vector2(x, y)
        self.radius = radius
        

    def IsColliding(self, otherCollider):
        distance = self.__GetWorldPos__().distance_to(
            otherCollider.__GetWorldPos__())
        return distance <= self.radius + otherCollider.radius

    def OnRender(self, screen):
        worldPos = self.__GetWorldPos__()
        pyg.draw.circle(screen, (0, 255, 0),
                        (int(worldPos.x), int(worldPos.y)),
                        int(self.radius), 0)

    def __GetWorldPos__(self):
        return self.gameObject.position + \
            self.localPosition.rotate(-self.gameObject.rotation)
