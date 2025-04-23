from OpenGL.GL import *
import time

class Bird:
    def __init__(self, texture_ids):
        self.texture_ids = texture_ids
        self.current_frame = 0
        self.frame_time = 0
        self.animation_speed = 0.1  # Time between frames in seconds
        self.last_frame_change = time.time()
        self.x_position = -0.6  # Position bird more to the left (from 0 to -0.6)
        self.height = 0.5  # Start in the middle of the screen
        self.speed = 0.0
        self.width = 0.07  # Reduced from 0.1
        self.sprite_height = 0.1  # Reduced from 0.3
        
    def update(self, delta_time, gravity):
        self.height += self.speed * delta_time
        self.speed += gravity * delta_time
        
        if self.height <= -0.4:  # Allow bird to fall to bottom of screen
            self.height = -0.4
            self.speed = 0
            
        # Update animation frame
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
        # Return a tuple (left, bottom, right, top) for collision detection
        left = self.x_position - self.width
        bottom = -0.4 + self.height
        right = self.x_position + self.width
        top = -0.4 + self.sprite_height + self.height
        return (left, bottom, right, top)
