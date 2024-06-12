import sys
import pygame
from PongGame import PongGame

if __name__ == "__main__":
    pygame.init()
    pong_game = PongGame()
    pong_game.executar()
    pygame.quit()
    sys.exit()
