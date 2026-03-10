import tkinter as tk

from core import *
from cameras import *
from geometry import *
from material import *
from lights import *
from random import random

class TestSurfaceMaterials(Base):

    def _logShaderBindings(self, bindings):
        print("Surface material shader bindings:")
        for label, material in bindings:
            print(f"  {label}: {material.__class__.__name__} -> {material.shaderName}")

    def _createOverlaySphere(self, geometry, baseMaterial, overlayMaterial, xPosition):
        sphereGroup = Object3D()
        sphereGroup.transform.translate(xPosition, 0, 0, Matrix.LOCAL)

        baseSphere = Mesh(geometry, baseMaterial)
        overlaySphere = Mesh(geometry, overlayMaterial)
        overlaySphere.transform.scaleUniform(1.002)

        sphereGroup.add(baseSphere)
        sphereGroup.add(overlaySphere)
        return sphereGroup
    
    def initialize(self):

        self.setWindowTitle('Surface Materials')
        self.setWindowSize(1200, 760)
        self.centerWindow()

        self.renderer = Renderer()
        #self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.25)
        
        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 0, 8)
        self.cameraControls = TrackballControls(self.input, self.camera, [0, 0, 0])
        
        self.scene.add( AmbientLight( strength=0.2 ) )
        self.scene.add( DirectionalLight( direction=[-1,-1,-2] ) )

        self.sphereList = []

        sphereGeom = SphereGeometry(radius=0.9)
        
        gridTexture  = OpenGLUtils.initializeTexture("images/color-grid.png")
        moonTexture  = OpenGLUtils.initializeTexture("images/moon.jpg")
        gridMaterial = SurfaceLightMaterial(texture=gridTexture)

        wireMaterial = SurfaceBasicMaterial(color=[0.8,0.8,0.8], wireframe=True, lineWidth=2)

        lightMaterial = SurfaceLightMaterial(color=[0.5,0.5,1.0])
        litOverlayBaseMaterial = SurfaceLightMaterial(texture=moonTexture)
        litOverlayWireMaterial = SurfaceLightMaterial(
            color=[0.1,0.8,0.1],
            alpha=0.65,
            wireframe=True,
            lineWidth=2,
        )
        
        rainbowMaterial = SurfaceLightMaterial(useVertexColors=True)
        vertexColorData = []
        for i in range(sphereGeom.vertexCount):
            color = [random(), random(), random()]
            vertexColorData.append(color)
        sphereGeom.setAttribute("vec3", "vertexColor", vertexColorData)
        
        sphere1 = Mesh( sphereGeom, wireMaterial )
        sphere1.transform.translate(-4, 0, 0, Matrix.LOCAL)
        self.sphereList.append(sphere1)

        sphere2 = Mesh( sphereGeom, lightMaterial )
        sphere2.transform.translate(-2, 0, 0, Matrix.LOCAL)
        self.sphereList.append(sphere2)
        
        sphere3 = Mesh( sphereGeom, rainbowMaterial )
        sphere3.transform.translate(0, 0, 0, Matrix.LOCAL)
        self.sphereList.append(sphere3)

        sphere4 = Mesh( sphereGeom, gridMaterial )
        sphere4.transform.translate(2, 0, 0, Matrix.LOCAL)
        self.sphereList.append(sphere4)

        sphere5 = self._createOverlaySphere(
            sphereGeom,
            litOverlayBaseMaterial,
            litOverlayWireMaterial,
            4,
        )
        self.sphereList.append(sphere5)

        self._logShaderBindings([
            ("wireMaterial", wireMaterial),
            ("lightMaterial", lightMaterial),
            ("rainbowMaterial", rainbowMaterial),
            ("gridMaterial", gridMaterial),
            ("litOverlayBaseMaterial", litOverlayBaseMaterial),
            ("litOverlayWireMaterial", litOverlayWireMaterial),
        ])

        for sphere in self.sphereList:
            self.scene.add(sphere)
        
    def update(self):
        
        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
                
        for sphere in self.sphereList:
            sphere.transform.rotateY(0.01, Matrix.LOCAL)
        
        self.renderer.render(self.scene, self.camera)
                    
class GLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.base = TestSurfaceMaterials(self)

def main() -> None:
    app = GLApp()
    app.mainloop()

if __name__ == "__main__":
    main()
