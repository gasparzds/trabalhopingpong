import pygame

class Raquete:
    def __init__(self, x, y, largura, altura, velocidade):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.velocidade = velocidade

    def mover(self, para_cima=True):
        if para_cima:
            self.rect.y -= self.velocidade
        else:
            self.rect.y += self.velocidade

        # Impede que a raquete saia da área de jogo
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))

    def desenhar(self, surface, cor):
        pygame.draw.rect(surface, cor, self.rect)
