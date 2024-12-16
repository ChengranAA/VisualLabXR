from state import state
from runtime import State_Info
from textrue import load_texture_from_image
from time import time 

# settings
iti = 2 # 2 Seconds
ibi = 3 # 3 Seconds

# Load textures
left_eye_texture = "../stimuli/grid_lines.png"
right_eye_texture = "../stimuli/grid_lines.png"

# Set up State Machine 
State1 = state()
State2 = state()

State1.Textures = [left_eye_texture, right_eye_texture]
State2.Textures = [right_eye_texture, left_eye_texture]

def first_update_func(state_info: State_Info):
    if state_info.get_elapsed_time() >= iti:
        state_info.reset_timer()
    return State1

def second_update_func(state_info: State_Info):
    if state_info.counter == iti:
        state_info.reset_counter()
        return State1
    return State2

State1.UpdateFun = first_update_func
State2.UpdateFun = second_update_func
    
first_state = State1