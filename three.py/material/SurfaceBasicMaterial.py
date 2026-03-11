from OpenGL.GL import *
from core import *
from core.UniformsLib import getUniformsLib
from material.Material import Material

class SurfaceBasicMaterial(Material):
        
    def __init__(self, color=[1,1,1], alpha=1, texture=None, wireframe=False, lineWidth=1, useVertexColors=False, alphaTest=0):

        super().__init__(shaderName="basic", name="SurfaceBasicMaterial", uniforms=getUniformsLib("common", "surface"))
                 
        # set default uniform values
        self.setUniform( "vec3", "color", color )
        self.setUniform( "float", "alpha", alpha )
        self.setUniform( "float", "alphaTest", alphaTest )
        
        if useVertexColors:
            self.setUniform( "bool", "useVertexColors", 1 )
        else:
            self.setUniform( "bool", "useVertexColors", 0 )
            
        if texture is None:
            self.setUniform( "bool", "useTexture", 0 )
            self.setUniform( "sampler2D", "image", -1 )
        else:
            self.setUniform( "bool", "useTexture", 1 )
            self.setUniform( "sampler2D", "image", texture )
            
        self.setUniform( "bool", "useLight", 0 )
        
        # set default render values
        self.drawStyle = GL_TRIANGLES
        
        # used for wireframe rendering
        self.lineWidth = lineWidth
        
        # customize draw style GL_TRIANGLES
        if wireframe:
            self.fillStyle  = GL_LINE
        else:
            self.fillStyle  = GL_FILL

        
