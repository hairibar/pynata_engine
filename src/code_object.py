import env


class CodeObject:
    def __init__(self):
        self.name = ""

        self.isPersistent = False
        env.game.AddCodeObject(self)

    def Update(self, dt):
        pass

    def OnRender(self, screen):
        pass

    def Destroy(self):
        if (self in env.game.codeObjects):
            env.game.codeObjects.remove(self)
