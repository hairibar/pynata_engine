from .. import math as pyñ_math


def CheckCollision(a, b):
    aType = type(a).__name__
    bType = type(b).__name__

    if aType == "CircleCollider" and bType == "CircleCollider":
        return Circle_Circle(a, b)
    elif aType == "RectCollider" and bType == "RectCollider":
        return Rect_Rect(a, b)
    elif aType == "RectCollider" and bType == "CircleCollider":
        return Rect_Circle(a, b)
    elif aType == "CircleCollider" and bType == "RectCollider":
        return Rect_Circle(b, a)


def Circle_Circle(a, b):
    distance = a.__GetWorldPos__().distance_to(
        b.__GetWorldPos__())
    return distance <= a.radius + b.radius


def Rect_Rect(a, b):
    aRect = a.GetWorldRect()
    bRect = b.GetWorldRect()

    xAxisCollision = (aRect.left + aRect.width >= bRect.left and
                      bRect.left + bRect.width >= aRect.left)
    yAxisCollision = (aRect.top + aRect.height >= bRect.top and
                      bRect.top + bRect.height >= aRect.top)

    return xAxisCollision and yAxisCollision


def Rect_Circle(rectCollider, circleCollider):

    rect = rectCollider.GetWorldRect()
    circleCenter = circleCollider.__GetWorldPos__()

    closestPoint = pyñ_math.ClosestPointInRect(circleCenter, rect)
    sqrDistance = (circleCenter - closestPoint).magnitude_squared()
    return sqrDistance < circleCollider.radius**2
