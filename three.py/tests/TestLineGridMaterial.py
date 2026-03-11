import sys
import tkinter as tk
from math import cos, sin
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from core import *
from cameras import *
from controls import *
from geometry import *
from lights import *
from material import *


class TestLineGridMaterial(Base):

    def initialize(self):

        self.setWindowTitle("Line Grid Material Prototype")
        self.setWindowSize(1280, 800)
        self.centerWindow()

        self.renderer = Renderer()
        self.renderer.setViewportSize(1280, 800)
        self.renderer.setClearColor(0.78, 0.90, 0.98)

        self.scene = Scene()

        self.camera = PerspectiveCamera(aspectRatio=1280 / 800)
        self.camera.transform.setPosition(0, 6.0, 8.5)
        self.camera.transform.lookAt(0, 0.3, 0)

        self.cameraControls = TrackballControls(self.input, self.camera, [0, 0.2, 0])
        self.cameraControls.rotateSpeed = 0.010
        self.cameraControls.zoomSpeed = 0.015
        self.cameraControls.panSpeed = 0.001
        self.cameraControls.setDistanceLimits(3.5, 18)

        self.greenHalfSize = 4.8
        self.gridLift = 0.025
        self.dashLift = 0.040
        self.flowMaterials = []

        self._createLights()
        self._createGreenSurface()
        self._createPuttingGrid()
        self._createMarkers()

    def _createLights(self):
        self.scene.add(AmbientLight(color=[0.80, 0.86, 0.84], strength=0.25))
        self.scene.add(HemisphereLight(position=[0, 6, 0], skyColor=[0.76, 0.88, 0.98], groundColor=[0.32, 0.28, 0.22], strength=0.70))
        self.scene.add(DirectionalLight(position=[5, 8, 3], color=[1.0, 0.96, 0.90], strength=0.85, direction=[-1.0, -1.4, -0.5]))

    def _createGreenSurface(self):
        resolution = 48
        greenGeometry = SurfaceGeometry(
            -self.greenHalfSize,
            self.greenHalfSize,
            resolution,
            -self.greenHalfSize,
            self.greenHalfSize,
            resolution,
            lambda u, v: [u, self._greenHeight(u, v), v],
        )

        greenMaterial = SurfaceLightMaterial(color=[0.16, 0.56, 0.24])
        self.green = Mesh(greenGeometry, greenMaterial)
        self.scene.add(self.green)

    def _createPuttingGrid(self):
        lineSamples = 72
        gridCount = 15
        sampleValues = self._linspace(-self.greenHalfSize, self.greenHalfSize, lineSamples)
        gridValues = self._linspace(-self.greenHalfSize, self.greenHalfSize, gridCount)

        staticColor = [0.08, 0.22, 0.11]
        whiteDashColor = [0.96, 0.97, 0.95]
        yellowDashColor = [1.00, 0.86, 0.10]

        for u in gridValues:
            points = [self._surfacePoint(u, v, self.gridLift) for v in sampleValues]
            self.scene.add(
                Mesh(
                    LineGeometry(points),
                    LineBasicMaterial(color=staticColor, alpha=0.92, lineWidth=1),
                )
            )

            dashMaterial = LineDashedScrollingMaterial(
                color=yellowDashColor,
                alpha=0.95,
                lineWidth=2,
                dashLength=0.08,
                gapLength=0.72,
                dashSpeed=0.48,
            )
            dashPoints = [self._surfacePoint(u, v, self.dashLift) for v in sampleValues]
            self.flowMaterials.append(dashMaterial)
            self.scene.add(Mesh(LineGeometry(dashPoints), dashMaterial))

        for v in gridValues:
            points = [self._surfacePoint(u, v, self.gridLift) for u in sampleValues]
            self.scene.add(
                Mesh(
                    LineGeometry(points),
                    LineBasicMaterial(color=staticColor, alpha=0.92, lineWidth=1),
                )
            )

            dashMaterial = LineDashedScrollingMaterial(
                color=whiteDashColor,
                alpha=0.90,
                lineWidth=2,
                dashLength=0.16,
                gapLength=0.64,
                dashSpeed=0.85,
            )
            dashPoints = [self._surfacePoint(u, v, self.dashLift) for u in sampleValues]
            self.flowMaterials.append(dashMaterial)
            self.scene.add(Mesh(LineGeometry(dashPoints), dashMaterial))

    def _createMarkers(self):
        ballPosition = self._surfacePoint(2.9, 2.1, 0.13)
        ball = Mesh(SphereGeometry(radius=0.12, xResolution=24, yResolution=12), SurfaceLightMaterial(color=[0.97, 0.97, 0.95]))
        ball.transform.setPosition(ballPosition[0], ballPosition[1], ballPosition[2])
        self.scene.add(ball)

        cupPosition = self._surfacePoint(-2.8, -2.4, self.gridLift)
        cup = Mesh(RingGeometry(innerRadius=0.07, outerRadius=0.16, segments=32), SurfaceLightMaterial(color=[0.12, 0.11, 0.09]))
        cup.transform.rotateX(-3.14159 / 2, Matrix.LOCAL)
        cup.transform.setPosition(cupPosition[0], cupPosition[1], cupPosition[2])
        self.scene.add(cup)

        aimPoints = [
            ballPosition,
            self._surfacePoint(1.8, 1.2, self.dashLift),
            self._surfacePoint(0.3, 0.2, self.dashLift),
            self._surfacePoint(-1.2, -0.9, self.dashLift),
            self._surfacePoint(-2.2, -1.8, self.dashLift),
            self._surfacePoint(-2.8, -2.4, self.dashLift),
        ]
        aimMaterial = LineDashedScrollingMaterial(
            color=[1.0, 0.88, 0.52],
            alpha=0.9,
            lineWidth=2,
            dashLength=0.16,
            gapLength=0.10,
            dashSpeed=1.1,
        )
        self.flowMaterials.append(aimMaterial)
        self.scene.add(Mesh(LineGeometry(aimPoints), aimMaterial))

    def _greenHeight(self, u, v):
        return (
            -0.085 * u
            + 0.030 * v
            + 0.20 * sin(0.55 * u + 0.35)
            + 0.12 * cos(0.80 * v - 0.15)
            + 0.07 * sin(0.42 * (u + v))
        )

    def _surfacePoint(self, u, v, lift=0.0):
        return [u, self._greenHeight(u, v) + lift, v]

    def _linspace(self, start, end, count):
        if count <= 1:
            return [start]

        values = []
        step = (end - start) / (count - 1)
        for index in range(count):
            values.append(start + step * index)
        return values

    def update(self):
        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio(size["width"] / size["height"])
            self.renderer.setViewportSize(size["width"], size["height"])

        for material in self.flowMaterials:
            material.update(self.deltaTime)

        self.renderer.render(self.scene, self.camera)


class GLApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.base = TestLineGridMaterial(self)


def main() -> None:
    app = GLApp()
    app.mainloop()


if __name__ == "__main__":
    main()
