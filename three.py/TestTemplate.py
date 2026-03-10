import tkinter as tk

from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *

class TestTemplate(Base):
    
    def initialize(self):

        self.setWindowTitle('Test')
        self.setWindowSize(1200,760)
        self.centerWindow()

        self.renderer = Renderer()
        #self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25, 0.25, 0.25)
        
        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 1, 5)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = TrackballControls(self.input, self.camera, [0, 0, 0])

        
        floorMesh = GridHelper(size=10, divisions=10, gridColor=[0,0,0], centerColor=[1,0,0])
        floorMesh.transform.rotateX(-3.14/2, Matrix.LOCAL)
        self.scene.add(floorMesh)
        
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
        self.base = TestTemplate(self)


def main() -> None:
    app = GLApp()
    app.mainloop()

if __name__ == "__main__":
    main()
