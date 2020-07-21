import pygame as pyg
from .. import env


class Camera:
    def __init__(self):
        self.position = pyg.math.Vector2(0, 0)
        self.cameraRect = pyg.Rect(
            pyg.math.Vector2(0, 0), env.game.SCREEN_SIZE)

    def WorldToScreenSpace(self, a):
        if isinstance(a, pyg.math.Vector2):
            return a + self.__GetWorldToScreenOffset__()
        elif isinstance(a, pyg.Rect):
            return a.move(self.__GetWorldToScreenOffset__())

    def ScreenToWorldSpace(self, a):
        if isinstance(a, pyg.math.Vector2):
            return a - self.__GetWorldToScreenOffset__()
        elif isinstance(a, pyg.Rect):
            return a.move(-self.__GetWorldToScreenOffset__())

    def __GetWorldToScreenOffset__(self):
        return pyg.math.Vector2(-self.position.x, -self.position.y) \
            + env.game.SCREEN_SIZE / 2

    def IsOnScreen(self, screenSpaceRect):
        return self.cameraRect.colliderect(screenSpaceRect)
