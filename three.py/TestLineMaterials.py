import tkinter as tk

from core import *
from cameras import *
from geometry import *
from material import *
from mathutils import *

import colorsys

class TestLineMaterials(Base):
    
    def initialize(self):

        self.setWindowTitle('Line Materials')
        self.setWindowSize(1200, 760)
        self.centerWindow()
        
        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.25)

        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 5, 10)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = TrackballControls(self.input, self.camera, [0, 0, 0])

        # line-based material
        linePoints = [[-6,0,-4],[6,0,-4],[6,0,4],[-6,0,4],[-6,0,-4]]
        lineGeo = LineGeometry(linePoints)
        lineMesh = Mesh(lineGeo, LineBasicMaterial())
        self.scene.add(lineMesh)

        self.meshList = []

        hilbertPoints = Hilbert3D(size=1, iterations=1)

        # set up a variety of materials to test
        solidMat = LineBasicMaterial(color=[0,0,1])
        dashedMat = LineDashedMaterial(lineWidth=1, dashLength=0.2, gapLength=0.1)
        rainbowMat = LineBasicMaterial(useVertexColors=True)

        # vertex colors for most geometries
        rainbowColors = []
        for i in range(256):
            rainbowColors.append( colorsys.hsv_to_rgb(i/256,1,1) )        

        hilbertPoints = Hilbert3D(size=1, iterations=1)
        hilbertGeo = LineGeometry(hilbertPoints)

        vertexColorMaterial = LineBasicMaterial()
        vertexColorMaterial.setUniform("bool", "useVertexColors", 1)

        # solid red
        hilbert1 = Mesh(LineGeometry(hilbertPoints), LineBasicMaterial(color=[1,0,0]))
        hilbert1.transform.translate(4,0,-2)
        self.meshList.append(hilbert1)

        # rainbow
        hilbertGeoA = LineGeometry(hilbertPoints)
        vertexColorDataA = []
        for i in range( len(hilbertPoints) ):
            vertexColorDataA.append( colorsys.hsv_to_rgb(i/len(hilbertPoints), 1, 1) )        
        hilbertGeoA.setAttribute("vec3", "vertexColor", vertexColorDataA)
        hilbert2 = Mesh(hilbertGeoA, vertexColorMaterial)
        hilbert2.transform.translate(0,0,-2)
        self.meshList.append(hilbert2)

        # color shift from front to back
        hilbertGeoD = LineGeometry(hilbertPoints)
        vertexColorDataD = []
        for i in range( len(hilbertPoints) ):
            vertexColorDataD.append( [hilbertPoints[i][2]*0.5 + 0.5, 0, 1] )        
        hilbertGeoD.setAttribute("vec3", "vertexColor", vertexColorDataD)
        hilbert3 = Mesh(hilbertGeoD, vertexColorMaterial)
        hilbert3.transform.translate(-4,0,-2)
        self.meshList.append(hilbert3)

        # dashed red
        hilbert4 = Mesh(LineGeometry(hilbertPoints), LineDashedMaterial(color=[1,0,0], dashLength=0.2, gapLength=0.1))
        hilbert4.transform.translate(4,0,2)
        self.meshList.append(hilbert4)

        # scrolling dashed cyan
        scrollingMat = LineDashedScrollingMaterial(color=[0,1,1], dashLength=0.20, gapLength=0.10, dashSpeed=0.75)
        hilbert7 = Mesh(LineGeometry(hilbertPoints), scrollingMat)
        hilbert7.transform.translate(0,2.5,0)
        self.meshList.append(hilbert7)

        # light to dark
        hilbertGeoB = LineGeometry(hilbertPoints)
        vertexColorDataB = []
        for i in range( len(hilbertPoints) ):
            vertexColorDataB.append( colorsys.hsv_to_rgb(1, 0, i/len(hilbertPoints)) )        
        hilbertGeoB.setAttribute("vec3", "vertexColor", vertexColorDataB)
        hilbert5 = Mesh(hilbertGeoB, vertexColorMaterial)
        hilbert5.transform.translate(0,0,2)
        self.meshList.append(hilbert5)
        
        # alternate colors
        hilbertGeoC = LineGeometry(hilbertPoints)
        vertexColorDataC = []
        for i in range( len(hilbertPoints) ):
            if i % 2 == 0:
                vertexColorDataC.append( [0.2,0.2,1] )
            else:
                vertexColorDataC.append( [1,0.5,1] )
        hilbertGeoC.setAttribute("vec3", "vertexColor", vertexColorDataC)
        hilbert6 = Mesh(hilbertGeoC, vertexColorMaterial)
        hilbert6.transform.translate(-4,0,2)
        self.meshList.append(hilbert6)
        
        for mesh in self.meshList:
            self.scene.add(mesh)
        
        
    def update(self):
        
        self.cameraControls.update()
        
        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])

        for mesh in self.meshList:
            mesh.transform.rotateX(0.030, Matrix.LOCAL)
            mesh.transform.rotateY(0.015, Matrix.LOCAL)
            if isinstance(mesh.material, LineDashedScrollingMaterial):
                mesh.material.update(self.deltaTime)

        self.renderer.render(self.scene, self.camera)
                    
class GLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.base = TestLineMaterials(self)

def main() -> None:
    app = GLApp()
    app.mainloop()

if __name__ == "__main__":
    main()
