import pygame
import random
from config import TELA, FPS, LARGURA, ALTURA, BRANCO, AZUL, VERDE, VERMELHO, clock

# Inicializa pygame
pygame.init()

# Jogador
player = pygame.Rect(100, 300, 40, 40)
velocidade = 5
oxigenio = 100

# Inimigos (peixes)
inimigos = [pygame.Rect(random.randint(200, 700), random.randint(50, 550), 50, 30) for _ in range(3)]

# Bolhas (ar)
bolhas = [pygame.Rect(random.randint(100, 700), random.randint(50, 550), 20, 20) for _ in range(5)]

# Saída (fim da fase)
saida = pygame.Rect(750, 250, 40, 100)

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
