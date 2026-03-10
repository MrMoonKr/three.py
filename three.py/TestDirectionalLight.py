import tkinter as tk

from core import *
from cameras import *
from lights import AmbientLight, DirectionalLight
from geometry import *
from material import *
from helpers import *

class TestDirectionalLight(Base):
    
    def initialize(self):

        self.setWindowTitle('Directional Light')
        self.setWindowSize(1200, 760)
        self.centerWindow()

        self.renderer = Renderer()
        #self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.75)
        
        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 1, 7)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = TrackballControls(self.input, self.camera, [0, 0, 0])

        ambientLight = AmbientLight(color=[0.1,0.1,0.2])
        self.scene.add( ambientLight )
        
        self.directionalLight = DirectionalLight(position=[2,3,0], direction=[-1,-1,0])
        self.scene.add( self.directionalLight )
        self.scene.add( DirectionalLightHelper(self.directionalLight) )
        
        gridTexture  = OpenGLUtils.initializeTexture("images/color-grid.png")
        lightMaterial = SurfaceLightMaterial( color=[1,1,1], texture=gridTexture );
        
        self.cube = Mesh( BoxGeometry(), lightMaterial )
        self.cube.transform.translate(1.5, 0, 0, Matrix.LOCAL)        
        self.scene.add(self.cube)
        
        self.sphere = Mesh( SphereGeometry(), lightMaterial )
        self.sphere.transform.translate(-1.5, 0, 0, Matrix.LOCAL)
        self.scene.add(self.sphere)
        
    def update(self):
        
        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
                
        self.cube.transform.rotateX(0.02, Matrix.LOCAL)
        self.cube.transform.rotateY(0.03, Matrix.LOCAL)

        self.sphere.transform.rotateY(0.025, Matrix.LOCAL)

        self.directionalLight.transform.rotateZ(0.002, Matrix.LOCAL)
        
        self.renderer.render(self.scene, self.camera)
                    
class GLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.base = TestDirectionalLight(self)

def main() -> None:
    app = GLApp()
    app.mainloop()

if __name__ == "__main__":
    main()
