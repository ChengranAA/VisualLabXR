from OpenGL import GL
from PIL import Image
import numpy as np
from functools import partial

# Vertex and fragment shader source
VERTEX_SHARDER_SRC = """
#version 330 core
layout(location = 0) in vec2 position;
layout(location = 1) in vec2 texCoords;

out vec2 TexCoords;

void main() {
    gl_Position = vec4(position, 0.0, 1.0);
    TexCoords = texCoords;
}
"""

FRAGMENT_SHARDER_SRC = """
#version 330 core
in vec2 TexCoords;
out vec4 color;

uniform sampler2D texture1;

void main() {
    color = texture(texture1, TexCoords);
}
"""

indices = np.array([
    0, 1, 2,  # First triangle
    2, 3, 0   # Second triangle
], dtype=np.uint32)

INDICES_LEN  = len(indices)


def create_shader(shader_type, source):
    """Compile a shader and return its ID."""
    shader_id = GL.glCreateShader(shader_type)
    GL.glShaderSource(shader_id, source)
    GL.glCompileShader(shader_id)

    # Check for compilation errors
    if not GL.glGetShaderiv(shader_id, GL.GL_COMPILE_STATUS):
        error = GL.glGetShaderInfoLog(shader_id).decode()
        raise RuntimeError(f"Shader compilation failed: {error}")

    return shader_id


def create_program(vertex_src, fragment_src):
    """Link vertex and fragment shaders into a shader program."""
    vertex_shader = create_shader(GL.GL_VERTEX_SHADER, vertex_src)
    fragment_shader = create_shader(GL.GL_FRAGMENT_SHADER, fragment_src)

    program_id = GL.glCreateProgram()
    GL.glAttachShader(program_id, vertex_shader)
    GL.glAttachShader(program_id, fragment_shader)
    GL.glLinkProgram(program_id)

    # Check for linking errors
    if not GL.glGetProgramiv(program_id, GL.GL_LINK_STATUS):
        error = GL.glGetProgramInfoLog(program_id).decode()
        raise RuntimeError(f"Program linking failed: {error}")

    return program_id

def set_up_opengl(vertices):
    VAO = GL.glGenVertexArrays(1)
    VBO = GL.glGenBuffers(1)
    EBO = GL.glGenBuffers(1)

    GL.glBindVertexArray(VAO)

    # Vertex buffer
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)

    # Element buffer
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, EBO)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL.GL_STATIC_DRAW)

    # Vertex attributes
    GL.glVertexAttribPointer(0, 2, GL.GL_FLOAT, GL.GL_FALSE, 4 * vertices.itemsize, GL.GLvoidp(0))
    GL.glEnableVertexAttribArray(0)
    GL.glVertexAttribPointer(1, 2, GL.GL_FLOAT, GL.GL_FALSE, 4 * vertices.itemsize, GL.GLvoidp(2 * vertices.itemsize))
    GL.glEnableVertexAttribArray(1)

    GL.glBindVertexArray(0)
    return VAO