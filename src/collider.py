import pygame as pyg


# Requires the owner to have a Vector2 position attribute.
class Collider:
    def __init__(self, owner, x, y, radius):
        self.owner = owner
        self.position = pyg.math.Vector2(x, y)
        self.radius = radius

    def IsColliding(self, otherCollider):
        distance = self.__GetWorldPos__().distance_to(
            otherCollider.__GetWorldPos__())
        return distance <= self.radius + otherCollider.radius

    def Draw(self, screen):
        worldPos = self.__GetWorldPos__()
        pyg.draw.circle(screen, (0, 255, 0),
                        (int(worldPos.x), int(worldPos.y)),
                        int(self.radius), 0)

    def __GetWorldPos__(self):
        return self.owner.position + self.position.rotate(-self.owner.rotation)
