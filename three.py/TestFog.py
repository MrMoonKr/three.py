import tkinter as tk

from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *

import random

class TestFog(Base):
    
    def initialize(self):

        self.setWindowTitle('Fog')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25, 0.25, 0.25)

        self.renderer.setFog( Fog(startDistance=2, endDistance=20, color=[0,0,0.15]) )
        
        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 2, 15)
        self.camera.transform.lookAt(0, 2, 0)
        self.cameraControls = TrackballControls(self.input, self.camera, [0, 2, 0])

        floorMesh = GridHelper(size=10, divisions=10, gridColor=[0,0,0], centerColor=[1,0,0])
        floorMesh.transform.rotateX(-3.14/2, Matrix.LOCAL)
        self.scene.add(floorMesh)

        boxGeo = BoxGeometry()
        boxTexture = OpenGLUtils.initializeTexture("images/color-grid.png")
        boxMat = SurfaceBasicMaterial(texture=boxTexture)

        for i in range(100):            
            box = Mesh(boxGeo, boxMat)
            box.transform.setPosition(
                random.uniform(-5,5),random.uniform(0,5),random.uniform(4,-10))
            box.transform.rotateX( random.uniform(0,6.28), Matrix.LOCAL )
            box.transform.rotateY( random.uniform(0,6.28), Matrix.LOCAL )
            self.scene.add(box)
            
    def update(self):

        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
            
        self.renderer.render(self.scene, self.camera)
                    
class GLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.base = TestFog(self)

def main() -> None:
    app = GLApp()
    app.mainloop()

if __name__ == "__main__":
    main()
