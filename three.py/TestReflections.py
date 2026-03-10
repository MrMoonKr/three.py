import tkinter as tk

from math import pi, sin

from core import *
from core.RenderTarget import RenderTarget as FrameRenderTarget
from cameras import *
from mathutils import *
from geometry import *
from material import *
from helpers import *

class TestReflections(Base):
    
    def initialize(self):

        self.setWindowTitle('Test Reflections')
        self.setWindowSize(800,800)
        self.centerWindow()
        
        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.25)

        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 3, 7)
        self.camera.transform.lookAt( 0, 0, 0 )
        self.cameraControls = TrackballControls(self.input, self.camera, [0, 1, 0])

        self.translationFunction = lambda t: [sin(t*2),sin(t),0]
        self.time = 0
        self.cubePosition = self.translationFunction(self.time)

        self.renderTarget = FrameRenderTarget(1024,768)
        self.firstReflectionCamera = PerspectiveCamera(aspectRatio=1024/768)
        self.reflectionTarget = [4, 1, 0]

        starTexture  = OpenGLUtils.initializeTexture("images/skysphere.jpg")
        stars = Mesh( SphereGeometry(200, 64,64), SurfaceBasicMaterial(texture=starTexture) )
        self.scene.add(stars)

        floorMesh = GridHelper(size=10, divisions=10, gridColor=[0,0,0], centerColor=[1,0,0], lineWidth=2)
        floorMesh.transform.rotateX(-pi / 2, Matrix.LOCAL)
        self.scene.add(floorMesh)


        #initialize shaders
        vsCode = """
        in vec3 vertexPosition;
        in vec2 vertexUV;

        out vec3 position;

        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;      
        
        void main()
        {
            position = vec3( modelMatrix * vec4(vertexPosition, 1) );
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
        }
        """

        fsCode = """

        in vec3 position;
        uniform float width;
        
        //credit to Laur(link: https://www.laurivan.com/rgb-to-hsv-to-rgb-for-shaders/)
        //for the conversion functions
        //functions for conversion from rgb to hsv and back
        vec3 rgb2hsv(vec3 c)
        {
            vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
            vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
            vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
 
            float d = q.x - min(q.w, q.y);
            float e = 1.0e-10;
            return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
        }

        vec3 hsv2rgb(vec3 c)
        {
            vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
            vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
            return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
        }

        void main(){
            float percent = mod(position.x/width,1.0);
            vec3 color = vec3(percent,1.0,1.0);
            //vec3 color = vec3(0.5,1.0,1.0);
            color = hsv2rgb(color);

            gl_FragColor = vec4(color,1.0);
        }
        """

        #setup the uniforms
        rainbowUniforms = [["float","width",2.5]]

        #make a custom material with the above values
        self.customMaterial = Material(vsCode,fsCode,rainbowUniforms)

        self.rainbowPanel = Mesh(QuadGeometry(width=3, height=3), self.customMaterial)
        self.rainbowPanel.transform.setPosition(self.reflectionTarget[0], self.reflectionTarget[1], self.reflectionTarget[2])
        self.rainbowPanel.transform.rotateY(-pi / 2, Matrix.LOCAL)
        self.scene.add(self.rainbowPanel)

        self.cubeGeo = BoxGeometry()
        self.cubeMesh = Mesh(self.cubeGeo, SurfaceBasicMaterial(texture=self.renderTarget.textureID))
        self.scene.add(self.cubeMesh)

        self.previewQuad = Mesh(QuadGeometry(width=2.2, height=1.6), SurfaceBasicMaterial(texture=self.renderTarget.textureID))
        self.previewQuad.transform.setPosition(-3.5, 1.5, -1.5)
        self.scene.add(self.previewQuad)
        
        self.cubeMesh.transform.setPosition(self.cubePosition[0],self.cubePosition[1],
                                            self.cubePosition[2],Matrix.GLOBAL)
        self._updateReflectionCamera()
        
        
    def update(self):
        self.time += self.deltaTime

        self.cubePosition = self.translationFunction(self.time)
        self.cubeMesh.transform.setPosition(self.cubePosition[0],self.cubePosition[1],
                                            self.cubePosition[2],Matrix.GLOBAL)
        self.cubeMesh.transform.rotateX(0.02,Matrix.LOCAL)
        self.cubeMesh.transform.rotateY(0.015,Matrix.LOCAL)
        self.cameraControls.update()
        self._updateReflectionCamera()
        
        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])

        self.cubeMesh.visible = False
        self.previewQuad.visible = False
        self.renderer.render(self.scene, self.firstReflectionCamera, self.renderTarget)
        self.previewQuad.visible = True
        self.cubeMesh.visible = True
        self.renderer.render(self.scene, self.camera)

    def _updateReflectionCamera(self):
        self.firstReflectionCamera.transform.setPosition(
            self.cubePosition[0],
            self.cubePosition[1],
            self.cubePosition[2],
            Matrix.GLOBAL,
        )
        self.firstReflectionCamera.transform.lookAt(
            self.reflectionTarget[0],
            self.reflectionTarget[1],
            self.reflectionTarget[2],
        )
                    
class GLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.base = TestReflections(self)

def main() -> None:
    app = GLApp()
    app.mainloop()

if __name__ == "__main__":
    main()
