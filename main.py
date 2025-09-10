import pygame
import random
from config import *
from src.entities.player import *
from src.entities.enemy import *
from src.scenes.maps import *
from src.scenes.menu import menu


# Inicializa pygame
pygame.init()

# antes de rodar o jogo, chama o menu
escolha = menu(TELA, clock)

# Loop principal
rodando = True
while rodando:
    clock.tick(FPS)
    TELA.fill(AZUL)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Movimento do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and player.left > 0:
        player.x -= velocidade
    if teclas[pygame.K_RIGHT] and player.right < LARGURA:
        player.x += velocidade
    if teclas[pygame.K_UP] and player.top > 0:
        player.y -= velocidade
    if teclas[pygame.K_DOWN] and player.bottom < ALTURA:
        player.y += velocidade

    # Diminuir oxigênio
    oxigenio -= 0.05
    if oxigenio <= 0:
        print("Você ficou sem ar! Game Over.")
        rodando = False

    # Movimentar inimigos (ida e volta)
    for inimigo in inimigos:
        inimigo.x += random.choice([-2, 2])
        if inimigo.left < 0:
            inimigo.left = 0
        if inimigo.right > LARGURA:
            inimigo.right = LARGURA

    # Colisão com inimigos
    for inimigo in inimigos:
        for vida in inimigos:
            if vida -10
            vida.x -= random.choice ([-10, 10])
        if player.colliderect(inimigo):
            print("Você foi pego por um peixe! Game Over.")
            rodando = False

    # Colisão com bolhas (recupera ar)
    for bolha in bolhas[:]:
        if player.colliderect(bolha):
            oxigenio = min(100, oxigenio + 20)
            bolhas.remove(bolha)

    # Colisão com saída (vitória)
    if player.colliderect(saida):
        print("Parabéns! Você passou de fase.")
        rodando = False

    # Desenhar elementos
    pygame.draw.rect(TELA, BRANCO, player)          # Jogador
    for inimigo in inimigos:
        pygame.draw.rect(TELA, VERMELHO, inimigo)   # Inimigos
    for bolha in bolhas:
        pygame.draw.circle(TELA, VERDE, bolha.center, bolha.width//2)  # Bolhas
    pygame.draw.rect(TELA, (255, 215, 0), saida)    # Saída

    # Barra de oxigênio
    pygame.draw.rect(TELA, (0,0,0), (10, 10, 200, 20))
    pygame.draw.rect(TELA, (0, 255, 255), (10, 10, int(2 * oxigenio), 20))

    pygame.display.update()

pygame.quit()
