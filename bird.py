from OpenGL.GL import *

class Bird:
    def __init__(self, texture_id):
        self.texture_id = texture_id
        self.height = 0.5  # Start in the middle of the screen
        self.speed = 0.0
        self.width = 0.1
        self.sprite_height = 0.3
        
    def update(self, delta_time, gravity):
        self.height += self.speed * delta_time
        self.speed += gravity * delta_time
        
        if self.height <= -0.4:  # Allow bird to fall to bottom of screen
            self.height = -0.4
            self.speed = 0
            
    def jump(self):
        self.speed = 3.5

    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-self.width, -0.4 + self.height, 0)

        glTexCoord2f(1.0, 0.0)
        glVertex3f(self.width, -0.4 + self.height, 0)

        glTexCoord2f(1.0, 1.0)
        glVertex3f(self.width, -0.4 + self.sprite_height + self.height, 0)

        glTexCoord2f(0.0, 1.0)
        glVertex3f(-self.width, -0.4 + self.sprite_height + self.height, 0)

        glEnd()

        glDisable(GL_TEXTURE_2D)
