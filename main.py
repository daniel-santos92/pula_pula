import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image, ImageDraw, ImageFont
import time
import numpy as np
import random
import math

# Função para carregar uma imagem e criar uma textura OpenGL
def load_texture(path):
    try:
        image = Image.open(path).convert("RGBA")
    except Exception as e:
        print(f"Erro ao carregar {path}: {e}")
        return None, 0, 0
    image_data = image.tobytes("raw", "RGBA", 0, -1)
    width, height = image.size
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    return texture, width, height

# Função para desenhar um quad texturizado (com opção de rotação e centro)
def draw_texture(texture, x, y, width, height, rotation=0, center=None):
    glPushMatrix()
    if center is not None:
        # Translada para (x+center) e depois aplica rotação e retorna
        glTranslatef(x + center[0], y + center[1], 0)
        glRotatef(rotation, 0, 0, 1)
        glTranslatef(-center[0], -center[1], 0)
    else:
        glTranslatef(x, y, 0)
        glRotatef(rotation, 0, 0, 1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(0, 0)
    glTexCoord2f(1, 0); glVertex2f(width, 0)
    glTexCoord2f(1, 1); glVertex2f(width, height)
    glTexCoord2f(0, 1); glVertex2f(0, height)
    glEnd()
    glPopMatrix()

# Função para renderizar texto via PIL e desenhar como textura
def draw_text(text, x, y, font_size=20):
    # Utiliza a fonte padrão – se desejar, pode carregar uma fonte TrueType
    font = ImageFont.load_default()
    # Cria uma imagem com o tamanho necessário para o texto
    dummy_img = Image.new("RGBA", (1,1))
    draw = ImageDraw.Draw(dummy_img)
    text_size = draw.textsize(text, font=font)
    text_img = Image.new("RGBA", text_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_img)
    draw.text((0, 0), text, font=font, fill=(255,255,255,255))
    
    text_data = text_img.tobytes("raw", "RGBA", 0, -1)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_size[0], text_size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    draw_texture(texture, x, y, text_size[0], text_size[1])
    glDeleteTextures([texture])

# Classes que representam os elementos do jogo

class Background:
    def __init__(self, game):
        self.game = game
        self.texture, self.width, self.height = load_texture("img/BG.png")
    def draw(self):
        # Desenha o fundo com base na altura da janela
        y = self.game.height - self.height
        draw_texture(self.texture, 0, y, self.width, self.height)

class Ground:
    def __init__(self, game):
        self.game = game
        self.texture, self.width, self.height = load_texture("img/ground.png")
        self.x = 0
    def update(self):
        if self.game.state != Game.PLAY:
            return
        self.x -= self.game.dx
        # "wrap-around": reinicia o deslocamento quando passa de metade da largura da textura
        self.x = self.x % (self.width / 2)
    def draw(self):
        y = self.game.height - self.height
        draw_texture(self.texture, self.x, y, self.width, self.height)

class PipeManager:
    def __init__(self, game):
        self.game = game
        self.top_texture, self.top_width, self.top_height = load_texture("img/toppipe.png")
        self.bot_texture, self.bot_width, self.bot_height = load_texture("img/botpipe.png")
        self.gap = 85
        self.pipes = []  # Cada pipe será um dicionário com "x" e "y"
        self.moved = True
    def update(self):
        if self.game.state != Game.PLAY:
            return
        if self.game.frames % 100 == 0:
            new_pipe = {
                "x": self.game.width,
                "y": -210 * min(random.random() + 1, 1.8)
            }
            self.pipes.append(new_pipe)
        for pipe in self.pipes:
            pipe["x"] -= self.game.dx
        if self.pipes and self.pipes[0]["x"] < -self.top_width:
            self.pipes.pop(0)
            self.moved = True
    def draw(self):
        for p in self.pipes:
            x = p["x"]
            y = p["y"]
            # Desenha o cano superior
            draw_texture(self.top_texture, x, y, self.top_width, self.top_height)
            # Desenha o cano inferior; o y é ajustado com a altura do cano superior + gap
            draw_texture(self.bot_texture, x, y + self.top_height + self.gap, self.bot_width, self.bot_height)

class Bird:
    def __init__(self, game):
        self.game = game
        # Carrega as imagens da animação do pássaro
        self.frames_textures = []
        paths = ["img/bird/b0.png", "img/bird/b1.png", "img/bird/b2.png", "img/bird/b0.png"]
        for p in paths:
            tex, w, h = load_texture(p)
            self.frames_textures.append((tex, w, h))
        self.x = 50
        self.y = 100
        self.speed = 0.0
        self.gravity = 0.125
        self.thrust = 3.6
        self.frame = 0
        self.rotation = 0  # em graus
    def update(self):
        if self.game.state == Game.GET_READY:
            self.rotation = 0
            if self.game.frames % 10 == 0:
                self.y += math.sin(self.game.frames)  # pequeno movimento oscilatório
                self.frame = (self.frame + 1) % len(self.frames_textures)
        elif self.game.state == Game.PLAY:
            if self.game.frames % 5 == 0:
                self.frame = (self.frame + 1) % len(self.frames_textures)
            self.y += self.speed
            self.set_rotation()
            self.speed += self.gravity
            # Verifica colisão com o solo
            ground_y = self.game.height - self.game.ground.height
            tex0, w, h = self.frames_textures[0]
            r = (h/4 + w/4)
            if self.y + r >= ground_y or self.check_collision():
                self.game.state = Game.GAME_OVER
        elif self.game.state == Game.GAME_OVER:
            self.frame = 1
            tex0, w, h = self.frames_textures[0]
            r = (h/4 + w/4)
            if self.y + r < self.game.height - self.game.ground.height:
                self.y += self.speed
                self.set_rotation()
                self.speed += self.gravity * 2
            else:
                self.speed = 0
                self.y = self.game.height - self.game.ground.height - r
                self.rotation = 90
        self.frame %= len(self.frames_textures)
    def draw(self):
        tex, w, h = self.frames_textures[self.frame]
        # Desenha o pássaro centrado (a rotação é aplicada em torno do centro)
        draw_texture(tex, self.x, self.y, w, h, rotation=self.rotation, center=(w/2, h/2))
    def flap(self):
        if self.y > 0:
            # Aqui seria reproduzido o efeito sonoro (não implementado)
            self.speed = -self.thrust
    def set_rotation(self):
        if self.speed <= 0:
            self.rotation = max(-25, (-25 * self.speed) / (-1 * self.thrust) if self.thrust != 0 else -25)
        else:
            self.rotation = min(90, (90 * self.speed) / (self.thrust * 2))
    def check_collision(self):
        if not self.game.pipes.pipes:
            return False
        # Verifica colisão com o primeiro cano da lista
        p = self.game.pipes.pipes[0]
        x_pipe = p["x"]
        y_pipe = p["y"]
        tex0, w, h = self.frames_textures[0]
        r = (h/4 + w/4)
        roof = y_pipe + self.game.pipes.top_height
        floor = roof + self.game.pipes.gap
        w_pipe = self.game.pipes.top_width
        if self.x + r >= x_pipe:
            if self.x + r < x_pipe + w_pipe:
                if self.y - r <= roof or self.y + r >= floor:
                    # Aqui seria reproduzido o efeito de colisão
                    return True
            elif self.game.pipes.moved:
                self.game.ui.score += 1
                self.game.pipes.moved = False
        return False

class UI:
    def __init__(self, game):
        self.game = game
        self.get_ready_texture, self.get_ready_width, self.get_ready_height = load_texture("img/getready.png")
        self.game_over_texture, self.game_over_width, self.game_over_height = load_texture("img/go.png")
        # Imagens "tap" para indicação
        self.tap_textures = []
        tex, w, h = load_texture("img/tap/t0.png")
        self.tap_textures.append((tex, w, h))
        tex, w, h = load_texture("img/tap/t1.png")
        self.tap_textures.append((tex, w, h))
        self.tap_frame = 0
        self.score = 0
        self.best = 0
    def update(self):
        if self.game.state == Game.PLAY:
            return
        if self.game.frames % 10 == 0:
            self.tap_frame = (self.tap_frame + 1) % len(self.tap_textures)
    def draw(self):
        if self.game.state == Game.GET_READY:
            x = (self.game.width - self.get_ready_width) / 2
            y = (self.game.height - self.get_ready_height) / 2
            draw_texture(self.get_ready_texture, x, y, self.get_ready_width, self.get_ready_height)
            tap_tex, tap_w, tap_h = self.tap_textures[self.tap_frame]
            tx = (self.game.width - tap_w) / 2
            ty = y + self.get_ready_height - tap_h
            draw_texture(tap_tex, tx, ty, tap_w, tap_h)
        elif self.game.state == Game.GAME_OVER:
            x = (self.game.width - self.game_over_width) / 2
            y = (self.game.height - self.game_over_height) / 2
            draw_texture(self.game_over_texture, x, y, self.game_over_width, self.game_over_height)
            tap_tex, tap_w, tap_h = self.tap_textures[self.tap_frame]
            tx = (self.game.width - tap_w) / 2
            ty = y + self.game_over_height - tap_h
            draw_texture(tap_tex, tx, ty, tap_w, tap_h)
        self.draw_score()
    def draw_score(self):
        if self.game.state == Game.PLAY:
            # Desenha a pontuação no topo central
            draw_text(str(self.score), self.game.width/2 - 5, 50, font_size=35)
        elif self.game.state == Game.GAME_OVER:
            # Atualiza o recorde
            self.best = max(self.best, self.score)
            sc_text = f"SCORE :     {self.score}"
            bs_text = f"BEST  :     {self.best}"
            x = self.game.width / 2 - 80
            y = self.game.height / 2
            draw_text(sc_text, x, y, font_size=40)
            draw_text(bs_text, x, y + 30, font_size=40)

class Game:
    GET_READY = 0
    PLAY = 1
    GAME_OVER = 2
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.state = Game.GET_READY
        self.frames = 0
        self.dx = 2
        self.background = Background(self)
        self.ground = Ground(self)
        self.pipes = PipeManager(self)
        self.bird = Bird(self)
        self.ui = UI(self)
    def update(self):
        self.bird.update()
        self.ground.update()
        self.pipes.update()
        self.ui.update()
        self.frames += 1
    def draw(self):
        # Preenche o fundo com a cor #30c0df (valor aproximado em float)
        glClearColor(0.188, 0.75, 0.87, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        self.background.draw()
        self.pipes.draw()
        self.bird.draw()
        self.ground.draw()
        self.ui.draw()

# Manipulação de entrada: clique do mouse e teclas
def handle_input():
    global game
    if game.state == Game.GET_READY:
        game.state = Game.PLAY
        # Aqui seria reproduzido SFX.start
    elif game.state == Game.PLAY:
        game.bird.flap()
    elif game.state == Game.GAME_OVER:
        game.state = Game.GET_READY
        game.bird.speed = 0
        game.bird.y = 100
        game.pipes.pipes = []
        game.ui.score = 0
        game.pipes.moved = True

def on_mouse_button(window, button, action, mods):
    if action == glfw.PRESS:
        handle_input()

def on_key(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        if key in [glfw.KEY_SPACE, glfw.KEY_W, glfw.KEY_UP]:
            handle_input()

# Função principal do jogo
def main():
    global game
    if not glfw.init():
        return
    width, height = 288, 512  # tamanho da janela similar ao original
    window = glfw.create_window(width, height, "Flappy Bird (PyOpenGL)", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Define uma projeção ortográfica onde (0,0) é o canto superior esquerdo
    glOrtho(0, width, height, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_TEXTURE_2D)
    
    glfw.set_mouse_button_callback(window, on_mouse_button)
    glfw.set_key_callback(window, on_key)
    
    game = Game(width, height)
    
    # Loop principal
    while not glfw.window_should_close(window):
        glfw.poll_events()
        game.update()
        game.draw()
        glfw.swap_buffers(window)
        time.sleep(0.02)
    glfw.terminate()

if __name__ == "__main__":
    main()