from OpenGL.GL import *


# This class provides static methods to load/compile openGL shaders
# and link to create GPU programs

class OpenGLUtils(object):

    @staticmethod
    def initializeShader(shaderCode, shaderType):
        # specify OpenGL version and requirements
        shaderCode = "#version 330\n" + shaderCode

        # create empty shader object and return ref value
        shaderRef = glCreateShader(shaderType)
        # store source in shader
        glShaderSource(shaderRef, shaderCode)
        # compile source code in shader
        glCompileShader(shaderRef)

        # query whether compilation was successful

        compileSuccess = glGetShaderiv(shaderRef,
                                       GL_COMPILE_STATUS)
        if not compileSuccess:
            # retrieve error message
            errorMessage = glGetShaderInfoLog(shaderRef)
            # free some memory
            glDeleteShader(shaderRef)
            # convert byte string to character string
            errorMessage = "\n" + errorMessage.decode("utf-8")
            # raise exception, halt program, print error message
            raise Exception(errorMessage)

        # compilation successful
        return shaderRef

    @staticmethod
    def initializeProgram(vertexShaderCode, fragmentShaderCode):
        # compile shaders and store refs
        vertexShaderRef = OpenGLUtils.initializeShader(vertexShaderCode, GL_VERTEX_SHADER)
        fragmentShaderRef = OpenGLUtils.initializeShader(fragmentShaderCode, GL_FRAGMENT_SHADER)

        # create program object and store ref
        programRef = glCreateProgram()

        # attach previously compiled shaders
        glAttachShader(programRef, vertexShaderRef)
        glAttachShader(programRef, fragmentShaderRef)

        # link vertex shader to the fragment shader
        glLinkProgram(programRef)

        # query if linking was successful
        linkSuccess = glGetProgramiv(programRef, GL_LINK_STATUS)

        if not linkSuccess:

            errorMessage = glGetProgramInfoLog(programRef)
            glDeleteProgram(programRef)

            # convert byte string to character string
            errorMessage = "\n" + errorMessage.decode("utf-8")
            # raise exception , halt program, print error message
            raise Exception(errorMessage)

        # linking was successful
        return programRef

