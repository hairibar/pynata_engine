import pygame as pyg
from Scripts import env
from Scripts.collider import Collider


class Entity(pyg.sprite.Sprite):
    """The basic object class. Physics are enabled by default."""

    def __init__(self, animation):
        # Initialize the sprite
        pyg.sprite.Sprite.__init__(self)

        self.name = ""

        self.InitializeAnimation(animation)
        self.image = self.originalImage.copy()

        # Movement
        self.position = pyg.math.Vector2(0, 0)
        self.velocity = pyg.math.Vector2(0, 0)
        self.rotation = 0

        self.simulatePhysics = True
        self.drag = 0

        # Rect
        self.rect = self.image.get_rect()   # lol
        self.rect.center = (self.position.x, self.position.y)

        # Colliders
        self.colliders = []

        env.game.AddEntity(self)

    # Engine messages
    def Update(self, dt):
        self.UpdateAnimation(dt)

    def DoPhysics(self, dt):
        self.position += self.velocity * dt

        velocityMagnitudeSquared = self.velocity.length_squared()
        if (velocityMagnitudeSquared != 0):
            self.velocity -= velocityMagnitudeSquared * \
                self.drag * dt * self.velocity.normalize()

    def OnRender(self, screen):
        pass

    # Animation
    def UpdateAnimation(self, dt):
        # Go to the next frame if necessary
        if self.frameElapsed >= self.frameDuration:
            self.currentFrameIndex += 1
            self.frameElapsed = self.frameElapsed % self.frameDuration
            self.currentFrameIndex = self.currentFrameIndex % len(
                self.animation)
            self.SetAnimationFrame(self.currentFrameIndex)

        # Increment the counter
        self.frameElapsed += dt

    def SetAnimationFrame(self, frameIndex):
        self.originalImage = self.animation[frameIndex]

    def InitializeAnimation(self, animation):
        self.frameDuration = 0.16
        self.frameElapsed = 0
        self.currentFrameIndex = 0

        self.animation = animation
        self.SetAnimationFrame(0)

    def IsColliding(self, otherEntity):
        theirColliders = otherEntity.colliders

        for theirCollider in theirColliders:
            for myCollider in self.colliders:
                if myCollider.IsColliding(theirCollider):
                    return True

        return False
