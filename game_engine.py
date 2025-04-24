import time
import random
import glfw
from OpenGL.GL import *
from renderer import clear_screen
from texture import load_texture
from bird import Bird
from ground import Ground
from background import Background
from pipe import Pipe
from score import Score
from get_ready_screen import GetReadyScreen
from game_over_screen import GameOverScreen
from enemy_bird import EnemyBird

class GameEngine:
    def __init__(self):
        self.window = None
        self.bird = None
        self.ground = None
        self.pipes = []  # Lista para armazenar múltiplos canos
        self.enemy_birds = []  # Lista para armazenar pássaros inimigos
        self.gravity = -7.8
        self.prev_space_key_state = glfw.RELEASE
        self.previous_time = time.time()
        self.pipe_spawn_timer = 0
        self.pipe_spawn_interval = 2.0  # Tempo em segundos entre a criação de novos canos
        self.enemy_bird_spawn_timer = 0
        self.enemy_bird_spawn_interval = random.uniform(8.0, 15.0)  # Intervalo aleatório de 10 a 15 segundos
        self.upper_pipe_texture = None
        self.lower_pipe_texture = None
        self.game_state = "READY"  # Estados do jogo: "READY", "PLAYING", "GAME_OVER"
        self.get_ready_texture = None
        self.game_over_texture = None
        self.tap_textures = []  # salvar os IDs das texturas de toque
        self.score = Score()
        self.get_ready_screen = None
        self.game_over_screen = None

    def init(self, window):
        self.window = window
        # Carregar todos os frames de animação do pássaro
        bird_textures = [
            load_texture("img/bird/b0.png"),
            load_texture("img/bird/b1.png"),
            load_texture("img/bird/b2.png"),
            load_texture("img/bird/b0.png")  # Adicionar o primeiro quadro novamente para um loop contínuo suave
        ]
        self.bird = Bird(bird_textures)
        
        # Guardar as texturas dos pássaros para os inimigos
        self.bird_textures = bird_textures
        
        # Carregar a textura do terreno
        ground_texture = load_texture("img/ground.png")
        self.ground = Ground(ground_texture)

        # Carregar a textura de plano de fundo
        background_texture = load_texture("img/BG.png")
        self.background = Background(background_texture)

        # Carregar as texturas dos canos do jogo
        self.upper_pipe_texture = load_texture("img/toppipe.png")
        self.lower_pipe_texture = load_texture("img/botpipe.png")
        
        # Carregar a textura de preparação
        self.get_ready_texture = load_texture("img/getready.png")
        
        # Carregar a textura de fim de jogo
        self.game_over_texture = load_texture("img/go.png")
        
        # Carregar as texturas de interação
        self.tap_textures = [
            load_texture("img/tap/t0.png"),
            load_texture("img/tap/t1.png")
        ]
        
        # initialize scoring
        self.score = Score()

        # instancia telas separadas
        self.get_ready_screen = GetReadyScreen(self.get_ready_texture, self.tap_textures)
        self.game_over_screen = GameOverScreen(self.game_over_texture)

    def reset_game(self):
        # Redefinir o estado do jogo para os valores iniciais
        self.bird = Bird(self.bird_textures)
        self.pipes = []
        self.enemy_birds = []
        self.pipe_spawn_timer = 0
        self.enemy_bird_spawn_timer = 0
        self.enemy_bird_spawn_interval = random.uniform(10.0, 15.0)
        self.game_state = "READY"
        self.score.reset()
        # RRestaurar o nível de escuridão do fundo
        self.background.darkness_level = 0.0
        
    def spawn_pipe(self):
        # Cria um novo cano no lado direito da tela
        gap_position = Pipe.generate_random_gap()
        new_pipe = Pipe(self.upper_pipe_texture, self.lower_pipe_texture, 1.2, gap_position, self.score)
        self.pipes.append(new_pipe)
        
    def spawn_enemy_bird(self):
        # Criar um novo pássaro inimigo surgindo do lado direito da tela
        new_enemy_bird = EnemyBird(self.bird_textures)
        self.enemy_birds.append(new_enemy_bird)
        # Estabelecer um novo intervalo aleatório para o surgimento do próximo pássaro
        self.enemy_bird_spawn_interval = random.uniform(8.0, 15.0)
        # Reiniciar o tempo para que outro pássaro possa aparecer depois do intervalo
        self.enemy_bird_spawn_timer = 0
        
    def process_input(self):
        space_key_state = glfw.get_key(self.window, glfw.KEY_SPACE)
        
        if space_key_state == glfw.PRESS and self.prev_space_key_state == glfw.RELEASE:
            if self.game_state == "READY":
                # Muda para o estado de jogo quando a tecla espaço for pressionada pela primeira vez
                self.game_state = "PLAYING"
                # Agora o pássaro começa a cair
                self.bird.update(0.01, self.gravity)
            elif self.game_state == "PLAYING":
                # Comportamento normal de pulo durante o jogo
                self.bird.jump()
            elif self.game_state == "GAME_OVER":
                # Reiniciar o jogo quando pressionar espaço após game over
                self.reset_game()
            
        self.prev_space_key_state = space_key_state
    
    def check_collisions(self):
        # Capturar a área delimitadora do pássaro
        bird_box = self.bird.get_bounding_box()
        
        # Verificação simplificada de colisão com o chão
        if bird_box[1] <= -0.8:  # O fundo da tela está por volta de -0,4
            return True
            
        # Checar colisão com a parte superior da tela
        if bird_box[3] >= 1.0:  # Parte superior da tela (y=1.0)
            return True
            
        # Checar colisão com os canos
        for pipe in self.pipes:
            upper_pipe_box = pipe.get_upper_pipe_box()
            lower_pipe_box = pipe.get_lower_pipe_box()
            
            # Detectar se a caixa de colisão do pássaro toca em qualquer um dos canos
            # Para detectar a interseção, checamos se as caixas se sobrepõem nas direções x e y
            
            # Colisão com o canos superior
            if (bird_box[0] < upper_pipe_box[2] and bird_box[2] > upper_pipe_box[0] and 
                bird_box[1] < upper_pipe_box[3] and bird_box[3] > upper_pipe_box[1]):
                return True
                
            # Colisão com o canos inferior
            if (bird_box[0] < lower_pipe_box[2] and bird_box[2] > lower_pipe_box[0] and 
                bird_box[1] < lower_pipe_box[3] and bird_box[3] > lower_pipe_box[1]):
                return True
                
        # Detectar colisão com os pássaros inimigos
        for enemy_bird in self.enemy_birds:
            enemy_box = enemy_bird.get_bounding_box()
            
            # Checar se a caixa de colisão do pássaro do jogador colide com o pássaro inimigo
            if (bird_box[0] < enemy_box[2] and bird_box[2] > enemy_box[0] and
                bird_box[1] < enemy_box[3] and bird_box[3] > enemy_box[1]):
                return True
                
        return False
        
    def update(self):
        current_time = time.time()
        delta_time = current_time - self.previous_time
        self.previous_time = current_time
        delta_time = min(delta_time, 0.1)
        
        self.process_input()
        
        # Atualizar a animação da tela de 'Prepare-se' se estiver no estado PRONTO
        if self.game_state == "READY":
            self.get_ready_screen.update()
        
        # Somente atualiza o jogo se estiver no estado PLAYING
        if self.game_state == "PLAYING":
            # Ajustar o multiplicador de velocidade de acordo com a pontuação
            new_multiplier = 1.0 + (self.score.value // 5) * 0.1
            self.speed_multiplier = min(new_multiplier, 2.0)  # Cap at 2x speed
            
            self.bird.update(delta_time, self.gravity)
            
            # Atualizar o timer para geração de canos
            self.pipe_spawn_timer += delta_time
            if self.pipe_spawn_timer >= self.pipe_spawn_interval:
                self.spawn_pipe()
                self.pipe_spawn_timer = 0
                
            # Atualizar o timer de surgimento dos pássaros inimigos
            self.enemy_bird_spawn_timer += delta_time
            if self.enemy_bird_spawn_timer >= self.enemy_bird_spawn_interval:
                self.spawn_enemy_bird()
                self.enemy_bird_spawn_timer = 0
                
            # Atualizar todos os canos existentes
            pipes_to_remove = []
            for pipe in self.pipes:
                pipe.update(delta_time, self.speed_multiplier)
                
                # Verificar se o pássaro passou pelo cano e ainda não foi contabilizado
                if not pipe.passed and pipe.x_position < self.bird.x_position - self.bird.width:
                    pipe.passed = True
                    self.score.increment()
                    # Aumentar a escuridão ao passar pelo cano
                    self.background.increase_darkness(0.1)
                
                # Marcar canos que saíram da tela para remoção
                if pipe.is_off_screen():
                    pipes_to_remove.append(pipe)
                    
            # Remover canos que saíram da tela
            for pipe in pipes_to_remove:
                self.pipes.remove(pipe)
                
            # Atualizar os pássaros adversários
            enemy_birds_to_remove = []
            for enemy_bird in self.enemy_birds:
                enemy_bird.update(delta_time)
                
                # Identificar os pássaros inimigos que saíram da tela para remoção
                if enemy_bird.is_off_screen():
                    enemy_birds_to_remove.append(enemy_bird)
                    
            # Remover os pássaros inimigos fora da tela
            for enemy_bird in enemy_birds_to_remove:
                self.enemy_birds.remove(enemy_bird)
                
            # Detectar colisões
            if self.check_collisions():
                self.game_state = "GAME_OVER"
    
    def render(self):
        clear_screen()
        self.background.draw()
        
        # Desenhar os elementos do jogo de acordo com o estado atual
        if self.game_state == "READY":
            # No estado READY, desenha apenas o fundo, o pássaro e a imagem "Get Ready"
            self.ground.draw()
            self.bird.draw()
            self.get_ready_screen.draw()
        elif self.game_state == "PLAYING":
            # No estado PLAYING, desenha todos os elementos do jogo
            for pipe in self.pipes:
                pipe.draw()
                
            # Renderizar os pássaros inimigos
            for enemy_bird in self.enemy_birds:
                enemy_bird.draw()
                
            self.ground.draw()
            self.bird.draw()
            self.score.draw()
        elif self.game_state == "GAME_OVER":
            # No estado GAME_OVER, desenha todos os elementos congelados e a imagem de game over
            for pipe in self.pipes:
                pipe.draw()
                
            # Renderizar os pássaros inimigos
            for enemy_bird in self.enemy_birds:
                enemy_bird.draw()
                
            self.ground.draw()
            self.bird.draw()
            self.game_over_screen.draw()
            self.score.draw()
        
    def run(self):
        while not glfw.window_should_close(self.window):
            self.update()
            self.render()
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()
