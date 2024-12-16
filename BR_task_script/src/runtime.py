from time import time

class State_Info:
    def __init__(self):
        self.counter = 0
        self.current_time = None
        self.last_time = None 
    
    def update_counter(self, default = 1):
        self.counter += default
    
    def reset_counter(self, default = 0):
        self.counter = default