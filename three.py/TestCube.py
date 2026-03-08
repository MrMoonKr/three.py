import tkinter as tk

from core import *
from cameras import *
from lights import *
from geometry import *
from material import *


class TestCube(Base):

    def initialize(self):

        self.setWindowTitle("Cube")
        self.setWindowSize(1200, 760)
        self.centerWindow()

        self.renderer = Renderer()
        #self.renderer.setViewportSize(800, 600)
        self.renderer.setClearColor(0.25, 0.25, 0.25)

        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 1, 7)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        self.scene.add(AmbientLight(strength=0.25))
        self.scene.add(DirectionalLight(direction=[-1, -1, -1]))

        self.cube = Mesh(BoxGeometry(), SurfaceLightMaterial(color=[0.5, 0.5, 1.0]))
        self.scene.add(self.cube)

    def update(self):

        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio(size["width"] / size["height"])
            self.renderer.setViewportSize(size["width"], size["height"])

        self.cube.transform.rotateX(0.02, Matrix.LOCAL)
        self.cube.transform.rotateY(0.03, Matrix.LOCAL)

        self.renderer.render(self.scene, self.camera)


class GLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.base = TestCube(self)


def main() -> None:
    app = GLApp()
    app.mainloop()


if __name__ == "__main__":
    main()
