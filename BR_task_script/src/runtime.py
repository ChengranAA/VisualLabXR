from time import time

class State_Info:
    def __init__(self):
        self.counter = 0
        self.current_time = None
        self.last_time = time()
        self.keyboard_state = {}
    
    def update_time(self):
        self.current_time = time()

    def get_elapsed_time(self):
        return self.current_time - self.last_time

    def reset_timer(self):
        self.current_time = time()
        self.last_time = self.current_time