import pygame as pyg


def MoveTowards(current, target, maxStep):
    difference = target - current
    distance = difference.magnitude()

    if distance <= maxStep or distance == 0:
        return target
    else:
        return current + difference / distance * maxStep


def ClosestPointInRect(point, rect):
    return pyg.math.Vector2(Clamp(point.x, rect.left, rect.right),
                            Clamp(point.y, rect.top, rect.bottom))


def Clamp(value, minValue, maxValue):
    return max(min(value, maxValue), minValue)


def Lerp(a, b, t):
    return t * a + (1 - t) * b


def InverseLerp(a, b, value, clamped=False):
    t = (value - a) / (b - a)
    if clamped:
        return Clamp(t, 0, 1)
    else:
        return t


def Remap(inMin, inMax, outMin, outMax, value):
    t = InverseLerp(inMin, inMax)
    return Lerp(outMin, outMax, t)
