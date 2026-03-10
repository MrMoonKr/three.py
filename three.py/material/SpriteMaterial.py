from OpenGL.GL import *
from core import *
from core.UniformsLib import getUniformsLib
from material import Material

class SpriteMaterial(Material):
        
    def __init__(self, size=[1,1], anchor=[0.5,0.5], texture=None, color=[1,1,1], alpha=1, alphaTest=0):

        super().__init__(shaderName="sprite", name="SpriteMaterial", uniforms=getUniformsLib("common", "sprite"))
                
        # set default render values
        self.drawStyle = GL_TRIANGLES

        # set default uniform values
        self.setUniform( "vec2", "size", size )
        self.setUniform( "vec2", "anchor", anchor )
        self.setUniform( "sampler2D", "image", texture )
        self.setUniform( "vec3", "color", color )
        self.setUniform( "float", "alpha", alpha )
        self.setUniform( "float", "alphaTest", alphaTest )
        
        

        
