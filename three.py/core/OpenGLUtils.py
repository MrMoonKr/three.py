# static methods to load and compile OpenGL shader programs
from OpenGL.GL import *

import numpy as np
from PIL import Image, ImageOps
from pathlib import Path

class OpenGLUtils(object):

    @staticmethod
    def initializeShader(shaderCode, shaderType):
        
        extension = '#extension GL_ARB_shading_language_420pack : require\n'
        shaderCode = '#version 130\n' + extension + shaderCode
        
        # create empty shader object and return reference value
        shaderID = glCreateShader(shaderType)
        # stores the source code in the shader
        glShaderSource(shaderID, shaderCode)
        # compiles source code previously stored in the shader object
        glCompileShader(shaderID)

        # queries whether shader compile was successful
        compileSuccess = glGetShaderiv(shaderID, GL_COMPILE_STATUS)
        if not compileSuccess:
            # retreive error message
            errorMessage = glGetShaderInfoLog(shaderID)
            # free memory used to store shader program
            glDeleteShader(shaderID)
            # TODO: parse str(errorMessage) for better printing
            raise Exception(errorMessage)  
            
        # compilation was successful; return shader reference value
        return shaderID

    @staticmethod
    def initializeShaderFromCode(vertexShaderCode, fragmentShaderCode):
        
        vertexShaderID   = OpenGLUtils.initializeShader(vertexShaderCode,   GL_VERTEX_SHADER)
        fragmentShaderID = OpenGLUtils.initializeShader(fragmentShaderCode, GL_FRAGMENT_SHADER)
    
        programID = glCreateProgram()
        glAttachShader(programID, vertexShaderID)
        glAttachShader(programID, fragmentShaderID)
        glLinkProgram(programID)
        
        return programID

    """
    @staticmethod
    def initializeShaderFromFiles(vertexShaderFileName, fragmentShaderFileName):

        vertexShaderFile = open(vertexShaderFileName, mode='r')
        vertexShaderCode = vertexShaderFile.read()
        vertexShaderFile.close()

        fragmentShaderFile = open(fragmentShaderFileName, mode='r')
        fragmentShaderCode = fragmentShaderFile.read()
        fragmentShaderFile.close()
        
        return OpenGLUtils.initializeShaderFromCode(vertexShaderCode, fragmentShaderCode)
    """
    
    @staticmethod
    def initializeTexture(imageFileName):
        # load image from file
        imagePath = OpenGLUtils._resolvePath(imageFileName)
        with Image.open(imagePath) as image:
            return OpenGLUtils.initializeSurface(image.copy())
        
    @staticmethod
    def initializeSurface(surface):
        # transfer image to string buffer
        textureData, width, height = OpenGLUtils._surfaceToTextureData(surface)
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)

        # send image data to texture buffer
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
                     
        # generate a mipmap for use with 2d textures
        glGenerateMipmap(GL_TEXTURE_2D)
        
        # default: use smooth interpolated color sampling when textures magnified
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # use the mip map filter rather than standard filter
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        
        return texid

    @staticmethod
    def updateSurface(surface, textureID):
        textureData, width, height = OpenGLUtils._surfaceToTextureData(surface)
        glBindTexture(GL_TEXTURE_2D, textureID)
        # send image data to texture buffer
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    @staticmethod
    def _surfaceToTextureData(surface):
        if isinstance(surface, Image.Image):
            image = ImageOps.flip(surface.convert("RGBA"))
            width, height = image.size
            return image.tobytes(), width, height

        array = np.asarray(surface, dtype=np.uint8)
        if array.ndim == 2:
            array = np.stack([array, array, array, np.full_like(array, 255)], axis=-1)
        elif array.shape[2] == 3:
            alpha = np.full((array.shape[0], array.shape[1], 1), 255, dtype=np.uint8)
            array = np.concatenate([array, alpha], axis=2)

        array = np.flipud(array)
        height, width = array.shape[:2]
        return np.ascontiguousarray(array).tobytes(), width, height

    @staticmethod
    def _resolvePath(fileName):
        path = Path(fileName)
        if path.exists():
            return path
        return Path(__file__).resolve().parent.parent / path
                     
