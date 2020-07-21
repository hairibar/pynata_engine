import pygame as pyg
from .collider import Collider


class RectCollider(Collider):
    def __init__(self, gameObject, rect):
        Collider.__init__(self, gameObject)

        self.rect = rect

    def OnRender(self, screen, camera):
        rect = self.GetWorldRect()
        rect = camera.WorldToScreenSpace(rect)
        pyg.draw.rect(screen, (0, 255, 200), rect)

    def __GetLocalPos__(self):
        return pyg.math.Vector2(self.rect.center) - \
            pyg.math.Vector2(self.rect.size) / 2

    def GetWorldRect(self):
        rect = self.rect.copy()
        rect.center = self.__GetWorldPos__()
        return rect
