from OpenGL.GL import *
import random

class Pipe:
    def __init__(self, upper_texture_id, lower_texture_id, x_position, gap_position=0.0, score=0):
        self.upper_texture_id = upper_texture_id
        self.lower_texture_id = lower_texture_id
        self.x_position = x_position
        self.gap_position = gap_position  # Posição vertical do centro da abertura
        self.height = 0.7
        self.width = 0.15
        self.gap_size = 0.4  # Tamanho FIXO da abertura entre os canos
        self.gap_size = 0.4    # Tamanho FIXO da abertura entre os canos
        self.passed = False  # Indica se o pássaro já passou por este cano
        self.score = score
        self.base_speed = 0.5  # Velocidade base dos canos
        self.max_speed = 3.0  # Velocidade máxima dos canos
        self.speed_multiplier = 0.1  # Multiplicador de velocidade dos canos
        
    def update(self, delta_time, speed_multiplier=1.0):
        # Move o cano para a esquerda (valores negativos de x)
        # A velocidade é ajustada com base no multiplicador de velocidade
        self.x_position -= self.base_speed * min(speed_multiplier + self.score.value, self.max_speed) * delta_time
        
    def is_off_screen(self):
        # Verifica se o cano saiu completamente da tela pela esquerda
        return self.x_position < -1.2
        
    @staticmethod
    def generate_random_gap():
        # Gera apenas a posição vertical do gap, garantindo que não fique muito alto ou baixo
        # Limitando entre -0.3 e 0.3 para manter os canos visíveis na tela
        return random.uniform(-0.3, 0.3)
        
    def draw(self):
        glEnable(GL_TEXTURE_2D)
        
        # Metade do tamanho da abertura - sempre constante
        half_gap = self.gap_size / 2
        
        # Draw upper pipe - começa exatamente no ponto superior do gap
        glBindTexture(GL_TEXTURE_2D, self.upper_texture_id)
        glBegin(GL_QUADS)
        
        upper_pipe_bottom = self.gap_position + half_gap  # Posição inferior do cano superior
        
        glTexCoord2f(0.0, 0.0)
        glVertex3f(self.x_position - self.width, upper_pipe_bottom, 0)
        
        glTexCoord2f(1.0, 0.0)
        glVertex3f(self.x_position + self.width, upper_pipe_bottom, 0)
        
        glTexCoord2f(1.0, 1.0)
        glVertex3f(self.x_position + self.width, 1.0, 0)
        
        glTexCoord2f(0.0, 1.0)
        glVertex3f(self.x_position - self.width, 1.0, 0)
        glEnd()
        
        # Draw lower pipe - termina exatamente no ponto inferior do gap
        glBindTexture(GL_TEXTURE_2D, self.lower_texture_id)
        glBegin(GL_QUADS)
        
        lower_pipe_top = self.gap_position - half_gap  # Posição superior do cano inferior
        
        glTexCoord2f(0.0, 0.0)
        glVertex3f(self.x_position - self.width, -1.0, 0)
        
        glTexCoord2f(1.0, 0.0)
        glVertex3f(self.x_position + self.width, -1.0, 0)
        
        glTexCoord2f(1.0, 1.0)
        glVertex3f(self.x_position + self.width, lower_pipe_top, 0)
        
        glTexCoord2f(0.0, 1.0)
        glVertex3f(self.x_position - self.width, lower_pipe_top, 0)
        glEnd()
        
        glDisable(GL_TEXTURE_2D)
        
    def get_upper_pipe_box(self):
        # Bounding box for the upper pipe (left, bottom, right, top)
        half_gap = self.gap_size / 2
        upper_pipe_bottom = self.gap_position + half_gap
        return (self.x_position - self.width, upper_pipe_bottom, 
                self.x_position + self.width, 1.0)
                
    def get_lower_pipe_box(self):
        # Bounding box for the lower pipe (left, bottom, right, top)
        half_gap = self.gap_size / 2
        lower_pipe_top = self.gap_position - half_gap
        return (self.x_position - self.width, -1.0, 
                self.x_position + self.width, lower_pipe_top)