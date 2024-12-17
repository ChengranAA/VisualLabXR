from Example_VR_Template.BR_task_script.VisualLabXR.experiment.opengl_related import wrappers
import xr 
import numpy as np 
from graphics import defaults, shader

class core:
    def __init__(self, entry):
        self._vertices = {"left": defaults.DEFAULT_VERTICES_LEFT, "right": defaults.DEFAULT_VERTICES_RIGHT}
        self._programs = None
        self._VAO = None
        self.entry = entry
        
    def init_gl(self):
        self._programs = {"left": shader.create_program(defaults.VERTEX_SHARDER_SRC, defaults.FRAGMENT_SHARDER_SRC)}
        self._VAO = {"left", wrappers.set_up_opengl(self._vertices["left"]), wrappers.opengl_setup(self._vertices["right"])}
        
        
    def run(self):
        with xr.ContextObject(
            instance_create_info=xr.InstanceCreateInfo(
            enabled_extension_names=[xr.KHR_OPENGL_ENABLE_EXTENSION_NAME],
        ),
        ) as context:
            self.init_gl()
        # Rendering loop
            counter = 0
            current_state = self.entry
            current_info = State_Info()

            for frame_index, frame_state in enumerate(context.frame_loop()): 
                # Check if current_state does not exxit
                if current_state is None:
                    break

                for view_index, view in enumerate(context.view_loop(frame_state)):

                    GL.glClear(GL.GL_COLOR_BUFFER_BIT)

                    # Bind the correct texture for the current eye
                    if view_index == 0:
                        GL.glUseProgram(self._programs["left"])
                        GL.glBindTexture(GL.GL_TEXTURE_2D, current_state.require_texture_left())
                        GL.glBindVertexArray(self._VAO["left"])
                        GL.glDrawElements(GL.GL_TRIANGLES, INDICES_LEN, GL.GL_UNSIGNED_INT, None)
                    elif view_index == 1:
                        GL.glUseProgram(program_right)
                        GL.glBindTexture(GL.GL_TEXTURE_2D, current_state.require_texture_right())
                        GL.glBindVertexArray(VAO_right)
                        GL.glDrawElements(GL.GL_TRIANGLES, INDICES_LEN, GL.GL_UNSIGNED_INT, None)


                # update current state information  
                current_info.update_counter()

                # End render current state, check update logic
                current_state = current_state.check_state(current_info)
