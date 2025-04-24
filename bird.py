from OpenGL.GL import *
import time

class Bird:
    def __init__(self, texture_ids):
        self.texture_ids = texture_ids
        self.current_frame = 0
        self.frame_time = 0
        self.animation_speed = 0.1  # Tempo entre os frames em segundos
        self.last_frame_change = time.time()
        self.x_position = -0.6  # Mover o pássaro mais para a esquerda (de 0 a -0.6)
        self.height = 0.5  # Começar no centro da tela
        self.speed = 0.0
        self.width = 0.07  # Reduzido a partir de 0.1
        self.sprite_height = 0.1  # Diminuído de 0.3
        
    def update(self, delta_time, gravity):
        self.height += self.speed * delta_time
        self.speed += gravity * delta_time
        
        if self.height <= -0.4:  # Permitir que o pássaro caia até a parte inferior da tela
            self.height = -0.4
            self.speed = 0
            
        # Atualizar o quadro de animação
        current_time = time.time()
        if current_time - self.last_frame_change >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.texture_ids)
            self.last_frame_change = current_time
            
    def jump(self):
        self.speed = 1.7

    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[self.current_frame])

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(self.x_position - self.width, -0.4 + self.height, 0)

        glTexCoord2f(0.98, 0.0)
        glVertex3f(self.x_position + self.width, -0.4 + self.height, 0)

        glTexCoord2f(0.98, 1.0)
        glVertex3f(self.x_position + self.width, -0.4 + self.sprite_height + self.height, 0)

        glTexCoord2f(0.0, 1.0)
        glVertex3f(self.x_position - self.width, -0.4 + self.sprite_height + self.height, 0)

        glEnd()

        glDisable(GL_TEXTURE_2D)
        
    def get_bounding_box(self):
        # Retornar uma tupla (esquerda, fundo, direita, topo) para detecção de colisão
        left = self.x_position - self.width
        bottom = -0.4 + self.height
        right = self.x_position + self.width
        top = -0.4 + self.sprite_height + self.height
        return (left, bottom, right, top)
