import tkinter as tk

from core import Base, Renderer, Scene, RenderTarget, Mesh, FirstPersonController, OpenGLUtils
from cameras import PerspectiveCamera
from lights import AmbientLight, DirectionalLight
from geometry import QuadGeometry, SphereGeometry, BoxGeometry
from material import SurfaceBasicMaterial, SurfaceLightMaterial
from mathutils import Matrix
from helpers import DirectionalLightHelper, OrthographicCameraHelper

class TestShadows(Base):

    def _logShaderBindings(self, bindings):
        print("Shadow test shader bindings:")
        for label, material in bindings:
            print(f"  {label}: {material.__class__.__name__} -> {material.shaderName}")
    
    def initialize(self):

        self.setWindowTitle('Shadows')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.5,0.5,0.75)

        # to render shadows, the renderer has to do an additional pass
        #   to store depth data in a shadowmap texture;
        #   this is indicated by setting shadowMapEnabled to True.
        self.renderer.shadowMapEnabled = True
        
        self.scene = Scene() 

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 3, 5)
        self.camera.transform.lookAt(0, 1, 0)
        self.cameraControls = TrackballControls(self.input, self.camera, [0, 1, 0])

        self.scene.add( AmbientLight(strength=0.5) )
        
        # setup directional light that casts shadows
        directionalLight = DirectionalLight(position=[2,2,0], direction=[-2,-1,0])
        directionalLight.enableShadows(strength=0.5)
        # the tighter the fit on the shadow region,
        #   the better the shadow resolution will be.
        # adjust as necessary according to the contents of the scene
        directionalLight.shadowCamera.setViewRegion(
            left=-2, right=2, top=2, bottom=-2, near=10, far=0)
        self.scene.add( directionalLight )

        self.scene.add( DirectionalLightHelper(directionalLight) )
        self.scene.add( OrthographicCameraHelper(directionalLight.shadowCamera) )
        
        gridTexture  = OpenGLUtils.initializeTexture("images/color-grid.png")

        geo = QuadGeometry(width=4,height=4)
        mat = SurfaceLightMaterial(texture=gridTexture)
        
        floor = Mesh( geo, SurfaceLightMaterial(texture=gridTexture) )
        floor.transform.rotateX(-3.14/2)        
        floor.setReceiveShadow()
        self.scene.add( floor )

        # illustrate the contents of the shadowMap
        backWall = Mesh(geo,
            SurfaceBasicMaterial(texture=directionalLight.shadowRenderTarget.textureID))
        backWall.transform.translate(0,2,-2)
        self.scene.add(backWall)

        sideWall = Mesh(geo, mat)
        sideWall.transform.translate(-2,2,0)
        sideWall.transform.rotateY(3.14/2, Matrix.LOCAL)
        sideWall.setReceiveShadow()
        self.scene.add(sideWall)

        sphere = Mesh( SphereGeometry(radius=0.3), mat )
        sphere.transform.setPosition(1,2.1,0)
        sphere.setCastShadow()
        self.scene.add( sphere )
        
        self.box = Mesh( BoxGeometry(1,1,1), mat )
        self.box.transform.setPosition(0,1,0)
        self.box.setCastShadow()
        self.box.setReceiveShadow()
        self.scene.add( self.box )

        self._logShaderBindings([
            ("floor", floor.material),
            ("backWall", backWall.material),
            ("sideWall", sideWall.material),
            ("sphere", sphere.material),
            ("box", self.box.material),
            ("shadowPass", directionalLight.shadowMaterial),
        ])

    def update(self):

        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])

        self.box.transform.rotateY(0.005)
        
        self.renderer.render(self.scene, self.camera)
                    
class GLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.base = TestShadows(self)

def main() -> None:
    app = GLApp()
    app.mainloop()

if __name__ == "__main__":
    main()
