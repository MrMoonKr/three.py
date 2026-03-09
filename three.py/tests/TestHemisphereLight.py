import sys
import tkinter as tk
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from core import *
from cameras import *
from controls import *
from geometry import *
from helpers import *
from lights import *
from material import *


class TestHemisphereLight(Base):

    def initialize(self):

        skyColor = [0.56, 0.72, 0.96]
        groundColor = [0.40, 0.35, 0.28]
        gridColor = [0.55, 0.50, 0.42]
        centerColor = [0.46, 0.42, 0.35]

        self.setWindowTitle("HemisphereLight")
        self.setWindowSize(1200, 760)
        self.centerWindow()

        self.renderer = Renderer()
        self.renderer.setViewportSize(1200, 760)
        self.renderer.setClearColor(skyColor[0], skyColor[1], skyColor[2])

        self.scene = Scene()

        self.camera = PerspectiveCamera(aspectRatio=1200 / 760)
        self.camera.transform.setPosition(6, 4, 6)
        self.camera.transform.lookAt(0, 1, 0)

        self.cameraControls = TrackballControls(self.input, self.camera, [0, 1, 0])
        self.cameraControls.rotateSpeed = 0.012
        self.cameraControls.zoomSpeed = 0.01
        self.cameraControls.panSpeed = 0.001
        self.cameraControls.setDistanceLimits(2.5, 25)

        self.hemisphereLightStrength = 1.0
        self.sunLightStrength = 0.8
        self.hemisphereLightEnabled = True
        self.sunLightEnabled = True

        self.hemisphereLight = HemisphereLight(
            position=[0, 4, 0],
            skyColor=skyColor,
            groundColor=groundColor,
            strength=self.hemisphereLightStrength
        )
        self.scene.add(self.hemisphereLight)
        self.hemisphereHelper = HemisphereLightHelper(self.hemisphereLight, radius=100)
        self.scene.add(self.hemisphereHelper)

        self.sunLight = DirectionalLight(
            position=[5, 8, 2],
            color=[1.0, 0.95, 0.82],
            strength=self.sunLightStrength,
            direction=[-1.0, -1.2, -0.4]
        )
        self.scene.add(self.sunLight)
        self.sunHelper = DirectionalLightHelper(self.sunLight, planeSize=0.6)
        self.scene.add(self.sunHelper)

        floorMesh = GridHelper(size=20, divisions=20, gridColor=gridColor, centerColor=centerColor)
        floorMesh.transform.rotateX(-3.14 / 2, Matrix.LOCAL)
        self.scene.add(floorMesh)

        self.sphere = Mesh(
            SphereGeometry(radius=1, xResolution=32, yResolution=16),
            SurfaceLightMaterial(color=[0.90, 0.72, 0.35])
        )
        self.sphere.transform.setPosition(0, 1.1, 0)
        self.scene.add(self.sphere)

        self.boxA = Mesh(
            BoxGeometry(),
            SurfaceLightMaterial(color=[0.85, 0.28, 0.24])
        )
        self.boxA.transform.setPosition(-2.5, 0.75, 1.2)
        self.scene.add(self.boxA)

        self.boxB = Mesh(
            BoxGeometry(),
            SurfaceLightMaterial(color=[0.18, 0.55, 0.86])
        )
        self.boxB.transform.setPosition(2.3, 0.6, -1.4)
        self.boxB.transform.scaleUniform(0.8)
        self.scene.add(self.boxB)

        self.torus = Mesh(
            TorusGeometry(centralRadius=1.2, tubeRadius=0.35, tubularSegments=64, radialSegments=32),
            SurfaceLightMaterial(color=[0.35, 0.82, 0.58])
        )
        self.torus.transform.setPosition(0, 2.8, -2.8)
        self.scene.add(self.torus)

    def update(self):

        self.cameraControls.update()

        if self.input.isKeyDown("h") or self.input.isKeyDown("H"):
            self.hemisphereLightEnabled = not self.hemisphereLightEnabled
            strength = self.hemisphereLightStrength if self.hemisphereLightEnabled else 0
            self.hemisphereLight.uniformList.setUniformValue("strength", strength)
            self.hemisphereHelper.visible = self.hemisphereLightEnabled

        if self.input.isKeyDown("l") or self.input.isKeyDown("L"):
            self.sunLightEnabled = not self.sunLightEnabled
            strength = self.sunLightStrength if self.sunLightEnabled else 0
            self.sunLight.uniformList.setUniformValue("strength", strength)
            self.sunHelper.visible = self.sunLightEnabled

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio(size["width"] / size["height"])
            self.renderer.setViewportSize(size["width"], size["height"])

        self.sphere.transform.rotateY(0.01, Matrix.LOCAL)
        self.boxA.transform.rotateX(0.015, Matrix.LOCAL)
        self.boxA.transform.rotateY(0.01, Matrix.LOCAL)
        self.boxB.transform.rotateY(-0.017, Matrix.LOCAL)
        self.torus.transform.rotateX(0.01, Matrix.LOCAL)
        self.torus.transform.rotateY(0.02, Matrix.LOCAL)

        self.renderer.render(self.scene, self.camera)


class GLApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.base = TestHemisphereLight(self)


def main() -> None:
    app = GLApp()
    app.mainloop()


if __name__ == "__main__":
    main()
