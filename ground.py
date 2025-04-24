from OpenGL.GL import *

class Ground:
    def __init__(self, texture_id):
        self.texture_id = texture_id
        self.position = -1.2  # Posicionar no fundo da tela
        self.width = 1.0       # Cobrir a largura total da tela
        self.height = 0.4     # altura do solo
        
    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, self.position, 0)
        
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1.0, self.position, 0)
        
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.0, self.position + self.height, 0)
        
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0, self.position + self.height, 0)
        glEnd()
        
        glDisable(GL_TEXTURE_2D)
