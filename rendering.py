from PIL import Image
from base import Base
from Ewg2MajorProject.AutomaticFacialEnhancementAndBeautification.App.utils.opengGLUtils import OpenGLUtils
from OpenGL.GL import *
from imageProcessing import ImageProcessing
import time as t

# This class extends base and renders tha data obtained from imageProcessing with OpenGL.


class Rendering(Base):

    def initialize(self):

        vsCode = """
        layout(location = 0) in vec3 a_position;
        layout(location = 1) in vec3 a_color;
        layout(location = 2) in vec2 a_texture;
        
        out vec3 v_color;
        out vec2 v_texture;
        void main(){

        gl_Position =vec4(a_position, 1.0);
        v_color = a_color;
        v_texture = a_texture;

        }
        """
        fsCode = """
        in vec3 v_color;
        in vec2 v_texture;
        out vec4 out_color;
        uniform sampler2D s_texture;
        void main()
        {
            out_color = texture(s_texture, v_texture);
        }
        """

        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        # vertex array object
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)

        # attributes
        self.pos = ImageProcessing()
        self.positionData = self.pos.updateData()

        self.indices = self.pos.indices

        # buffer for vertices
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.positionData.nbytes, self.positionData, GL_STATIC_DRAW)

        # buffer for indices
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        self.indicesCount = len(self.indices)

        # point position coordinates, color and texture coordinates in the array
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.positionData.itemsize * 8, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, self.positionData.itemsize * 8, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, self.positionData.itemsize * 8, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)

        # Generate texture
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        # Set wrapping filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        self.image = Image.open("images/img.jpg")

        img_data = self.image.convert("RGBA").tobytes()

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.image.width, self.image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     img_data)


    def update(self):
        glUseProgram(self.programRef)

        glClear(GL_COLOR_BUFFER_BIT)

        self.image = Image.open("images/img.jpg")

        img_data = self.image.convert("RGBA").tobytes()

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.image.width, self.image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     img_data)

        self.positionData = self.pos.updateData()

        glBufferData(GL_ARRAY_BUFFER, self.positionData.ravel(), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, self.positionData.itemsize * 8, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, False, self.positionData.itemsize * 8, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 2, GL_FLOAT, False, self.positionData.itemsize * 8, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)

        glDrawElements(GL_TRIANGLES, self.indicesCount, GL_UNSIGNED_INT, None)


Rendering().run()
