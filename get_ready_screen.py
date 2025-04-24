from OpenGL.GL import *
import time

class GetReadyScreen:
    def __init__(self, texture_id, tap_texture_ids=None):
        self.texture_id = texture_id
        self.tap_texture_ids = tap_texture_ids if tap_texture_ids else []
        self.current_tap_frame = 0
        self.last_frame_change = time.time()
        self.animation_speed = 0.3  # Tempo entre os frames em segundos

    def update(self):
        # Alternar entre os frames de toque
        current_time = time.time()
        if current_time - self.last_frame_change >= self.animation_speed and self.tap_texture_ids:
            self.current_tap_frame = (self.current_tap_frame + 1) % len(self.tap_texture_ids)
            self.last_frame_change = current_time

    def draw(self):
        # Desenhar a imagem de 'Preparar'
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.3, 0)
        glTexCoord2f(1.0, 0.03); glVertex3f( 0.5, -0.3, 0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 0.5,  0.3, 0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-0.5,  0.3, 0)
        glEnd()
        
        # Desenhar a imagem de 'Tap' embaixo da imagem de 'Get Ready
        if self.tap_texture_ids and len(self.tap_texture_ids) > 0:
            glBindTexture(GL_TEXTURE_2D, self.tap_texture_ids[self.current_tap_frame])
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0); glVertex3f(-0.3, -0.6, 0)
            glTexCoord2f(1.0, 0.0); glVertex3f( 0.3, -0.6, 0)
            glTexCoord2f(1.0, 0.98); glVertex3f( 0.3, -0.4, 0)
            glTexCoord2f(0.0, 0.98); glVertex3f(-0.3, -0.4, 0)
            glEnd()
            
        glDisable(GL_TEXTURE_2D)
