import pygame as pyg
from .. import env, config
from ..import debug_flags as debug
from pygame import locals
from pygame import transform


class Game:

    """The global object that represents the game instance"""

    def __init__(self):
        env.game = self

        # Initialize audio
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

        # Set the window icon
        if config.WINDOW_ICON_PATH != "":
            pyg.display.set_icon(pyg.image.load(
                config.WINDOW_ICON_PATH).convert_alpha())

        # TODO: Don't do this here. Provide API to change background.
        # self.background = pyg.image.load("Assets/Sprites/background.png")
        # self.backgroundRect = self.background.get_rect()

        self.gameObjects = []
        self.sceneLoader = None

    # Main loop
    def MainLoop(self):
        while True:

            # If a scene load has been requested, load it
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
            self.PhysicsUpdate(dt)

            self.DeleteDeadObjects()

            # Render the frame
            self.Render()
            pyg.display.update()

            # Wait until the next frame
            self.clock.tick(self.TARGET_FRAMERATE)

    def DeleteDeadObjects(self):
        for gameObject in self.gameObjects[::-1]:
            if not gameObject.isAlive:
                self.gameObjects.remove(gameObject)

    def Update(self, dt):
        for gameObject in self.gameObjects:
            if gameObject.isAlive:
                gameObject.Update(dt)

    def PhysicsUpdate(self, dt):
        for gameObject in self.gameObjects:
            if gameObject.isAlive:
                gameObject.PhysicsUpdate(dt)

    def Render(self):

        for gameObject in self.gameObjects:

            if not gameObject.isAlive:
                continue

            # Make sure that the rotation is between 0 and 360.
            # Not sure if pygame needs this, but just in case.
            # It's good practice anyway.
            gameObject.rotation = gameObject.rotation % 360

            gameObject.OnRender(self.screen)

    # GameObject management
    def NewObject(self, newObject):
        self.gameObjects.append(newObject)

    def DestroyObject(self, objectToDestroy):
        objectToDestroy.isAlive = False
        objectToDestroy.OnDestroy()

    # Scene management
    def RequestLoadScene(self, sceneLoader):
        # Queue a scene load
        self.sceneLoader = sceneLoader

        # Mark all entities for deletion
        for gameObject in self.gameObjects:
            if not gameObject.isPersistent:
                self.DestroyObject(gameObject)

    def __LoadScene__(self, sceneLoader):
        self.DeleteDeadObjects()
        sceneLoader()
        self.sceneLoader = None
