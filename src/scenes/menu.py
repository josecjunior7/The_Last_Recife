import pygame
import sys
from config import *

pygame.init()

# --- CARREGAR IMAGEM DE FUNDO ---
background = pygame.image.load("assets/images/Background.png").convert()
background = pygame.transform.scale(background, (LARGURA, ALTURA))

# --- CARREGAR IMAGENS DOS BOTÕES ---
img_novo_jogo = pygame.image.load("assets/images/NewGame.png").convert_alpha()
img_sair = pygame.image.load("assets/images/Out.png").convert_alpha()

# --- ESCALAS INDIVIDUAIS ---
escala_novo = 0.25   # escala do botão "Novo Jogo"
escala_sair = 0.15   # escala do botão "Sair"

# --- REDIMENSIONAMENTO COM ESCALAS INDIVIDUAIS ---
largura_novo, altura_novo = img_novo_jogo.get_size()
img_novo_jogo = pygame.transform.scale(
    img_novo_jogo,
    (int(largura_novo * escala_novo), int(altura_novo * escala_novo))
)

largura_sair, altura_sair = img_sair.get_size()
img_sair = pygame.transform.scale(
    img_sair,
    (int(largura_sair * escala_sair), int(altura_sair * escala_sair))
)

# --- POSIÇÕES INDIVIDUAIS DOS BOTÕES ---
# Aqui você controla manualmente onde cada elemento aparece
pos_novo_jogo = (500, 360)  # (x, y)
pos_sair = (550, 535)       # (x, y)

# --- FUNÇÃO DO MENU ---
def menu(tela, clock):
    rodando = True
    while rodando:
        tela.blit(background, (0, 0))

        # --- EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- LÓGICA DO MOUSE ---
        mouse = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()

        # --- DEFINIR RECTS NAS POSIÇÕES ESPECÍFICAS ---
        jogar_rect = img_novo_jogo.get_rect(topleft=pos_novo_jogo)
        sair_rect = img_sair.get_rect(topleft=pos_sair)

        # --- DESENHA BOTÕES ---
        tela.blit(img_novo_jogo, jogar_rect)
        tela.blit(img_sair, sair_rect)

        # --- CLIQUES ---
        if jogar_rect.collidepoint(mouse) and clique[0]:
            return "jogar"

        if sair_rect.collidepoint(mouse) and clique[0]:
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(FPS)
