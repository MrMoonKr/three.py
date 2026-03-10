from core import *
from core.UniformsLib import getUniformsLib
from material import *

class PointBasicMaterial(Material):

    def __init__(self, color=[1,1,1], alpha=1, texture=None, size=1, 
        usePerspective=True, useVertexColors=False, alphaTest=0.75):

        super().__init__(shaderName="points", name="PointBasicMaterial", uniforms=getUniformsLib("common", "points"))
        
        # set render values
        self.drawStyle = GL_POINTS

        # set default uniform values
        self.setUniform( "vec3", "color", color )
        self.setUniform( "float", "alpha", alpha )
        self.setUniform( "float", "size", size )
        self.setUniform( "float", "alphaTest", alphaTest )
        
        if useVertexColors:
            self.setUniform( "bool", "useVertexColors", 1 )
        else:
            self.setUniform( "bool", "useVertexColors", 0 )
            
        if usePerspective:
            self.setUniform( "bool", "usePerspective", 1 )
        else:
            self.setUniform( "bool", "usePerspective", 0 )
        
        if texture is None:
            self.setUniform( "bool", "useTexture", 0 )
            self.setUniform( "sampler2D", "image", -1 )
        else:
            self.setUniform( "bool", "useTexture", 1 )
            self.setUniform( "sampler2D", "image", texture )
        
