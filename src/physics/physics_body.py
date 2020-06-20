import pygame.math as math
from ..component import Component


class PhysicsBody(Component):

    def __init__(self, gameObject):
        
        Component.__init__(gameObject)

        # Assign self to the GameObject
        if (gameObject is None):
            print("[ERROR] Can't add a PhysicsBody to a None gameObject.")
            return
        elif gameObject.physicsBody is not None:
            print("[ERROR] " + gameObject.name + " already has a PhysicsBody")
            return

        gameObject.physicsBody = self
        
        # State
        self.isEnabled = True
        self.velocity = math.Vector2(0, 0)
        self.drag = 0

    def PhysicsUpdate(self, dt):
        velocityMagnitudeSquared = self.velocity.length_squared()
        if (velocityMagnitudeSquared > 0):
            self.velocity -= velocityMagnitudeSquared * \
                self.drag * dt * self.velocity.normalize()

        self.gameObject.position += self.velocity * dt
