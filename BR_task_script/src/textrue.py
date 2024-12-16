from OpenGL import GL
from PIL import Image
import numpy as np


def load_texture_from_image(image_path):
    """Load an image as an OpenGL texture."""
    img = Image.open(image_path).convert('RGBA')
    img_data = np.array(img, dtype=np.uint8)

    texture_id = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)
    GL.glTexImage2D(
        GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, img.width, img.height, 0,
        GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, img_data
    )
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

    return texture_id

def load_texture_from_array(array):
    texture_id = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)
    GL.glTexImage2D(
        GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, array.shape[1], array.shape[0], 0,
        GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, array
    )
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    
    return texture_id
    