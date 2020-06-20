from src import pyñata_engine
import scene_loaders

# Start the game
game = pyñata_engine.Game()

# Load the starting scene
game.RequestLoadScene(scene_loaders.InitialScene)

# Start the main loop
game.MainLoop()
