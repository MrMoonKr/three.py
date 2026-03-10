import tkinter as tk

from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *

import numpy as np
import random

class TestUpdatingTexture(Base):
    
    def initialize(self):

        self.setWindowTitle('Updating Textures')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25, 0.25, 0.25)
        
        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 0, 2)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = TrackballControls(self.input, self.camera, [0, 0, 0])

        self.canvas = np.full((128, 128, 4), 255, dtype=np.uint8)
        self.canvasID = OpenGLUtils.initializeSurface(self.canvas)
            
        geometry = QuadGeometry(width=1, height=1, widthResolution=1, heightResolution=1)
        material = SurfaceBasicMaterial(texture=self.canvasID)
        # disable filtering to see individual pixels more clearly
        material.linearFiltering = False
        mesh = Mesh(geometry, material)
        self.scene.add(mesh)

    def update(self):

        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])

        # changing the color of 1000 pixels per frame
        for i in range(1000):
            x = random.randint(1,126)
            y = random.randint(1,126)
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            self.canvas[y, x] = (r, g, b, 255)

        OpenGLUtils.updateSurface(self.canvas, self.canvasID)
        
        self.renderer.render(self.scene, self.camera)
                    
class GLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.base = TestUpdatingTexture(self)

def main() -> None:
    app = GLApp()
    app.mainloop()

if __name__ == "__main__":
    main()
