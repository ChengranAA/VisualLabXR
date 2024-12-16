from runtime import State_Info
from textrue import load_texture_from_image

class state():
    def __init__(self):
        self.StateInfo = None
        self.Textures = [] # from left to right 
        self.UpdateFun = None 
        
    def __repr__(self):
        return self.StateInfo
        
    def check_state(self, state_info: State_Info):
        if self.UpdateFun is None:
            return None
        return self.UpdateFun(state_info)
    
    def require_texture_left(self):
        return load_texture_from_image(self.Textures[0])
    
    def require_texture_right(self):
        return load_texture_from_image(self.Textures[1])
        
            
        
    
        
    
    