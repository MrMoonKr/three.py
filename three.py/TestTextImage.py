import tkinter as tk

from core import *
from cameras import *
from geometry import *
from material import *
from lights import *

class TestTextImage(Base):
    
    def initialize(self):

        self.setWindowTitle('Text Images and HUD Text')
        self.setWindowSize(1200, 760)
        self.centerWindow()

        self.renderer = Renderer()
        #self.renderer.setViewportSize(600,600)
        self.renderer.setClearColor(0.75,0.75,0.75)
        
        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 1, 5)
        self.camera.transform.lookAt(0, 0, 0)        
        self.cameraControls = TrackballControls(self.input, self.camera, [0, 0, 0])

        self.scene.add( AmbientLight(strength=0.25) )
        self.scene.add( DirectionalLight(direction=[-1,-1,-1]) )

        messageImage = TextImage(text="Hello, World!",
                                 fontFileName="fonts/Souses.otf", fontSize=36,
                                 fontColor=[50,0,0], backgroundColor=[200,200,255],
                                 width=256, height=256,
                                 alignHorizontal="CENTER", alignVertical="MIDDLE")
        messageTexture = OpenGLUtils.initializeSurface(messageImage.surface)
        lightMaterial = SurfaceLightMaterial( texture=messageTexture )
        self.cube = Mesh( BoxGeometry(), lightMaterial )
        self.cube.transform.translate(-1.25, 0.0, 0.0)
        self.scene.add(self.cube)

        koreanImage = TextImage(text="안녕하세요",
                                fontFileName="fonts/D2Coding-Ver1.3.2-20180524.ttf", fontSize=30,
                                fontColor=[10,40,90], backgroundColor=[220,240,220],
                                width=256, height=256,
                                alignHorizontal="CENTER", alignVertical="MIDDLE")
        koreanTexture = OpenGLUtils.initializeSurface(koreanImage.surface)
        koreanMaterial = SurfaceLightMaterial(texture=koreanTexture)
        self.koreanCube = Mesh(BoxGeometry(), koreanMaterial)
        self.koreanCube.transform.translate(1.25, 0.0, 0.0)
        self.scene.add(self.koreanCube)

        # set up the HUD (heads-up display)
        self.hudScene = Scene()
        self.hudCamera = OrthographicCamera(left=0, right=600, bottom=0, top=600)

        hudImage = TextImage(text="This is a test of HUD text.",
                          fontFileName="fonts/Souses.otf", fontSize=28,
                          transparent=True)
        hudTexture = OpenGLUtils.initializeSurface(hudImage.surface)
        quad = Sprite( SpriteMaterial( size=[hudImage.width, hudImage.height], anchor=[0,0], texture=hudTexture) )
        quad.transform.setPosition(5,5)
        self.hudScene.add( quad )

        hudKoreanImage = TextImage(text="D2Coding 한글 HUD 예제",
                                   fontFileName="fonts/D2Coding-Ver1.3.2-20180524.ttf", fontSize=24,
                                   fontColor=[20,20,20], transparent=True)
        hudKoreanTexture = OpenGLUtils.initializeSurface(hudKoreanImage.surface)
        hudKoreanQuad = Sprite(SpriteMaterial(size=[hudKoreanImage.width, hudKoreanImage.height],
                                              anchor=[0,0], texture=hudKoreanTexture))
        hudKoreanQuad.transform.setPosition(5,40)
        self.hudScene.add(hudKoreanQuad)

        self.fpsImage = TextImage(text="FPS: 0",
                                  fontFileName="fonts/D2Coding-Ver1.3.2-20180524.ttf", fontSize=20,
                                  fontColor=[255,255,255], backgroundColor=[30,30,30],
                                  transparent=False, width=120, height=28,
                                  alignHorizontal="LEFT", alignVertical="MIDDLE")
        self.fpsTexture = OpenGLUtils.initializeSurface(self.fpsImage.surface)
        self.fpsQuad = Sprite(SpriteMaterial(size=[self.fpsImage.width, self.fpsImage.height],
                                             anchor=[0,0], texture=self.fpsTexture))
        self.fpsQuad.transform.setPosition(5, 70)
        self.hudScene.add(self.fpsQuad)

        self.fpsFrameCount = 0
        self.fpsElapsed = 0.0
        
    def update(self):
        
        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.hudCamera.setViewRegion( left=0, right=size["width"], bottom=0, top=size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
                
        self.cube.transform.rotateX(0.005, Matrix.LOCAL)
        self.cube.transform.rotateY(0.01, Matrix.LOCAL)
        self.koreanCube.transform.rotateX(-0.005, Matrix.LOCAL)
        self.koreanCube.transform.rotateY(0.01, Matrix.LOCAL)

        self.fpsFrameCount += 1
        self.fpsElapsed += self.deltaTime
        if self.fpsElapsed >= 0.25:
            fps = self.fpsFrameCount / self.fpsElapsed
            self.fpsImage.text = f"FPS: {fps:.1f}"
            self.fpsImage.renderImage()
            OpenGLUtils.updateSurface(self.fpsImage.surface, self.fpsTexture)
            self.fpsFrameCount = 0
            self.fpsElapsed = 0.0
        
        self.renderer.render(self.scene, self.camera)

        self.renderer.render(self.hudScene, self.hudCamera, clearColor=False)

class GLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.base = TestTextImage(self)

def main() -> None:
    app = GLApp()
    app.mainloop()

if __name__ == "__main__":
    main()
