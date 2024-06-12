import pygame
from Raquete import Raquete
from Bola import Bola
import sys


class PongGame:
    PRETO = (0, 0, 0)
    BRANCO = (255, 255, 255)
    largura = 800
    altura = 600
    font_file = "font/PressStart2P-Regular.ttf"

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.largura, self.altura))
        self.clock = pygame.time.Clock()

        # Criação das raquetes e bola
        self.raquete_pc = Raquete(10, self.altura // 2 - 60 // 2, 10, 60, 5)
        self.raquete_player_1 = Raquete(self.largura - 20, self.altura // 2 - 60 // 2, 10, 60, 5)
        self.bola = Bola(self.largura // 2 - 10 // 2, self.altura // 2 - 10 // 2, 10, 3, 3)

        self.score_pc = 0
        self.score_player_1 = 0
        self.vencedor = ""
        self.controle = False
        self.rodando = True

        # Timer para aumentar a velocidade
        self.ultimo_aumento = pygame.time.get_ticks()
        self.intervalo_aumento = 5000  # Aumenta a cada 5 segundos
        self.incremento_velocidade = 0.5  # Valor do incremento da velocidade

        # Carregar fonte
        self.font = pygame.font.Font(self.font_file, 36)

        # Carregar sons
        pygame.mixer.music.load("audios/music_game.mp3")
        pygame.mixer.music.play(-1)
        self.som = pygame.mixer.Sound("audios/Sound_A.wav")

    def menu_principal(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.controle = True
                        return

            self.screen.fill(self.PRETO)
            texto_menu = self.font.render("Pong", True, self.BRANCO)
            text_menu_rect = texto_menu.get_rect(center=(self.largura // 2, self.altura // 2))
            self.screen.blit(texto_menu, text_menu_rect)

            tempo = pygame.time.get_ticks()
            if tempo % 2000 < 1000:
                texto_iniciar = self.font.render("Pressione Espaço", True, self.BRANCO)
                texto_iniciar_rect = texto_iniciar.get_rect(center=(self.largura // 2, 450))
                self.screen.blit(texto_iniciar, texto_iniciar_rect)

            self.clock.tick(1)
            pygame.display.flip()

    def posicao_inicial(self):
        self.raquete_pc.rect.y = self.altura // 2 - 60 // 2
        self.raquete_player_1.rect.y = self.altura // 2 - 60 // 2
        self.bola.rect.x = self.largura // 2 - 10 // 2
        self.bola.rect.y = self.altura // 2 - 10 // 2
        self.score_pc = 0
        self.score_player_1 = 0
        self.ultimo_aumento = pygame.time.get_ticks()

    def fim_jogo(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.controle = True
                        self.posicao_inicial()
                        return

            self.screen.fill(self.PRETO)
            texto_fim = self.font.render(f"Vencedor: {self.vencedor}", True, self.BRANCO)
            text_fim_rect = texto_fim.get_rect(center=(self.largura // 2, self.altura // 2))
            self.screen.blit(texto_fim, text_fim_rect)
            pygame.display.flip()

    def executar(self):
        self.menu_principal()
        self.posicao_inicial()

        while self.rodando:
            if not self.controle:
                self.fim_jogo()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.rodando = False

                self.screen.fill(self.PRETO)
                self.bola.mover()

                # Verifica se é hora de aumentar a velocidade
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - self.ultimo_aumento > self.intervalo_aumento:
                    self.bola.aumentar_velocidade(self.incremento_velocidade)
                    self.ultimo_aumento = tempo_atual

                if self.bola.rect.colliderect(self.raquete_pc.rect) or self.bola.rect.colliderect(self.raquete_player_1.rect):
                    self.som.play()
                    self.bola.inverter_direcao_x()

                if self.bola.rect.left <= 0:
                    self.bola.rect.x = self.largura // 2 - 10 // 2
                    self.bola.rect.y = self.altura // 2 - 10 // 2
                    self.bola.inverter_direcao_x()
                    self.score_player_1 += 1
                    if self.score_player_1 == 5:
                        self.vencedor = "Player 1"
                        self.fim_jogo()

                if self.bola.rect.right >= self.largura:
                    self.bola.rect.x = self.largura // 2 - 10 // 2
                    self.bola.rect.y = self.altura // 2 - 10 // 2
                    self.bola.inverter_direcao_x()
                    self.score_pc += 1
                    if self.score_pc == 5:
                        self.vencedor = "PC"
                        self.fim_jogo()

                if self.raquete_pc.rect.centery < self.bola.rect.centery:
                    self.raquete_pc.mover(para_cima=False)
                elif self.raquete_pc.rect.centery > self.bola.rect.centery:
                    self.raquete_pc.mover(para_cima=True)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] and self.raquete_player_1.rect.top > 0:
                    self.raquete_player_1.mover(para_cima=True)
                if keys[pygame.K_DOWN] and self.raquete_player_1.rect.bottom < self.altura:
                    self.raquete_player_1.mover(para_cima=False)

                fonte_score = pygame.font.Font(self.font_file, 16)
                score_texto = fonte_score.render(
                    f"Score PC: {self.score_pc}       Score Player_1: {self.score_player_1}", True, self.BRANCO
                )
                score_rect = score_texto.get_rect(center=(self.largura // 2, 30))
                self.screen.blit(score_texto, score_rect)

                self.raquete_pc.desenhar(self.screen, self.BRANCO)
                self.raquete_player_1.desenhar(self.screen, self.BRANCO)
                self.bola.desenhar(self.screen)
                pygame.draw.aaline(self.screen, self.BRANCO, (self.largura // 2, 0), (self.largura // 2, self.altura))

                pygame.display.flip()
                self.clock.tick(60)
