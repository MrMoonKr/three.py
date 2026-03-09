import numpy as np
from math import cos, sin, pi

from core.Input import Input


class TrackballControls(object):

    def __init__(self, inputObject, targetObject, targetPosition=None):

        super().__init__()

        self.input = inputObject
        self.object = targetObject

        if targetPosition is None:
            targetPosition = [0, 0, 0]

        self.target = np.array(targetPosition, dtype=float)

        self.rotateSpeed = 0.01
        self.zoomSpeed = 0.01
        self.panSpeed = 0.002
        self.keyPanSpeed = 0.01
        self.mouseWheelZoomStep = 12
        self.minDistance = 0.5
        self.maxDistance = 5000

        self.mouseRotateButton = Input.MOUSE_BUTTON_LEFT
        self.mouseZoomButton = Input.MOUSE_BUTTON_MIDDLE
        self.mousePanButton = Input.MOUSE_BUTTON_RIGHT

        self.KEY_MOVE_FORWARDS = "w"
        self.KEY_MOVE_BACKWARDS = "s"
        self.KEY_MOVE_LEFT = "a"
        self.KEY_MOVE_RIGHT = "d"
        self.KEY_MOVE_UP = "q"
        self.KEY_MOVE_DOWN = "e"

        self._previousMousePosition = np.array(self.input.getMousePosition(), dtype=float)
        self._distance = 1.0
        self._azimuth = 0.0
        self._elevation = 0.0

        self._syncFromObject()
        self._applyTransform()

    def update(self):

        currentMousePosition = np.array(self.input.getMousePosition(), dtype=float)
        mouseDelta = currentMousePosition - self._previousMousePosition
        self._previousMousePosition = currentMousePosition

        if self.input.isMousePressed(self.mouseRotateButton):
            self._rotate(mouseDelta[0], mouseDelta[1])

        if self.input.isMousePressed(self.mouseZoomButton):
            self._zoom(mouseDelta[1])

        mouseWheelDelta = self.input.getMouseWheel()
        if mouseWheelDelta != 0:
            self._zoom(-mouseWheelDelta * self.mouseWheelZoomStep)

        if self.input.isMousePressed(self.mousePanButton):
            self._pan(mouseDelta[0], mouseDelta[1])

        self._updateKeyboardMovement()

        self._applyTransform()

    def setTarget(self, x=0, y=0, z=0):
        self.target = np.array([x, y, z], dtype=float)
        self._syncFromObject()
        self._applyTransform()

    def getTarget(self):
        return self.target.tolist()

    def setDistance(self, distance):
        self._distance = min(max(distance, self.minDistance), self.maxDistance)
        self._applyTransform()

    def setDistanceLimits(self, minDistance=0.5, maxDistance=1000):
        self.minDistance = minDistance
        self.maxDistance = maxDistance
        self._distance = min(max(self._distance, self.minDistance), self.maxDistance)
        self._applyTransform()

    def _rotate(self, deltaX, deltaY):
        self._azimuth -= deltaX * self.rotateSpeed
        self._elevation += deltaY * self.rotateSpeed
        maxElevation = pi / 2 - 0.001
        self._elevation = min(max(self._elevation, -maxElevation), maxElevation)

    def _zoom(self, deltaY):
        zoomScale = 1.0 + deltaY * self.zoomSpeed
        if zoomScale <= 0:
            zoomScale = 0.01
        self._distance *= zoomScale
        self._distance = min(max(self._distance, self.minDistance), self.maxDistance)

    def _pan(self, deltaX, deltaY):
        forward, right, up = self._getViewAxes()
        panScale = self._distance * self.panSpeed

        self.target -= right * deltaX * panScale
        self.target += up * deltaY * panScale

    def _updateKeyboardMovement(self):
        moveDirection = np.array([0.0, 0.0, 0.0])

        if self.input.isKeyPressed(self.KEY_MOVE_FORWARDS):
            moveDirection += self._getGroundForward()

        if self.input.isKeyPressed(self.KEY_MOVE_BACKWARDS):
            moveDirection -= self._getGroundForward()

        if self.input.isKeyPressed(self.KEY_MOVE_LEFT):
            moveDirection -= self._getGroundRight()

        if self.input.isKeyPressed(self.KEY_MOVE_RIGHT):
            moveDirection += self._getGroundRight()

        if self.input.isKeyPressed(self.KEY_MOVE_UP):
            moveDirection += np.array([0.0, 1.0, 0.0])

        if self.input.isKeyPressed(self.KEY_MOVE_DOWN):
            moveDirection -= np.array([0.0, 1.0, 0.0])

        moveLength = np.linalg.norm(moveDirection)
        if moveLength == 0:
            return

        moveScale = self._distance * self.keyPanSpeed 
        self.target += (moveDirection / moveLength) * moveScale

    def _syncFromObject(self):
        position = np.array(self.object.transform.getPosition(), dtype=float)
        offset = position - self.target
        self._distance = np.linalg.norm(offset)

        if self._distance == 0:
            offset = np.array([0.0, 0.0, 1.0])
            self._distance = 1.0

        horizontalDistance = np.sqrt(offset[0] * offset[0] + offset[2] * offset[2])
        self._azimuth = np.arctan2(offset[0], offset[2])
        self._elevation = np.arctan2(offset[1], horizontalDistance)
        self._distance = min(max(self._distance, self.minDistance), self.maxDistance)

    def _applyTransform(self):
        offset = self._getOffsetVector()
        position = self.target + offset
        self.object.transform.setPosition(position[0], position[1], position[2])
        self.object.transform.lookAt(self.target[0], self.target[1], self.target[2])

    def _getOffsetVector(self):
        cosElevation = cos(self._elevation)
        return np.array([
            self._distance * sin(self._azimuth) * cosElevation,
            self._distance * sin(self._elevation),
            self._distance * cos(self._azimuth) * cosElevation
        ])

    def _getViewAxes(self):
        offset = self._getOffsetVector()
        forward = self._normalize(-offset)
        worldUp = np.array([0.0, 1.0, 0.0])
        right = self._normalize(np.cross(forward, worldUp))

        if np.linalg.norm(right) == 0:
            right = np.array([1.0, 0.0, 0.0])

        up = self._normalize(np.cross(right, forward))
        return forward, right, up

    def _getGroundForward(self):
        forward, _, _ = self._getViewAxes()
        groundForward = np.array([forward[0], 0.0, forward[2]])

        if np.linalg.norm(groundForward) == 0:
            return np.array([0.0, 0.0, -1.0])

        return self._normalize(groundForward)

    def _getGroundRight(self):
        groundForward = self._getGroundForward()
        worldUp = np.array([0.0, 1.0, 0.0])
        return self._normalize(np.cross(groundForward, worldUp))

    def _normalize(self, vector):
        length = np.linalg.norm(vector)
        if length == 0:
            return vector
        return vector / length
