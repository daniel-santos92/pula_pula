from OpenGL.GL import *
import random
import time

class EnemyBird:
    def __init__(self, texture_ids):
        self.texture_ids = texture_ids
        self.current_frame = 0
        self.frame_time = 0
        self.animation_speed = 0.1  # Time between frames in seconds
        self.last_frame_change = time.time()
        self.x_position = 1.2  # Start from right side of screen
        self.height = random.uniform(-0.6, 0.6)  # Random height within visible area
        self.speed = 0.7  # Speed of movement (from right to left)
        self.width = 0.07  # Same as player bird
        self.sprite_height = 0.1  # Same as player bird
        
    def update(self, delta_time):
        # Move bird from right to left
        self.x_position -= self.speed * delta_time
        
        # Update animation frame
        current_time = time.time()
        if current_time - self.last_frame_change >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.texture_ids)
            self.last_frame_change = current_time
            
    def is_off_screen(self):
        # Check if the bird has left the screen
        return self.x_position < -1.2
            
    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[self.current_frame])
        
        # Set color to red tint
        glColor3f(1.0, 0.5, 0.5)  # Red tint

        glBegin(GL_QUADS)
        # Flip the texture coordinates horizontally to make bird face left
        glTexCoord2f(0.98, 0.0)
        glVertex3f(self.x_position - self.width, -0.4 + self.height, 0)

        glTexCoord2f(0.0, 0.0)
        glVertex3f(self.x_position + self.width, -0.4 + self.height, 0)

        glTexCoord2f(0.0, 1.0)
        glVertex3f(self.x_position + self.width, -0.4 + self.sprite_height + self.height, 0)

        glTexCoord2f(0.98, 1.0)
        glVertex3f(self.x_position - self.width, -0.4 + self.sprite_height + self.height, 0)
        glEnd()

        # Reset color
        glColor3f(1.0, 1.0, 1.0)
        glDisable(GL_TEXTURE_2D)
        
    def get_bounding_box(self):
        # Return a tuple (left, bottom, right, top) for collision detection
        left = self.x_position - self.width
        bottom = -0.4 + self.height
        right = self.x_position + self.width
        top = -0.4 + self.sprite_height + self.height
        return (left, bottom, right, top) 