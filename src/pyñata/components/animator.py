from ..component import Component
from . import sprite


def __LoadAnimationImages__(framePaths):
    images = []
    for path in framePaths:
        images.append(sprite.LoadImage(path))
    return images


class Animator(Component):
    def __init__(self, gameObject, sprite):
        Component.__init__(self, gameObject)
        gameObject.updateListeners.append(self)

        self.sprite = sprite
        self.animationStates = {}

        # Default values
        self.currentAnimationState = None

    def SetAnimationState(self, stateName, forceRestart=False):
        if self.animationStates[stateName] == self.currentAnimationState \
                and not forceRestart:
            return

        self.currentAnimationState = self.animationStates[stateName]
        self.frameElapsed = 0
        self.currentFrameIndex = 0
        self.SetImageFrame(0)

    def AddAnimationState(self, stateName, framePaths, frameDuration=0.16):
        self.animationStates[stateName] = AnimationState(
            framePaths, frameDuration)

    def Update(self, dt):
        if self.currentAnimationState is None:
            return

        # Go to the next frame if necessary
        if self.frameElapsed >= self.currentAnimationState.frameDuration:
            self.currentFrameIndex += 1
            self.frameElapsed = self.frameElapsed %  \
                self.currentAnimationState.frameDuration
            self.currentFrameIndex = self.currentFrameIndex % len(
                self.currentAnimationState.images)
            self.SetImageFrame(self.currentFrameIndex)

        # Increment the counter
        self.frameElapsed += dt

    def SetImageFrame(self, frameIndex):
        self.sprite.SetPreloadedImage(
            self.currentAnimationState.images[frameIndex])


class AnimationState:
    def __init__(self, paths, frameDuration):
        self.images = __LoadAnimationImages__(paths)
        self.frameDuration = frameDuration
