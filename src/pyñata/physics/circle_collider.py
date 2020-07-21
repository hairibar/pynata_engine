import pygame as pyg
from .collider import Collider


class CircleCollider(Collider):
    def __init__(self, gameObject, x, y, radius):
        Collider.__init__(self, gameObject)

        self.localPosition = pyg.math.Vector2(x, y)
        self.radius = radius

    def OnRender(self, screen, camera):
        position = self.__GetWorldPos__()
        position = camera.WorldToScreenSpace(position)
        pyg.draw.circle(screen, (0, 255, 0),
                        (int(position.x), int(position.y)),
                        int(self.radius), 0)

    def __GetLocalPos__(self):
        return self.localPosition
