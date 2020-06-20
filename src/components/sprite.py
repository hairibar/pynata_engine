import pygame as pyg
from . import env


# Double inheritance. I know. I'm sorry.
class Sprite(pyg.sprite.Sprite, Component):

    def __init__(self, gameObject):

        # Initialize parent classes
        pyg.sprite.Sprite.__init__(self)
        Component.__init__(self, gameObject)

        # Assign self to the GameObject
        if (gameObject is None):
            print("[ERROR] Can't add a PhysicsBody to a None gameObject.")
            return
        elif gameObject.physicsBody is not None:
            print("[ERROR] " + gameObject.name + " already has a PhysicsBody")
            return

        self.gameObject = gameObject
        gameObject.updateListeners.append(self)
        gameObject.onRenderListeners.append(self)

        # Default values
        self.frameDuration = 0.16
        self.animation = None

    # Engine messages
    def Update(self, dt):
        self.__UpdateAnimation__(dt)

    def OnRender(self, screen):
        self.rect.center = (
                    gameObject.position.x, gameObject.position.y) 
        self.image = transform.rotate(
            self.originalImage, gameObject.rotation)

        self.rect = self.image.get_rect()
        self.rect.center = (
            gameObject.position.x, gameObject.position.y)

    # Public API
    @staticmethod
    def LoadAnimation(animationFramePaths):
        animation = []
        for path in animationFramePaths:
            animation.append(pyg.image.load(path).convert_alpha())
        return animation

    def SetAnimation(self, framePaths):
        self.animation = LoadAnimation(framePaths)

        # Initialize progress
        self.frameElapsed = 0
        self.currentFrameIndex = 0
        self.SetAnimationFrame(0)

        self.image = self.originalImage.copy()

        # Update the rect
        self.rect = self.image.get_rect()   # lol
        self.rect.center = (self.position.x, self.position.y)

    def __UpdateAnimation__(self, dt):
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
