import pygame as pyg
from pygame import locals
from pygame import transform
import src.env as env
import src.config as config


class Game:

    """The global object that represents the game instance"""

    def __init__(self):
        env.game = self
        
        pyg.mixer.pre_init(
            config.AUDIO_SAMPLING_RATE, -16, 2, config.AUDIO_BUFFER_SIZE)
        pyg.mixer.init()
        pyg.init()

        # Clock
        self.clock = pyg.time.Clock()
        self.TARGET_FRAMERATE = config.TARGET_FRAMERATE

        # Screen initialization
        self.SCREEN_SIZE = pyg.math.Vector2(
            config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.screen = pyg.display.set_mode(
            (int(self.SCREEN_SIZE.x), int(self.SCREEN_SIZE.y)))
        pyg.display.set_caption(config.WINDOW_CAPTION)
        
        if config.WINDOW_ICON_PATH != "":
            pyg.display.set_icon(pyg.image.load(
                config.WINDOW_ICON_PATH).convert_alpha())

        # TO DO: Don't do this here. Provide API to change background.
        # self.background = pyg.image.load("Assets/Sprites/background.png")
        # self.backgroundRect = self.background.get_rect()

        self.entities = pyg.sprite.RenderClear()
        self.codeObjects = []
        self.sceneLoader = None

    def MainLoop(self):
        while (True):

            # If there a scene oadload has been requested, load it
            if self.sceneLoader is not None:
                self.__LoadScene__(self.sceneLoader)

            # Check for events
            for event in pyg.event.get():
                if (event.type == locals.QUIT):
                    pyg.quit()
                    return

            # Compute the delta time in seconds
            dt = self.clock.get_time() / 1000

            # Simulate the game logic
            self.Update(dt)
            self.DoPhysics(dt)

            # Render the frame
            self.Render()
            pyg.display.update()

            # Wait until the next frame
            self.clock.tick(self.TARGET_FRAMERATE)

    def Update(self, dt):
        for entity in self.entities:
            entity.Update(dt)

        for codeObject in self.codeObjects:
            codeObject.Update(dt)

    def DoPhysics(self, dt):
        for entity in self.entities:
            if entity.simulatePhysics:
                entity.DoPhysics(dt)

    def Render(self):
        # TO DO: Uncomment this once the API for the background is there
        # Draw the background
        #if self.background not None:
            #self.screen.blit(self.background, self.backgroundRect)

        # Transform the sprite
        for entity in self.entities:
            entity.rotation = entity.rotation % 360

            entity.rect.center = (entity.position.x, entity.position.y)

            entity.image = transform.rotate(
                entity.originalImage, entity.rotation)

            entity.rect = entity.image.get_rect()
            entity.rect.center = (entity.position.x, entity.position.y)

        self.entities.draw(self.screen)

        for entity in self.entities:
            entity.OnRender(self.screen)

        for codeObject in self.codeObjects:
            codeObject.OnRender(self.screen)

    # Entity management
    def AddEntity(self, newEntity):
        self.entities.add(newEntity)

    def AddCodeObject(self, newCodeObject):
        self.codeObjects.append(newCodeObject)

    # Scene management
    def RequestLoadScene(self, sceneLoader):
        # Queue a scene load
        self.sceneLoader = sceneLoader

    def __LoadScene__(self, sceneLoader):
        # Mark all entities for deletion
        for entity in self.entities:
            entity.kill()

        for i in range(len(self.codeObjects) - 1, -1, -1):
            if not self.codeObjects[i].isPersistent:
                self.codeObjects[i].Destroy()

        sceneLoader()
        self.sceneLoader = None

    # Utilities
    @staticmethod
    def LoadAnimation(animationFramePaths):
        animation = []
        for path in animationFramePaths:
            animation.append(pyg.image.load(path).convert_alpha())
        return animation
