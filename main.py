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

# Variáveis do jogador
vida = 100        # Vida do jogador (0 a 100)
oxigenio = 100    # Oxigênio inicial
velocidade = 5    # Velocidade de movimento

# Invencibilidade
INVENCIBILIDADE = 1000  # em milissegundos (1s)
ultimo_dano = 0         # guarda o tempo do último hit

# Loop principal
rodando = True
while rodando:
    clock.tick(FPS)
    TELA.fill(AZUL)

    tempo_atual = pygame.time.get_ticks()  # tempo desde início do jogo (ms)

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

    # Colisão com inimigos -> agora tem tempo de invencibilidade
    for inimigo in inimigos:
        if player.colliderect(inimigo):
            if tempo_atual - ultimo_dano > INVENCIBILIDADE:
                vida -= 10
                ultimo_dano = tempo_atual
                print(f"Você foi atingido! Vida: {vida}")
                if vida <= 0:
                    print("Sua vida chegou a zero! Game Over.")
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

    # --- Desenhar elementos ---
    pygame.draw.rect(TELA, BRANCO, player)          # Jogador
    for inimigo in inimigos:
        pygame.draw.rect(TELA, VERMELHO, inimigo)   # Inimigos
    for bolha in bolhas:
        pygame.draw.circle(TELA, VERDE, bolha.center, bolha.width//2)  # Bolhas
    pygame.draw.rect(TELA, (255, 215, 0), saida)    # Saída

    # Barra de oxigênio
    pygame.draw.rect(TELA, (0,0,0), (10, 10, 200, 20))  # Fundo
    pygame.draw.rect(TELA, (0, 255, 255), (10, 10, int(2 * oxigenio), 20))  # Oxigênio

    # Barra de vida
    pygame.draw.rect(TELA, (0,0,0), (10, 40, 200, 20))  # Fundo
    pygame.draw.rect(TELA, (255,0,0), (10, 40, int(2 * vida), 20))  # Vida

    pygame.display.update()

pygame.quit()
