import pygame
import sys
from config import *

pygame.init()

# Carregar imagens
background = pygame.image.load("assets/images/Background.png").convert()
background = pygame.transform.scale(background, (LARGURA, ALTURA))

# --- CARREGAR IMAGENS DOS BOTÕES E AJUSTAR TAMANHO ---
img_novo_jogo = pygame.image.load("assets/images/NewGame.png").convert_alpha()
img_sair = pygame.image.load("assets/images/Out.png").convert_alpha()

# Tamanho dos botões
largura_botao = 200
altura_botao = 50
img_novo_jogo = pygame.transform.scale(img_novo_jogo, (largura_botao, altura_botao))
img_sair = pygame.transform.scale(img_sair, (largura_botao, altura_botao))
# ----------------------------------------------------

def menu(tela, clock):
    rodando = True
    while rodando:
        # DESENHA O FUNDO
        tela.blit(background, (0, 0))

        # --- EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- LÓGICA DO MOUSE ---
        mouse = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()

        # --- BOTÃO NOVO JOGO ---
        jogar_rect = img_novo_jogo.get_rect(topleft=(530, 522))
        tela.blit(img_novo_jogo, jogar_rect.topleft)

        if jogar_rect.collidepoint(mouse) and clique[0]:
            return "jogar"

        # --- BOTÃO SAIR ---
        sair_rect = img_sair.get_rect(topleft=(530, 622))
        tela.blit(img_sair, sair_rect.topleft)

        if sair_rect.collidepoint(mouse) and clique[0]:
            pygame.quit()
            sys.exit()

        # --- ATUALIZAÇÃO DE TELA ---
        pygame.display.flip()
        clock.tick(FPS)
