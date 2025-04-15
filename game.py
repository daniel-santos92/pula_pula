import glfw
from renderer import init_window
from game_engine import GameEngine

def main():
    window = init_window()
    if not window:
        return
    
    game = GameEngine()
    game.init(window)
    game.run()
    
    glfw.terminate()

if __name__ == "__main__":
    main()
