import pygame as pyg
from . import env


class GameObject:

    def __init__(self):
        self.name = ""

        # Lifetime
        self.isAlive = True
        self.isPersistent = False

        # Transform
        self.position = pyg.math.Vector2(0, 0)
        self.rotation = 0

        # Components
        self.components = []
        self.updateListeners = []
        self.physicsUpdateListeners = []
        self.onRenderListeners = []

        # TODO: How do we access components?
        self.sprite = None
        
        self.physicsBody = None
        self.colliders = []

        env.game.NewObject(self)

    # Public API
    def Destroy(self):
        self.isAlive = False

    def IsColliding(self, otherObject):
        theirColliders = otherObject.colliders

        for theirCollider in theirColliders:
            for myCollider in self.colliders:
                if myCollider.IsColliding(theirCollider):
                    return True

        return False

    # Engine messages
    def Update(self, dt):
        for component in self.updateListeners:
            component.Update(dt)

    def PhysicsUpdate(self, dt):
        for component in self.physicsUpdateListeners:
            component.PhysicsUpdate(dt)

        if self.physicsBody is not None:
            self.physicsBody.PhysicsUpdate(dt)

    def OnRender(self, screen):
        for component in self.onRenderListeners:
            component.OnRender(screen)
