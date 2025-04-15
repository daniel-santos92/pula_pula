import glfw
from OpenGL.GL import *

def init_window():
    if not glfw.init():
        return None
    
    window = glfw.create_window(800, 600, "Flappy Bird", None, None)
    if not window:
        glfw.terminate()
        return None
    
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    return window

def clear_screen():
    glClearColor(0.5, 0.7, 1.0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
