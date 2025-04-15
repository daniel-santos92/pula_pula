import time
import glfw
from renderer import clear_screen
from texture import load_texture
from bird import Bird

class GameEngine:
    def __init__(self):
        self.window = None
        self.bird = None
        self.gravity = -9.8
        self.prev_space_key_state = glfw.RELEASE
        self.previous_time = time.time()
        
    def init(self, window):
        self.window = window
        bird_texture = load_texture("img/bird/b0.png")
        self.bird = Bird(bird_texture)
        
    def process_input(self):
        space_key_state = glfw.get_key(self.window, glfw.KEY_SPACE)
        
        if space_key_state == glfw.PRESS and self.prev_space_key_state == glfw.RELEASE:
            self.bird.jump()
            
        self.prev_space_key_state = space_key_state
        
    def update(self):
        current_time = time.time()
        delta_time = current_time - self.previous_time
        self.previous_time = current_time
        delta_time = min(delta_time, 0.1)
        
        self.process_input()
        self.bird.update(delta_time, self.gravity)
        
    def render(self):
        clear_screen()
        self.bird.draw()
        
    def run(self):
        while not glfw.window_should_close(self.window):
            self.update()
            self.render()
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()
