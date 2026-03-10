from core import *
from core.UniformsLib import getUniformsLib
from material import *

class LineBasicMaterial(Material):
        
    def __init__(self, color=[1,1,1], alpha=1, lineWidth=4, useVertexColors=False):

        super().__init__(shaderName="line_basic", name="LineBasicMaterial", uniforms=getUniformsLib("common", "line"))
        
        # set render values
        self.drawStyle = GL_LINE_STRIP
        self.lineWidth = lineWidth
        
        # set default uniform values
        self.setUniform( "vec3", "color", color )
        self.setUniform( "float", "alpha", alpha )

        if useVertexColors:
            self.setUniform( "bool", "useVertexColors", 1 )
        else:
            self.setUniform( "bool", "useVertexColors", 0 )
        
        self.setUniform( "bool", "useDashes", 0 )
        self.setUniform( "float", "dashLength", 0 )
        self.setUniform( "float", "gapLength", 0 )
        
