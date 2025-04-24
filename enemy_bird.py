from OpenGL.GL import *
import random
import time

class EnemyBird:
    def __init__(self, texture_ids):
        self.texture_ids = texture_ids
        self.current_frame = 0
        self.frame_time = 0
        self.animation_speed = 0.1  # Tempo entre os frames em segundos
        self.last_frame_change = time.time()
        self.x_position = 1.2  # Iniciar do lado direito da tela
        self.height = random.uniform(-0.6, 0.6)  # Altura aleatória na área visível
        self.speed = 0.7  # Velocidade do movimento (da direita para a esquerda)
        self.width = 0.07  # Semelhante ao pássaro do jogador
        self.sprite_height = 0.1  
        
    def update(self, delta_time):
        # "Deslocar o pássaro da direita para a esquerda
        self.x_position -= self.speed * delta_time
        
        # Atualizar o frame da animação
        current_time = time.time()
        if current_time - self.last_frame_change >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.texture_ids)
            self.last_frame_change = current_time
            
    def is_off_screen(self):
        # Checar se o pássaro deixou a tela
        return self.x_position < -1.2
            
    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[self.current_frame])
        
        # Definir a cor para um tom de vermelho
        glColor3f(1.0, 0.5, 0.5)  # Red tint

        glBegin(GL_QUADS)
        # Inverter as coordenadas da textura na horizontal para o pássaro ficar voltado para a esquerda
        glTexCoord2f(0.98, 0.0)
        glVertex3f(self.x_position - self.width, -0.4 + self.height, 0)

        glTexCoord2f(0.0, 0.0)
        glVertex3f(self.x_position + self.width, -0.4 + self.height, 0)

        glTexCoord2f(0.0, 1.0)
        glVertex3f(self.x_position + self.width, -0.4 + self.sprite_height + self.height, 0)

        glTexCoord2f(0.98, 1.0)
        glVertex3f(self.x_position - self.width, -0.4 + self.sprite_height + self.height, 0)
        glEnd()

        # Reiniciar a cor
        glColor3f(1.0, 1.0, 1.0)
        glDisable(GL_TEXTURE_2D)
        
    def get_bounding_box(self):
        # Devolver uma tupla (esquerda, inferior, direita, superior) para a detecção de colisão
        left = self.x_position - self.width
        bottom = -0.4 + self.height
        right = self.x_position + self.width
        top = -0.4 + self.sprite_height + self.height
        return (left, bottom, right, top) 