import pygame as pyg
from ..component import Component


def LoadImage(path):
    return pyg.image.load(path).convert_alpha()


class Sprite(Component):

    def __init__(self, gameObject, offset=pyg.math.Vector2(0, 0),
                 inCameraSpace=False):

        # Initialize parent classes
        Component.__init__(self, gameObject)

        # Assign self to the GameObject
        if (gameObject is None):
            print("[ERROR] Can't add a Sprite to a None gameObject.")
            return

        gameObject.onRenderListeners.append(self)

        self.originalImage = None
        self.transformedImage = None

        self.offset = offset
        self.flipX = False
        self.flipY = False

        self.inCameraSpace = inCameraSpace

        # Values for previous rendered transformation
        self.previousFlipX = self.flipX
        self.previousFlipY = self.flipY
        self.previousScale = self.gameObject.scale
        self.previousRotation = self.gameObject.rotation
        self.previousOriginalImage = None

    def OnRender(self, screen, camera):
        self.__TransformOriginalImageIfOutdated__()
        rect = self.__GetScreenSpaceRect__(camera)

        if camera.IsOnScreen(rect):
            screen.blit(self.transformedImage, rect)

    def SetPreloadedImage(self, image):
        self.originalImage = image
        self.transformedImage = image
        originalRect = self.originalImage.get_rect()
        self.originalWidth = originalRect.width
        self.originalHeight = originalRect.height

    def SetImageByPath(self, path):
        image = LoadImage(path)
        self.SetPreloadedImage(image)

    def __TransformOriginalImageIfOutdated__(self):

        image = self.originalImage

        # See what changed
        originalImageChanged = self.originalImage != self.previousOriginalImage
        flipChanged = self.flipX != self.previousFlipX or \
            self.flipY != self.previousFlipY
        scaleChanged = self.gameObject.scale != self.previousScale
        rotationChanged = self.gameObject.rotation != self.previousRotation

        # See what transformations must happen
        hasNonDefaultFlip = self.flipX or self.flipY
        hasNonDefaultScale = self.gameObject != 1
        hasNonDefaultRotation = self.gameObject.rotation != 0

        mustBeFlipped = (
            originalImageChanged and hasNonDefaultFlip) or flipChanged
        mustBeScaled = (
            originalImageChanged and hasNonDefaultScale) or scaleChanged
        mustBeRotated = (
            originalImageChanged and hasNonDefaultRotation) or rotationChanged

        mustBeTransformed = originalImageChanged or flipChanged \
            or scaleChanged or rotationChanged

        if mustBeTransformed:
            mustBeFlipped = mustBeFlipped or hasNonDefaultFlip
            mustBeScaled = mustBeScaled or hasNonDefaultScale
            mustBeRotated = mustBeRotated or hasNonDefaultRotation

        if mustBeFlipped:
            image = pyg.transform.flip(image, self.flipX,
                                       self.flipY)

        if mustBeScaled:
            xSize = int(self.gameObject.scale * self.originalWidth)
            ySize = int(self.gameObject.scale * self.originalHeight)
            image = pyg.transform.scale(image, (xSize, ySize))

        if mustBeRotated:
            image = pyg.transform.rotate(
                image, self.gameObject.rotation)

        self.previousFlipX = self.flipX
        self.previousFlipY = self.flipY
        self.previousScale = self.gameObject.scale
        self.previousRotation = self.gameObject.rotation
        self.previousOriginalImage = self.originalImage

        if mustBeTransformed:
            self.transformedImage = image

    def __GetScreenSpaceRect__(self, camera):
        rect = self.transformedImage.get_rect()
        rect.center = (
            self.gameObject.position.x, self.gameObject.position.y)
        rect.x += self.offset.x
        rect.y += self.offset.y

        if not self.inCameraSpace:
            rect = camera.WorldToScreenSpace(rect)

        return rect
