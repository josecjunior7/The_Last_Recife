import pygame
import sys
from config import *

pygame.init()

fonte_titulo = pygame.font.SysFont("fonts/assets/Creepster-Regular.ttf", 50, bold=True)
fonte_opcoes = pygame.font.SysFont("arial", 30)

def desenhar_texto(tela, texto, fonte, cor, x, y):
    render = fonte.render(texto, True, cor)
    tela.blit(render, (x - render.get_width() // 2, y))

def menu(tela, clock):
    rodando = True
    while rodando:
        tela.fill(AZUL)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mouse = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()

        # título
        desenhar_texto(tela, "O Ultimo Recife", fonte_titulo, BRANCO, LARGURA // 2, 80)

        # botão jogar
        jogar_rect = pygame.Rect(500, 250, 200, 50)
        pygame.draw.rect(tela, VERDE, jogar_rect)
        desenhar_texto(tela, "Novo Jogo", fonte_opcoes, AZUL, jogar_rect.centerx, jogar_rect.y + 10)

        if jogar_rect.collidepoint(mouse) and clique[0]:
            return "jogar"

        # botão sair
        sair_rect = pygame.Rect(500, 310, 200, 50)
        pygame.draw.rect(tela, VERMELHO, sair_rect)
        desenhar_texto(tela, "Sair", fonte_opcoes, AZUL, sair_rect.centerx, sair_rect.y + 10)

        if sair_rect.collidepoint(mouse) and clique[0]:
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(FPS)
