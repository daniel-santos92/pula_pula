from OpenGL.GL import *

class Background:
    def __init__(self, texture_id):
        self.texture_id = texture_id
        self.darkness_level = 0.0  # 0.0 é o normal, 1.0 é preto absoluto
        
    def increase_darkness(self, amount=0.05):
        # Incrementar o nível de escuridão, mas limitar a 1.0 (preto total)
        self.darkness_level = min(1.0, self.darkness_level + amount)
        
    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # Calcular o brilho de acordo com o nível de escuridão
        # À medida que o nível de escuridão aumenta, os valores RGB ficam menores
        brightness = 1.0 - self.darkness_level
        glColor3f(brightness, brightness, brightness)
        
        glBegin(GL_QUADS)
        # Canto inferior esquerdo
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, -1, 0.0)
        
        # Canto inferior direito
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1.0, -1, 0.0)
        
        # Canto superior direito - ajustar coordenada de textura para 0.98 em vez de 1.0
        glTexCoord2f(1.0, 0.98)
        glVertex3f(1.0, 0.3, 0.0)
        
        # Canto superior esquerdo - ajustar coordenada de textura para 0.98 em vez de 1.0
        glTexCoord2f(0.0, 0.98)
        glVertex3f(-1.0, 0.3, 0.0)
        glEnd()
        
        # Restaurar a cor para branco
        glColor3f(1.0, 1.0, 1.0)
        glDisable(GL_TEXTURE_2D)
