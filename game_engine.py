import time
import random
import glfw
from renderer import clear_screen
from texture import load_texture
from bird import Bird
from ground import Ground
from background import Background
from pipe import Pipe

class GameEngine:
    def __init__(self):
        self.window = None
        self.bird = None
        self.ground = None
        self.pipes = []  # Lista para armazenar múltiplos canos
        self.gravity = -7.8
        self.prev_space_key_state = glfw.RELEASE
        self.previous_time = time.time()
        self.pipe_spawn_timer = 0
        self.pipe_spawn_interval = 2.0  # Tempo em segundos entre a criação de novos canos
        self.upper_pipe_texture = None
        self.lower_pipe_texture = None
        
    def init(self, window):
        self.window = window
        # Load all bird animation frames
        bird_textures = [
            load_texture("img/bird/b0.png"),
            load_texture("img/bird/b1.png"),
            load_texture("img/bird/b2.png"),
            load_texture("img/bird/b0.png")  # Include first frame again for smooth loop
        ]
        self.bird = Bird(bird_textures)
        
        # Load ground texture
        ground_texture = load_texture("img/ground.png")
        self.ground = Ground(ground_texture)

        # Load background texture
        background_texture = load_texture("img/BG.png")
        self.background = Background(background_texture)

        # Load pipe textures
        self.upper_pipe_texture = load_texture("img/toppipe.png")
        self.lower_pipe_texture = load_texture("img/botpipe.png")

        # Criar o primeiro cano
        self.spawn_pipe()
        
    def spawn_pipe(self):
        # Cria um novo cano no lado direito da tela
        gap_position = Pipe.generate_random_gap()
        new_pipe = Pipe(self.upper_pipe_texture, self.lower_pipe_texture, 1.2, gap_position)
        self.pipes.append(new_pipe)
        
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
        
        # Atualizar o timer para geração de canos
        self.pipe_spawn_timer += delta_time
        if self.pipe_spawn_timer >= self.pipe_spawn_interval:
            self.spawn_pipe()
            self.pipe_spawn_timer = 0
            
        # Atualizar todos os canos existentes
        pipes_to_remove = []
        for pipe in self.pipes:
            pipe.update(delta_time)
            
            # Marcar canos que saíram da tela para remoção
            if pipe.is_off_screen():
                pipes_to_remove.append(pipe)
                
        # Remover canos que saíram da tela
        for pipe in pipes_to_remove:
            self.pipes.remove(pipe)
        
    def render(self):
        clear_screen()
        self.background.draw()
        
        # Desenhar todos os canos
        for pipe in self.pipes:
            pipe.draw()
            
        self.ground.draw()
        self.bird.draw()
        
    def run(self):
        while not glfw.window_should_close(self.window):
            self.update()
            self.render()
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()
