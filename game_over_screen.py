from OpenGL.GL import *

class GameOverScreen:
    def __init__(self, texture_id):
        self.texture_id = texture_id

    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.3, 0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 0.5, -0.3, 0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 0.5,  0.3, 0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-0.5,  0.3, 0)
        glEnd()
        glDisable(GL_TEXTURE_2D)
