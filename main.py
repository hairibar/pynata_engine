from src import pyranha_engine
import scene_loaders

# Start the game
game = pyranha_engine.Game()

# Load the starting scene
# game.RequestLoadScene(scene_loaders.BotTest)

# Start the main loop
game.MainLoop()
