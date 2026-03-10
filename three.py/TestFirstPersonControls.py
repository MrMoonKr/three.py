import tkinter as tk

from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *

# Note: TrackballControls can be attached to any camera-facing Object3D
class TestFirstPersonControls(Base):
    
    def initialize(self):

        self.setWindowTitle('First Person Controls')
        self.setWindowSize(1200, 760)
        self.centerWindow()

        self.renderer = Renderer()
        #self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25, 0.25, 0.25)
        
        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 0.5, 5)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = TrackballControls(self.input, self.camera, [0, 0, 0])
        self.cameraControls.rotateSpeed = 0.012
        self.cameraControls.zoomSpeed = 0.01
        self.cameraControls.panSpeed = 0.001

        skyTexture  = OpenGLUtils.initializeTexture("images/skysphere.jpg")
        sky = Mesh( SphereGeometry(200, 64,64), SurfaceBasicMaterial(texture=skyTexture) )
        self.scene.add(sky)
        
        floorMesh = GridHelper(size=20, divisions=100, gridColor=[0,0,0], centerColor=[1,0,0])
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
        self.base = TestFirstPersonControls(self)

def main() -> None:
    app = GLApp()
    app.mainloop()

if __name__ == "__main__":
    main()
