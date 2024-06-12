import pygame
import random

class Bola:
    def __init__(self, x, y, tamanho, velocidade_x, velocidade_y):
        self.rect = pygame.Rect(x, y, tamanho, tamanho)
        self.velocidade_x = velocidade_x
        self.velocidade_y = velocidade_y
        self.cor = (255, 255, 255)  # Inicialmente branca

    def mover(self):
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y

        # Rebater nas bordas superior e inferior
        if self.rect.top <= 0 or self.rect.bottom >= 600:  # Ajuste para a altura da tela
            self.velocidade_y = -self.velocidade_y
            self.mudar_cor()  # Mudar a cor da bola

    def inverter_direcao_x(self):
        self.velocidade_x = -self.velocidade_x
        self.mudar_cor()  # Mudar a cor da bola

    def aumentar_velocidade(self, incremento):
        if self.velocidade_x > 0:
            self.velocidade_x += incremento
        else:
            self.velocidade_x -= incremento
        
        if self.velocidade_y > 0:
            self.velocidade_y += incremento
        else:
            self.velocidade_y -= incremento

    def mudar_cor(self):
        self.cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def desenhar(self, surface):
        pygame.draw.ellipse(surface, self.cor, self.rect)
