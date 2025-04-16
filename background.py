from OpenGL.GL import *

class Background:
    def __init__(self, texture_id):
        self.texture_id = texture_id
        
    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
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
        
        glDisable(GL_TEXTURE_2D)
