import numpy as np
from math import acos

from lights import Light
from mathutils import MatrixFactory


class HemisphereLight(Light):

    DEFAULT = np.array([0.0, 1.0, 0.0])

    def __init__(self, position=[0,1,0], skyColor=[1,1,1], groundColor=[0.2,0.2,0.2], strength=1):
        super().__init__(position=position, color=skyColor, strength=strength)

        self.uniformList.setUniformValue("isHemisphere", 1)
        self.uniformList.setUniformValue("groundColor", groundColor)

    def getDirection(self):
        position = np.array(self.transform.getPosition(), dtype=float)
        magnitude = np.linalg.norm(position)

        if magnitude < 0.0001:
            direction = self.DEFAULT.copy()
        else:
            direction = position / magnitude

        self._alignTransform(direction)
        return list(direction)

    def _alignTransform(self, direction):
        crossProduct = np.cross(self.DEFAULT, direction)
        magnitude = np.linalg.norm(crossProduct)

        if magnitude > 0.0001:
            crossProduct = crossProduct / magnitude
            theta = acos(np.clip(np.dot(self.DEFAULT, direction), -1.0, 1.0))
            rotationMatrix = MatrixFactory.makeRotationAxisAngle(crossProduct, theta)
        elif np.dot(self.DEFAULT, direction) < 0:
            rotationMatrix = MatrixFactory.makeRotationAxisAngle([1, 0, 0], np.pi)
        else:
            rotationMatrix = MatrixFactory.makeIdentity()

        self.transform.setRotationSubmatrix(rotationMatrix)
