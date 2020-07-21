class Component:

    def __init__(self, gameObject):
        self.gameObject = gameObject
        gameObject.components.append(self)
