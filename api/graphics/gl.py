from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

from api.handlers.exceptions import CoreGraphicsAPIError

__all__ = ['GLContext', 'DrawMode']


class GLContext:

    def __init__(self, vertices):

        self.vbo = vbo.VBO(vertices)

    def set_vertex_shader(self, code_str):

        vtx_shader = shaders.compileShader(code_str, GL_VERTEX_SHADER)

        setattr(self, 'vertexShader', vtx_shader)

    def set_fragment_shader(self, code_str):

        frg_shader = shaders.compileShader(code_str, GL_FRAGMENT_SHADER)

        setattr(self, 'fragmentShader', frg_shader)

    @property
    def vertex_shader(self):

        return self.get_attr('vertexShader',
                             'Vertex Shader is not defined, consider using, '
                             'self.set_vertex_shader(code_str), method')

    @property
    def fragment_shader(self):

        return self.get_attr('fragmentShader',
                             'Fragment Shader is not defined, consider using, '
                             'self.set_fragment_shader(code_str), method')

    def compile_shaders(self):

        ctx_shader = shaders.compileProgram(self.vertex_shader, self.fragment_shader)

        setattr(self, 'ctxShader', ctx_shader)

    @property
    def shader(self):

        return self.get_attr('ctxShader',
                             'Shader is not defined, consider using, '
                             'self.compile_shaders(), method')

    @property
    def data(self):

        return self.vbo.data

    def set_shader_on_use(self):

        glUseProgram(self.shader)

    def draw(self, mode, first, count):

        try:

            self.vbo.bind()

            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointerf(self.vbo)

            glDrawArrays(mode, first, count)

        except Exception as _err:

            raise CoreGraphicsAPIError('An error occurred, while drawing, ' + str(_err))

        else:

            self.vbo.unbind()

            glDisableClientState(GL_VERTEX_ARRAY)
            glUseProgram(GL_NONE)

    @staticmethod
    def gl_clear(*color):

        glClearColor(*color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    @staticmethod
    def glsl_version():

        version = glGetString(GL_SHADING_LANGUAGE_VERSION)
        version = version.decode().replace('.', '')
        version = int(version)

        return version

    def get_attr(self, attr_name, err_msg=''):

        if hasattr(self, attr_name):

            return getattr(self, attr_name)

        else:

            raise ValueError(err_msg)

    def transform(self, x, y, z):
        pass


class DrawMode:

    POINTS = GL_POINTS
    LINE_STRIP = GL_LINE_STRIP
    LINE_LOOP = GL_LINE_LOOP
    LINES = GL_LINES
    TRIANGLE_STRIP = GL_TRIANGLE_STRIP
    TRIANGLE_FAN = GL_TRIANGLE_FAN
    TRIANGLES = GL_TRIANGLES
    QUAD_STRIP = GL_QUAD_STRIP
    QUADS = GL_QUADS
    POLYGON = GL_POLYGON
