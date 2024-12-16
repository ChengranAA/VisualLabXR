import numpy as np

# TODO: verify the resolution ratio, because it is definitely not 1:1 
# Quad vertex data 
DEFAULT_VERTICES_LEFT = np.array([
    # Positions     # Texture Coords
     0.1, -0.2,     0.0, 1.0,  # Bottom-left
     0.5, -0.2,     1.0, 1.0,  # Bottom-right
     0.5,  0.2,     1.0, 0.0,  # Top-right
     0.1,  0.2,     0.0, 0.0,  # Top-left
], dtype=np.float32)

DEFAULT_VERTICES_RIGHT = np.array([
    # Positions     # Texture Coords
    -0.5, -0.2,     0.0, 1.0,  # Bottom-left
    -0.1, -0.2,     1.0, 1.0,  # Bottom-right
    -0.1,  0.2,     1.0, 0.0,  # Top-right
    -0.5,  0.2,     0.0, 0.0,  # Top-left
], dtype=np.float32)

DEFAULT_INDICES = np.array([
    0, 1, 2,  # First triangle
    2, 3, 0   # Second triangle
], dtype=np.uint32)

INDICES_LEN  = len(DEFAULT_INDICES)

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