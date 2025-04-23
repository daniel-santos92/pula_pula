from OpenGL.GL import *

class Background:
    def __init__(self, texture_id):
        self.texture_id = texture_id
        self.darkness_level = 0.0  # 0.0 is normal, 1.0 is pitch black
        
    def increase_darkness(self, amount=0.05):
        # Increase darkness level, but cap at 1.0 (pitch black)
        self.darkness_level = min(1.0, self.darkness_level + amount)
        
    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # Calculate brightness based on darkness level
        # As darkness increases, RGB values decrease
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
        
        # Reset color to white
        glColor3f(1.0, 1.0, 1.0)
        glDisable(GL_TEXTURE_2D)
