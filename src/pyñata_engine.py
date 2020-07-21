import pygame as pyg
from .camera import Camera
from .. import env, config
from ..import debug_flags as debug
from pygame import locals


CLEAR_COLOR = pyg.Color(0, 0, 0)


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
        self.debugTextFont = pyg.font.SysFont("Arial", 18)

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

        # Initialize camera
        env.camera = Camera()
        env.camera.position = pyg.math.Vector2(self.SCREEN_SIZE / 2)

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

        self.screen.fill(CLEAR_COLOR)

        # PERF: Maybe not the most optimal solution
        toRender = []

        for gameObject in self.gameObjects:

            if not gameObject.isAlive:
                continue

            toRender.append(gameObject)

        toRender.sort(key=self.__GetDepth__)

        for gameObject in toRender:

            # Make sure that the rotation is between 0 and 360.
            # Not sure if pygame needs this, but just in case.
            # It's good practice anyway.
            gameObject.rotation = gameObject.rotation % 360

            gameObject.OnRender(self.screen, env.camera)

        if debug.SHOW_FPS:
            self.__DrawFramerate__()

    def __GetDepth__(self, gameObject):
        return gameObject.depth

    def __DrawFramerate__(self):
        fps = str(int(self.clock.get_fps()))
        fpsTextSurface = self.debugTextFont.render(fps, False,
                                                   pyg.Color(255, 255, 255),
                                                   pyg.Color(0, 0, 0))
        self.screen.blit(fpsTextSurface, (0, 0))

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
