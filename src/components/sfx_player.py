import pygame as pyg
import random
from ..component import Component
from ... import debug_flags as debug
from ... import config as config
from .. import math as pyñ_math
from ... import env
import os


class SFXPlayer(Component):
    def __init__(self, gameObject, paths):
        Component.__init__(self, gameObject)

        gameObject.updateListeners.append(self)

        self.sounds = self.__LoadSFX__(paths)
        self.currentlyPlayingSound = None

        # Parameters
        self.volume = 0 if debug.MUTE else 1
        self.forceSingleVoice = True

        self.loop = False
        self.loopCount = -1

        self.fadeInLength_ms = 0
        self.fadeOutLength_ms = 200

        self.fadeOutOverDistance = False
        self.minFadeoutDistance = config.DEFAULT_MIN_FADEOUT_DISTANCE
        self.maxFadeoutDistance = config.DEFAULT_MAX_FADEOUT_DISTANCE

    def Play(self):

        if self.forceSingleVoice and self.currentlyPlayingSound:
            self.currentlyPlayingSound.stop()

        index = random.randrange(0, len(self.sounds))
        sound = self.sounds[index]

        sound.set_volume(self.__GetActualVolume__())
        sound.play(loops=self.__GetPygameLoopParameter__(),
                   fade_ms=self.fadeInLength_ms)

        self.currentlyPlayingSound = sound

    def Stop(self, doFade=True):
        if self.currentlyPlayingSound:
            if doFade:
                self.currentlyPlayingSound.fadeout(self.fadeOutLength_ms)
            else:
                self.currentlyPlayingSound.stop()

            self.currentlyPlayingSound = None

    def SetLoop(self, loop):
        if isinstance(loop, bool):
            self.loop = loop
            if loop:
                self.loopCount = -1
        else:
            if loop == -1:
                self.loop = True
            elif loop == 0:
                self.loop = False
            else:
                self.loop = True
                self.loopCount = loop

    def Update(self, dt):
        if self.currentlyPlayingSound and self.fadeOutOverDistance:
            self.currentlyPlayingSound.set_volume(
                self.__GetActualVolume__())

    def __LoadSFX__(self, paths):
        sounds = []

        for path in paths:
            os.getcwd()
            sound = pyg.mixer.Sound(path)
            sounds.append(sound)

        return sounds

    def __GetActualVolume__(self):
        if debug.MUTE:
            return 0
        else:
            return self.volume * self.__GetDistanceFadeoutFactor__() * config.MASTER_VOLUME

    def __GetPygameLoopParameter__(self):
        if self.loop:
            return self.loopCount
        else:
            return 0

    def __GetDistanceFadeoutFactor__(self):
        if self.fadeOutOverDistance:
            distance = env.camera.position.distance_to(
                self.gameObject.position)
            return pyñ_math.InverseLerp(
                self.maxFadeoutDistance, self.minFadeoutDistance, distance, 
                clamped=True)
        else:
            return 1
