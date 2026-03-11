from OpenGL.GL import *
from core import OpenGLUtils
from material import LineBasicMaterial

class LineDashedMaterial(LineBasicMaterial):
        
    def __init__(self, color=[1,1,1], alpha=1, lineWidth=4, dashLength=0.50, gapLength=0.25, dashOffset=0.0, useVertexColors=False):

        super().__init__(color=color, alpha=alpha, lineWidth=lineWidth, useVertexColors=useVertexColors)

        self.setUniform( "bool", "useDashes", 1 )
        self.setUniform( "float", "dashLength", dashLength )
        self.setUniform( "float", "gapLength", gapLength )
        self.setUniform( "float", "dashOffset", dashOffset )

    def setDashOffset(self, dashOffset):
        self.setUniform("float", "dashOffset", dashOffset)

    def advance(self, deltaOffset):
        dashOffset = self.uniformList["dashOffset"].value + deltaOffset
        self.setUniform("float", "dashOffset", dashOffset)
