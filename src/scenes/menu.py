import pygame
import sys
from config import *

pygame.init()

# carregando imagens
background = pygame.image.load("assets/images/Background.png")  # sua imagem
background = pygame.transform.scale(background, (LARGURA, ALTURA))  # ajusta ao tamanho da tela

fonte_titulo = pygame.font.SysFont("fonts/assets/CinzelDecorative-Bold.ttf", 90, bold=True)
fonte_opcoes = pygame.font.SysFont("fonts/assets/CinzelDecorative-Bold.ttf", 55)

def desenhar_texto(tela, texto, fonte, cor, x, y):
    render = fonte.render(texto, True, cor)
    tela.blit(render, (x - render.get_width() // 2, y))

def menu(tela, clock):
    rodando = True
    while rodando:
        tela.blit(background, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mouse = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()

        # título
        #desenhar_texto(tela, "O Ultimo Recife", fonte_titulo, BRANCO, LARGURA // 2, 80)

        # botão jogar
        jogar_rect = pygame.Rect(530, 522, 200, 50) # (1º Largura, 2º Altura)

        # cria uma surface com transparência
        jogar_surface = pygame.Surface((jogar_rect.width, jogar_rect.height), pygame.SRCALPHA)

        # pinta a surface (último valor é alpha → 0=transparente, 255=opaco)
        jogar_surface.fill((0, 255, 0, 0))  # semi-transparente

        # desenha na tela
        tela.blit(jogar_surface, jogar_rect.topleft)

        # escreve o texto por cima
        desenhar_texto(tela, "Novo Jogo", fonte_opcoes, AZUL, jogar_rect.centerx, jogar_rect.y + 10)

        # clique do mouse
        if jogar_rect.collidepoint(mouse) and clique[0]:
            return "jogar"


        # botão Sair
        sair_rect = pygame.Rect(530, 622, 200, 50) # (1º Largura, 2º Altura)

        # cria uma surface com transparência
        sair_surface = pygame.Surface((sair_rect.width, sair_rect.height), pygame.SRCALPHA)

        # pinta a surface (último valor é alpha → 0=transparente, 255=opaco)
        sair_surface.fill((0, 255, 0, 0))  # semi-transparente

        # desenha na tela
        tela.blit(sair_surface, sair_rect.topleft)

        # escreve o texto por cima
        desenhar_texto(tela, "Sair", fonte_opcoes, AZUL, sair_rect.centerx, sair_rect.y + 10)

        if sair_rect.collidepoint(mouse) and clique[0]:
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(FPS)
