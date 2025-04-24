from OpenGL.GL import *
import time

class Bird:
    def __init__(self, texture_ids):
        self.texture_ids = texture_ids
        self.current_frame = 0
        self.frame_time = 0
        self.animation_speed = 0.1
        self.last_frame_change = time.time()
        self.x_position = -0.6
        self.height = 0.5
        self.speed = 0.0
        self.width = 0.07
        self.sprite_height = 0.1

        # Parâmetros refinados para suavidade
        self.gravity = -2.0         # gravidade bem mais leve
        self.jump_velocity = 0.9    # pulo mais suave
        self.max_fall_speed = -0.8  # queda controlada
        self.damping = 0.995        # amortecimento maior

    def update(self, delta_time, _):
        # Aplica física de queda com gravidade e amortecimento
        self.speed += self.gravity * delta_time
        self.speed *= self.damping  # amortecimento gradual

        # Limitar velocidade máxima de queda
        if self.speed < self.max_fall_speed:
            self.speed = self.max_fall_speed

        # Atualizar altura com base na velocidade
        self.height += self.speed * delta_time

        # Limitar a altura mínima (chão)
        if self.height <= -0.4:
            self.height = -0.4
            self.speed = 0

        # Atualizar frame de animação
        current_time = time.time()
        if current_time - self.last_frame_change >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.texture_ids)
            self.last_frame_change = current_time

    def jump(self):
        self.speed = self.jump_velocity

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
        left = self.x_position - self.width
        bottom = -0.4 + self.height
        right = self.x_position + self.width
        top = -0.4 + self.sprite_height + self.height
        return (left, bottom, right, top)
