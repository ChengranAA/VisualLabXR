from shader import *
from textrue import load_texture_from_image
from demo_experiment import first_state
from runtime import State_Info
import xr
from PIL import Image
import numpy as np
from OpenGL import GL
from pynput import keyboard

# Global variables for keyboard input
key_pressed = None
exit_loop = False

def on_press(key):
    global key_pressed, exit_loop
    try:
        key_pressed = key.char  # Capture key character
    except AttributeError:
        if key == keyboard.Key.esc:
            exit_loop = True  # Exit on Escape key

def on_release(key):
    global key_pressed
    key_pressed = None  # Clear the key when released

# Set up the keyboard listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

hw_ratio = 2208/2064
off_set = 0.3

# TODO: verify the resolution ratio, because it is definitely not 1:1 
# Quad vertex data 
vertices_left = np.array([
    # Positions     # Texture Coords
     0.1, -0.2,     0.0, 1.0,  # Bottom-left
     0.5, -0.2,     1.0, 1.0,  # Bottom-right
     0.5,  0.2,     1.0, 0.0,  # Top-right
     0.1,  0.2,     0.0, 0.0,  # Top-left
], dtype=np.float32)

vertices_right = np.array([
    # Positions     # Texture Coords
    -0.5, -0.2,     0.0, 1.0,  # Bottom-left
    -0.1, -0.2,     1.0, 1.0,  # Bottom-right
    -0.1,  0.2,     1.0, 0.0,  # Top-right
    -0.5,  0.2,     0.0, 0.0,  # Top-left
], dtype=np.float32)

# OpenXR context and rendering
with xr.ContextObject(
    instance_create_info=xr.InstanceCreateInfo(
        enabled_extension_names=[xr.KHR_OPENGL_ENABLE_EXTENSION_NAME],
    ),
) as context:
    
    # Set up OpenGL
    program_left = create_program(vertex_src=VERTEX_SHARDER_SRC, fragment_src=FRAGMENT_SHARDER_SRC)
    program_right = create_program(vertex_src=VERTEX_SHARDER_SRC, fragment_src=FRAGMENT_SHARDER_SRC)
    
    VAO_left = set_up_opengl(vertices_left)
    VAO_right = set_up_opengl(vertices_right)

    # Rendering loop
    current_state = first_state
    last_state = None
    
    for frame_index, frame_state in enumerate(context.frame_loop()):
        # Check if current_state does not exxit
        if current_state is None:
            break

        if frame_index == 0:
            print("waiting few frames to let it get stable")
            continue
        elif frame_index < 10:
            continue
        elif frame_index == 10: 
            # Keeping record of the time at the beginnning of the experiment 
            current_info = State_Info()

        if current_state is not last_state:
            texture_id_left = current_state.require_texture_left()
            texture_id_right = current_state.require_texture_right()
        
        for view_index, view in enumerate(context.view_loop(frame_state)):
            
            GL.glClear(GL.GL_COLOR_BUFFER_BIT)

            # Bind the correct texture for the current eye
            if view_index == 0:
                GL.glUseProgram(program_left)
                GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id_left)
                GL.glBindVertexArray(VAO_left)
                GL.glDrawElements(GL.GL_TRIANGLES, INDICES_LEN, GL.GL_UNSIGNED_INT, None)
            elif view_index == 1:
                GL.glUseProgram(program_right)
                GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id_right)
                GL.glBindVertexArray(VAO_right)
                GL.glDrawElements(GL.GL_TRIANGLES, INDICES_LEN, GL.GL_UNSIGNED_INT, None)
        
        if key_pressed == 'a':
            print("Key 'A' pressed! Performing an action...")
            # Implement action for 'A'
        elif key_pressed == 'b':
            print("Key 'B' pressed! Performing another action...")
            # Implement action for 'B'   

        # update current state information  
        current_info.update_time()
        # End render current state, check update logic
        last_state = current_state
        current_state = current_state.check_state(current_info)
        

    listener.stop()
            
